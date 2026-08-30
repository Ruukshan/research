"""
Collaborative Filtering Recommendation Module for Sri Lankan A/L Students.

Implements Nearest-Neighbor ($k$-NN) Profile Similarity over historical student profiles.
Incorporates a transparent cold-start fallback mechanism (complying with Section 17).
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from app.ml.config.ml_config import STREAM_CLASSES
from app.ml.preprocessing.pipeline import StudentFeaturePreprocessor
from app.config import settings

logger = logging.getLogger(__name__)


class CollaborativeFilteringRecommender:
    """User-Profile Nearest Neighbors Collaborative Filtering Engine."""

    def __init__(
        self,
        dataset_path: Optional[Path] = None,
        preprocessor_path: Optional[Path] = None,
        n_neighbors: int = 15
    ):
        self.dataset_path = dataset_path or settings.SYNTHETIC_DATA_PATH
        self.preprocessor_path = preprocessor_path or (settings.MODEL_ARTIFACTS_DIR / "preprocessor.joblib")
        self.n_neighbors = n_neighbors
        self.nn_model: Optional[NearestNeighbors] = None
        self.historical_df: Optional[pd.DataFrame] = None
        self.historical_X: Optional[np.ndarray] = None
        self.preprocessor: Optional[StudentFeaturePreprocessor] = None
        self.is_indexed = False

        self._build_peer_index()

    def _build_peer_index(self):
        """Indexes historical/development student profiles for fast nearest neighbor querying."""
        try:
            if not self.dataset_path.exists() or not self.preprocessor_path.exists():
                logger.warning("Dataset or preprocessor not found. CF will operate in heuristic fallback mode.")
                return

            self.historical_df = pd.read_csv(self.dataset_path)
            self.preprocessor = StudentFeaturePreprocessor.load(self.preprocessor_path)

            X_features = self.historical_df.drop(columns=["al_stream", "record_id", "data_source"], errors="ignore")
            self.historical_X = self.preprocessor.transform(X_features)

            self.nn_model = NearestNeighbors(
                n_neighbors=min(self.n_neighbors, len(self.historical_X)),
                metric="cosine"
            )
            self.nn_model.fit(self.historical_X)
            self.is_indexed = True
            logger.info(f"Indexed {len(self.historical_X)} historical student profiles for Collaborative Filtering.")
        except Exception as e:
            logger.warning(f"Failed to build Collaborative Filtering peer index: {e}. Using fallback mechanism.")
            self.is_indexed = False

    def compute_collaborative_scores(
        self,
        student_profile: Dict[str, Any],
        pathways_kb: List[Dict[str, Any]]
    ) -> Tuple[Dict[str, float], str]:
        """
        Finds $k$ most similar peers to the query student, analyzes peer stream selections,
        and computes peer affinity score for each pathway.
        """
        if not self.is_indexed or self.historical_df is None or self.preprocessor is None:
            # Fallback heuristic
            status_msg = "Fallback Prior (Limited Interaction History / Cold-Start Active)"
            collab_scores = {p["pathway_id"]: 0.50 for p in pathways_kb}
            return collab_scores, status_msg

        try:
            df_query = pd.DataFrame([student_profile])
            X_query = self.preprocessor.transform(df_query)

            distances, indices = self.nn_model.kneighbors(X_query)
            peer_indices = indices[0]
            peer_weights = 1.0 - distances[0]  # Cosine similarities
            peer_weights = np.maximum(peer_weights, 0.01)
            norm_weights = peer_weights / peer_weights.sum()

            peer_df = self.historical_df.iloc[peer_indices]

            # Compute peer stream distribution
            peer_stream_distribution = {}
            for stream in STREAM_CLASSES:
                mask = (peer_df["al_stream"] == stream).values
                weighted_support = np.sum(norm_weights[mask])
                peer_stream_distribution[stream] = float(weighted_support)

            collab_scores = {}
            for p in pathways_kb:
                p_stream = p["stream"]
                base_stream_support = peer_stream_distribution.get(p_stream, 0.10)
                # Map into [0.0, 1.0]
                collab_scores[p["pathway_id"]] = float(np.clip(base_stream_support * 1.2, 0.0, 1.0))

            status_msg = f"Active ($k$-NN Nearest Peer Similarity over {len(peer_indices)} similar student profiles)"
            return collab_scores, status_msg

        except Exception as e:
            logger.warning(f"Error computing collaborative scores: {e}. Using fallback.")
            return {p["pathway_id"]: 0.50 for p in pathways_kb}, "Fallback (Error Recovery)"
