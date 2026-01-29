import sys
from pypdf import PdfReader

def extract_text(pdf_path, output_path):
    try:
        reader = PdfReader(pdf_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            for page in reader.pages:
                f.write(page.extract_text() + "\n\n")
        print(f"Successfully extracted text to {output_path}")
    except Exception as e:
        print(f"Error extracting text: {e}")

if __name__ == "__main__":
    extract_text("Crear LLM.pdf", "pdf_content.txt")
