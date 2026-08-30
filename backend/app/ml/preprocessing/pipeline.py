"""
Feature Engineering and Preprocessing Pipeline for Sri Lankan A/L Recommendation System.

Transforms raw student survey records (O/L grades, extracurriculars, RIASEC dimensions,
demographics) into numerical feature matrices suitable for machine learning algorithms.
Guarantees strict train/test separation to prevent data leakage.
"""

import os
from pathlib import Path
from typing import Tuple, Dict, Any, List, Optional
import numpy as np
import pandas as pd
import joblib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

from app.ml.config.ml_config import (
    STREAM_CLASSES,
    STREAM_TO_IDX,
    IDX_TO_STREAM,
    GRADE_POINTS,
    RIASEC_DIMENSIONS,
    TARGET_COLUMN
)
from app.config import settings

GRADE_COLS = [
    "math_grade", "science_grade", "english_grade",
    "first_lang_grade", "history_grade", "religion_grade",
    "basket_1_grade", "basket_2_grade", "basket_3_grade"
]

CATEGORICAL_COLS = [
    "basket_1_subject", "basket_2_subject", "basket_3_subject",
    "medium", "school_type"
]

EXTRACURRICULAR_COLS = [
    "has_sports", "has_clubs_societies", "has_coding_robotics",
    "has_debating_media", "has_music_performing_arts", "has_visual_arts",
    "has_volunteering_scouts", "has_leadership_prefect", "has_reading_writing",
    "has_entrepreneurship"
]

INFLUENCE_COLS = [
    "parental_influence_level", "teacher_guidance_level"
]


class StudentFeaturePreprocessor(BaseEstimator, TransformerMixin):
    """Custom Scikit-Learn transformer for student profile feature engineering and scaling."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        self.is_fitted = False
        self.feature_names: List[str] = []

    def _extract_engineered_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Converts raw columns into numeric arrays: grade points, engineered aggregates, extracurriculars."""
        # 1. Convert Letter Grades to Grade Points
        grade_pts = []
        for col in GRADE_COLS:
            if col in df.columns:
                pts = df[col].map(lambda x: GRADE_POINTS.get(str(x).strip().upper(), 0.0)).values
            else:
                pts = np.zeros(len(df))
            grade_pts.append(pts)
        grade_matrix = np.column_stack(grade_pts)  # Shape (N, 9)

        # 2. Derived Academic Features
        math_pts = grade_matrix[:, 0]
        sci_pts = grade_matrix[:, 1]
        eng_pts = grade_matrix[:, 2]
        lang_pts = grade_matrix[:, 3]
        hist_pts = grade_matrix[:, 4]

        stem_aptitude = (math_pts + sci_pts) / 2.0
        humanities_aptitude = (lang_pts + hist_pts) / 2.0
        gpa_approx = np.mean(grade_matrix, axis=1)
        num_distinctions = np.sum(grade_matrix == 4.0, axis=1)

        engineered_academic = np.column_stack([
            stem_aptitude, humanities_aptitude, gpa_approx, num_distinctions
        ])

        # 3. RIASEC Dimensions and Influences
        riasec_vals = []
        for col in RIASEC_DIMENSIONS:
            if col in df.columns:
                riasec_vals.append(df[col].fillna(3.0).astype(float).values)
            else:
                riasec_vals.append(np.full(len(df), 3.0))

        for col in INFLUENCE_COLS:
            if col in df.columns:
                riasec_vals.append(df[col].fillna(3.0).astype(float).values)
            else:
                riasec_vals.append(np.full(len(df), 3.0))

        numeric_matrix = np.column_stack([grade_matrix, engineered_academic] + riasec_vals)

        # 4. Extracurricular Binary Indicators
        extra_vals = []
        for col in EXTRACURRICULAR_COLS:
            if col in df.columns:
                extra_vals.append(df[col].fillna(0).astype(int).values)
            else:
                extra_vals.append(np.zeros(len(df), dtype=int))
        extra_matrix = np.column_stack(extra_vals)

        # 5. Categorical DataFrame for One-Hot Encoding
        cat_df = pd.DataFrame(index=df.index)
        for col in CATEGORICAL_COLS:
            if col in df.columns:
                cat_df[col] = df[col].fillna("Unknown").astype(str)
            else:
                cat_df[col] = "Unknown"

        return numeric_matrix, extra_matrix, cat_df

    def fit(self, X: pd.DataFrame, y=None):
        """Fit scaler on numeric features and encoder on categorical columns."""
        numeric_mat, extra_mat, cat_df = self._extract_engineered_features(X)

        self.scaler.fit(numeric_mat)
        self.encoder.fit(cat_df)
        self.is_fitted = True

        # Construct feature names
        num_names = [f"{col}_pts" for col in GRADE_COLS] + [
            "stem_aptitude", "humanities_aptitude", "gpa_approx", "num_distinctions"
        ] + RIASEC_DIMENSIONS + INFLUENCE_COLS
        cat_names = list(self.encoder.get_feature_names_out(CATEGORICAL_COLS))
        self.feature_names = num_names + EXTRACURRICULAR_COLS + cat_names

        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """Transform incoming DataFrame using fitted scaling and encoding."""
        if not self.is_fitted:
            raise RuntimeError("StudentFeaturePreprocessor must be fitted before transforming data.")

        numeric_mat, extra_mat, cat_df = self._extract_engineered_features(X)
        scaled_numeric = self.scaler.transform(numeric_mat)
        encoded_cat = self.encoder.transform(cat_df)

        return np.hstack([scaled_numeric, extra_mat, encoded_cat])

    def save(self, filepath: Optional[Path] = None):
        """Persist fitted preprocessor artifact to disk."""
        target = filepath or (settings.MODEL_ARTIFACTS_DIR / "preprocessor.joblib")
        target.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, target)

    @classmethod
    def load(cls, filepath: Optional[Path] = None) -> "StudentFeaturePreprocessor":
        """Load fitted preprocessor from disk."""
        target = filepath or (settings.MODEL_ARTIFACTS_DIR / "preprocessor.joblib")
        if not target.exists():
            raise FileNotFoundError(f"Preprocessor artifact not found at: {target}")
        return joblib.load(target)


def encode_target_labels(series: pd.Series) -> np.ndarray:
    """Encodes string stream names to class indices (0 to 4)."""
    return series.map(STREAM_TO_IDX).values


def decode_target_labels(indices: np.ndarray) -> List[str]:
    """Decodes class indices back to stream names."""
    return [IDX_TO_STREAM[int(idx)] for idx in indices]


def load_and_preprocess_dataset(
    csv_path: Optional[Path] = None,
    test_size: float = 0.20,
    random_seed: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, StudentFeaturePreprocessor]:
    """
    Loads dataset, performs stratified train/test split, and fits preprocessor on training data.
    Ensures zero data leakage between train and test sets.
    """
    file_path = csv_path or settings.SYNTHETIC_DATA_PATH
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")

    df = pd.read_csv(file_path)
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not present in dataset.")

    X = df.drop(columns=[TARGET_COLUMN])
    y = encode_target_labels(df[TARGET_COLUMN])

    # Stratified Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_seed, stratify=y
    )

    preprocessor = StudentFeaturePreprocessor()
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    # Save preprocessor artifact
    preprocessor.save()

    return X_train_proc, X_test_proc, y_train, y_test, preprocessor


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, prep = load_and_preprocess_dataset()
    print("Feature Preprocessing Pipeline successfully executed.")
    print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    print(f"X_test shape:  {X_test.shape},  y_test shape:  {y_test.shape}")
    print(f"Total extracted features: {len(prep.feature_names)}")
