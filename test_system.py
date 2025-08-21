#!/usr/bin/env python3
"""
Test script for the cleaned RAG system
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from ingest import get_embedding, setup_database, ingest_navyakosh_data
import requests

def test_embedding():
    """Test embedding generation"""
    print("🧪 Testing BAAI/bge-small-en-v1.5 embedding...")
    
    test_text = "Navyakosh fertilizer application for sugarcane"
    embedding = get_embedding(test_text)
    
    if embedding:
        print(f"✅ SUCCESS! Generated {len(embedding)}-dimensional embedding")
        print(f"Sample values: {embedding[:5]}")
        return True
    else:
        print("❌ FAILED to generate embedding")
        return False

def test_database():
    """Test database connection"""
    print("🧪 Testing database connection...")
    
    if setup_database():
        print("✅ Database connection successful!")
        return True
    else:
        print("❌ Database connection failed!")
        return False

def test_local_api():
    """Test the chat API locally if possible"""
    print("🧪 Testing local API simulation...")
    
    try:
        # Simulate the API call
        query = "Tell me about Navyakosh fertilizer application rate"
        embedding = get_embedding(query)
        
        if embedding:
            print(f"✅ Query embedding generated: {len(embedding)} dims")
            print("🎯 RAG pipeline ready for deployment!")
            return True
        else:
            print("❌ Failed to generate query embedding")
            return False
            
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 RAG SYSTEM DEPLOYMENT TEST")
    print("=" * 50)
    
    tests = [
        ("Embedding Generation", test_embedding),
        ("Database Connection", test_database), 
        ("API Simulation", test_local_api)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {test_name}")
    
    if all(results):
        print("\n🎉 ALL TESTS PASSED! System ready for deployment!")
        print("\n📋 Next steps:")
        print("1. Run: python3 test_system.py")
        print("2. Deploy: git add . && git commit -m 'Clean RAG system' && git push")
        print("3. Test: https://ai-chat-swart-chi.vercel.app/api/chat")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
