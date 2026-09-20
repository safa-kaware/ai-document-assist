from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    filename: str
    size_bytes: int
    status: str
    page_count: int
    pages_with_text: int


class ChatRequest(BaseModel):
    document_id: str
    question: str


class RetrievedChunk(BaseModel):
    text: str
    filename: str
    page: int
    distance: float


class RetrievalResponse(BaseModel):
    question: str
    retrieved_chunks: list[RetrievedChunk]