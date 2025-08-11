#!/usr/bin/env python3

import subprocess
import time
import requests
import json
import sys
import os

def test_server():
    print("Testing RAG Chatbot API...")
    
    # Test 1: Add a document
    print("\n1. Testing document ingestion...")
    try:
        response = requests.post("http://localhost:8000/documents", 
                                json={
                                    "content": "Python is a high-level programming language. It was created by Guido van Rossum and first released in 1991.",
                                    "metadata": {"topic": "programming", "language": "python"}
                                })
        if response.status_code == 200:
            doc_data = response.json()
            print(f"✓ Document added successfully! ID: {doc_data.get('document_id')}")
        else:
            print(f"✗ Document addition failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Document addition failed: {e}")
        return False
    
    # Wait a moment for indexing
    time.sleep(2)
    
    # Test 2: Chat query
    print("\n2. Testing chat functionality...")
    try:
        response = requests.post("http://localhost:8000/chat",
                                json={"query": "What is Python?"})
        if response.status_code == 200:
            chat_data = response.json()
            print(f"✓ Chat response received: {chat_data.get('response')[:100]}...")
        else:
            print(f"✗ Chat failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Chat failed: {e}")
        return False
    
    print("\n✅ All tests passed! Your RAG chatbot is working correctly.")
    return True

if __name__ == "__main__":
    # Start server in background
    print("Starting FastAPI server...")
    
    # Activate virtual environment and start server
    os.chdir("/home/harshit/rag-chatbot-project/backend")
    
    # Start server
    process = subprocess.Popen([
        "bash", "-c", 
        "source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(10)
    
    try:
        # Test server
        success = test_server()
        
        if success:
            print(f"\n🚀 Server is running at http://localhost:8000")
            print("📖 API docs available at http://localhost:8000/docs")
            print("\nPress Ctrl+C to stop the server...")
            
            # Keep server running
            process.wait()
        else:
            print("\n❌ Tests failed. Check the error messages above.")
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
    finally:
        process.terminate()
        process.wait()
