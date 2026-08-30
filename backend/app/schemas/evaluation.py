"""Model evaluation and experiment report schemas."""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ModelExperimentRecord(BaseModel):
    experiment_id: str
    date: datetime
    dataset_source: str  # "synthetic" | "real" | "mixed"
    dataset_size: int
    feature_version: str
    preprocessing_version: str
    model_name: str
    hyperparameters: Dict[str, Any]
    cv_mean: float
    cv_std: float
    test_accuracy: float
    test_precision: float
    test_recall: float
    test_f1: float
    random_seed: int
    selected_model: bool
    notes: Optional[str] = None


class ModelComparisonReport(BaseModel):
    dataset_source: str
    total_samples: int
    models: List[ModelExperimentRecord]
    selected_model_name: str
    evaluation_summary: str
    created_at: datetime
