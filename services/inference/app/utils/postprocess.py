"""
Post-processing for raw OCR output.

Input: raw string from OCR engine
Output: cleaned, normalized string
"""
from __future__ import annotations

import re


def normalize_whitespace(text: str) -> str:
    """Collapse multiple whitespace characters into a single space, strip edges."""
    return re.sub(r"\s+", " ", text).strip()


def capitalize_sentences(text: str) -> str:
    """Capitalize the first character of each sentence (naive split on '. ')."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(s.capitalize() for s in sentences if s)


def remove_stray_characters(text: str) -> str:
    """Strip isolated non-alphanumeric characters that are likely OCR artefacts."""
    # Remove single non-word characters surrounded by spaces
    return re.sub(r"(?<= )[^\w\s](?= )", "", text)


def postprocess(text: str) -> str:
    """Full post-processing pipeline: normalize → strip artefacts → capitalize."""
    text = normalize_whitespace(text)
    text = remove_stray_characters(text)
    text = capitalize_sentences(text)
    return text
