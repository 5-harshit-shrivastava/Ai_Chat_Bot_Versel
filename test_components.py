#!/usr/bin/env python3
"""
Simple test to check RAG components
"""
import os
import sys

# Add project root to path
sys.path.append('/home/harshit/rag-chatbot-project')

# You need to set your actual API tokens here
HUGGINGFACE_TOKEN = "hf_your_token_here"  # Replace with your token
GEMINI_KEY = "your_gemini_key_here"       # Replace with your key
NEON_URL = "postgresql://neondb_owner:npg_4MwpAhIlPt5x@ep-small-flower-adimixak-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def test_database():
    """Test database connection"""
    try:
        import psycopg2
        conn = psycopg2.connect(NEON_URL)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM documents')
        count = cursor.fetchone()[0]
        print(f"✅ Database: {count} documents found")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_embedding():
    """Test embedding generation"""
    try:
        import requests
        headers = {
            'Authorization': f'Bearer {HUGGINGFACE_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://api-inference.huggingface.co/models/BAAI/bge-small-en-v1.5',
            headers=headers,
            json={'inputs': 'test query'},
            timeout=30
        )
        
        if response.status_code == 200:
            embedding = response.json()
            if isinstance(embedding, list) and len(embedding) == 384:
                print(f"✅ Embedding: Generated {len(embedding)} dimensions")
                return True
            else:
                print(f"❌ Embedding: Wrong format - {type(embedding)}")
                return False
        else:
            print(f"❌ Embedding API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return False

def test_gemini():
    """Test Gemini API"""
    try:
        import requests
        
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}',
            headers={'Content-Type': 'application/json'},
            json={
                'contents': [{
                    'parts': [{'text': 'Hello, this is a test. Please respond with "API working"'}]
                }]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result:
                print("✅ Gemini: API working")
                return True
            else:
                print(f"❌ Gemini: Unexpected response format")
                return False
        else:
            print(f"❌ Gemini API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing RAG system components...")
    print("\n⚠️  IMPORTANT: Update the API tokens at the top of this file!")
    print("   - Get HuggingFace token from: https://huggingface.co/settings/tokens")
    print("   - Get Gemini key from: https://aistudio.google.com/app/apikey")
    print()
    
    # Test each component
    db_ok = test_database()
    embedding_ok = test_embedding()
    gemini_ok = test_gemini()
    
    print(f"\n📊 Test Results:")
    print(f"   Database: {'✅' if db_ok else '❌'}")
    print(f"   Embeddings: {'✅' if embedding_ok else '❌'}")
    print(f"   Gemini AI: {'✅' if gemini_ok else '❌'}")
    
    if all([db_ok, embedding_ok, gemini_ok]):
        print(f"\n🎉 All components working! Ready for Vercel deployment.")
    else:
        print(f"\n⚠️  Fix the failing components before deploying to Vercel.")
