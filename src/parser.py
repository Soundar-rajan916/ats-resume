from pdfminer.high_level import extract_text
import docx

def parse_resume(file_path):
    if file_path.lower().endswith('.pdf'):
        text = extract_text(file_path)
    elif file_path.lower().endswith('.docx'):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        text = ""
    return text