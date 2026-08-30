"""Assessment input and submission schemas."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.schemas.student import (
    AcademicProfileSchema,
    ExtracurricularProfileSchema,
    PersonalityProfileSchema,
    CareerPreferenceSchema,
)


class StudentAssessmentInput(BaseModel):
    """Complete 6-step assessment submission payload."""
    gender: Optional[str] = Field("Prefer not to say", description="Gender demographic")
    district: Optional[str] = Field("Colombo", description="Sri Lankan District")
    school_type: Optional[str] = Field("1AB National School", description="Type of school")
    medium: Optional[str] = Field("Sinhala", description="Instruction Medium")

    academic: AcademicProfileSchema
    extracurricular: ExtracurricularProfileSchema
    personality: PersonalityProfileSchema
    career: CareerPreferenceSchema


class AssessmentSubmissionResult(BaseModel):
    """Result returned after processing an assessment."""
    student_id: str
    record_id: str
    data_source: str
    stream_probabilities: Dict[str, float]
    predicted_stream: str
    recommendations: List[Dict[str, Any]]
    shap_explanation: Optional[Dict[str, Any]] = None
    disclaimer: str = (
        "This system provides AI-assisted career pathway recommendations for educational decision support. "
        "It should not replace advice from qualified teachers, counsellors, parents or career guidance professionals."
    )
