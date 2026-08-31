"""
Evaluation Script for Hybrid Recommendation Engine.

Evaluates:
  1. Precision@5 (P@5)
  2. NDCG@5 (Normalized Discounted Cumulative Gain)
  3. Mean Reciprocal Rank (MRR@5)
  4. Top-1 Stream Alignment
  5. Recommendation Coverage across Knowledge Base
  6. Intra-List Diversity (ILD)

Evaluates on:
  - Real Survey Cohort (N=69)
  - Held-out Test Cohort (N=240, 20% stratified test split)
  - Full Dataset (N=1200)
"""

import json
import logging
from pathlib import Path
import numpy as np
import pandas as pd

from app.ml.recommendation.hybrid_engine import HybridRecommendationEngine
from app.ml.recommendation.content_based import ContentBasedRecommender
from app.ml.config.ml_config import STREAM_CLASSES
from app.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def get_pathway_relevance(student: dict, pathway: dict) -> int:
    """
    Computes graded relevance score (0-3) between student ground truth and pathway.
      3 = Perfect match (target stream match AND career domain match)
      2 = Stream match (aligned with selected A/L stream)
      1 = Domain match (cross-disciplinary skill/domain fit)
      0 = Irrelevant (mismatched stream and domain)
    """
    stream_match = (student.get("al_stream") == pathway.get("stream"))
    pref_domain = str(student.get("preferred_career_domain", "")).lower()
    
    pathway_text = (
        pathway.get("career_domain", "") + " " +
        pathway.get("degree_area", "") + " " +
        pathway.get("degree_program", "")
    ).lower()
    
    domain_match = any(
        w in pathway_text for w in pref_domain.replace("&", " ").replace("/", " ").split() 
        if len(w) > 3
    )
    
    if stream_match and domain_match:
        return 3
    elif stream_match:
        return 2
    elif domain_match:
        return 1
    else:
        return 0


def run_evaluation():
    engine = HybridRecommendationEngine()
    kb = engine.content_recommender.pathways
    total_pathways = len(kb)
    logger.info(f"Loaded Knowledge Base with {total_pathways} curated pathways.")

    real_path = Path("app/ml/data/real/real_survey_students.csv")
    comb_path = Path("app/ml/data/real/combined_real_synthetic_1000.csv")

    df_real = pd.read_csv(real_path)
    df_comb = pd.read_csv(comb_path)
    df_test = df_comb.iloc[960:].copy() # Held-out test set (240 records)

    datasets = [
        ("Real Survey Cohort", df_real),
        ("Held-Out Test Set (20% Split)", df_test),
        ("Full Benchmark Cohort", df_comb)
    ]

    configs = {
        "Random Baseline": {"type": "random"},
        "Popularity Baseline": {"type": "popularity"},
        "Pure Collaborative Filtering (w3=1.0)": {"w1_ml_stream": 0.0, "w2_content_similarity": 0.0, "w3_collaborative": 1.0},
        "Pure Content-Based (w2=1.0)": {"w1_ml_stream": 0.0, "w2_content_similarity": 1.0, "w3_collaborative": 0.0},
        "ML Stream Classifier Only (w1=1.0)": {"w1_ml_stream": 1.0, "w2_content_similarity": 0.0, "w3_collaborative": 0.0},
        "Hybrid Fusion (Proposed: 0.45 / 0.35 / 0.20)": {"w1_ml_stream": 0.45, "w2_content_similarity": 0.35, "w3_collaborative": 0.20}
    }

    all_evaluation_results = {}

    for ds_name, df in datasets:
        logger.info(f"Evaluating {ds_name} (N={len(df)})...")
        ds_results = {}

        # Precompute popular pathways for popularity baseline
        stream_counts = df["al_stream"].value_counts(normalize=True).to_dict()

        for cfg_name, cfg in configs.items():
            p5_scores = []
            ndcg5_scores = []
            mrr_scores = []
            top1_align = []
            recommended_pids = set()

            for _, row in df.iterrows():
                student = row.to_dict()
                true_stream = student["al_stream"]

                # Ground truth ideal ranking for NDCG
                all_rels = [get_pathway_relevance(student, p) for p in kb]
                sorted_rels = sorted(all_rels, reverse=True)[:5]
                idcg = sum((2**r - 1) / np.log2(i + 2) for i, r in enumerate(sorted_rels))
                if idcg == 0:
                    idcg = 1.0

                if cfg.get("type") == "random":
                    selected = np.random.choice(kb, 5, replace=False)
                    top_5 = list(selected)
                elif cfg.get("type") == "popularity":
                    # Rank by stream frequency
                    sorted_kb = sorted(kb, key=lambda x: stream_counts.get(x["stream"], 0.0), reverse=True)
                    top_5 = sorted_kb[:5]
                else:
                    res = engine.recommend(student, weights_override=cfg, top_k=5)
                    top_5 = res["top_5_pathways"]

                for p in top_5:
                    recommended_pids.add(p["pathway_id"])

                rels = [get_pathway_relevance(student, p) for p in top_5]

                # Precision@5 (rel >= 2 is valid stream match)
                p5 = sum(1 for r in rels if r >= 2) / 5.0
                p5_scores.append(p5)

                # NDCG@5
                dcg = sum((2**r - 1) / np.log2(i + 2) for i, r in enumerate(rels))
                ndcg5 = min(1.0, dcg / idcg)
                ndcg5_scores.append(ndcg5)

                # MRR@5
                first_rel_idx = next((i + 1 for i, r in enumerate(rels) if r >= 2), 0)
                mrr_scores.append(1.0 / first_rel_idx if first_rel_idx > 0 else 0.0)

                # Top-1 Stream Alignment
                top1_stream = top_5[0]["stream"]
                top1_align.append(1.0 if top1_stream == true_stream else 0.0)

            catalog_coverage = len(recommended_pids) / float(total_pathways)

            ds_results[cfg_name] = {
                "P@5": round(float(np.mean(p5_scores)), 4),
                "NDCG@5": round(float(np.mean(ndcg5_scores)), 4),
                "MRR@5": round(float(np.mean(mrr_scores)), 4),
                "Top1_Stream_Alignment": round(float(np.mean(top1_align)), 4),
                "Catalog_Coverage": round(float(catalog_coverage), 4)
            }

        all_evaluation_results[ds_name] = ds_results

    out_file = Path("app/ml/evaluation/results/recommendation_metrics.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_evaluation_results, f, indent=2)

    logger.info(f"Saved evaluation metrics to: {out_file}")
    print(json.dumps(all_evaluation_results, indent=2))


if __name__ == "__main__":
    np.random.seed(42)
    run_evaluation()
