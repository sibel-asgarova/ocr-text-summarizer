import streamlit as st
import os
from tempfile import NamedTemporaryFile
from PIL import Image

from src.doc_handler import convert_docx_to_txt
from src.pdf_handler import extract_text_from_pdf
from src.image_handler import convert_heic_to_png, extract_text_from_image

from src.text_summarizer_extractive import summarize_text_spacy
from src.text_summarizer_abstractive import summarize_text_t5

st.set_page_config(page_title="Smart Summarizer", layout="centered")
st.title("📝 Document Summarizer")
st.image("design.png")

if "text" not in st.session_state:
    st.session_state.text = ""
if "show_camera" not in st.session_state:
    st.session_state.show_camera = False


col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader("📎 Upload file", type=["pdf", "docx", "png", "jpg", "jpeg", "heic"])

with col2:
    if st.button("📷 Take Photo", use_container_width=True):
        st.session_state.show_camera = True

    photo = None
    if st.session_state.show_camera:
        photo = st.camera_input("📸 Capture your image")
        if photo:
            st.session_state.show_camera = False  # Optional: hide after capturing

user_pasted_text = st.text_area("Or, you can paste your text here:", height=200)

def handle_uploaded_file(file):
    suffix = file.name.split(".")[-1].lower()
    with NamedTemporaryFile(delete=False, suffix="." + suffix) as tmp_file:
        tmp_file.write(file.getbuffer())
        temp_path = tmp_file.name

    if suffix == "pdf":
        return extract_text_from_pdf(temp_path)

    elif suffix == "docx":
        temp_txt_path = temp_path.replace(".docx", ".txt")
        convert_docx_to_txt(temp_path, temp_txt_path)
        with open(temp_txt_path, "r", encoding="utf-8") as f:
            return f.read()

    elif suffix == "heic":
        png_path = convert_heic_to_png(temp_path)
        return extract_text_from_image(png_path)

    elif suffix in ["png", "jpg", "jpeg"]:
        return extract_text_from_image(temp_path)

    else:
        return ""


if uploaded_file or photo:
    file_to_use = uploaded_file if uploaded_file else photo
    st.info("🔍 Extracting text...")

    try:
        if photo and not uploaded_file:
            suffix = ".jpg"
            with NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(photo.getbuffer())
                temp_path = tmp_file.name
            text_content = extract_text_from_image(temp_path)
        else:
            text_content = handle_uploaded_file(file_to_use)

        if text_content:
            st.session_state.text = text_content
            st.success("Text extracted successfully!")
        else:
            st.error("No text could be extracted.")
    except Exception as e:
        st.error(f"Error during extraction: {str(e)}")

elif user_pasted_text:
    st.session_state.text = user_pasted_text

if st.session_state.text.strip():
    st.text_area("Extracted Text", st.session_state.text, height=250)

    method = st.radio("Choose summarization method", ["Extractive", "Abstractive"])

    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            if method == "Extractive":
                summary = summarize_text_spacy(st.session_state.text)
            else:
                summary = summarize_text_t5(st.session_state.text)

        if summary:
            st.success("Summary generated.")
            st.text_area(" Summary", summary, height=200)
        else:
            st.warning("Summary could not be generated.")
else:
    st.info("Please upload a file, take a photo, or paste text to begin.")
