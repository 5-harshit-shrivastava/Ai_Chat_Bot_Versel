from sqlalchemy.orm import Session
from db import Document
from embeddings import embedder
from typing import List, Tuple

def search_similar_documents(query: str, db: Session, top_k: int = 5) -> List[Tuple[Document, float]]:
    query_embedding = embedder.get_embedding(query)
    
    # Use vector similarity search provided by pgvector
    similar_documents = db.query(Document, Document.embedding.cosine_distance(query_embedding).label('distance')) \
        .order_by('distance') \
        .limit(top_k) \
        .all()
    
    # Invert the distance to get similarity
    return [(doc, 1 - distance) for doc, distance in similar_documents]