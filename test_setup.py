import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Test if API key is loaded
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print("✓ API key loaded from .env")
    print(f"  Key starts with: {api_key[:10]}...")
    
    try:
        genai.configure(api_key=api_key)
        
        # Test API connection with correct model name
        print("\n🔄 Testing Gemini API connection...")
        model = genai.GenerativeModel('gemini-1.5-flash')  # Correct: no 'models/' prefix
        response = model.generate_content("Say hello in one sentence!")
        print("✓ Google Gemini API working!")
        print(f"✓ Response: {response.text}")
        
    except Exception as e:
        print(f"✗ Error connecting to Gemini API: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check if your API key is valid")
        print("2. Verify Gemini API is enabled: https://makersuite.google.com/app/apikey")
        print("3. Make sure you have API quota remaining")
else:
    print("✗ API key not found in .env file")
    print("\nPlease create a .env file with:")
    print("GOOGLE_API_KEY=your_api_key_here")