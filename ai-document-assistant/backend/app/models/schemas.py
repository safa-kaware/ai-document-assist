from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    filename: str
    size_bytes: int
    status: str
    page_count: int
    pages_with_text: int


class DocumentListItem(BaseModel):
    id: str
    filename: str
    size_bytes: int
    page_count: int
    pages_with_text: int


class ChatRequest(BaseModel):
    document_id: str
    question: str


class Source(BaseModel):
    document: str
    page: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]