"""
Hybrid Career Pathway Recommendation Engine for Sri Lankan A/L Students.

Fuses:
  1. Machine Learning Multi-Class Stream Probability ($S_{ML}$, weight $w_1$)
  2. Content-Based Knowledge Base Similarity ($S_{Content}$, weight $w_2$)
  3. Collaborative Filtering Peer Preference Score ($S_{Collab}$, weight $w_3$)

Implements diversity promotion and produces ranked Top-5 recommendations with full transparency.
"""

import logging
from typing import Dict, Any, List, Optional
import numpy as np

from app.ml.config.ml_config import DEFAULT_WEIGHTS
from app.ml.prediction.predictor import get_stream_predictor
from app.ml.recommendation.content_based import ContentBasedRecommender
from app.ml.recommendation.collaborative import CollaborativeFilteringRecommender

logger = logging.getLogger(__name__)


class HybridRecommendationEngine:
    """Multi-evidence recommendation fusion engine."""

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None
    ):
        self.weights = weights or DEFAULT_WEIGHTS
        self.content_recommender = ContentBasedRecommender()
        self.collaborative_recommender = CollaborativeFilteringRecommender()
        self.predictor = get_stream_predictor()

    def recommend(
        self,
        student_profile: Dict[str, Any],
        weights_override: Optional[Dict[str, float]] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Executes complete hybrid recommendation pipeline for a student profile.
        Returns Top-5 ranked career pathways with score decomposition and explanations.
        """
        w = weights_override or self.weights
        w1 = w.get("w1_ml_stream", 0.45)
        w2 = w.get("w2_content_similarity", 0.35)
        w3 = w.get("w3_collaborative", 0.20)

        # 1. Obtain ML Stream Probabilities
        ml_prediction = self.predictor.predict_profile(student_profile)
        stream_probs = ml_prediction["stream_probabilities"]
        predicted_stream = ml_prediction["predicted_stream"]
        model_name = ml_prediction["model_name"]

        # 2. Obtain Content-Based Pathway Similarities
        content_scored = self.content_recommender.score_all_pathways(student_profile)

        # 3. Obtain Collaborative Peer Filtering Scores
        collab_scores, cf_status = self.collaborative_recommender.compute_collaborative_scores(
            student_profile, self.content_recommender.pathways
        )

        # 4. Score Fusion
        fused_pathways = []
        for item in content_scored:
            pid = item["pathway_id"]
            stream = item["stream"]
            ml_stream_score = stream_probs.get(stream, 0.10)
            content_sim_score = item["content_similarity_score"]
            collab_score = collab_scores.get(pid, 0.50)

            # Linear Weighted Score Fusion
            final_score = (w1 * ml_stream_score) + (w2 * content_sim_score) + (w3 * collab_score)
            final_score = float(np.round(np.clip(final_score, 0.0, 1.0), 4))

            fused_pathways.append({
                "pathway_id": pid,
                "stream": stream,
                "degree_area": item["degree_area"],
                "degree_program": item["degree_program"],
                "career_domain": item["career_domain"],
                "score": final_score,
                "ml_stream_score": round(ml_stream_score, 4),
                "content_similarity_score": round(content_sim_score, 4),
                "collaborative_score": round(collab_score, 4),
                "riasec_match": item.get("riasec_match", 0.0),
                "academic_match": item.get("academic_match", 0.0),
                "interest_match": item.get("interest_match", 0.0),
                "required_subjects": item.get("required_subjects", []),
                "preferred_subjects": item.get("preferred_subjects", []),
                "sample_job_titles": item.get("sample_job_titles", []),
                "description": item.get("description", "")
            })

        # 5. Sort by Fused Score
        fused_pathways.sort(key=lambda x: x["score"], reverse=True)

        # 6. Diversity Promotion (Section 19: avoid returning 5 identical variations)
        top_selected = []
        seen_degree_areas = set()

        # First pass: Pick distinct degree areas from top candidates
        for item in fused_pathways:
            if item["degree_area"] not in seen_degree_areas:
                top_selected.append(item)
                seen_degree_areas.add(item["degree_area"])
                if len(top_selected) == top_k:
                    break

        # Fallback if knowledge base has fewer unique degree areas than top_k
        if len(top_selected) < top_k:
            for item in fused_pathways:
                if item not in top_selected:
                    top_selected.append(item)
                    if len(top_selected) == top_k:
                        break

        # 7. Add Rank and Qualitative Explanations
        ranked_results = []
        for rank, item in enumerate(top_selected, start=1):
            score = item["score"]
            if score >= 0.75:
                compat = "High Match"
            elif score >= 0.55:
                compat = "Moderate Match"
            else:
                compat = "Exploratory Match"

            explanation = (
                f"Ranked #{rank} with a {compat} ({score*100:.1f}%). "
                f"Driven by strong {item['stream']} probability ({item['ml_stream_score']*100:.1f}%), "
                f"RIASEC personality alignment ({item['riasec_match']*100:.1f}%), and subject prerequisites fit ({item['academic_match']*100:.1f}%)."
            )

            item["rank"] = rank
            item["compatibility_level"] = compat
            item["explanation"] = explanation
            ranked_results.append(item)

        return {
            "predicted_stream": predicted_stream,
            "model_name": model_name,
            "stream_probabilities": stream_probs,
            "top_5_pathways": ranked_results,
            "weights_used": {"w1_ml_stream": w1, "w2_content_similarity": w2, "w3_collaborative": w3},
            "cf_status": cf_status
        }


_hybrid_recommender_instance: Optional[HybridRecommendationEngine] = None


def get_hybrid_recommender() -> HybridRecommendationEngine:
    """Singleton getter for HybridRecommendationEngine."""
    global _hybrid_recommender_instance
    if _hybrid_recommender_instance is None:
        _hybrid_recommender_instance = HybridRecommendationEngine()
    return _hybrid_recommender_instance
