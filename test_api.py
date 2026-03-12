import requests

def test_scan():
    url = "http://localhost:8000/scan"
    file_path = "test_resume.docx"
    
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        data = {"job_description": "We are looking for a Python Developer with experience in FastAPI and NLP."}
        
        print(f"Sending request to {url}...")
        response = requests.post(url, files=files, data=data)
        
    if response.status_code == 200:
        print("Success!")
        print(response.json())
    else:
        print(f"Failed with status code {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_scan()
