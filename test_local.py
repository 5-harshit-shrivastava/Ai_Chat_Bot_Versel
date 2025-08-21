#!/usr/bin/env python3
"""
Test script to simulate Vercel serverless function locally
"""
import sys
import os
sys.path.append('/home/harshit/rag-chatbot-project')

# Set up environment variables (you'll need to add real tokens)
os.environ['HUGGINGFACE_API_TOKEN'] = 'hf_your_token_here'
os.environ['GEMINI_API_KEY'] = 'your_gemini_key_here'
os.environ['NEON_DATABASE_URL'] = 'postgresql://neondb_owner:npg_4MwpAhIlPt5x@ep-small-flower-adimixak-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

# Import the handler function
from api.chat import handler

# Create a mock Vercel request
class MockRequest:
    def __init__(self, method='POST', body=None):
        self.method = method
        self.body = body or '{"message": "What is machine learning?"}'
        
    def get_json(self):
        import json
        return json.loads(self.body)

class MockResponse:
    def __init__(self):
        self.status_code = 200
        self.headers = {}
        self.data = None
        
    def json(self, data):
        import json
        self.data = json.dumps(data)
        print(f"✅ Response: {self.data}")
        return self
        
    def status(self, code):
        self.status_code = code
        return self

# Test the function
if __name__ == "__main__":
    print("🚀 Testing RAG Chat API locally...")
    
    # Test with a sample question
    request = MockRequest()
    response = MockResponse()
    
    try:
        result = handler(request, response)
        print(f"✅ Test completed successfully!")
        print(f"Status Code: {response.status_code}")
        if hasattr(response, 'data') and response.data:
            print(f"Response Data: {response.data}")
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
