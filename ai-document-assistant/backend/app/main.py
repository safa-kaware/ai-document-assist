from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import upload, chat, documents
from app.config import ALLOWED_ORIGINS

app = FastAPI(title="AI Document Assistant API")

app.add_middleware(
    CORSMiddleware,
       allow_origins=[
        "http://localhost:5173",  # local dev
        "https://ai-document-assist-eight.vercel.app",  # your deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(documents.router)


@app.get("/")
def health_check():
    return {"status": "ok"}