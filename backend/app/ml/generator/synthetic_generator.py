"""
Probabilistic Synthetic Dataset Generator for Sri Lankan GCE A/L Career Pathway System.

Generates realistic student profiles containing O/L academic performance,
extracurricular participation, Holland RIASEC personality scores, career aspirations,
and parental/teacher influence factors with domain-grounded distributions.
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

from app.ml.config.ml_config import STREAM_CLASSES
from app.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Sri Lankan Context Constants
DISTRICTS = [
    "Colombo", "Gampaha", "Kalutara", "Kandy", "Matale", "Nuwara Eliya",
    "Galle", "Matara", "Hambantota", "Jaffna", "Kilinochchi", "Mannar",
    "Vavuniya", "Mullaitivu", "Batticaloa", "Ampara", "Trincomalee",
    "Kurunegala", "Puttalam", "Anuradhapura", "Polonnaruwa", "Badulla",
    "Monaragala", "Ratnapura", "Kegalle"
]

DISTRICT_WEIGHTS = [
    0.14, 0.12, 0.06, 0.08, 0.03, 0.03,
    0.06, 0.05, 0.03, 0.04, 0.01, 0.01,
    0.01, 0.01, 0.03, 0.03, 0.02,
    0.07, 0.03, 0.04, 0.02, 0.03,
    0.02, 0.05, 0.04
]
# Normalize district weights
DISTRICT_WEIGHTS = [w / sum(DISTRICT_WEIGHTS) for w in DISTRICT_WEIGHTS]

SCHOOL_TYPES = [
    "1AB National School",
    "1AB Provincial School",
    "1C School",
    "Type 2 School",
    "Private/Semi-Government"
]
SCHOOL_WEIGHTS = [0.30, 0.35, 0.20, 0.08, 0.07]

GENDERS = ["Male", "Female"]
MEDIUMS = ["Sinhala", "Tamil", "English"]
MEDIUM_WEIGHTS = [0.72, 0.22, 0.06]

BASKET_1_CHOICES = ["ICT", "Commerce", "Geography", "Civics", "Second Language", "Entrepreneurship Studies"]
BASKET_2_CHOICES = ["Art", "Music", "Drama", "Dancing", "English Literature", "Sinhala Literature"]
BASKET_3_CHOICES = ["Design_Tech", "Agriculture", "Home_Economics", "Health_Science", "Aquatic_Resources"]

CAREER_DOMAINS_BY_STREAM = {
    "Physical Science": [
        "Software Engineering & AI", "Civil & Structural Engineering",
        "Data Science & Analytics", "Electronics & Embedded Systems",
        "Mechanical & Aerospace Engineering", "Quantitative Finance & Actuarial"
    ],
    "Biological Science": [
        "Medicine & Clinical Surgery", "Biomedical & Molecular Genetics",
        "Pharmaceutical & Drug Development", "Veterinary Medicine",
        "Sustainable Agriculture & Forestry", "Public Health & Nutrition"
    ],
    "Commerce": [
        "Accounting, Audit & Taxation", "Banking & Investment Management",
        "Digital Marketing & Brand Strategy", "International Trade & Logistics",
        "Business Management & Entrepreneurship", "Corporate Law & Compliance"
    ],
    "Arts": [
        "Law, Judiciary & Advocacy", "Journalism & Digital Mass Media",
        "UI/UX Design & Creative Direction", "International Relations & Diplomacy",
        "Language Translation & Linguistics", "Psychology & Social Work"
    ],
    "Technology": [
        "Robotics, Mechatronics & Automation", "Cloud Infrastructure & Cybersecurity",
        "Biosystems & Industrial Food Tech", "Applied Automotive & Mechanical Tech",
        "Renewable Energy & Power Systems", "Construction & Quantity Surveying Tech"
    ]
}

WORK_STYLES = [
    "Team-based & Project-driven",
    "Independent Analytical & Research",
    "Hands-on Practical & Fieldwork",
    "Client-facing & Communicative",
    "Structured, Routine & Detail-focused"
]

HIGHER_ED_GOALS = [
    "State University Degree (UGC Merit/District)",
    "State University Technology/Applied Degree",
    "Private/Foreign Affiliated University Degree",
    "Professional Qualification (CA/CIMA/SLIIT/IESL/Attorney)",
    "National Diploma / Vocational Higher Education (NVQ 5/6)"
]


class SyntheticDatasetGenerator:
    """Generates synthetic student data adhering to Sri Lankan educational domain logic."""

    def __init__(self, random_seed: int = 42):
        self.random_seed = random_seed
        self.rng = np.random.default_rng(random_seed)

    def _sample_grade(self, probabilities: List[float]) -> str:
        """Sample a grade (A, B, C, S, W) according to assigned probabilities."""
        return self.rng.choice(["A", "B", "C", "S", "W"], p=probabilities)

    def _sample_riasec_score(self, mean: float, std: float = 0.55) -> float:
        """Sample a RIASEC score on a 1.0 to 5.0 scale with bounding and rounding."""
        val = self.rng.normal(loc=mean, scale=std)
        return float(np.clip(np.round(val, 2), 1.0, 5.0))

    def generate_record(self, record_idx: int) -> Dict[str, Any]:
        """Generate a single plausible student survey record."""
        # 1. Base demographic context
        district = self.rng.choice(DISTRICTS, p=DISTRICT_WEIGHTS)
        school_type = self.rng.choice(SCHOOL_TYPES, p=SCHOOL_WEIGHTS)
        gender = self.rng.choice(GENDERS, p=[0.48, 0.52])
        medium = self.rng.choice(MEDIUMS, p=MEDIUM_WEIGHTS)

        # 2. Select latent/target stream with balanced distribution and domain realism
        # Stream distribution: roughly 22% Physical, 20% Bio, 24% Commerce, 18% Arts, 16% Tech
        stream_probs = [0.22, 0.20, 0.24, 0.18, 0.16]
        target_stream = self.rng.choice(STREAM_CLASSES, p=stream_probs)

        # Noise factor (12% of records exhibit cross-domain or unconventional profile combinations)
        is_atypical = self.rng.random() < 0.12

        # 3. Generate O/L Academic Profile conditioned on the stream
        if target_stream == "Physical Science":
            math_p = [0.65, 0.25, 0.08, 0.02, 0.00] if not is_atypical else [0.35, 0.35, 0.20, 0.08, 0.02]
            sci_p  = [0.60, 0.28, 0.10, 0.02, 0.00] if not is_atypical else [0.30, 0.40, 0.20, 0.08, 0.02]
            eng_p  = [0.45, 0.30, 0.15, 0.08, 0.02]
            fl_p   = [0.40, 0.35, 0.18, 0.06, 0.01]
            hist_p = [0.35, 0.35, 0.20, 0.08, 0.02]
            rel_p  = [0.55, 0.30, 0.12, 0.03, 0.00]
            b1_sub = self.rng.choice(["ICT", "Commerce", "Geography"], p=[0.60, 0.25, 0.15])
            b2_sub = self.rng.choice(["English Literature", "Art", "Music"], p=[0.40, 0.35, 0.25])
            b3_sub = self.rng.choice(["Design_Tech", "Health_Science", "Agriculture"], p=[0.50, 0.30, 0.20])

            r_mean, i_mean, a_mean, s_mean, e_mean, c_mean = (4.1, 4.6, 2.2, 2.5, 3.2, 3.7)

            ec_coding = bool(self.rng.random() < 0.65)
            ec_sports = bool(self.rng.random() < 0.50)
            ec_clubs  = bool(self.rng.random() < 0.70)
            ec_debate = bool(self.rng.random() < 0.35)
            ec_music  = bool(self.rng.random() < 0.25)
            ec_visual = bool(self.rng.random() < 0.20)
            ec_volunt = bool(self.rng.random() < 0.40)
            ec_leader = bool(self.rng.random() < 0.45)
            ec_read   = bool(self.rng.random() < 0.55)
            ec_entrep = bool(self.rng.random() < 0.30)

        elif target_stream == "Biological Science":
            math_p = [0.40, 0.35, 0.18, 0.06, 0.01]
            sci_p  = [0.70, 0.22, 0.07, 0.01, 0.00] if not is_atypical else [0.35, 0.35, 0.20, 0.08, 0.02]
            eng_p  = [0.55, 0.30, 0.12, 0.03, 0.00]
            fl_p   = [0.45, 0.35, 0.15, 0.04, 0.01]
            hist_p = [0.38, 0.35, 0.20, 0.06, 0.01]
            rel_p  = [0.60, 0.28, 0.10, 0.02, 0.00]
            b1_sub = self.rng.choice(["ICT", "Geography", "Civics"], p=[0.40, 0.35, 0.25])
            b2_sub = self.rng.choice(["Music", "Art", "English Literature"], p=[0.40, 0.35, 0.25])
            b3_sub = self.rng.choice(["Health_Science", "Agriculture", "Home_Economics"], p=[0.55, 0.35, 0.10])

            r_mean, i_mean, a_mean, s_mean, e_mean, c_mean = (3.4, 4.7, 2.1, 4.4, 2.8, 3.6)

            ec_coding = bool(self.rng.random() < 0.20)
            ec_sports = bool(self.rng.random() < 0.45)
            ec_clubs  = bool(self.rng.random() < 0.65)
            ec_debate = bool(self.rng.random() < 0.30)
            ec_music  = bool(self.rng.random() < 0.35)
            ec_visual = bool(self.rng.random() < 0.25)
            ec_volunt = bool(self.rng.random() < 0.70)
            ec_leader = bool(self.rng.random() < 0.45)
            ec_read   = bool(self.rng.random() < 0.60)
            ec_entrep = bool(self.rng.random() < 0.20)

        elif target_stream == "Commerce":
            math_p = [0.35, 0.40, 0.18, 0.06, 0.01]
            sci_p  = [0.25, 0.35, 0.28, 0.10, 0.02]
            eng_p  = [0.45, 0.35, 0.15, 0.04, 0.01]
            fl_p   = [0.40, 0.38, 0.18, 0.04, 0.00]
            hist_p = [0.30, 0.35, 0.25, 0.08, 0.02]
            rel_p  = [0.50, 0.35, 0.12, 0.03, 0.00]
            b1_sub = self.rng.choice(["Commerce", "Entrepreneurship Studies", "ICT"], p=[0.65, 0.20, 0.15])
            b2_sub = self.rng.choice(["Music", "Art", "Drama"], p=[0.40, 0.35, 0.25])
            b3_sub = self.rng.choice(["Design_Tech", "Home_Economics", "Health_Science"], p=[0.40, 0.35, 0.25])

            r_mean, i_mean, a_mean, s_mean, e_mean, c_mean = (2.2, 3.4, 2.5, 3.5, 4.6, 4.7)

            ec_coding = bool(self.rng.random() < 0.20)
            ec_sports = bool(self.rng.random() < 0.55)
            ec_clubs  = bool(self.rng.random() < 0.60)
            ec_debate = bool(self.rng.random() < 0.45)
            ec_music  = bool(self.rng.random() < 0.30)
            ec_visual = bool(self.rng.random() < 0.20)
            ec_volunt = bool(self.rng.random() < 0.45)
            ec_leader = bool(self.rng.random() < 0.55)
            ec_read   = bool(self.rng.random() < 0.40)
            ec_entrep = bool(self.rng.random() < 0.70)

        elif target_stream == "Arts":
            math_p = [0.15, 0.25, 0.35, 0.20, 0.05]
            sci_p  = [0.12, 0.25, 0.38, 0.20, 0.05]
            eng_p  = [0.55, 0.30, 0.12, 0.03, 0.00]
            fl_p   = [0.65, 0.25, 0.08, 0.02, 0.00]
            hist_p = [0.60, 0.28, 0.10, 0.02, 0.00]
            rel_p  = [0.60, 0.30, 0.08, 0.02, 0.00]
            b1_sub = self.rng.choice(["Geography", "Civics", "Second Language"], p=[0.45, 0.35, 0.20])
            b2_sub = self.rng.choice(["Art", "Music", "Drama", "Dancing", "English Literature"], p=[0.25, 0.25, 0.20, 0.15, 0.15])
            b3_sub = self.rng.choice(["Home_Economics", "Health_Science", "Agriculture"], p=[0.45, 0.35, 0.20])

            r_mean, i_mean, a_mean, s_mean, e_mean, c_mean = (2.1, 3.6, 4.8, 4.3, 3.6, 2.5)

            ec_coding = bool(self.rng.random() < 0.10)
            ec_sports = bool(self.rng.random() < 0.35)
            ec_clubs  = bool(self.rng.random() < 0.50)
            ec_debate = bool(self.rng.random() < 0.65)
            ec_music  = bool(self.rng.random() < 0.65)
            ec_visual = bool(self.rng.random() < 0.65)
            ec_volunt = bool(self.rng.random() < 0.55)
            ec_leader = bool(self.rng.random() < 0.40)
            ec_read   = bool(self.rng.random() < 0.75)
            ec_entrep = bool(self.rng.random() < 0.25)

        else:  # Technology
            math_p = [0.30, 0.38, 0.22, 0.08, 0.02]
            sci_p  = [0.35, 0.40, 0.18, 0.06, 0.01]
            eng_p  = [0.30, 0.35, 0.25, 0.08, 0.02]
            fl_p   = [0.35, 0.40, 0.20, 0.05, 0.00]
            hist_p = [0.25, 0.35, 0.28, 0.10, 0.02]
            rel_p  = [0.50, 0.35, 0.12, 0.03, 0.00]
            b1_sub = self.rng.choice(["ICT", "Geography", "Entrepreneurship Studies"], p=[0.70, 0.15, 0.15])
            b2_sub = self.rng.choice(["Art", "Music", "Drama"], p=[0.45, 0.35, 0.20])
            b3_sub = self.rng.choice(["Design_Tech", "Agriculture", "Aquatic_Resources"], p=[0.60, 0.30, 0.10])

            r_mean, i_mean, a_mean, s_mean, e_mean, c_mean = (4.7, 4.1, 2.4, 2.6, 3.4, 3.8)

            ec_coding = bool(self.rng.random() < 0.55)
            ec_sports = bool(self.rng.random() < 0.50)
            ec_clubs  = bool(self.rng.random() < 0.55)
            ec_debate = bool(self.rng.random() < 0.25)
            ec_music  = bool(self.rng.random() < 0.25)
            ec_visual = bool(self.rng.random() < 0.30)
            ec_volunt = bool(self.rng.random() < 0.35)
            ec_leader = bool(self.rng.random() < 0.35)
            ec_read   = bool(self.rng.random() < 0.35)
            ec_entrep = bool(self.rng.random() < 0.40)

        # Draw actual grades
        math_g  = self._sample_grade(math_p)
        sci_g   = self._sample_grade(sci_p)
        eng_g   = self._sample_grade(eng_p)
        fl_g    = self._sample_grade(fl_p)
        hist_g  = self._sample_grade(hist_p)
        rel_g   = self._sample_grade(rel_p)
        b1_g    = self._sample_grade([0.45, 0.30, 0.18, 0.06, 0.01])
        b2_g    = self._sample_grade([0.40, 0.35, 0.18, 0.06, 0.01])
        b3_g    = self._sample_grade([0.45, 0.30, 0.18, 0.06, 0.01])

        # Draw RIASEC scores with individual variance
        realistic_score     = self._sample_riasec_score(r_mean)
        investigative_score = self._sample_riasec_score(i_mean)
        artistic_score      = self._sample_riasec_score(a_mean)
        social_score        = self._sample_riasec_score(s_mean)
        enterprising_score  = self._sample_riasec_score(e_mean)
        conventional_score  = self._sample_riasec_score(c_mean)

        # Career domain aspiration & preferences
        domain_pool = CAREER_DOMAINS_BY_STREAM[target_stream]
        pref_domain = self.rng.choice(domain_pool)
        pref_work   = self.rng.choice(WORK_STYLES)
        high_ed     = self.rng.choice(HIGHER_ED_GOALS)

        # Parental and teacher influence (1 to 5)
        parent_inf  = int(self.rng.choice([1, 2, 3, 4, 5], p=[0.05, 0.15, 0.35, 0.30, 0.15]))
        teacher_inf = int(self.rng.choice([1, 2, 3, 4, 5], p=[0.10, 0.20, 0.40, 0.20, 0.10]))

        record = {
            "record_id": f"STU-SYN-{record_idx:05d}",
            "data_source": "synthetic",
            "gender": gender,
            "district": district,
            "school_type": school_type,
            "medium": medium,
            "math_grade": math_g,
            "science_grade": sci_g,
            "english_grade": eng_g,
            "first_lang_grade": fl_g,
            "history_grade": hist_g,
            "religion_grade": rel_g,
            "basket_1_subject": b1_sub,
            "basket_1_grade": b1_g,
            "basket_2_subject": b2_sub,
            "basket_2_grade": b2_g,
            "basket_3_subject": b3_sub,
            "basket_3_grade": b3_g,
            "has_sports": int(ec_sports),
            "has_clubs_societies": int(ec_clubs),
            "has_coding_robotics": int(ec_coding),
            "has_debating_media": int(ec_debate),
            "has_music_performing_arts": int(ec_music),
            "has_visual_arts": int(ec_visual),
            "has_volunteering_scouts": int(ec_volunt),
            "has_leadership_prefect": int(ec_leader),
            "has_reading_writing": int(ec_read),
            "has_entrepreneurship": int(ec_entrep),
            "score_realistic": realistic_score,
            "score_investigative": investigative_score,
            "score_artistic": artistic_score,
            "score_social": social_score,
            "score_enterprising": enterprising_score,
            "score_conventional": conventional_score,
            "preferred_career_domain": pref_domain,
            "preferred_work_style": pref_work,
            "higher_education_interest": high_ed,
            "parental_influence_level": parent_inf,
            "teacher_guidance_level": teacher_inf,
            "al_stream": target_stream
        }
        return record

    def generate_dataset(self, num_records: int = 1200) -> pd.DataFrame:
        """Generate a DataFrame containing synthetic student records."""
        logger.info(f"Generating {num_records} synthetic student profiles with seed {self.random_seed}...")
        records = [self.generate_record(i + 1) for i in range(num_records)]
        df = pd.DataFrame(records)
        logger.info(f"Successfully generated {len(df)} records. Class distribution:\n{df['al_stream'].value_counts()}")
        return df


def generate_and_save_synthetic_data(
    count: int = 1200,
    seed: int = 42,
    csv_path: Optional[Path] = None,
    json_path: Optional[Path] = None
) -> pd.DataFrame:
    """Utility function to generate and persist synthetic dataset."""
    generator = SyntheticDatasetGenerator(random_seed=seed)
    df = generator.generate_dataset(num_records=count)

    out_csv = csv_path or settings.SYNTHETIC_DATA_PATH
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    logger.info(f"Saved synthetic dataset CSV to: {out_csv}")

    if json_path or (out_csv.parent / "synthetic_students.json"):
        out_json = json_path or (out_csv.parent / "synthetic_students.json")
        df.to_json(out_json, orient="records", indent=2)
        logger.info(f"Saved synthetic dataset JSON to: {out_json}")

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic Student Dataset Generator for A/L Stream & Pathway Recommendation")
    parser.add_argument("--count", type=int, default=1200, help="Number of records to generate (default: 1200)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility (default: 42)")
    parser.add_argument("--output", type=str, default=None, help="Output CSV path")
    parser.add_argument("--json-output", type=str, default=None, help="Output JSON path")
    args = parser.parse_args()

    csv_out = Path(args.output) if args.output else None
    json_out = Path(args.json_output) if args.json_output else None

    generate_and_save_synthetic_data(count=args.count, seed=args.seed, csv_path=csv_out, json_path=json_out)
