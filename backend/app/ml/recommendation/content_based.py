"""
Content-Based Career Pathway Recommendation Module.

Computes multi-dimensional compatibility between a student's profile and
curated Sri Lankan degree/career pathways in the knowledge base using:
  1. Holland RIASEC Personality Cosine Similarity
  2. Academic Subject Prerequisites & Grade Strength
  3. Domain Interest & Skill Tag Alignment
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np

from app.ml.config.ml_config import GRADE_POINTS, RIASEC_DIMENSIONS
from app.config import settings

logger = logging.getLogger(__name__)


class ContentBasedRecommender:
    """Content-Based Filtering for Career Pathways."""

    def __init__(self, kb_path: Optional[Path] = None):
        self.kb_path = kb_path or settings.KNOWLEDGE_BASE_PATH
        self.pathways = self._load_knowledge_base()

    def _load_knowledge_base(self) -> List[Dict[str, Any]]:
        """Loads curated pathways from JSON knowledge base."""
        if not self.kb_path.exists():
            logger.warning(f"Knowledge base file not found at: {self.kb_path}")
            return []
        with open(self.kb_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _compute_riasec_similarity(self, student_riasec: Dict[str, float], pathway_riasec: Dict[str, float]) -> float:
        """Calculates cosine similarity between 6-dimensional RIASEC vectors."""
        vec_student = np.array([
            student_riasec.get("score_realistic", student_riasec.get("realistic", 3.0)),
            student_riasec.get("score_investigative", student_riasec.get("investigative", 3.0)),
            student_riasec.get("score_artistic", student_riasec.get("artistic", 3.0)),
            student_riasec.get("score_social", student_riasec.get("social", 3.0)),
            student_riasec.get("score_enterprising", student_riasec.get("enterprising", 3.0)),
            student_riasec.get("score_conventional", student_riasec.get("conventional", 3.0))
        ], dtype=float)

        vec_pathway = np.array([
            pathway_riasec.get("realistic", 3.0),
            pathway_riasec.get("investigative", 3.0),
            pathway_riasec.get("artistic", 3.0),
            pathway_riasec.get("social", 3.0),
            pathway_riasec.get("enterprising", 3.0),
            pathway_riasec.get("conventional", 3.0)
        ], dtype=float)

        norm_s = np.linalg.norm(vec_student)
        norm_p = np.linalg.norm(vec_pathway)

        if norm_s == 0 or norm_p == 0:
            return 0.5

        cosine_sim = np.dot(vec_student, vec_pathway) / (norm_s * norm_p)
        # Cosine similarity for non-negative vectors ranges [0, 1]
        return float(np.clip(cosine_sim, 0.0, 1.0))

    def _compute_academic_prerequisites_fit(self, student_acad: Dict[str, Any], pathway: Dict[str, Any]) -> float:
        """Evaluates how well student's O/L grades meet pathway prerequisite demands."""
        stream = pathway["stream"]
        math_pt = GRADE_POINTS.get(str(student_acad.get("math_grade", "C")).upper(), 2.0)
        sci_pt = GRADE_POINTS.get(str(student_acad.get("science_grade", "C")).upper(), 2.0)
        eng_pt = GRADE_POINTS.get(str(student_acad.get("english_grade", "C")).upper(), 2.0)
        lang_pt = GRADE_POINTS.get(str(student_acad.get("first_lang_grade", "C")).upper(), 2.0)
        hist_pt = GRADE_POINTS.get(str(student_acad.get("history_grade", "C")).upper(), 2.0)

        b1_sub = str(student_acad.get("basket_1_subject", "")).lower()
        b1_pt = GRADE_POINTS.get(str(student_acad.get("basket_1_grade", "C")).upper(), 2.0)

        if stream == "Physical Science":
            base_fit = (math_pt * 0.55 + sci_pt * 0.35 + eng_pt * 0.10) / 4.0
            if "ict" in b1_sub:
                base_fit = min(1.0, base_fit + (b1_pt / 4.0) * 0.10)
        elif stream == "Biological Science":
            base_fit = (sci_pt * 0.55 + math_pt * 0.20 + eng_pt * 0.25) / 4.0
        elif stream == "Commerce":
            comm_bonus = 0.10 if ("commerce" in b1_sub or "entrepreneurship" in b1_sub) else 0.0
            base_fit = (math_pt * 0.35 + eng_pt * 0.35 + lang_pt * 0.30) / 4.0 + comm_bonus
        elif stream == "Arts":
            base_fit = (lang_pt * 0.40 + hist_pt * 0.35 + eng_pt * 0.25) / 4.0
        else:  # Technology
            tech_bonus = 0.10 if ("ict" in b1_sub or "design" in str(student_acad.get("basket_3_subject", "")).lower()) else 0.0
            base_fit = (sci_pt * 0.40 + math_pt * 0.30 + eng_pt * 0.30) / 4.0 + tech_bonus

        return float(np.clip(base_fit, 0.0, 1.0))

    def _compute_interest_overlap(self, student_career: Dict[str, Any], pathway: Dict[str, Any]) -> float:
        """Computes keyword semantic overlap between student aspirations and pathway metadata."""
        student_domain = str(student_career.get("preferred_career_domain", "")).lower()
        student_style = str(student_career.get("preferred_work_style", "")).lower()

        pathway_text = (
            pathway["career_domain"] + " " +
            pathway["degree_area"] + " " +
            pathway["degree_program"] + " " +
            " ".join(pathway.get("interest_tags", [])) + " " +
            " ".join(pathway.get("skill_tags", [])) + " " +
            pathway.get("description", "")
        ).lower()

        # Token overlap
        student_tokens = set(student_domain.replace("&", " ").replace("/", " ").split())
        if not student_tokens:
            return 0.5

        matched_tokens = sum(1 for t in student_tokens if len(t) > 2 and t in pathway_text)
        token_overlap = matched_tokens / max(1, len(student_tokens))

        # Check direct domain match
        direct_bonus = 0.30 if (student_domain in pathway["career_domain"].lower() or pathway["degree_area"].lower() in student_domain) else 0.0

        return float(np.clip(token_overlap * 0.70 + direct_bonus, 0.0, 1.0))

    def score_all_pathways(self, student_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Scores all pathways in the knowledge base against the student profile.
        Returns a list of scored pathway dictionaries with detailed component breakdowns.
        """
        scored_list = []

        student_riasec = {
            "score_realistic": student_profile.get("score_realistic", 3.0),
            "score_investigative": student_profile.get("score_investigative", 3.0),
            "score_artistic": student_profile.get("score_artistic", 3.0),
            "score_social": student_profile.get("score_social", 3.0),
            "score_enterprising": student_profile.get("score_enterprising", 3.0),
            "score_conventional": student_profile.get("score_conventional", 3.0)
        }

        for p in self.pathways:
            riasec_score = self._compute_riasec_similarity(student_riasec, p["riasec_profile"])
            acad_score = self._compute_academic_prerequisites_fit(student_profile, p)
            interest_score = self._compute_interest_overlap(student_profile, p)

            # Weighted Content Score: 50% RIASEC, 30% Academic fit, 20% Interest match
            content_sim = round(0.50 * riasec_score + 0.30 * acad_score + 0.20 * interest_score, 4)

            scored_list.append({
                "pathway_id": p["pathway_id"],
                "stream": p["stream"],
                "degree_area": p["degree_area"],
                "degree_program": p["degree_program"],
                "career_domain": p["career_domain"],
                "content_similarity_score": content_sim,
                "riasec_match": round(riasec_score, 4),
                "academic_match": round(acad_score, 4),
                "interest_match": round(interest_score, 4),
                "required_subjects": p.get("required_subjects", []),
                "preferred_subjects": p.get("preferred_subjects", []),
                "sample_job_titles": p.get("sample_job_titles", []),
                "description": p.get("description", "")
            })

        return scored_list
