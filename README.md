# AI Document Assistant

An AI-powered document Q&A tool built with a Retrieval-Augmented Generation (RAG) pipeline. Upload a PDF, ask questions about it, and get answers grounded in the document's actual content — with page-level source citations.

**Live demo:** [ai-document-assist-eight.vercel.app](https://ai-document-assist-eight.vercel.app/)

> Note: the backend runs on Render's free tier and spins down after periods of inactivity. The first request after idle time may take up to a minute while it wakes up — please allow it to load before testing.

---

## How it works

1. **Upload** a PDF document through the web interface.
2. The backend **extracts text**, splits it into overlapping chunks, and generates vector **embeddings** for each chunk.
3. Chunks are stored in a **vector database**.
4. When you ask a question, it's embedded the same way and used to **retrieve the most relevant chunks** from the document.
5. Those chunks are passed to an **LLM**, which generates an answer grounded only in the retrieved context — along with the document and page number each part of the answer came from.

This approach (RAG) keeps answers accurate and traceable, instead of relying on the LLM's general knowledge, which can hallucinate facts not actually in the document.

---

## Tech stack

**Frontend**
- React + Vite
- Tailwind CSS

**Backend**
- Python + FastAPI + Uvicorn
- PyMuPDF for PDF text extraction
- LangChain text splitters for chunking
- fastembed (ONNX-based) for local embedding generation
- ChromaDB as the vector store
- Groq API for LLM-generated answers

**Deployment**
- Frontend: Vercel
- Backend: Render
- (Planned) Vector storage migration: Supabase (PostgreSQL + pgvector)

---

## Project structure

```
ai-document-assistant/
├── frontend/           # React + Vite app
│   └── src/
└── backend/
    ├── app/
    │   ├── api/        # Route handlers (upload, chat, documents)
    │   ├── services/    # Embedding, vector DB, LLM logic
    │   └── main.py      # FastAPI app entrypoint
    └── requirements.txt
```

---

## Running locally

**Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

Create a `.env` file in `backend/` with your Groq API key and any other required config (see `app/config.py`).

---

## Key RAG concepts used

- **Chunking:** splitting long documents into smaller overlapping pieces so relevant context can be retrieved precisely, without exceeding the LLM's context window.
- **Embeddings:** converting text into numerical vectors that capture semantic meaning, enabling similarity-based search instead of keyword matching.
- **Vector search:** finding the chunks most semantically relevant to a question by comparing embedding vectors.
- **Grounded generation:** the LLM is instructed to answer only from retrieved context, reducing hallucination and enabling source citations.

---

## Author

Built by Safa — Computer Science (AI & ML) student, as a portfolio project.
