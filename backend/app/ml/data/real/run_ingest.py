"""
Ingestion, cleaning, and model retraining runner for real and mixed datasets.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from app.ml.data.real.save_and_clean_survey import (
    process_raw_survey_dataframe,
    RAW_CSV_PATH,
    REAL_CLEANED_PATH,
    SYNTHETIC_DATA_PATH,
    COMBINED_DATA_PATH
)

def run_ingestion():
    # Read chunk 1
    c1_path = Path(r"d:\research_2\backend\app\ml\data\real\raw_survey.csv")
    c2_path = Path(r"d:\research_2\backend\app\ml\data\real\raw_survey_chunk2.csv")
    
    df1 = pd.read_csv(c1_path)
    
    if c2_path.exists():
        df2 = pd.read_csv(c2_path, header=None)
        df2.columns = df1.columns
        df_all_raw = pd.concat([df1, df2], ignore_index=True)
    else:
        df_all_raw = df1
        
    df_all_raw.to_csv(RAW_CSV_PATH, index=False)
    print(f"Total raw rows: {len(df_all_raw)}")
    
    # Process into clean schema
    df_real = process_raw_survey_dataframe(df_all_raw)
    df_real.to_csv(REAL_CLEANED_PATH, index=False)
    print(f"\n[Phase 1] Cleaned real survey records: {len(df_real)}")
    print("Real stream distribution:")
    print(df_real["al_stream"].value_counts())
    
    # Create Augmented Combined Dataset for Phase 2 1000+ benchmark
    if SYNTHETIC_DATA_PATH.exists():
        df_syn = pd.read_csv(SYNTHETIC_DATA_PATH)
        target_size = 1200
        syn_needed = max(0, target_size - len(df_real))
        df_syn_sample = df_syn.sample(n=min(syn_needed, len(df_syn)), random_state=42)
        
        df_combined = pd.concat([df_real, df_syn_sample], ignore_index=True)
        df_combined.to_csv(COMBINED_DATA_PATH, index=False)
        print(f"\n[Phase 1] Combined Real+Synthetic dataset saved: {len(df_combined)} records")
        print("Combined stream distribution:")
        print(df_combined["al_stream"].value_counts())

if __name__ == "__main__":
    run_ingestion()
