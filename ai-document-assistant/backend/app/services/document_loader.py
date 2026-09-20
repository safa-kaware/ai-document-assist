import pymupdf as fitz


class PDFExtractionError(Exception):
    """Raised when a PDF cannot be opened or has no usable text."""
    pass


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extracts text from a PDF, page by page.
    Returns a list like:
    [
        {"page": 1, "text": "..."},
        {"page": 2, "text": "..."},
    ]
    Pages with no extractable text are included with an empty string,
    not silently dropped — this matters later for accurate page citations.
    """
    try:
        doc = fitz.open(file_path)
    except Exception:
        raise PDFExtractionError("The file could not be opened. It may be corrupted or not a valid PDF.")

    if doc.page_count == 0:
        doc.close()
        raise PDFExtractionError("The PDF has no pages.")

    pages = []
    total_extracted_chars = 0

    for page_number, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        pages.append({"page": page_number, "text": text})
        total_extracted_chars += len(text)

    doc.close()

    if total_extracted_chars == 0:
        raise PDFExtractionError(
            "No extractable text was found in this PDF. "
            "It may be a scanned/image-based document (OCR is not supported yet)."
        )

    return pages