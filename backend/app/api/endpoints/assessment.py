"""Student assessment submission and retrieval endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.assessment import StudentAssessmentInput, AssessmentSubmissionResult
from app.services.assessment_service import AssessmentService

router = APIRouter()


@router.post("/assessment", response_model=AssessmentSubmissionResult, status_code=status.HTTP_201_CREATED, tags=["Assessment"])
def submit_student_assessment(
    assessment: StudentAssessmentInput,
    db: Session = Depends(get_db)
):
    """
    Submits a student's 6-step assessment profile.
    Stores the profile, generates A/L stream probability distributions, and returns ranked top-5 career pathways.
    """
    try:
        result = AssessmentService.process_and_save_assessment(assessment, db)
        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing student assessment: {str(e)}"
        )
