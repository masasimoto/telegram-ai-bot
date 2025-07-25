import os
from PyPDF2 import PdfReader

def read_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
        return text.strip() if text else "PDF tidak berisi teks yang bisa dibaca."
    except Exception as e:
        return f"Gagal membaca PDF: {str(e)}"

def read_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Gagal membaca file TXT: {str(e)}"

def read_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Gagal membaca file CSV: {str(e)}"

def auto_read_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return read_pdf(file_path)
    elif ext == ".txt":
        return read_txt(file_path)
    elif ext == ".csv":
        return read_csv(file_path)
    else:
        return "Format file belum didukung untuk dibaca otomatis."
