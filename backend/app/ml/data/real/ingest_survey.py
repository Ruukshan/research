"""
Ingestion, cleaning, and preprocessing script for real survey responses collected via Google Forms.
Maps raw survey questions to standardized research schema.
"""

import re
from pathlib import Path
import pandas as pd
import numpy as np

RAW_DATA_PATH = Path(r"d:\research_2\backend\app\ml\data\real\raw_google_forms_responses.csv")
PROCESSED_REAL_DATA_PATH = Path(r"d:\research_2\backend\app\ml\data\real\real_survey_students.csv")
SYNTHETIC_DATA_PATH = Path(r"d:\research_2\backend\app\ml\data\synthetic\synthetic_students.csv")
AUGMENTED_DATA_PATH = Path(r"d:\research_2\backend\app\ml\data\real\augmented_students.csv")
