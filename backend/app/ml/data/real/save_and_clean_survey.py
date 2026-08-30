"""
Complete pipeline to store, clean, standardize, augment, and retrain ML models 
using real survey data collected via Google Forms.
"""

import os
import re
import json
import logging
from pathlib import Path
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

RAW_CSV_PATH = Path(r"d:\research_2\backend\app\ml\data\real\raw_google_forms_responses.csv")
REAL_CLEANED_PATH = Path(r"d:\research_2\backend\app\ml\data\real\real_survey_students.csv")
SYNTHETIC_DATA_PATH = Path(r"d:\research_2\backend\app\ml\data\synthetic\synthetic_students.csv")
COMBINED_DATA_PATH = Path(r"d:\research_2\backend\app\ml\data\real\combined_real_synthetic_1000.csv")

def clean_letter_grade(val, default="C"):
    if pd.isna(val) or str(val).strip() == "":
        return default
    v = str(val).strip().upper()
    match = re.search(r'[ABCSW]', v)
    return match.group(0) if match else default

def clean_likert(val, default=3.0):
    if pd.isna(val) or str(val).strip() == "":
        return default
    try:
        score = float(str(val).strip())
        return float(np.clip(score, 1.0, 5.0))
    except:
        return default

def clean_school_type(st):
    if pd.isna(st):
        return "1AB Provincial School"
    s = str(st).lower()
    if "national" in s:
        return "1AB National School"
    elif "provincial" in s:
        return "1AB Provincial School"
    elif "semi" in s or "private" in s:
        return "Private/Semi-Government"
    return "1AB Provincial School"

def clean_stream(stream):
    if pd.isna(stream) or str(stream).strip() == "":
        return None
    s = str(stream).strip().lower()
    if "physical" in s or "math" in s:
        return "Physical Science"
    elif "bio" in s:
        return "Biological Science"
    elif "com" in s:
        return "Commerce"
    elif "art" in s:
        return "Arts"
    elif "tech" in s:
        return "Technology"
    return None

def process_raw_survey_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Transforms raw Google Forms survey dataframe into standardized project schema."""
    cleaned_rows = []
    
    # Check column names
    cols = list(df_raw.columns)
    logger.info(f"Loaded raw dataset with {len(df_raw)} rows and {len(cols)} columns.")
    
    for idx, row in df_raw.iterrows():
        # Stream (Target) - Step 8: drop rows with missing target variable
        target_stream = clean_stream(row.iloc[23] if len(row) > 23 else None)
        if not target_stream:
            continue
            
        gender = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "Other"
        province = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else "Western"
        school_type = clean_school_type(row.iloc[3])
        
        # O/L grades
        math_grade = clean_letter_grade(row.iloc[4])
        sci_grade = clean_letter_grade(row.iloc[5])
        eng_grade = clean_letter_grade(row.iloc[6])
        lang_grade = clean_letter_grade(row.iloc[7])
        hist_grade = clean_letter_grade(row.iloc[8])
        rel_grade = clean_letter_grade(row.iloc[9])
        
        # Basket subjects
        basket_1_grade = clean_letter_grade(row.iloc[10]) # Commerce/Geography
        basket_2_grade = clean_letter_grade(row.iloc[11]) # ICT/Health Science
        basket_3_grade = clean_letter_grade(row.iloc[12]) # Art/Music/Drama
        
        basket_1_subject = "Commerce" if basket_1_grade in ["A", "B"] else "Geography"
        basket_2_subject = "Drama" if basket_3_grade in ["A", "B"] else "Art"
        basket_3_subject = "Design_Tech" if basket_2_grade in ["A", "B"] else "Health_Science"
        
        # RIASEC scores (Q6 - Q11)
        score_i = clean_likert(row.iloc[14]) # Q6: Math / puzzles -> Investigative
        score_r = clean_likert(row.iloc[15]) # Q7: Tools / machines -> Realistic
        score_a = clean_likert(row.iloc[16]) # Q8: Creative / drawing / music -> Artistic
        score_s = clean_likert(row.iloc[17]) # Q9: Helping / teaching -> Social
        score_e = clean_likert(row.iloc[18]) # Q10: Leading / managing -> Enterprising
        score_c = clean_likert(row.iloc[19]) # Q11: Rules / data -> Conventional
        
        # Extracurricular activities (Q12)
        extra_str = str(row.iloc[20]).lower() if pd.notna(row.iloc[20]) else ""
        has_sports = 1 if "sport" in extra_str else 0
        has_clubs = 1 if "club" in extra_str or "science" in extra_str or "maths" in extra_str else 0
        has_coding = 1 if "coding" in extra_str or "robotics" in extra_str or "ict" in extra_str else 0
        has_debating = 1 if "debate" in extra_str or "media" in extra_str else 0
        has_music = 1 if "drama" in extra_str or "music" in extra_str or "singing" in extra_str else 0
        has_arts = 1 if "art" in extra_str else 0
        has_volunteering = 1 if "religious" in extra_str or "scout" in extra_str or "volunt" in extra_str else 0
        has_leadership = 1 if "prefect" in extra_str or "leadership" in extra_str else 0
        has_reading = 1 if "read" in extra_str or "writ" in extra_str else 0
        has_entrepreneurship = 1 if "entrepreneur" in extra_str or "business" in extra_str else 0
        
        # Influences (Q13)
        influencer = str(row.iloc[21]).lower() if pd.notna(row.iloc[21]) else "own interest"
        parent_inf = 5 if "parent" in influencer else (3 if "friend" in influencer else 2)
        teacher_inf = 5 if "teacher" in influencer else 2
        
        # Career aspirations (Q16)
        career_goal = str(row.iloc[24]).strip() if pd.notna(row.iloc[24]) else "Engineering & Technology"
        
        cleaned_rows.append({
            "record_id": f"STU-REAL-{len(cleaned_rows)+1:04d}",
            "data_source": "real",
            "gender": gender,
            "district": province,
            "school_type": school_type,
            "medium": "Sinhala",
            "math_grade": math_grade,
            "science_grade": sci_grade,
            "english_grade": eng_grade,
            "first_lang_grade": lang_grade,
            "history_grade": hist_grade,
            "religion_grade": rel_grade,
            "basket_1_subject": basket_1_subject,
            "basket_1_grade": basket_1_grade,
            "basket_2_subject": basket_2_subject,
            "basket_2_grade": basket_3_grade,
            "basket_3_subject": basket_3_subject,
            "basket_3_grade": basket_2_grade,
            "has_sports": has_sports,
            "has_clubs_societies": has_clubs,
            "has_coding_robotics": has_coding,
            "has_debating_media": has_debating,
            "has_music_performing_arts": has_music,
            "has_visual_arts": has_arts,
            "has_volunteering_scouts": has_volunteering,
            "has_leadership_prefect": has_leadership,
            "has_reading_writing": has_reading,
            "has_entrepreneurship": has_entrepreneurship,
            "score_realistic": score_r,
            "score_investigative": score_i,
            "score_artistic": score_a,
            "score_social": score_s,
            "score_enterprising": score_e,
            "score_conventional": score_c,
            "preferred_career_domain": career_goal,
            "preferred_work_style": "Hands-on Practical & Fieldwork",
            "higher_education_interest": "State University Degree (UGC Merit/District)",
            "parental_influence_level": parent_inf,
            "teacher_guidance_level": teacher_inf,
            "al_stream": target_stream
        })
        
    df_cleaned = pd.DataFrame(cleaned_rows)
    logger.info(f"Successfully extracted {len(df_cleaned)} valid student profiles with complete target stream labels.")
    return df_cleaned
