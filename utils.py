"""Utility functions for file handling and PDF processing."""
import os
import gc
import tempfile
from typing import BinaryIO, Optional, List

from pdf2image import convert_from_path
from PIL import Image


def save_uploaded_file(
    uploaded_file: BinaryIO,
    suffix: str = ".pdf",
) -> str:
    """Save uploaded file to temporary location."""
    if uploaded_file is None:
        raise ValueError("Uploaded file cannot be None")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(uploaded_file.read())
    temp_file.close()

    return temp_file.name


def convert_pdf_to_images(
    pdf_path: str,
    dpi: int = 300,
) -> List[Image.Image]:
    """Convert PDF pages to PIL Images using pdf2image.

    Returns all pages as RGB PIL Images (alpha removed if present).
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Use a single thread for predictable memory usage
    pil_pages = convert_from_path(pdf_path, dpi=dpi, thread_count=1)

    result: List[Image.Image] = []
    for img in pil_pages:
        # Ensure RGB (remove alpha if present)
        if img.mode == "RGBA":
            rgb_img = Image.new("RGB", img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
            result.append(rgb_img)
        else:
            result.append(img.convert("RGB") if img.mode != "RGB" else img)

    # Hint to GC
    del pil_pages
    gc.collect()

    return result


def normalize_page_lists(
    pages_a: list[Optional[Image.Image]],
    pages_b: list[Optional[Image.Image]],
) -> tuple[list[Optional[Image.Image]], list[Optional[Image.Image]]]:
    """Normalize two page lists to same length by padding with None."""
    max_pages = max(len(pages_a), len(pages_b))
    normalized_a = pages_a + [None] * (max_pages - len(pages_a))
    normalized_b = pages_b + [None] * (max_pages - len(pages_b))

    return normalized_a, normalized_b


def cleanup_temp_files(*file_paths: str) -> None:
    """Remove temporary files safely."""
    for file_path in file_paths:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except (OSError, Exception):
                pass


def save_pdf_from_images(
    images: list[Image.Image],
    output_path: str,
) -> None:
    """Save list of images as multi-page PDF optimized for memory."""
    if not images:
        raise ValueError("Cannot save PDF: images list is empty")

    # Convert all to RGB and optimize
    rgb_images = []
    for img in images:
        if img.mode != "RGB":
            img = img.convert("RGB")
        rgb_images.append(img)

    rgb_images[0].save(
        output_path,
        save_all=True,
        append_images=rgb_images[1:] if len(rgb_images) > 1 else None,
        optimize=True,
        quality=85,
    )

    # Clean up
    del rgb_images
    gc.collect()