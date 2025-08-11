from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from typing import Dict, Any
from sqlalchemy.orm import Session

from db import get_db, init_db, Document
from ingest import add_document
from chat import get_rag_response

app = FastAPI()

class DocumentRequest(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}

class ChatRequest(BaseModel):
    query: str

class DocumentResponse(BaseModel):
    document_id: str

class ChatResponse(BaseModel):
    response: str

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/")
async def root():
    """Redirects to the API documentation."""
    return RedirectResponse(url="/docs")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Handles browser's request for a favicon."""
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/documents", response_model=DocumentResponse)
def create_document(request: DocumentRequest, db: Session = Depends(get_db)):
    try:
        doc_id = add_document(request.content, request.metadata, db)
        return DocumentResponse(document_id=doc_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        response = await get_rag_response(request.query, db)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents")
def delete_all_documents(db: Session = Depends(get_db)):
    try:
        count = db.query(Document).count()
        db.query(Document).delete()
        db.commit()
        return {"message": f"Deleted {count} documents from database"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
