import requests
import os

def test_api():
    url = "http://127.0.0.1:8000/scan"
    
    # Create a dummy pdf file
    dummy_pdf = "dummy_resume.pdf"
    with open(dummy_pdf, "wb") as f:
        f.write(b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Count 1\n/Kids [3 0 R]\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Resources << >>\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 100 700 Td (Hello World) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000018 00000 n\n0000000077 00000 n\n0000000178 00000 n\n0000000457 00000 n\ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n565\n%%EOF")

    try:
        with open(dummy_pdf, "rb") as f:
            files = {"file": (dummy_pdf, f, "application/pdf")}
            data = {"job_description": "We need a software engineer with Python experience."}
            response = requests.post(url, files=files, data=data)
            
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(response.json())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(dummy_pdf):
            os.remove(dummy_pdf)

if __name__ == "__main__":
    test_api()
