"""Hybrid Recommendation Engine endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.assessment import StudentAssessmentInput
from app.schemas.recommendation import HybridRecommendationResponse
from app.services.assessment_service import AssessmentService
from app.ml.config.ml_config import DEFAULT_WEIGHTS

router = APIRouter()


@router.post("/recommend", response_model=HybridRecommendationResponse, tags=["Recommendation"])
def get_hybrid_recommendations(
    assessment: StudentAssessmentInput,
    db: Session = Depends(get_db)
):
    """
    Computes Top-5 Career Pathway recommendations using score fusion:
    Final Score = w1 * ML Stream Score + w2 * Content Similarity + w3 * Collaborative Score
    """
    result = AssessmentService.process_and_save_assessment(assessment, db)

    return HybridRecommendationResponse(
        student_id=result.student_id,
        predicted_stream=result.predicted_stream,
        top_5_pathways=result.recommendations,
        weights_used=DEFAULT_WEIGHTS,
        cf_data_status="Active (Fallback heuristic applied for cold-start development)"
    )
