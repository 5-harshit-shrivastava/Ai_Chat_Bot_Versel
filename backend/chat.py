import os
import google.generativeai as genai
import asyncio
from sqlalchemy.orm import Session
from search import search_similar_documents
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')


async def get_rag_response(query: str, db: Session) -> str:
    # Search for similar documents
    similar_docs = search_similar_documents(query, db, top_k=3)
    
    if not similar_docs:
        return "I don't have any relevant information to answer your question."
    
    # Build context from similar documents
    context = "\n\n".join([doc.content for doc, _ in similar_docs])
    
    # Create prompt for Gemini
    prompt = f"""
    Context information:
    {context}
    
    Question: {query}
    
    Based on the context information provided above, please answer the question. If the context doesn't contain enough information to answer the question, please say so.
    """
    
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text
    except Exception as e:
        error_message = f"Error generating response: {str(e)}"
        return error_message