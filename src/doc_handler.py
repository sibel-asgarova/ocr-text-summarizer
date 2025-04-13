from docx import Document

def convert_docx_to_txt(docx_path, txt_path):

    doc = Document(docx_path)
    text = ""
    
    for para in doc.paragraphs:
        text += para.text + "\n"
    
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
    
    print(f"Text has been saved to {txt_path}")


