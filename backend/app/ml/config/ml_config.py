"""ML Pipeline configuration, random seeds, and class constants."""

from pathlib import Path
from app.config import settings

# Supported A/L Streams (5 Target Classes)
STREAM_CLASSES = [
    "Physical Science",
    "Biological Science",
    "Commerce",
    "Arts",
    "Technology"
]

STREAM_TO_IDX = {stream: idx for idx, stream in enumerate(STREAM_CLASSES)}
IDX_TO_STREAM = {idx: stream for idx, stream in enumerate(STREAM_CLASSES)}

# RIASEC Dimension Names
RIASEC_DIMENSIONS = [
    "score_realistic",
    "score_investigative",
    "score_artistic",
    "score_social",
    "score_enterprising",
    "score_conventional"
]

# GCE O/L Grade Point mapping
GRADE_POINTS = {
    "A": 4.0,
    "B": 3.0,
    "C": 2.0,
    "S": 1.0,
    "W": 0.0
}

# Core ML Feature Columns
ACADEMIC_FEATURE_COLS = [
    "math_grade",
    "science_grade",
    "english_grade",
    "first_lang_grade",
    "history_grade",
    "religion_grade",
    "basket_1_grade",
    "basket_2_grade",
    "basket_3_grade",
]

EXTRACURRICULAR_FEATURE_COLS = [
    "has_sports",
    "has_clubs_societies",
    "has_coding_robotics",
    "has_debating_media",
    "has_music_performing_arts",
    "has_visual_arts",
    "has_volunteering_scouts",
    "has_leadership_prefect",
    "has_reading_writing",
    "has_entrepreneurship",
]

CAREER_PREF_COLS = [
    "parental_influence_level",
    "teacher_guidance_level"
]

ALL_NUMERIC_OR_ENCODED_COLS = (
    [f"{col}_pts" for col in ACADEMIC_FEATURE_COLS]
    + EXTRACURRICULAR_FEATURE_COLS
    + RIASEC_DIMENSIONS
    + CAREER_PREF_COLS
)

TARGET_COLUMN = "al_stream"

# Default Recommendation Fusion Weights
DEFAULT_WEIGHTS = {
    "w1_ml_stream": 0.45,
    "w2_content_similarity": 0.35,
    "w3_collaborative": 0.20,
}
