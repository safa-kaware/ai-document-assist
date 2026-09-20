import chromadb

from app.config import CHROMA_DIR

_client = None
_collection = None

COLLECTION_NAME = "documents"


def get_collection():
    """
    Returns a persistent ChromaDB collection, creating the client/collection
    once and reusing it across requests (same lazy-singleton pattern as the
    embedding model in Phase 6).
    """
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = _client.get_or_create_collection(name=COLLECTION_NAME)
    return _collection


def add_chunks(chunks: list[dict], embeddings: list[list[float]]):
    """
    Stores chunks + their embeddings + metadata in ChromaDB.
    `chunks` is the output of text_splitter.chunk_pages():
        [{"text": ..., "metadata": {"document_id", "filename", "page", "chunk_id"}}, ...]
    `embeddings` is the matching list of vectors from embeddings.embed_texts().
    """
    collection = get_collection()

    ids = [chunk["metadata"]["chunk_id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )


def search_similar_chunks(query_embedding: list[float], document_id: str, top_k: int = 4) -> list[dict]:
    """
    Finds the top_k chunks most similar to query_embedding, restricted to one document.
    Returns a list like:
    [
        {"text": "...", "metadata": {...}, "distance": 0.23},
        ...
    ]
    Lower distance = more similar.
    """
    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"document_id": document_id},
    )

    matches = []
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for text, metadata, distance in zip(documents, metadatas, distances):
        matches.append({"text": text, "metadata": metadata, "distance": distance})

    return matches


def delete_document(document_id: str):
    """Deletes all chunks belonging to a given document_id."""
    collection = get_collection()
    collection.delete(where={"document_id": document_id})