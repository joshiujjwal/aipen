from fastapi import FastAPI
from app.routers import health, infer

app = FastAPI(
    title="AIPen Inference Service",
    description="Handwriting OCR and ML inference — TrOCR + Tesseract",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(infer.router, prefix="/infer")
