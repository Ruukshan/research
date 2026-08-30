"""
FastAPI Main Application Entrypoint for Smart Career Pathway Recommendation System.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import init_db
from app.api.endpoints import (
    health,
    assessment,
    prediction,
    recommendation,
    pathways,
    evaluation,
)

# Initialize database tables on import
init_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "Research REST API for AI-assisted GCE A/L Stream & Career Pathway Recommendation System. "
        "Integrates multi-class classification, hybrid recommendation scoring, and SHAP explainability."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files for Research Evaluation Figures
if settings.RESEARCH_RESULTS_DIR.exists():
    app.mount("/static/results", StaticFiles(directory=str(settings.RESEARCH_RESULTS_DIR)), name="results")

# Wire Routers
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(assessment.router, prefix=settings.API_V1_STR)
app.include_router(prediction.router, prefix=settings.API_V1_STR)
app.include_router(recommendation.router, prefix=settings.API_V1_STR)
app.include_router(pathways.router, prefix=settings.API_V1_STR)
app.include_router(evaluation.router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    """Root route with project metadata and disclaimer."""
    return {
        "project": settings.PROJECT_NAME,
        "version": "1.0.0",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
        "data_mode": settings.DATA_MODE,
        "disclaimer": (
            "This system provides AI-assisted career pathway recommendations for educational decision support. "
            "It should not replace advice from qualified teachers, counsellors, parents or career guidance professionals."
        )
    }
