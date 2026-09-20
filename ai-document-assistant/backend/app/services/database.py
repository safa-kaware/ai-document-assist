import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector

from app.config import DATABASE_URL

_connection = None


def get_connection():
    """Lazy singleton connection, reused across requests."""
    global _connection
    if _connection is None or _connection.closed:
        _connection = psycopg2.connect(DATABASE_URL)
        register_vector(_connection)
    return _connection


def add_document(document: dict):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO documents (id, filename, size_bytes, page_count, pages_with_text, saved_filename)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                document["id"],
                document["filename"],
                document["size_bytes"],
                document["page_count"],
                document["pages_with_text"],
                document["saved_filename"],
            ),
        )
    conn.commit()


def list_documents() -> list[dict]:
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT id, filename, size_bytes, page_count, pages_with_text FROM documents ORDER BY created_at DESC"
        )
        return [dict(row) for row in cur.fetchall()]


def get_document(document_id: str) -> dict | None:
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM documents WHERE id = %s", (document_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def delete_document_record(document_id: str) -> bool:
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM documents WHERE id = %s", (document_id,))
        deleted = cur.rowcount > 0
    conn.commit()
    return deleted


def add_chunks(chunks: list[dict], embeddings: list[list[float]]):
    conn = get_connection()
    with conn.cursor() as cur:
        for chunk, embedding in zip(chunks, embeddings):
            cur.execute(
                """
                INSERT INTO document_chunks (document_id, chunk_text, page, embedding)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    chunk["metadata"]["document_id"],
                    chunk["text"],
                    chunk["metadata"]["page"],
                    embedding,
                ),
            )
    conn.commit()

def search_similar_chunks(query_embedding: list[float], document_id: str, top_k: int = 4) -> list[dict]:
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT dc.chunk_text, dc.page, d.filename,
                   dc.embedding <=> %s::vector AS distance
            FROM document_chunks dc
            JOIN documents d ON d.id = dc.document_id
            WHERE dc.document_id = %s
            ORDER BY distance ASC
            LIMIT %s
            """,
            (query_embedding, document_id, top_k),
        )
        rows = cur.fetchall()


    return [
        {
            "text": row["chunk_text"],
            "metadata": {"filename": row["filename"], "page": row["page"]},
            "distance": float(row["distance"]),
        }
        for row in rows
    ]