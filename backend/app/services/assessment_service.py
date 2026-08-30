"""
Assessment service for persisting student profiles, executing ML prediction,
generating hybrid pathway recommendations, and computing SHAP feature explanations.
"""

import uuid
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple
from sqlalchemy.orm import Session

from app.models.entities import (
    StudentProfile,
    AcademicProfile,
    ExtracurricularProfile,
    PersonalityProfile,
    CareerPreference,
    StreamPrediction,
    PathwayRecommendation,
)
from app.schemas.assessment import StudentAssessmentInput, AssessmentSubmissionResult
from app.ml.config.ml_config import GRADE_POINTS, STREAM_CLASSES, DEFAULT_WEIGHTS
from app.ml.recommendation.hybrid_engine import get_hybrid_recommender
from app.ml.explainability.shap_explainer import get_shap_explainer
from app.config import settings


class AssessmentService:
    """Core domain service for handling assessment intake, ML scoring, and SHAP explainability."""

    @staticmethod
    def _calculate_gpa_and_a_count(academic_data: dict) -> tuple[float, int]:
        grades = [
            academic_data.get("math_grade"),
            academic_data.get("science_grade"),
            academic_data.get("english_grade"),
            academic_data.get("first_lang_grade"),
            academic_data.get("history_grade"),
            academic_data.get("religion_grade"),
            academic_data.get("basket_1_grade"),
            academic_data.get("basket_2_grade"),
            academic_data.get("basket_3_grade"),
        ]
        valid_grades = [g for g in grades if g in GRADE_POINTS]
        if not valid_grades:
            return 0.0, 0
        points = [GRADE_POINTS[g] for g in valid_grades]
        a_count = sum(1 for g in valid_grades if g == "A")
        gpa = sum(points) / len(points)
        return round(gpa, 2), a_count

    @classmethod
    def _extract_flat_dict(cls, assessment: StudentAssessmentInput) -> Dict[str, Any]:
        """Flattens nested assessment schemas into a dictionary matching ML feature columns."""
        acad = assessment.academic.model_dump()
        extra = assessment.extracurricular.model_dump()
        pers = assessment.personality.model_dump()
        career = assessment.career.model_dump()

        flat = {
            "gender": assessment.gender,
            "district": assessment.district,
            "school_type": assessment.school_type,
            "medium": assessment.medium,
            **acad,
            **{k: int(v) for k, v in extra.items()},
            **pers,
            **career
        }
        return flat

    @classmethod
    def process_and_save_assessment(
        cls,
        assessment: StudentAssessmentInput,
        db: Session
    ) -> AssessmentSubmissionResult:
        """Processes intake assessment, computes stream probabilities and top-5 pathways, and saves to DB."""
        record_id = f"STU-{uuid.uuid4().hex[:8].upper()}"
        flat_dict = cls._extract_flat_dict(assessment)

        # 1. Create StudentProfile
        student = StudentProfile(
            record_id=record_id,
            data_source="real" if settings.is_real() else "synthetic",
            gender=assessment.gender,
            district=assessment.district,
            school_type=assessment.school_type,
            medium=assessment.medium,
        )
        db.add(student)
        db.flush()

        # 2. Academic Profile
        gpa, a_count = cls._calculate_gpa_and_a_count(assessment.academic.model_dump())
        acad_dict = assessment.academic.model_dump()
        acad_profile = AcademicProfile(
            student_id=student.id,
            math_grade=acad_dict["math_grade"],
            science_grade=acad_dict["science_grade"],
            english_grade=acad_dict["english_grade"],
            first_lang_grade=acad_dict["first_lang_grade"],
            history_grade=acad_dict["history_grade"],
            religion_grade=acad_dict["religion_grade"],
            basket_1_subject=acad_dict.get("basket_1_subject"),
            basket_1_grade=acad_dict.get("basket_1_grade"),
            basket_2_subject=acad_dict.get("basket_2_subject"),
            basket_2_grade=acad_dict.get("basket_2_grade"),
            basket_3_subject=acad_dict.get("basket_3_subject"),
            basket_3_grade=acad_dict.get("basket_3_grade"),
            gpa_approx=gpa,
            num_a_grades=a_count,
        )
        db.add(acad_profile)

        # 3. Extracurricular Profile
        extra_dict = assessment.extracurricular.model_dump()
        extra_count = sum(1 for v in extra_dict.values() if v is True)
        extra_profile = ExtracurricularProfile(
            student_id=student.id,
            total_activities_count=extra_count,
            **extra_dict
        )
        db.add(extra_profile)

        # 4. Personality Profile
        pers_dict = assessment.personality.model_dump()
        sorted_traits = sorted(
            [("R", pers_dict["score_realistic"]),
             ("I", pers_dict["score_investigative"]),
             ("A", pers_dict["score_artistic"]),
             ("S", pers_dict["score_social"]),
             ("E", pers_dict["score_enterprising"]),
             ("C", pers_dict["score_conventional"])],
            key=lambda x: x[1],
            reverse=True
        )
        dominant_code = "".join([t[0] for t in sorted_traits[:3]])

        pers_profile = PersonalityProfile(
            student_id=student.id,
            dominant_riasec=dominant_code,
            **pers_dict
        )
        db.add(pers_profile)

        # 5. Career Preferences
        career_dict = assessment.career.model_dump()
        career_profile = CareerPreference(
            student_id=student.id,
            **career_dict
        )
        db.add(career_profile)
        db.flush()

        # 6. Execute Hybrid Recommendation Engine
        recommender = get_hybrid_recommender()
        rec_result = recommender.recommend(flat_dict)

        predicted_stream = rec_result["predicted_stream"]
        stream_probs = rec_result["stream_probabilities"]
        ranked_recs = rec_result["top_5_pathways"]
        model_name = rec_result["model_name"]

        # 7. Execute SHAP Explainability Subsystem
        explainer = get_shap_explainer()
        shap_explanation = explainer.explain_instance(flat_dict, predicted_stream)

        # 8. Persist Stream Prediction with SHAP metadata
        prediction = StreamPrediction(
            student_id=student.id,
            model_name=model_name,
            model_version="v1.0.0",
            predicted_stream=predicted_stream,
            prob_physical_science=stream_probs.get("Physical Science", 0.0),
            prob_biological_science=stream_probs.get("Biological Science", 0.0),
            prob_commerce=stream_probs.get("Commerce", 0.0),
            prob_arts=stream_probs.get("Arts", 0.0),
            prob_technology=stream_probs.get("Technology", 0.0),
            probabilities_json=stream_probs,
            shap_explanation_json=shap_explanation
        )
        db.add(prediction)
        db.flush()

        # 9. Persist Top-5 Recommendations
        for rec in ranked_recs:
            pathway_rec = PathwayRecommendation(
                prediction_id=prediction.id,
                rank=rec["rank"],
                pathway_id=rec["pathway_id"],
                stream=rec["stream"],
                degree_area=rec["degree_area"],
                degree_program=rec["degree_program"],
                career_domain=rec["career_domain"],
                recommendation_score=rec["score"],
                ml_stream_score=rec["ml_stream_score"],
                content_similarity_score=rec["content_similarity_score"],
                collaborative_score=rec["collaborative_score"],
                explanation_text=rec["explanation"]
            )
            db.add(pathway_rec)

        db.commit()

        return AssessmentSubmissionResult(
            student_id=student.id,
            record_id=student.record_id,
            data_source=student.data_source,
            stream_probabilities=stream_probs,
            predicted_stream=predicted_stream,
            recommendations=ranked_recs,
            shap_explanation=shap_explanation
        )
