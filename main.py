import os
import tempfile
import asyncio
import logging
from typing import Annotated

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.parser import parse_resume
from src.cleaner import clean_text
from src.semantic_matcher import semantic_match
from src.scorer import calculate_score
from src.ai_feedback import generate_feedback
from src.config import API_TITLE, API_VERSION, DEFAULT_HOST, DEFAULT_PORT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title=API_TITLE, version=API_VERSION)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": f"Welcome to the {API_TITLE}", "version": API_VERSION}

@app.post("/scan")
async def scan_resume(
    file: Annotated[UploadFile, File(...)],
    job_description: Annotated[str, Form()] = ""
):
    logger.info(f"Processing scan request: {file.filename}")
    
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=400, 
            detail="Unsupported file format. Please upload a PDF or DOCX file."
        )
    
    tmp_path = None
    try:
        # Save uploaded file safely
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode='wb') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        # 1. Parse and Clean (Synchronous/CPU bound)
        # In a high-traffic app, these should be run in a threadpool
        loop = asyncio.get_event_loop()
        resume_text = await loop.run_in_executor(None, parse_resume, tmp_path)
        clean_resume = await loop.run_in_executor(None, clean_text, resume_text)
        
        # 2. Parallel Processing for Matching and AI Feedback
        if job_description:
            # Clean JD as well
            clean_jd = await loop.run_in_executor(None, clean_text, job_description)
            
            # Run AI feedback (async) and Semantic Match (threaded) concurrently
            ai_task = generate_feedback(clean_resume, clean_jd)
            match_task = loop.run_in_executor(None, semantic_match, clean_resume, clean_jd)
            
            (ai_result, ai_score), similarity = await asyncio.gather(ai_task, match_task)
            
            score = calculate_score(similarity)
            
            return JSONResponse({
                "match_percentage": score,
                "ai_score": ai_score,
                "feedback": ai_result,
                "status": "success"
            })
        else:
            # Only AI feedback if no JD
            feedback, ai_score = await generate_feedback(clean_resume)
            
            return JSONResponse({
                "match_percentage": None,
                "ai_score": ai_score,
                "feedback": feedback,
                "message": "General analysis performed (no job description provided).",
                "status": "success"
            })
            
    except Exception as e:
        logger.error(f"Error during scan: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error during analysis: {str(e)}"
        )
    finally:
        # Always clean up the temp file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception as e:
                logger.error(f"Failed to delete temp file {tmp_path}: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    uvicorn.run("main:app", host=DEFAULT_HOST, port=port, reload=True)