# ATS Scanner API

A powerful, FastAPI-based Applicant Tracking System (ATS) Scanner that analyzes resumes against job descriptions using semantic matching and AI-driven feedback.

## 🚀 Features

- **Multi-Format Support**: Parses both **PDF** and **DOCX** resume files.
- **Semantic Matching**: Uses `Sentence-Transformers` to calculate a deep contextual match between the resume and the job description.
- **AI Feedback**: Integrates with **Groq (Llama-3)** via LangChain to provide detailed, actionable feedback.
- **General Analysis**: Can analyze a resume even without a job description to provide general ATS readiness tips.
- **Modern API**: Built with **FastAPI**, featuring automatic Swagger UI documentation.
- **Robust Parsing**: Handles complex PDF/DOCX structures and cleans text for optimal NLP performance.

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn
- **NLP**: SpaCy, Sentence-Transformers (all-MiniLM-L6-v2)
- **AI/LLM**: LangChain, LangChain-Groq (Llama-3.3-70b-versatile)
- **Parsing**: Pdfminer.six, Python-docx
- **Dependency Management**: UV

## 📋 Prerequisites

- Python 3.11+
- A [Groq API Key](https://console.groq.com/) (required for AI feedback)

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Soundar-rajan916/ats-resume.git
   cd ats-resume
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Install Dependencies**:
   It is recommended to use `uv` for fast dependency management:
   ```bash
   uv pip install -r requirements.txt
   ```
   Or using standard pip:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the API

Start the server using `uv`:
```bash
uv run python main.py
```
The server will start at `http://localhost:8000`.

## 📖 API Usage

### 1. Interactive API Docs
Once the server is running, visit **[http://localhost:8000/docs](http://localhost:8000/docs)** to test the API directly from your browser using the built-in Swagger UI.

### 2. The `/scan` Endpoint (POST)
This endpoint accepts a multipart form-data request.

**Parameters**:
- `file`: The resume file (PDF or DOCX).
- `job_description` (Optional): The text of the job description.

**Example using Python Requests**:
```python
import requests

url = "http://localhost:8000/scan"
with open("my_resume.pdf", "rb") as f:
    files = {"file": ("my_resume.pdf", f, "application/pdf")}
    data = {"job_description": "We are looking for a Python Developer..."}
    response = requests.post(url, files=files, data=data)
    print(response.json())
```

## 📁 Project Structure

```text
ats-scanner/
├── main.py              # FastAPI Application Entry point
├── src/                 # Core Logic
│   ├── parser.py        # PDF and DOCX Parsing
│   ├── cleaner.py       # Text Cleaning/Normalization
│   ├── semantic_matcher.py # Vector-based Similarity Matching
│   ├── scorer.py        # Scoring Logic
│   └── ai_feedback.py   # LangChain/Groq Integration
├── requirements.txt     # Project Dependencies
└── .env                 # Environment Variables (API Keys)
```

## 📄 License
This project is licensed under the MIT License.
