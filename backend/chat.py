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


def is_meaningful_query(query: str) -> bool:
    """Check if the query is meaningful and complete enough to process"""
    query = query.strip().lower()
    
    # Reject very short queries (less than 3 characters)
    if len(query) < 3:
        return False
    
    # Reject single words unless they are complete words
    words = query.split()
    if len(words) == 1:
        # Allow complete words that are at least 4 characters
        return len(query) >= 4
    
    # For multi-word queries, check if they form a reasonable question
    question_words = ['what', 'where', 'when', 'who', 'why', 'how', 'which', 'is', 'are', 'can', 'do', 'does']
    has_question_structure = any(word in query for word in question_words)
    
    return has_question_structure or len(words) >= 2

async def get_rag_response(query: str, db: Session) -> str:
    # Validate query first
    if not is_meaningful_query(query):
        return "Please ask a complete and clear question. Your query seems too short or incomplete."
    
    # Search for similar documents using vector search
    similar_docs = search_similar_documents(query, db, top_k=5)
    
    if not similar_docs:
        return "I don't have any documents in my knowledge base. Please upload some documents first."
    
    # Filter documents by similarity threshold (only include if similarity > 0.3)
    relevant_docs = [(doc, score) for doc, score in similar_docs if score > 0.3]
    
    if not relevant_docs:
        return "I don't have information about that topic in my knowledge base."
    
    # Build context from relevant documents only
    context_parts = []
    for doc, score in relevant_docs:
        context_parts.append(f"Document (relevance: {score:.2f}):\n{doc.content}")
    
    context = "\n\n---\n\n".join(context_parts)
    
    # Create a strict prompt for Gemini
    prompt = f"""
    You are an AI assistant that answers questions based ONLY on the provided context documents.
    
    Context documents:
    {context}
    
    User question: {query}
    
    Instructions:
    1. ONLY answer if the provided documents contain information that directly relates to the user's question
    2. The question and the document content must have a clear topical match
    3. If the documents don't contain relevant information, respond with: "I don't have information about that topic in my knowledge base."
    4. Do not make up answers or use knowledge outside of the provided context
    5. Be precise and only use information directly from the documents
    6. Do not try to guess or infer from incomplete questions
    
    Answer:
    """
    
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text.strip()
    except Exception as e:
        error_message = f"Error generating response: {str(e)}"
        return error_message