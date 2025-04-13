from PIL import Image
import easyocr
import pillow_heif
import os

def convert_heic_to_png(heic_path, output_path="converted_image.png"):
    heif_file = pillow_heif.read_heif(heic_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw"
    )
    image.save(output_path, format="PNG")
    return output_path

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path, detail=0)
    return "\n".join(result).strip()

def process_image(image_path):
    ext = os.path.splitext(image_path)[-1].lower()

    if ext == ".heic":
        print("HEIC file detected. Converting to PNG...")
        converted_path = convert_heic_to_png(image_path)
        text = extract_text_from_image(converted_path)
        os.remove(converted_path)
    else:
        print("Standard image format detected. Running OCR...")
        text = extract_text_from_image(image_path)

    if text:
        print("Detected text:\n" + text)
        txt_output = os.path.splitext(image_path)[0] + ".txt"
        with open(txt_output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Text saved to {txt_output}")
    else:
        print("No text detected.")



