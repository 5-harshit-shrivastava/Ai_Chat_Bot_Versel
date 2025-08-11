from db import Document, get_db
from embeddings import embedder
from sqlalchemy.orm import Session
from typing import Dict, Any

def add_document(content: str, metadata: Dict[str, Any], db: Session):
    embedding = embedder.get_embedding(content)
    
    doc = Document(
        content=content,
        embedding=embedding,
        doc_metadata=metadata
    )
    
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return str(doc.id)