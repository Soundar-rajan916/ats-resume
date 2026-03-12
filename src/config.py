import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Project Constants
DEFAULT_MODEL = "llama-3.3-70b-versatile"
TEMPERATURE = 0.1
MAX_RETRIES = 2

# Path to the model for semantic matching
SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# API Settings
API_TITLE = "ATS Scanner API"
API_VERSION = "1.1.0"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
