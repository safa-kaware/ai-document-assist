import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.config import UPLOAD_DIR, MAX_FILE_SIZE_BYTES, ALLOWED_EXTENSIONS
from app.models.schemas import DocumentResponse
from app.services.document_loader import extract_text_from_pdf, PDFExtractionError
from app.services.text_splitter import chunk_pages
from app.services.embeddings import embed_texts
from app.services.vector_store import add_chunks

router = APIRouter()


@router.post("/api/documents/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Only PDF is supported right now.",
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE_BYTES // (1024*1024)} MB.",
        )
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    document_id = str(uuid.uuid4())
    safe_filename = f"{document_id}{ext}"
    save_path = os.path.join(UPLOAD_DIR, safe_filename)

    try:
        with open(save_path, "wb") as f:
            f.write(contents)
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to save the uploaded file.")

    try:
        pages = extract_text_from_pdf(save_path)
    except PDFExtractionError as e:
        os.remove(save_path)
        raise HTTPException(status_code=422, detail=str(e))

    pages_with_text = sum(1 for p in pages if p["text"])

    chunks = chunk_pages(pages, document_id=document_id, filename=file.filename)

    try:
        chunk_texts = [c["text"] for c in chunks]
        vectors = embed_texts(chunk_texts)
        add_chunks(chunks, vectors)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document for search: {str(e)}")

    return DocumentResponse(
        id=document_id,
        filename=file.filename,
        size_bytes=len(contents),
        status="uploaded",
        page_count=len(pages),
        pages_with_text=pages_with_text,
    )