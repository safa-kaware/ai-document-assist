from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, ChatResponse, Source
from app.services.embeddings import embed_query
from app.services.database import search_similar_chunks
from app.services.llm import generate_answer

router = APIRouter()

TOP_K = 4  # how many chunks to retrieve per question


@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # 1. Embed the question
    query_embedding = embed_query(request.question)

    # 2. Retrieve the most relevant chunks for this document
    matches = search_similar_chunks(
        query_embedding=query_embedding,
        document_id=request.document_id,
        top_k=TOP_K,
    )

    if not matches:
        raise HTTPException(
            status_code=404,
            detail="No document found with this ID, or it has no stored content.",
        )

    # 3. Send retrieved context to the LLM
    context_texts = [match["text"] for match in matches]
    try:
        answer = generate_answer(request.question, context_texts)
    except (RuntimeError, ValueError) as e:
        raise HTTPException(status_code=502, detail=f"Failed to generate an answer: {str(e)}")

    # 4. Build a deduplicated source list (same page cited by multiple chunks
    #    should only appear once)
    seen = set()
    sources = []
    for match in matches:
        filename = match["metadata"]["filename"]
        page = match["metadata"]["page"]
        key = (filename, page)
        if key not in seen:
            seen.add(key)
            sources.append(Source(document=filename, page=page))

    return ChatResponse(answer=answer, sources=sources)