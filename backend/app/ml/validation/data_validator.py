"""
Comprehensive Dataset Validator for Sri Lankan A/L Recommendation System.

Performs schema verification, missing value auditing, range and categorical integrity checks,
duplicate detection, and class-balance analytics.
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

from app.ml.schema.survey_schema import SURVEY_SCHEMA_SPEC
from app.ml.config.ml_config import STREAM_CLASSES
from app.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class DatasetValidator:
    """Validates survey and dataset data frames against academic schema specifications."""

    def __init__(self, schema_spec: Optional[Dict[str, Dict[str, Any]]] = None):
        self.schema = schema_spec or SURVEY_SCHEMA_SPEC

    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Runs the validation suite and returns a detailed status report."""
        report = {
            "total_records": len(df),
            "total_columns": len(df.columns),
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "missing_values": {},
            "duplicate_records_count": 0,
            "duplicate_record_ids_count": 0,
            "class_distribution": {},
            "column_type_checks": {}
        }

        if df.empty:
            report["is_valid"] = False
            report["errors"].append("Dataset is empty.")
            return report

        # 1. Required Columns Check
        for col_name, rules in self.schema.items():
            if rules.get("required", False):
                if col_name not in df.columns:
                    report["is_valid"] = False
                    report["errors"].append(f"Missing required column: '{col_name}'")

        # 2. Check for Duplicate Records & IDs
        if "record_id" in df.columns:
            dup_ids = df["record_id"].duplicated().sum()
            report["duplicate_record_ids_count"] = int(dup_ids)
            if dup_ids > 0:
                report["is_valid"] = False
                report["errors"].append(f"Found {dup_ids} duplicate 'record_id' entries.")

        # Check feature-level row duplicates (ignoring record_id)
        feature_cols = [c for c in df.columns if c not in ["record_id"]]
        dup_rows = df.duplicated(subset=feature_cols).sum()
        report["duplicate_records_count"] = int(dup_rows)
        if dup_rows > 0:
            report["warnings"].append(f"Found {dup_rows} identical student profiles (duplicate feature rows).")

        # 3. Missing Value Audit
        null_counts = df.isnull().sum().to_dict()
        for col, null_count in null_counts.items():
            if null_count > 0:
                report["missing_values"][col] = int(null_count)
                if col in self.schema and self.schema[col].get("required", False):
                    report["is_valid"] = False
                    report["errors"].append(f"Required column '{col}' has {null_count} missing (NaN) values.")

        # 4. Value Range and Category Validation
        for col in df.columns:
            if col not in self.schema:
                report["warnings"].append(f"Column '{col}' is not defined in standard schema.")
                continue

            rules = self.schema[col]
            series = df[col].dropna()

            # Categorical check
            if rules.get("type") == "categorical" or "allowed" in rules:
                allowed_vals = rules.get("allowed", [])
                invalid_vals = series[~series.isin(allowed_vals)].unique().tolist()
                if invalid_vals:
                    report["is_valid"] = False
                    report["errors"].append(
                        f"Column '{col}' contains invalid categories: {invalid_vals}. Allowed: {allowed_vals}"
                    )
                report["column_type_checks"][col] = "categorical_valid"

            # Numeric range check
            elif rules.get("type") == "numeric":
                min_val = rules.get("min")
                max_val = rules.get("max")
                try:
                    num_series = pd.to_numeric(series)
                    if min_val is not None and (num_series < min_val).any():
                        violators = num_series[num_series < min_val].count()
                        report["is_valid"] = False
                        report["errors"].append(f"Column '{col}' has {violators} values below minimum ({min_val}).")
                    if max_val is not None and (num_series > max_val).any():
                        violators = num_series[num_series > max_val].count()
                        report["is_valid"] = False
                        report["errors"].append(f"Column '{col}' has {violators} values above maximum ({max_val}).")
                    report["column_type_checks"][col] = "numeric_range_valid"
                except Exception as e:
                    report["is_valid"] = False
                    report["errors"].append(f"Column '{col}' cannot be parsed as numeric: {str(e)}")

        # 5. Class Distribution Check (Target variable)
        if "al_stream" in df.columns:
            class_counts = df["al_stream"].value_counts().to_dict()
            report["class_distribution"] = {str(k): int(v) for k, v in class_counts.items()}
            # Check if all 5 streams are represented
            missing_classes = [c for c in STREAM_CLASSES if c not in class_counts]
            if missing_classes:
                report["warnings"].append(f"Missing representation for target classes: {missing_classes}")

        return report


def validate_dataset_file(file_path: Path) -> Dict[str, Any]:
    """Load and validate a CSV or JSON dataset file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path)
    elif file_path.suffix.lower() == ".json":
        df = pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")

    validator = DatasetValidator()
    report = validator.validate(df)
    logger.info(f"Validation Report for {file_path.name}: Is Valid = {report['is_valid']}")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate dataset integrity against Sri Lankan Survey Schema")
    parser.add_argument("--file", type=str, default=str(settings.SYNTHETIC_DATA_PATH), help="Path to CSV/JSON dataset")
    args = parser.parse_args()

    target_path = Path(args.file)
    res = validate_dataset_file(target_path)
    print("\n" + "="*50)
    print("DATASET VALIDATION SUMMARY REPORT")
    print("="*50)
    print(json.dumps(res, indent=2))
