"""Stream Prediction & SHAP Explanation endpoints."""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.assessment import StudentAssessmentInput
from app.schemas.prediction import StreamPredictionResponse
from app.services.assessment_service import AssessmentService
from app.ml.prediction.predictor import get_stream_predictor
from app.ml.explainability.shap_explainer import get_shap_explainer

router = APIRouter()


@router.post("/predict", response_model=StreamPredictionResponse, tags=["Prediction"])
def predict_stream_distribution(
    assessment: StudentAssessmentInput
):
    """
    Computes 5-class A/L stream probability distribution and local SHAP feature explanations.
    """
    flat_dict = AssessmentService._extract_flat_dict(assessment)
    predictor = get_stream_predictor()
    pred_res = predictor.predict_profile(flat_dict)

    predicted_stream = pred_res["predicted_stream"]
    stream_probs = pred_res["stream_probabilities"]
    model_name = pred_res["model_name"]

    # Compute SHAP explanation
    explainer = get_shap_explainer()
    shap_res = explainer.explain_instance(flat_dict, predicted_stream)

    return StreamPredictionResponse(
        model_name=model_name,
        model_version="v1.0.0",
        predicted_stream=predicted_stream,
        stream_probabilities=stream_probs,
        shap_explanation=shap_res
    )
