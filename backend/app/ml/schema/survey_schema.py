"""Comprehensive GCE O/L & A/L Survey Schema Specification."""

from typing import Dict, Any, List
import pandas as pd

# Grade mapping
GRADE_MAP = {
    "A": 4.0,
    "B": 3.0,
    "C": 2.0,
    "S": 1.0,
    "W": 0.0
}

# Holland RIASEC Question Items (used for mapping individual 5-point survey questions into 6 dimensions)
RIASEC_QUESTIONS = {
    "realistic": [
        "I enjoy building, fixing, assembling mechanical/electronic equipment",
        "I prefer hands-on practical physical work over desk tasks",
        "I like working with tools, machines, hardware or outdoor environments"
    ],
    "investigative": [
        "I like solving complex math, scientific, or algorithmic problems",
        "I enjoy researching, analyzing scientific theories, and discovering how things work",
        "I prefer independent study and analytical thinking over routine execution"
    ],
    "artistic": [
        "I enjoy creative writing, visual design, sketching, or digital art",
        "I like music, drama, performing arts, or self-expression",
        "I value unconventional ideas, aesthetics, and creative freedom"
    ],
    "social": [
        "I find deep fulfillment in teaching, helping, caring for, or counselling others",
        "I work best in teams and enjoy community engagement",
        "I am empathetic and communicate well with different groups of people"
    ],
    "enterprising": [
        "I enjoy leading teams, public speaking, and organizing events",
        "I am interested in business ventures, trading, marketing, and sales",
        "I enjoy negotiating, convincing others, and taking strategic risks"
    ],
    "conventional": [
        "I like working with numbers, spreadsheets, accounting records, and tables",
        "I prefer structured environments, clear rules, and systematic record-keeping",
        "I pay close attention to detail, accuracy, and operational order"
    ]
}

# Complete Schema Specification for Survey & ML
SURVEY_SCHEMA_SPEC: Dict[str, Dict[str, Any]] = {
    # 1. Identification & Meta
    "record_id": {"type": "string", "required": True, "description": "Anonymized unique student ID (e.g. STU-00001)"},
    "data_source": {"type": "string", "required": True, "allowed": ["synthetic", "real"], "description": "Data origin"},
    
    # 2. Demographic Context
    "gender": {"type": "string", "required": False, "allowed": ["Male", "Female", "Other", "Prefer not to say"]},
    "district": {"type": "string", "required": False, "description": "Sri Lankan Administrative District (e.g., Colombo, Kandy, Galle, Jaffna)"},
    "school_type": {"type": "string", "required": False, "allowed": ["1AB National School", "1AB Provincial School", "1C School", "Type 2 School", "Private/Semi-Government"]},
    "medium": {"type": "string", "required": False, "allowed": ["Sinhala", "Tamil", "English"]},

    # 3. GCE O/L Academic Grades (A, B, C, S, W)
    "math_grade": {"type": "categorical", "required": True, "allowed": ["A", "B", "C", "S", "W"]},
    "science_grade": {"type": "categorical", "required": True, "allowed": ["A", "B", "C", "S", "W"]},
    "english_grade": {"type": "categorical", "required": True, "allowed": ["A", "B", "C", "S", "W"]},
    "first_lang_grade": {"type": "categorical", "required": True, "allowed": ["A", "B", "C", "S", "W"]},
    "history_grade": {"type": "categorical", "required": True, "allowed": ["A", "B", "C", "S", "W"]},
    "religion_grade": {"type": "categorical", "required": True, "allowed": ["A", "B", "C", "S", "W"]},
    "basket_1_subject": {"type": "string", "required": False, "allowed": ["ICT", "Commerce", "Geography", "Civics", "Second Language", "Entrepreneurship Studies"]},
    "basket_1_grade": {"type": "categorical", "required": False, "allowed": ["A", "B", "C", "S", "W"]},
    "basket_2_subject": {"type": "string", "required": False, "allowed": ["Art", "Music", "Drama", "Dancing", "English Literature", "Sinhala/Tamil Literature"]},
    "basket_2_grade": {"type": "categorical", "required": False, "allowed": ["A", "B", "C", "S", "W"]},
    "basket_3_subject": {"type": "string", "required": False, "allowed": ["Design_Tech", "Agriculture", "Home_Economics", "Health_Science", "Aquatic_Resources"]},
    "basket_3_grade": {"type": "categorical", "required": False, "allowed": ["A", "B", "C", "S", "W"]},

    # 4. Extracurricular Features (0 or 1 / bool)
    "has_sports": {"type": "boolean", "required": True},
    "has_clubs_societies": {"type": "boolean", "required": True},
    "has_coding_robotics": {"type": "boolean", "required": True},
    "has_debating_media": {"type": "boolean", "required": True},
    "has_music_performing_arts": {"type": "boolean", "required": True},
    "has_visual_arts": {"type": "boolean", "required": True},
    "has_volunteering_scouts": {"type": "boolean", "required": True},
    "has_leadership_prefect": {"type": "boolean", "required": True},
    "has_reading_writing": {"type": "boolean", "required": True},
    "has_entrepreneurship": {"type": "boolean", "required": True},

    # 5. Holland RIASEC Profile Scores (1.0 to 5.0 scale)
    "score_realistic": {"type": "numeric", "required": True, "min": 1.0, "max": 5.0},
    "score_investigative": {"type": "numeric", "required": True, "min": 1.0, "max": 5.0},
    "score_artistic": {"type": "numeric", "required": True, "min": 1.0, "max": 5.0},
    "score_social": {"type": "numeric", "required": True, "min": 1.0, "max": 5.0},
    "score_enterprising": {"type": "numeric", "required": True, "min": 1.0, "max": 5.0},
    "score_conventional": {"type": "numeric", "required": True, "min": 1.0, "max": 5.0},

    # 6. Career Interests & Influences
    "preferred_career_domain": {"type": "string", "required": False},
    "preferred_work_style": {"type": "string", "required": False},
    "higher_education_interest": {"type": "string", "required": False},
    "parental_influence_level": {"type": "numeric", "required": True, "min": 1, "max": 5},
    "teacher_guidance_level": {"type": "numeric", "required": True, "min": 1, "max": 5},

    # 7. Target Variable (Selected / Recommended A/L Stream)
    "al_stream": {"type": "categorical", "required": True, "allowed": [
        "Physical Science",
        "Biological Science",
        "Commerce",
        "Arts",
        "Technology"
    ]}
}


def map_raw_survey_to_schema(raw_df: pd.DataFrame, column_mapping: Dict[str, str] = None) -> pd.DataFrame:
    """
    Transforms raw Google Forms or survey CSV columns to the standardized internal schema.
    Used for Phase 10 (Real Survey Integration) and validation.
    """
    df = raw_df.copy()
    if column_mapping:
        df = df.rename(columns=column_mapping)

    # Standardize string columns
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    return df
