"""
PDF extraction utilities for VERITYAI.

This module extracts text from PDF files without modifying
the original document.
"""

from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(file_path: str | Path) -> str:
    """
    Extract text from all pages of a PDF file.

    Parameters
    ----------
    file_path : str | Path
        Path to the PDF file.

    Returns
    -------
    str
        Extracted text from the PDF.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got: {path.suffix}")

    try:
        reader = PdfReader(path)
    except Exception as exc:
        raise RuntimeError(
            f"Unable to read PDF file: {path}"
        ) from exc

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
            extracted_pages.append(
                f"--- Page {page_number} ---\n{text}"
            )
        except Exception as exc:
            extracted_pages.append(
                f"--- Page {page_number} ---\n"
                f"[Unable to extract text: {exc}]"
            )

    return "\n\n".join(extracted_pages)


if __name__ == "__main__":
    print("PDF parser module loaded successfully.")