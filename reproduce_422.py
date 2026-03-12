import requests
import io

def test_multipart():
    url = "http://localhost:8000/scan"
    file_content = b"fake pdf content %PDF-1.4"
    file_obj = io.BytesIO(file_content)
    
    files = {"file": ("test.pdf", file_obj, "application/pdf")}
    data = {"job_description": "test jd"}
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, files=files, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_multipart()
