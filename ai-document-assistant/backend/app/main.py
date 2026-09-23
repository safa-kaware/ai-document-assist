from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import upload, chat, documents
from app.config import ALLOWED_ORIGINS
from app.services.embeddings import get_embedding_model

app = FastAPI(title="AI Document Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # local dev
        "https://ai-document-assist-eight.vercel.app",  # deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(documents.router)


@app.on_event("startup")
async def startup_event():
    get_embedding_model()  # load embedding model once, at boot


@app.get("/")
def health_check():
    return {"status": "ok"}