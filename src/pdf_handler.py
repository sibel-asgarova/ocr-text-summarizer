import pdfplumber
import fitz 
from PIL import Image
import easyocr
from io import BytesIO
import os

def extract_text_from_pdf(pdf_path):

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if text.strip():
        print("Extracted text using pdfplumber.")
        return text.strip()


    print("No text found with pdfplumber. Falling back to OCR...")
    doc = fitz.open(pdf_path)
    reader = easyocr.Reader(['en'])
    ocr_text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=300)
        image = Image.open(BytesIO(pix.tobytes()))
        image_path = f"page_{page_num}.png"
        image.save(image_path)

        result = reader.readtext(image_path, detail=0)
        ocr_text += "\n".join(result) + "\n"

        os.remove(image_path)

    doc.close()
    return ocr_text.strip()


