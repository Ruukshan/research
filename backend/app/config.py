"""Configuration management using Pydantic Settings."""

import os
from pathlib import Path
from typing import List, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "app" / "ml"
DATA_DIR = ML_DIR / "data"


class Settings(BaseSettings):
    """Application and ML Pipeline configuration settings."""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "Smart Career Pathway Recommendation System"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api"

    # Data Source & Mode: "synthetic" | "real" | "mixed"
    DATA_MODE: Literal["synthetic", "real", "mixed"] = "synthetic"

    # Database Configuration
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'research_app.db'}"

    # Reproducibility Seed
    RANDOM_SEED: int = 42

    # CORS Origins
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"

    # ML Directory Paths
    SYNTHETIC_DATA_PATH: Path = DATA_DIR / "synthetic" / "synthetic_students.csv"
    REAL_DATA_PATH: Path = DATA_DIR / "real" / "real_survey_students.csv"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    KNOWLEDGE_BASE_PATH: Path = DATA_DIR / "knowledge_base" / "career_pathways.json"
    MODEL_ARTIFACTS_DIR: Path = ML_DIR / "artifacts"
    RESEARCH_RESULTS_DIR: Path = ML_DIR / "evaluation" / "results"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    def is_synthetic(self) -> bool:
        return self.DATA_MODE == "synthetic"

    def is_real(self) -> bool:
        return self.DATA_MODE == "real"

    def is_mixed(self) -> bool:
        return self.DATA_MODE == "mixed"


settings = Settings()

# Ensure directories exist
for directory in [
    DATA_DIR / "synthetic",
    DATA_DIR / "real",
    settings.PROCESSED_DATA_DIR,
    DATA_DIR / "knowledge_base",
    settings.MODEL_ARTIFACTS_DIR,
    settings.RESEARCH_RESULTS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)
