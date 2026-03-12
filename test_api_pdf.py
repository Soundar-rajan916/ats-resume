import requests
import os

def test_api_pdf():
    url = "http://localhost:8000/scan"
    file_path = "test_resume.pdf"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/pdf")}
        data = {"job_description": "Software engineer with knowledge in computer science basics."}
        
        print(f"Sending request to {url}...")
        try:
            response = requests.post(url, files=files, data=data)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("Success!")
                print(response.json())
            else:
                print("Failure:")
                print(response.text)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_api_pdf()
