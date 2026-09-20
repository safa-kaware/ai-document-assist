from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL

SYSTEM_PROMPT = """You are an AI document assistant.
Answer the user's question using ONLY the provided document context.
If the answer cannot be found in the provided document context, say:
"I couldn't find this information in the uploaded document."
Do not invent information.
Do not use unsupported outside knowledge."""

_client = None


def get_client() -> Groq:
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set. Check your backend/.env file.")
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def generate_answer(question: str, context_chunks: list[str]) -> str:
    """
    Sends the question + retrieved context to Groq, returns the answer text.
    context_chunks is a list of raw chunk text strings from retrieval.
    """
    context = "\n\n---\n\n".join(context_chunks)

    user_message = f"""Context:
{context}

Question:
{question}"""

    client = get_client()

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,  # low temperature — we want grounded, consistent answers, not creativity
        )
    except Exception as e:
        raise RuntimeError(f"Groq API call failed: {str(e)}")

    return response.choices[0].message.content