"""Unit tests for Hybrid Recommendation Engine and SHAP Explainability."""

import pytest
from app.ml.generator.synthetic_generator import SyntheticDatasetGenerator
from app.ml.recommendation.content_based import ContentBasedRecommender
from app.ml.recommendation.collaborative import CollaborativeFilteringRecommender
from app.ml.recommendation.hybrid_engine import HybridRecommendationEngine
from app.ml.explainability.shap_explainer import ShapExplainer


@pytest.fixture
def sample_profile():
    generator = SyntheticDatasetGenerator(random_seed=42)
    return generator.generate_record(1)


def test_content_based_recommender(sample_profile):
    recommender = ContentBasedRecommender()
    results = recommender.score_all_pathways(sample_profile)

    assert len(results) >= 10
    for item in results:
        assert "pathway_id" in item
        assert "stream" in item
        assert 0.0 <= item["content_similarity_score"] <= 1.0
        assert 0.0 <= item["riasec_match"] <= 1.0


def test_collaborative_filtering_recommender(sample_profile):
    cf = CollaborativeFilteringRecommender()
    cb = ContentBasedRecommender()
    scores, status = cf.compute_collaborative_scores(sample_profile, cb.pathways)

    assert len(scores) == len(cb.pathways)
    assert len(status) > 0
    for pid, score in scores.items():
        assert 0.0 <= score <= 1.0


def test_hybrid_recommendation_engine(sample_profile):
    engine = HybridRecommendationEngine()
    res = engine.recommend(sample_profile)

    assert "predicted_stream" in res
    assert "stream_probabilities" in res
    assert len(res["stream_probabilities"]) == 5
    assert len(res["top_5_pathways"]) == 5

    # Check ranks 1 to 5
    ranks = [item["rank"] for item in res["top_5_pathways"]]
    assert ranks == [1, 2, 3, 4, 5]

    # Verify scores are sorted descending or diverse
    scores = [item["score"] for item in res["top_5_pathways"]]
    assert all(0.0 <= s <= 1.0 for s in scores)


def test_shap_explainer(sample_profile):
    explainer = ShapExplainer()
    explanation = explainer.explain_instance(sample_profile, "Physical Science")

    assert "predicted_stream" in explanation
    assert "top_positive" in explanation
    assert "top_negative" in explanation
    assert len(explanation["top_positive"]) > 0
    assert len(explanation["top_negative"]) > 0
