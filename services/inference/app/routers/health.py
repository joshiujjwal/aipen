from fastapi import APIRouter
import platform
import sys

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def health_check() -> dict:
    """Health check — returns service status and Python version."""
    return {
        "status": "ok",
        "service": "inference",
        "python": sys.version,
        "platform": platform.system(),
        # TODO: add model loaded status once model loader is implemented
    }
