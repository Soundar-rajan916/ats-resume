import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import json

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    # Using a common versatile model from Groq
    return ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)

def generate_feedback(resume, job=""):
    llm = get_llm()
    if not llm:
        return "GROQ_API_KEY not found. Please check your environment variables.", 0
    
    if not job:
        prompt = PromptTemplate.from_template(
            """Analyze this resume comprehensively without a specific job description.

            Resume:
            {resume}

            Please provide your response in valid JSON format ONLY, like this:
            {{
                "score": <a number from 0 to 100 representing overall resume quality and ATS readiness>,
                "feedback": "<your detailed markdown feedback. Include specific sections for: 1. AI Suggestions & Improvements, 2. ATS Optimization Tips, 3. Potential Missing Keywords>"
            }}
            """
        )
        data = {"resume": resume}
    else:
        prompt = PromptTemplate.from_template(
            """Compare this resume with the job description.

            Resume:
            {resume}

            Job Description:
            {job}

            Please provide your response in valid JSON format ONLY, like this:
            {{
                "score": <a number from 0 to 100 representing the match percentage based on skills and experience>,
                "feedback": "<your detailed markdown feedback. Include specific sections for: 1. Missing Keywords, 2. AI Suggestions & Improvements, 3. Formatting & Clarity>"
            }}
            """
        )
        data = {"resume": resume, "job": job}

    chain = prompt | llm
    try:
        response = chain.invoke(data)
        content = response.content
        
        # Robust JSON extraction
        content = content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        # Ensure it looks like JSON
        start = content.find('{')
        end = content.rfind('}')
        if start != -1 and end != -1:
            content = content[start:end+1]
        
        try:
            # strict=False allows control characters like literal newlines inside strings
            result = json.loads(content, strict=False)
        except json.JSONDecodeError:
            try:
                # Cleanup of newlines within the object
                content_clean = content.replace('\n', ' ').replace('\r', '')
                result = json.loads(content_clean, strict=False)
            except Exception:
                return f"Raw AI Feedback (Parse Error):\n\n{content}", 0

        # Support multiple possible key names for score
        score = result.get("score") or result.get("overall_score") or result.get("match_score") or 0
        return result.get("feedback", "No feedback provided."), score
    except Exception as e:
        return f"Error communicating with AI: {str(e)}", 0

