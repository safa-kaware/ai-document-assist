import os
from fastembed import TextEmbedding

_model = None  # loaded lazily, once, and reused

# Small, ONNX-based embedding model — low memory footprint vs. PyTorch-based
# sentence-transformers. 384-dim output.
MODEL_NAME = "BAAI/bge-small-en-v1.5"

# Explicit local cache dir so the model is downloaded once and reused across
# requests/restarts within the same container filesystem, instead of being
# re-fetched from the network on every cold process.
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", ".model_cache")


def get_embedding_model() -> TextEmbedding:
    """
    Loads the embedding model once and caches it in memory (and on disk).
    threads=1 keeps ONNX Runtime from spinning up multiple threads/buffers,
    which matters on memory-constrained hosts like Render's free tier.
    """
    global _model
    if _model is None:
        _model = TextEmbedding(
            model_name=MODEL_NAME,
            cache_dir=CACHE_DIR,
            threads=1,
        )
    return _model


def embed_texts(texts: list[str], batch_size: int = 8) -> list[list[float]]:
    """
    Embeds a list of text chunks in small batches to keep peak memory low.
    Returns a list of vectors (one per input text), each 384-dimensional.
    """
    model = get_embedding_model()
    embeddings = model.embed(texts, batch_size=batch_size)
    return [vec.tolist() for vec in embeddings]


def embed_query(text: str) -> list[float]:
    """
    Embeds a single piece of text — used for the user's question at query time.
    """
    model = get_embedding_model()
    embedding = next(model.embed([text]))
    return embedding.tolist()