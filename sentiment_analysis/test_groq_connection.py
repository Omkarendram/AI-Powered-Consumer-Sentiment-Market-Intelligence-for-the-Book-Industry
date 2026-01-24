import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test Groq API connection
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key loaded: {api_key[:20]}..." if api_key else "API Key NOT found!")

# Initialize Groq client
client = Groq(api_key=api_key)

# Test a simple API call
print("\nTesting Groq API connection...")
try:
    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": 'Respond with JSON: {"sentiment": "positive", "confidence": 0.9}'
            }
        ],
        temperature=0.3,
        max_tokens=50
    )
    
    print("✓ API Connection Successful!")
    print(f"Response: {message.choices[0].message.content}")
    
except Exception as e:
    print(f"✗ API Connection Failed!")
    print(f"Error: {type(e).__name__}")
    print(f"Details: {str(e)}")
