"""
Stream Predictor Inference Service.

Loads the trained best model artifact and fitted feature preprocessor
to generate five-class A/L stream probability distributions for student intake profiles.
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import joblib

from app.ml.config.ml_config import STREAM_CLASSES, STREAM_TO_IDX, IDX_TO_STREAM
from app.ml.preprocessing.pipeline import StudentFeaturePreprocessor
from app.config import settings

logger = logging.getLogger(__name__)


class StreamPredictor:
    """Inference engine for GCE A/L stream predictions."""

    def __init__(self, model_path: Optional[Path] = None, preprocessor_path: Optional[Path] = None):
        self.model_path = model_path or (settings.MODEL_ARTIFACTS_DIR / "best_stream_model.joblib")
        self.preprocessor_path = preprocessor_path or (settings.MODEL_ARTIFACTS_DIR / "preprocessor.joblib")
        self.model_name = "Heuristic Fallback"
        self.model = None
        self.preprocessor: Optional[StudentFeaturePreprocessor] = None
        self._load_artifacts()

    def _load_artifacts(self):
        """Loads model and preprocessor if available on disk."""
        try:
            if self.preprocessor_path.exists():
                self.preprocessor = StudentFeaturePreprocessor.load(self.preprocessor_path)
                logger.info("Loaded StudentFeaturePreprocessor from disk.")

            if self.model_path.exists():
                loaded = joblib.load(self.model_path)
                if isinstance(loaded, dict) and "model" in loaded:
                    self.model = loaded["model"]
                    self.model_name = loaded.get("model_name", "Best Trained Model")
                else:
                    self.model = loaded
                    self.model_name = "Trained ML Model"
                logger.info(f"Loaded ML model '{self.model_name}' from disk.")
        except Exception as e:
            logger.warning(f"Could not load ML artifacts: {e}. Inference will fall back to domain heuristic.")

    def is_ml_ready(self) -> bool:
        """Returns True if both model and preprocessor are loaded."""
        return self.model is not None and self.preprocessor is not None

    def predict_profile(self, student_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accepts a student record dictionary, applies preprocessing,
        and returns multi-class stream probabilities and the winning prediction.
        """
        if not self.is_ml_ready():
            # Domain heuristic fallback
            return {
                "model_name": "Domain Heuristic (Fallback)",
                "predicted_stream": "Physical Science",
                "stream_probabilities": {s: 0.20 for s in STREAM_CLASSES}
            }

        # Convert dictionary to single-row DataFrame
        df = pd.DataFrame([student_dict])
        X_proc = self.preprocessor.transform(df)

        probs_arr = self.model.predict_proba(X_proc)[0]  # Shape: (5,)
        stream_probs = {STREAM_CLASSES[i]: float(np.round(probs_arr[i], 4)) for i in range(len(STREAM_CLASSES))}

        # Normalize to ensure sum = 1.0
        total_p = sum(stream_probs.values())
        if total_p > 0:
            stream_probs = {k: round(v / total_p, 4) for k, v in stream_probs.items()}

        predicted_stream = max(stream_probs, key=stream_probs.get)

        return {
            "model_name": self.model_name,
            "predicted_stream": predicted_stream,
            "stream_probabilities": stream_probs
        }


# Global singleton instance
_predictor_instance: Optional[StreamPredictor] = None


def get_stream_predictor() -> StreamPredictor:
    """Returns singleton StreamPredictor instance."""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = StreamPredictor()
    return _predictor_instance
