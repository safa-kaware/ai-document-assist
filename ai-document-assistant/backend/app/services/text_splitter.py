import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


def chunk_pages(pages: list[dict], document_id: str, filename: str) -> list[dict]:
    """
    Takes the page-level output from document_loader (list of {page, text})
    and splits it into overlapping chunks, each carrying metadata needed
    later for embeddings and source citations.

    Returns a list like:
    [
        {
            "text": "...",
            "metadata": {
                "document_id": "...",
                "filename": "machine_learning.pdf",
                "page": 5,
                "chunk_id": "..."
            }
        },
        ...
    ]
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )

    chunks = []

    for page in pages:
        page_text = page["text"]
        if not page_text:
            continue  # skip pages with no extractable text — nothing to chunk

        page_chunks = splitter.split_text(page_text)

        for chunk_text in page_chunks:
            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "document_id": document_id,
                    "filename": filename,
                    "page": page["page"],
                    "chunk_id": str(uuid.uuid4()),
                },
            })

    return chunks