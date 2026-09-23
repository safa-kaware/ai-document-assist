from fastembed import TextEmbedding

_model = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = TextEmbedding(
            model_name="BAAI/bge-small-en-v1.5",
            threads=1,  # limit ONNX Runtime threads on constrained memory
        )
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