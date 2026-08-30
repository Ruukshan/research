"""Tests for the dataset validator."""

import pytest
import pandas as pd
from app.ml.validation.data_validator import DatasetValidator
from app.ml.generator.synthetic_generator import SyntheticDatasetGenerator


def test_validation_on_valid_synthetic_data():
    generator = SyntheticDatasetGenerator(random_seed=42)
    df = generator.generate_dataset(num_records=50)
    validator = DatasetValidator()
    report = validator.validate(df)

    assert report["is_valid"] is True
    assert len(report["errors"]) == 0
    assert report["duplicate_record_ids_count"] == 0
    assert len(report["missing_values"]) == 0


def test_validation_catches_invalid_categories():
    generator = SyntheticDatasetGenerator(random_seed=42)
    df = generator.generate_dataset(num_records=10)
    # Introduce invalid grade
    df.loc[0, "math_grade"] = "INVALID_GRADE"
    validator = DatasetValidator()
    report = validator.validate(df)

    assert report["is_valid"] is False
    assert any("math_grade" in err for err in report["errors"])


def test_validation_catches_out_of_range_numeric():
    generator = SyntheticDatasetGenerator(random_seed=42)
    df = generator.generate_dataset(num_records=10)
    # Introduce out-of-range RIASEC score
    df.loc[0, "score_realistic"] = 99.0
    validator = DatasetValidator()
    report = validator.validate(df)

    assert report["is_valid"] is False
    assert any("score_realistic" in err for err in report["errors"])
