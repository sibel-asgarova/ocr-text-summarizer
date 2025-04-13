# OCR and Text Summarizer

This project combines **Optical Character Recognition (OCR)** and **Text Summarization** techniques to extract text from images and generate concise summaries. The goal of the project is to provide an automated solution for processing images with text and summarizing the content.

## Features

- **OCR (Optical Character Recognition)**: Extracts text from images using library **EasyOCR**.
- **Text Summarization**: Summarizes the extracted text using advanced models such as  **T5**, or any other text summarization techniques.
- **Streamlit App**: A simple user interface to upload images and view the summarized text.
  
## Installation

To run this project locally, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/sibel-asgarova/ocr-text-summarizer.git
cd ocr-text-summarizer
```

### 2.Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows
```

### 3. Install requirements 
```bash
pip install -r requirements.txt
```

### 4.Run streamlit app

```bash
streamlit run app.py
```
