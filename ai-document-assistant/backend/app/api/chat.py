from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, RetrievalResponse, RetrievedChunk
from app.services.embeddings import embed_query
from app.services.vector_store import search_similar_chunks

router = APIRouter()

TOP_K = 4  # how many chunks to retrieve per question


@router.post("/api/documents/retrieve-test", response_model=RetrievalResponse)
async def retrieve_test(request: ChatRequest):
    """
    TEMPORARY endpoint for Phase 8 testing only.
    Embeds the question, searches ChromaDB, returns raw matches.
    Will be replaced by the real /api/chat endpoint in Phase 9.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    query_embedding = embed_query(request.question)

    matches = search_similar_chunks(
        query_embedding=query_embedding,
        document_id=request.document_id,
        top_k=TOP_K,
    )

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="No matching document found, or the document has no stored chunks.",
        )

    retrieved_chunks = [
        RetrievedChunk(
            text=match["text"],
            filename=match["metadata"]["filename"],
            page=match["metadata"]["page"],
            distance=match["distance"],
        )
        for match in matches
    ]

    return RetrievalResponse(question=request.question, retrieved_chunks=retrieved_chunks)