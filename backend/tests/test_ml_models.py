"""Unit tests for ML Preprocessing, Model Architectures, and Predictor."""

import pytest
import numpy as np
import pandas as pd
from app.ml.generator.synthetic_generator import SyntheticDatasetGenerator
from app.ml.preprocessing.pipeline import StudentFeaturePreprocessor, encode_target_labels
from app.ml.config.ml_config import STREAM_CLASSES
from app.ml.training.train_models import PyTorchDNNWrapper
from app.ml.prediction.predictor import StreamPredictor
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


@pytest.fixture
def sample_dataset():
    generator = SyntheticDatasetGenerator(random_seed=42)
    return generator.generate_dataset(num_records=60)


def test_preprocessor_fit_transform(sample_dataset):
    X = sample_dataset.drop(columns=["al_stream"])
    y = encode_target_labels(sample_dataset["al_stream"])

    preprocessor = StudentFeaturePreprocessor()
    X_proc = preprocessor.fit_transform(X)

    assert X_proc.shape[0] == len(sample_dataset)
    assert X_proc.shape[1] > 30
    assert not np.isnan(X_proc).any()
    assert len(preprocessor.feature_names) == X_proc.shape[1]


def test_random_forest_probability_output(sample_dataset):
    X = sample_dataset.drop(columns=["al_stream"])
    y = encode_target_labels(sample_dataset["al_stream"])

    preprocessor = StudentFeaturePreprocessor()
    X_proc = preprocessor.fit_transform(X)

    rf = RandomForestClassifier(n_estimators=20, max_depth=6, random_state=42)
    rf.fit(X_proc, y)

    probs = rf.predict_proba(X_proc[:5])
    assert probs.shape == (5, 5)
    np.testing.assert_allclose(probs.sum(axis=1), np.ones(5), atol=1e-5)


def test_xgboost_probability_output(sample_dataset):
    X = sample_dataset.drop(columns=["al_stream"])
    y = encode_target_labels(sample_dataset["al_stream"])

    preprocessor = StudentFeaturePreprocessor()
    X_proc = preprocessor.fit_transform(X)

    xgb = XGBClassifier(n_estimators=15, max_depth=4, eval_metric="mlogloss", random_state=42)
    xgb.fit(X_proc, y)

    probs = xgb.predict_proba(X_proc[:5])
    assert probs.shape == (5, 5)
    np.testing.assert_allclose(probs.sum(axis=1), np.ones(5), atol=1e-5)


def test_pytorch_dnn_probability_output(sample_dataset):
    X = sample_dataset.drop(columns=["al_stream"])
    y = encode_target_labels(sample_dataset["al_stream"])

    preprocessor = StudentFeaturePreprocessor()
    X_proc = preprocessor.fit_transform(X)

    dnn = PyTorchDNNWrapper(epochs=10, batch_size=16, random_seed=42)
    dnn.fit(X_proc, y)

    probs = dnn.predict_proba(X_proc[:5])
    assert probs.shape == (5, 5)
    np.testing.assert_allclose(probs.sum(axis=1), np.ones(5), atol=1e-4)


def test_stream_predictor_end_to_end(sample_dataset):
    record = sample_dataset.iloc[0].to_dict()
    predictor = StreamPredictor()
    result = predictor.predict_profile(record)

    assert "predicted_stream" in result
    assert "stream_probabilities" in result
    assert len(result["stream_probabilities"]) == 5
    assert result["predicted_stream"] in STREAM_CLASSES
