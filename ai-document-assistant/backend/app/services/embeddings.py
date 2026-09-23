from fastembed import TextEmbedding

_model = None  # loaded lazily, once, and reused

# BAAI/bge-small-en-v1.5 is a close equivalent to all-MiniLM-L6-v2 in
# quality and size, but runs via ONNX Runtime (fastembed) instead of
# PyTorch — this uses a fraction of the memory, which is what fixes
# the OOM kill on Render's 512MB free tier.
# NOTE: this model outputs 384-dim vectors, same as MiniLM-L6-v2, so
# your ChromaDB collection dimension is unaffected — but the actual
# vector values differ from the old model, so you MUST re-embed and
# re-store any documents that were embedded with the old model.
MODEL_NAME = "BAAI/bge-small-en-v1.5"


def get_embedding_model() -> TextEmbedding:
    """
    Loads the embedding model once and caches it in memory.
    fastembed uses ONNX Runtime under the hood instead of PyTorch,
    which keeps peak memory well under Render's 512MB free-tier limit.
    """
    global _model
    if _model is None:
        _model = TextEmbedding(model_name=MODEL_NAME)
    return _model


def embed_texts(texts: list[str], batch_size: int = 16) -> list[list[float]]:
    """
    Embeds a list of text chunks in small batches to keep peak memory low
    on memory-constrained environments (e.g. Render's free tier).
    Returns a list of vectors (one per input text), each 384-dimensional.
    """
    model = get_embedding_model()
    # fastembed's .embed() returns a generator of numpy arrays
    embeddings = model.embed(texts, batch_size=batch_size)
    return [vec.tolist() for vec in embeddings]


def embed_query(text: str) -> list[float]:
    """
    Embeds a single piece of text — used for the user's question at query time.
    Kept as a separate function from embed_texts for clarity of intent,
    even though the underlying call is the same.
    """
    model = get_embedding_model()
    embedding = next(model.embed([text]))
    return embedding.tolist()