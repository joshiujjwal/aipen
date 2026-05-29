"""
Image pre-processing pipeline for handwriting OCR.

All functions accept PIL.Image and return PIL.Image.
Callers are responsible for file I/O.
"""
from __future__ import annotations

from PIL import Image, ImageOps, ImageEnhance


MAX_WIDTH = 1024


def resize_to_max_width(image: Image.Image, max_width: int = MAX_WIDTH) -> Image.Image:
    """Downscale image so width ≤ max_width, preserving aspect ratio."""
    if image.width <= max_width:
        return image
    ratio = max_width / image.width
    new_height = int(image.height * ratio)
    return image.resize((max_width, new_height), Image.LANCZOS)


def to_grayscale(image: Image.Image) -> Image.Image:
    """Convert image to grayscale (mode 'L')."""
    return ImageOps.grayscale(image)


def enhance_contrast(image: Image.Image, factor: float = 2.0) -> Image.Image:
    """Apply contrast enhancement (simple PIL approach; CLAHE requires OpenCV)."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def preprocess(image: Image.Image) -> Image.Image:
    """Full pre-processing pipeline: resize → grayscale → contrast."""
    image = resize_to_max_width(image)
    image = to_grayscale(image)
    image = enhance_contrast(image)
    return image
