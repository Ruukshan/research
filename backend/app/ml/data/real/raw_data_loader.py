"""
Script containing the complete raw data pasted by the user.
Writes raw_google_forms_responses.csv and executes preprocessing.
"""

from pathlib import Path
import pandas as pd
from app.ml.data.real.save_and_clean_survey import process_raw_survey_dataframe, REAL_CLEANED_PATH, SYNTHETIC_DATA_PATH, COMBINED_DATA_PATH

RAW_CSV_PATH = Path(r"d:\research_2\backend\app\ml\data\real\raw_google_forms_responses.csv")

def save_and_process():
    # Read the raw csv
    df_raw = pd.read_csv(RAW_CSV_PATH)
    df_real = process_raw_survey_dataframe(df_raw)
    
    # Save clean real dataset
    df_real.to_csv(REAL_CLEANED_PATH, index=False)
    print(f"Saved cleaned real survey dataset ({len(df_real)} records) to: {REAL_CLEANED_PATH}")
    print("\nClass distribution in real collected data:")
    print(df_real["al_stream"].value_counts())
    
    # Combine with synthetic data to create 1,000+ augmented dataset
    if SYNTHETIC_DATA_PATH.exists():
        df_syn = pd.read_csv(SYNTHETIC_DATA_PATH)
        # Select synthetic records to balance and reach 1,200 records
        target_total = 1200
        syn_needed = max(0, target_total - len(df_real))
        df_syn_sample = df_syn.sample(n=min(syn_needed, len(df_syn)), random_state=42)
        
        df_combined = pd.concat([df_real, df_syn_sample], ignore_index=True)
        df_combined.to_csv(COMBINED_DATA_PATH, index=False)
        print(f"\nSaved combined real + synthetic dataset ({len(df_combined)} records) to: {COMBINED_DATA_PATH}")
        print("Combined Class Distribution:")
        print(df_combined["al_stream"].value_counts())

if __name__ == "__main__":
    save_and_process()
