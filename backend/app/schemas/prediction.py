"""Machine Learning Prediction Schemas."""

from typing import Dict, Optional, Any, List
from pydantic import BaseModel, Field, ConfigDict


class StreamProbabilities(BaseModel):
    """Five-class probability distribution."""
    model_config = ConfigDict(populate_by_name=True)

    physical_science: float = Field(..., alias="Physical Science")
    biological_science: float = Field(..., alias="Biological Science")
    commerce: float = Field(..., alias="Commerce")
    arts: float = Field(..., alias="Arts")
    technology: float = Field(..., alias="Technology")


class ShapFeatureContribution(BaseModel):
    feature_name: str
    feature_value: Any
    shap_value: float
    contribution_type: str  # "positive" | "negative"
    friendly_description: str


class ShapExplanationResult(BaseModel):
    predicted_stream: str
    base_value: float
    top_positive_factors: List[ShapFeatureContribution]
    top_negative_factors: List[ShapFeatureContribution]
    feature_contributions: List[ShapFeatureContribution]
    summary_text: str


class StreamPredictionResponse(BaseModel):
    model_name: str
    model_version: str
    predicted_stream: str
    stream_probabilities: Dict[str, float]
    shap_explanation: Optional[ShapExplanationResult] = None
