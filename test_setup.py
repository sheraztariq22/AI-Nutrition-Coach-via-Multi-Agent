import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Test if API key is loaded
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print("✓ API key loaded from .env")
    genai.configure(api_key=api_key)
    
    # Test API connection
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello!")
    print("✓ Google Gemini API working!")
    print(f"Response: {response.text}")
else:
    print("✗ API key not found in .env file")