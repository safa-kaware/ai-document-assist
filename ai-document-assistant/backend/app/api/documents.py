import os

from fastapi import APIRouter, HTTPException

from app.config import UPLOAD_DIR
from app.models.schemas import DocumentListItem
from app.services.database import list_documents, get_document, delete_document_record

router = APIRouter()


@router.get("/api/documents", response_model=list[DocumentListItem])
async def get_documents():
    documents = list_documents()
    return [
        DocumentListItem(
            id=str(doc["id"]),
            filename=doc["filename"],
            size_bytes=doc["size_bytes"],
            page_count=doc["page_count"],
            pages_with_text=doc["pages_with_text"],
        )
        for doc in documents
    ]


@router.delete("/api/documents/{document_id}")
async def delete_document(document_id: str):
    doc = get_document(document_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    file_path = os.path.join(UPLOAD_DIR, doc["saved_filename"])
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass

    delete_document_record(document_id)  # cascades to document_chunks automatically

    return {"status": "deleted", "id": document_id}