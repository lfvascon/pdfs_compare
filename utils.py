"""Utility functions for file handling and PDF processing."""
import os
import tempfile
from pathlib import Path
from typing import BinaryIO, Optional

from pdf2image import convert_from_path
from PIL import Image


def save_uploaded_file(
    uploaded_file: BinaryIO,
    suffix: str = ".pdf",
) -> str:
    """Save uploaded file to temporary location.

    Args:
        uploaded_file: Streamlit uploaded file object.
        suffix: File suffix.

    Returns:
        Path to temporary file.
    """
    if uploaded_file is None:
        raise ValueError("Uploaded file cannot be None")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(uploaded_file.read())
    temp_file.close()

    return temp_file.name


def convert_pdf_to_images(
    pdf_path: str,
    dpi: int = 200,
) -> list[Image.Image]:
    """Convert PDF pages to PIL Images.

    Args:
        pdf_path: Path to PDF file.
        dpi: Resolution for conversion.

    Returns:
        List of PIL Images, one per page.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    return convert_from_path(pdf_path, dpi=dpi)


def normalize_page_lists(
    pages_a: list[Optional[Image.Image]],
    pages_b: list[Optional[Image.Image]],
) -> tuple[list[Optional[Image.Image]], list[Optional[Image.Image]]]:
    """Normalize two page lists to same length by padding with None.

    Args:
        pages_a: First list of pages.
        pages_b: Second list of pages.

    Returns:
        Tuple of normalized page lists.
    """
    max_pages = max(len(pages_a), len(pages_b))
    normalized_a = pages_a + [None] * (max_pages - len(pages_a))
    normalized_b = pages_b + [None] * (max_pages - len(pages_b))

    return normalized_a, normalized_b


def cleanup_temp_files(*file_paths: str) -> None:
    """Remove temporary files safely.

    Args:
        *file_paths: Variable number of file paths to remove.
    """
    for file_path in file_paths:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass  # Ignore errors during cleanup


def save_pdf_from_images(
    images: list[Image.Image],
    output_path: str,
) -> None:
    """Save list of images as multi-page PDF.

    Args:
        images: List of PIL Images.
        output_path: Output PDF file path.

    Raises:
        ValueError: If images list is empty.
    """
    if not images:
        raise ValueError("Cannot save PDF: images list is empty")

    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:] if len(images) > 1 else None,
    )

