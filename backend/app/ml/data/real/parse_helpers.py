import io
import csv
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(r"d:\research_2\backend\app\ml\data")
REAL_DIR = DATA_DIR / "real"
REAL_DIR.mkdir(parents=True, exist_ok=True)

# Grade cleaning helper
def clean_grade(val):
    if pd.isna(val):
        return "C" # default fallback
    v = str(val).strip().upper()
    # Check if multiple grades like "A, C" or "B, C"
    match = re.search(r'[ABCSW]', v)
    if match:
        return match.group(0)
    return "C"

# Clean RIASEC Likert score
def clean_likert(val, default=3.0):
    if pd.isna(val):
        return default
    try:
        score = float(str(val).strip())
        return max(1.0, min(5.0, score))
    except:
        return default

# Map raw province to valid district or province
def clean_district(prov):
    if pd.isna(prov):
        return "Colombo"
    p = str(prov).strip()
    return p if p else "Colombo"

# Map school type
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
    elif "1c" in s:
        return "1C School"
    return "1AB Provincial School"
