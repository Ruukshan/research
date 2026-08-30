"""Hybrid recommendation response and pathway schemas."""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class CareerPathwaySchema(BaseModel):
    pathway_id: str
    stream: str
    degree_area: str
    degree_program: str
    career_domain: str
    required_subjects: List[str]
    preferred_subjects: List[str]
    interest_tags: List[str]
    riasec_profile: Dict[str, float]
    skill_tags: List[str]
    description: str
    sample_job_titles: Optional[List[str]] = None


class PathwayRecommendationItem(BaseModel):
    rank: int = Field(..., ge=1, le=5)
    pathway_id: str
    stream: str
    degree_area: str
    degree_program: str
    career_domain: str
    score: float
    ml_stream_score: float
    content_similarity_score: float
    collaborative_score: float
    compatibility_level: str  # "High Match", "Moderate Match", "Exploratory Match"
    explanation: str
    prerequisites: Optional[List[str]] = None
    sample_job_titles: Optional[List[str]] = None


class HybridRecommendationResponse(BaseModel):
    student_id: Optional[str] = None
    predicted_stream: str
    top_5_pathways: List[PathwayRecommendationItem]
    weights_used: Dict[str, float]
    cf_data_status: str  # e.g., "Active (Cold-start fallback applied if sparse)"
    disclaimer: str = (
        "Educational decision support only. Consult school career guidance teachers and official UGC handbooks."
    )
