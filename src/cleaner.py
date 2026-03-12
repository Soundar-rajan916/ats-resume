import re

# Pre-compile regex for performance
# Preserving some symbols used in tech stack like C#, C++, .NET
CLEAN_CHARS = re.compile(r'[^a-zA-Z0-9 +#.]')
NEWLINE_SPACE = re.compile(r'\n')

def clean_text(text: str) -> str:
    """Normalize text by lowering case, replacing newlines, and removing special chars."""
    if not text:
        return ""
    
    # Simple normalization
    text = text.lower()
    text = NEWLINE_SPACE.sub(' ', text)
    text = CLEAN_CHARS.sub('', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text