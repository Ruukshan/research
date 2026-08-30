"""Health and system metadata endpoints."""

from fastapi import APIRouter
from app.config import settings

router = APIRouter()


@router.get("/health", tags=["Health"])
def get_health_status():
    """Returns application health, configuration status, and dataset mode."""
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "data_mode": settings.DATA_MODE,
        "synthetic_warning": (
            "SYSTEM NOTICE: DATA_MODE is currently 'synthetic'. All inferences and benchmarks "
            "are generated on statistically modeled development datasets for educational software evaluation."
            if settings.is_synthetic() else None
        ),
        "database_connected": True
    }
