import os
import json
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import Tuple, Optional

from .config import GROQ_API_KEY, DEFAULT_MODEL, TEMPERATURE

class FeedbackResponse(BaseModel):
    score: int = Field(description="A number from 0 to 100 representing the match percentage or quality")
    feedback: str = Field(description="Detailed markdown feedback with specific sections")

# Initialize parser
parser = JsonOutputParser(pydantic_object=FeedbackResponse)

def get_llm():
    if not GROQ_API_KEY:
        return None
    return ChatGroq(
        model=DEFAULT_MODEL, 
        api_key=GROQ_API_KEY,
        temperature=TEMPERATURE
    )

async def generate_feedback(resume: str, job: str = "") -> Tuple[str, int]:
    llm = get_llm()
    if not llm:
        return "GROQ_API_KEY not found. Please check your environment variables.", 0
    
    if not job:
        template = """Analyze this resume comprehensively for its general quality and ATS readiness.
        
        Resume: {resume}
        
        {format_instructions}
        Include sections for: AI Suggestions, ATS Optimization, and Missing Keywords.
        """
    else:
        template = """Compare this resume with the following job description.
        
        Resume: {resume}
        Job Description: {job}
        
        {format_instructions}
        Include sections for: Match Analysis, Missing Keywords, and AI Suggestions.
        """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["resume", "job"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser
    
    try:
        data = {"resume": resume, "job": job}
        result = await chain.ainvoke(data)
        
        score = result.get("score", 0)
        feedback = result.get("feedback", "No feedback provided.")
        
        return feedback, score
        
    except Exception as e:
        return f"Error communicating with AI: {str(e)}", 0

