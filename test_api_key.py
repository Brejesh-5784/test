"""
Simple script to verify your Gemini API key is working correctly.
Run this before running the main app to ensure your API key is valid.
"""

import os
from dotenv import load_dotenv
from google.genai import Client

# Load environment variables
load_dotenv()

def test_api_key():
    """Test if the Gemini API key is valid and working."""
    
    print("=" * 60)
    print("GEMINI API KEY VERIFICATION TEST")
    print("=" * 60)
    
    # Check if API key exists
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file")
        print("\nPlease:")
        print("1. Create a .env file in the project root")
        print("2. Add: GEMINI_API_KEY=your_actual_api_key")
        print("3. Get your key from: https://aistudio.google.com/app/apikey")
        return False
    
    print(f"✓ API Key found: {api_key[:20]}...{api_key[-4:]}")
    print(f"✓ API Key length: {len(api_key)} characters")
    
    # Test the API key with a simple request
    print("\n" + "-" * 60)
    print("Testing API connection...")
    print("-" * 60)
    
    try:
        # Initialize client
        client = Client(api_key=api_key)
        
        # Make a simple test request
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say 'Hello, FitSync Pro!' in exactly 5 words."
        )
        
        print("✅ SUCCESS! API key is valid and working!")
        print(f"\nTest Response: {response.text}")
        print("\n" + "=" * 60)
        print("Your API key is configured correctly!")
        print("You can now run: streamlit run app.py")
        print("=" * 60)
        return True
        
    except Exception as e:
        print("❌ ERROR: API key validation failed!")
        print(f"\nError details: {str(e)}")
        print("\n" + "-" * 60)
        print("Possible solutions:")
        print("1. Get a new API key from: https://aistudio.google.com/app/apikey")
        print("2. Make sure you're using Google AI Studio API key (not Google Cloud)")
        print("3. Check if the API key has been revoked or expired")
        print("4. Ensure there are no extra spaces in your .env file")
        print("-" * 60)
        return False

if __name__ == "__main__":
    test_api_key()
