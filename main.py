import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.parser import parse_resume
from src.cleaner import clean_text
from src.semantic_matcher import semantic_match
from src.scorer import calculate_score
from src.ai_feedback import generate_feedback

from typing import Annotated
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ATS Scanner API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the ATS Scanner API"}

@app.post("/scan")
async def scan_resume(
    file: Annotated[UploadFile, File(...)],
    job_description: Annotated[str, Form()] = ""
):
    logger.info(f"Received scan request for file: {file.filename}")
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are supported.")
    
    try:
        # Save uploaded file to a temporary file
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(await file.read())
            tmp_path = tmp_file.name

        # Process the resume
        resume_text = parse_resume(tmp_path)
        clean_resume = clean_text(resume_text)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        if job_description:
            # Calculate Match
            similarity = semantic_match(clean_resume, job_description)
            score = calculate_score(similarity)
            feedback, ai_score = generate_feedback(clean_resume, job_description)
            
            return JSONResponse({
                "match_percentage": score,
                "ai_score": ai_score,
                "feedback": feedback
            })
        else:
            feedback, ai_score = generate_feedback(clean_resume)
            return JSONResponse({
                "match_percentage": None,
                "ai_score": ai_score,
                "feedback": feedback,
                "message": "No Job Description provided. Performed general analysis."
            })
            
    except Exception as e:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)