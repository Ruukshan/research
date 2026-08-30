"""Tests for the synthetic dataset generator."""

import pytest
import pandas as pd
from app.ml.generator.synthetic_generator import SyntheticDatasetGenerator
from app.ml.config.ml_config import STREAM_CLASSES


def test_synthetic_generator_record_structure():
    generator = SyntheticDatasetGenerator(random_seed=42)
    record = generator.generate_record(1)

    assert "record_id" in record
    assert record["record_id"] == "STU-SYN-00001"
    assert record["data_source"] == "synthetic"
    assert record["al_stream"] in STREAM_CLASSES
    assert record["math_grade"] in ["A", "B", "C", "S", "W"]
    assert 1.0 <= record["score_investigative"] <= 5.0
    assert 1 <= record["parental_influence_level"] <= 5


def test_synthetic_generator_dataset_batch():
    generator = SyntheticDatasetGenerator(random_seed=42)
    df = generator.generate_dataset(num_records=100)

    assert len(df) == 100
    assert (df["data_source"] == "synthetic").all()
    # Check that all 5 streams are present
    unique_streams = df["al_stream"].unique()
    assert len(unique_streams) == 5
    for stream in STREAM_CLASSES:
        assert stream in unique_streams
