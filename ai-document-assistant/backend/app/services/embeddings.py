from sentence_transformers import SentenceTransformer

_model = None  # loaded lazily, once, and reused


def get_embedding_model() -> SentenceTransformer:
    """
    Loads the embedding model once and caches it in memory.
    Loading the model from disk takes a second or two — we don't
    want to repeat that on every request.
    """
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embeds a list of text chunks. Returns a list of vectors (one per input text),
    each a list of floats of fixed length (384 dimensions for this model).
    """
    model = get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


def embed_query(text: str) -> list[float]:
    """
    Embeds a single piece of text — used for the user's question at query time.
    Kept as a separate function from embed_texts for clarity of intent,
    even though the underlying call is the same.
    """
    model = get_embedding_model()
    embedding = model.encode([text], show_progress_bar=False)[0]
    return embedding.tolist()