import json
import os
import requests
import psycopg2
from psycopg2.extras import RealDictCursor

def get_embedding(text):
    """Generate embedding using BAAI/bge-small-en-v1.5 model"""
    headers = {
        'Authorization': f'Bearer {os.getenv("HUGGINGFACE_API_TOKEN")}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            'https://api-inference.huggingface.co/models/BAAI/bge-small-en-v1.5',
            headers=headers,
            json={'inputs': text},
            timeout=30
        )
        
        if response.status_code == 200:
            embedding = response.json()
            if isinstance(embedding, list) and len(embedding) == 384:
                return embedding
            else:
                print(f"Unexpected embedding format: {type(embedding)}")
                return None
        else:
            print(f"Embedding API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Embedding generation error: {e}")
        return None

def search_documents(query_embedding, limit=3):
    """Search for similar documents using cosine similarity"""
    try:
        conn = psycopg2.connect(os.getenv('NEON_DATABASE_URL'))
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Convert embedding to string format for PostgreSQL
        embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
        
        query = """
        SELECT content, doc_metadata, 
               1 - (embedding <=> %s::vector) as similarity
        FROM documents 
        ORDER BY embedding <=> %s::vector 
        LIMIT %s
        """
        
        cursor.execute(query, (embedding_str, embedding_str, limit))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return [dict(row) for row in results]
        
    except Exception as e:
        print(f"Database search error: {e}")
        return []

def generate_response(query, context_docs):
    """Generate response using Gemini with context"""
    try:
        # Prepare context from retrieved documents
        context = "\n\n".join([
            f"Document: {doc.get('doc_metadata', {}).get('product_name', 'Unknown')}\nContent: {doc['content']}"
            for doc in context_docs
        ])
        
        prompt = f"""Based on the following context documents, please answer the user's question. 
If the answer is not in the context, say so politely.

Context:
{context}

Question: {query}

Answer:"""

        # Call Gemini API
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={os.getenv("GEMINI_API_KEY")}',
            headers={'Content-Type': 'application/json'},
            json={
                'contents': [{
                    'parts': [{'text': prompt}]
                }]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "I apologize, but I'm having trouble generating a response right now."
        else:
            print(f"Gemini API error: {response.status_code}")
            return "I apologize, but I'm having trouble generating a response right now."
            
    except Exception as e:
        print(f"Gemini error: {e}")
        return "I apologize, but I'm having trouble generating a response right now."

def handler(request):
    """Main Vercel handler for RAG system"""
    try:
        # Parse request
        if request.method != 'POST':
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        
        if not query:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Query is required'})
            }
        
        # Step 1: Generate embedding for query
        query_embedding = get_embedding(query)
        if not query_embedding:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to generate embedding'})
            }
        
        # Step 2: Search for similar documents
        similar_docs = search_documents(query_embedding)
        
        # Step 3: Generate response with context
        response = generate_response(query, similar_docs)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'response': response,
                'sources': len(similar_docs),
                'model': 'BAAI/bge-small-en-v1.5'
            })
        }
        
    except Exception as e:
        print(f"Handler error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
