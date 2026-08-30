"""Pydantic Schemas Package"""
from app.schemas.student import (
    AcademicProfileSchema,
    ExtracurricularProfileSchema,
    PersonalityProfileSchema,
    CareerPreferenceSchema,
    StudentProfileCreate,
    StudentProfileResponse,
)
from app.schemas.assessment import StudentAssessmentInput, AssessmentSubmissionResult
from app.schemas.prediction import StreamPredictionResponse, StreamProbabilities
from app.schemas.recommendation import (
    PathwayRecommendationItem,
    HybridRecommendationResponse,
    CareerPathwaySchema,
)
from app.schemas.evaluation import ModelExperimentRecord, ModelComparisonReport

__all__ = [
    "AcademicProfileSchema",
    "ExtracurricularProfileSchema",
    "PersonalityProfileSchema",
    "CareerPreferenceSchema",
    "StudentProfileCreate",
    "StudentProfileResponse",
    "StudentAssessmentInput",
    "AssessmentSubmissionResult",
    "StreamPredictionResponse",
    "StreamProbabilities",
    "PathwayRecommendationItem",
    "HybridRecommendationResponse",
    "CareerPathwaySchema",
    "ModelExperimentRecord",
    "ModelComparisonReport",
]
