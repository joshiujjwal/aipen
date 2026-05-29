from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["infer"])

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
SUPPORTED_MIME_TYPES = {"image/png", "image/jpeg", "image/tiff"}


class WordResult(BaseModel):
    word: str
    confidence: float
    bbox: tuple[int, int, int, int]  # x, y, w, h


class RecognitionResult(BaseModel):
    job_id: str
    text: str
    words: list[WordResult]
    engine: str
    model_version: str
    processing_ms: int


@router.post("/", response_model=RecognitionResult)
async def infer_image(
    file: UploadFile = File(...),
    engine: str = "trocr",
    job_id: str = "standalone",
) -> RecognitionResult:
    """
    Accept an image upload and return handwriting recognition result.
    Supports engines: 'trocr' (default), 'tesseract'.
    """
    # Validate MIME type
    if file.content_type not in SUPPORTED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. "
                   f"Supported: {', '.join(SUPPORTED_MIME_TYPES)}",
        )

    # Validate file size
    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds 10 MB limit")

    # TODO Phase 1: plug in real OCR pipeline
    # from app.models.trocr import get_trocr_model
    # result = await run_inference(contents, engine)
    raise HTTPException(status_code=501, detail="Inference not yet implemented — see TODO.md Phase 1")
