"""
Model Training, 10-Fold Stratified Cross-Validation, and Comparison Module.

Trains and evaluates:
  1. Random Forest Classifier (Baseline)
  2. XGBoost Multi-Class Classifier
  3. Deep Neural Network (PyTorch Tabular MLP)

Performs 10-fold Stratified CV, computes research metrics, and persists the best model artifact.
"""

import os
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

from app.ml.config.ml_config import STREAM_CLASSES, STREAM_TO_IDX
from app.ml.preprocessing.pipeline import load_and_preprocess_dataset, StudentFeaturePreprocessor
from app.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ==========================================
# 1. PyTorch Tabular Deep Neural Network
# ==========================================
class TabularMLP(nn.Module):
    """Deep Neural Network for Tabular Classification."""

    def __init__(self, input_dim: int, num_classes: int = 5, dropout_rate: float = 0.25):
        super(TabularMLP, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        self.eval()
        with torch.no_grad():
            tensor_x = torch.tensor(X, dtype=torch.float32)
            logits = self.forward(tensor_x)
            probs = torch.softmax(logits, dim=1).numpy()
        return probs

    def predict(self, X: np.ndarray) -> np.ndarray:
        probs = self.predict_proba(X)
        return np.argmax(probs, axis=1)


class PyTorchDNNWrapper:
    """Scikit-Learn compatible wrapper for the PyTorch Tabular MLP."""

    def __init__(
        self,
        epochs: int = 80,
        batch_size: int = 32,
        lr: float = 0.001,
        dropout_rate: float = 0.25,
        patience: int = 10,
        random_seed: int = 42
    ):
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr
        self.dropout_rate = dropout_rate
        self.patience = patience
        self.random_seed = random_seed
        self.model: Optional[TabularMLP] = None
        self.input_dim: int = 0
        self.classes_ = np.arange(len(STREAM_CLASSES))
        self.training_history = {"train_loss": [], "val_loss": [], "val_acc": []}

    def fit(self, X: np.ndarray, y: np.ndarray, validation_data: Optional[Tuple[np.ndarray, np.ndarray]] = None):
        torch.manual_seed(self.random_seed)
        np.random.seed(self.random_seed)

        self.input_dim = X.shape[1]
        self.model = TabularMLP(input_dim=self.input_dim, num_classes=len(STREAM_CLASSES), dropout_rate=self.dropout_rate)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.lr, weight_decay=1e-4)

        train_dataset = TensorDataset(torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.long))
        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)

        best_val_loss = float("inf")
        patience_counter = 0
        best_state = None

        self.training_history = {"train_loss": [], "val_loss": [], "val_acc": []}

        for epoch in range(self.epochs):
            self.model.train()
            running_loss = 0.0
            for batch_x, batch_y in train_loader:
                optimizer.zero_grad()
                outputs = self.model(batch_x)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                running_loss += loss.item() * batch_x.size(0)

            epoch_loss = running_loss / len(X)
            self.training_history["train_loss"].append(epoch_loss)

            if validation_data is not None:
                val_x, val_y = validation_data
                self.model.eval()
                with torch.no_grad():
                    val_logits = self.model(torch.tensor(val_x, dtype=torch.float32))
                    val_loss = criterion(val_logits, torch.tensor(val_y, dtype=torch.long)).item()
                    val_preds = torch.argmax(val_logits, dim=1).numpy()
                    val_acc = accuracy_score(val_y, val_preds)

                self.training_history["val_loss"].append(val_loss)
                self.training_history["val_acc"].append(val_acc)

                # Early stopping check
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    patience_counter = 0
                    best_state = {k: v.cpu().clone() for k, v in self.model.state_dict().items()}
                else:
                    patience_counter += 1
                    if patience_counter >= self.patience:
                        logger.info(f"DNN Early stopping triggered at epoch {epoch + 1}")
                        break

        if best_state is not None:
            self.model.load_state_dict(best_state)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


# ==========================================
# 2. Multi-Model Trainer & Evaluator
# ==========================================
class ModelTrainer:
    """Executes 10-fold Stratified CV, model comparison, and persistence."""

    def __init__(self, random_seed: int = 42):
        self.random_seed = random_seed
        self.cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=random_seed)

    def evaluate_model_cv(self, model: Any, X: np.ndarray, y: np.ndarray, model_name: str) -> Dict[str, Any]:
        """Calculates 10-fold Stratified Cross-Validation scores."""
        logger.info(f"Running 10-fold Stratified CV for: {model_name}...")
        fold_accuracies = []
        fold_f1_macros = []

        for train_idx, val_idx in self.cv.split(X, y):
            X_fold_train, X_fold_val = X[train_idx], X[val_idx]
            y_fold_train, y_fold_val = y[train_idx], y[val_idx]

            if isinstance(model, PyTorchDNNWrapper):
                fold_model = PyTorchDNNWrapper(random_seed=self.random_seed)
                fold_model.fit(X_fold_train, y_fold_train, validation_data=(X_fold_val, y_fold_val))
            else:
                from sklearn.base import clone
                fold_model = clone(model)
                fold_model.fit(X_fold_train, y_fold_train)

            preds = fold_model.predict(X_fold_val)
            fold_accuracies.append(accuracy_score(y_fold_val, preds))
            fold_f1_macros.append(f1_score(y_fold_val, preds, average="macro", zero_division=0))

        return {
            "cv_accuracy_mean": float(np.mean(fold_accuracies)),
            "cv_accuracy_std": float(np.std(fold_accuracies)),
            "cv_f1_mean": float(np.mean(fold_f1_macros)),
            "cv_f1_std": float(np.std(fold_f1_macros)),
            "fold_accuracies": [float(a) for a in fold_accuracies],
            "fold_f1_scores": [float(f) for f in fold_f1_macros]
        }

    def train_and_evaluate_all(
        self,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_train: np.ndarray,
        y_test: np.ndarray,
        feature_names: List[str]
    ) -> Dict[str, Any]:
        """Trains RF, XGBoost, and DNN, performs 10-fold CV, and evaluates on test split."""
        models = {
            "Random Forest (Baseline)": RandomForestClassifier(
                n_estimators=200,
                max_depth=12,
                min_samples_split=4,
                class_weight="balanced",
                random_state=self.random_seed,
                n_jobs=-1
            ),
            "XGBoost Multi-Class": XGBClassifier(
                n_estimators=150,
                max_depth=5,
                learning_rate=0.08,
                subsample=0.85,
                colsample_bytree=0.85,
                eval_metric="mlogloss",
                random_state=self.random_seed,
                n_jobs=-1
            ),
            "Deep Neural Network (Tabular MLP)": PyTorchDNNWrapper(
                epochs=80,
                batch_size=32,
                lr=0.001,
                dropout_rate=0.25,
                patience=12,
                random_seed=self.random_seed
            )
        }

        results = {}
        fitted_models = {}

        for name, model in models.items():
            logger.info(f"\n{'='*20} Training {name} {'='*20}")

            # 1. 10-Fold Stratified Cross-Validation
            cv_metrics = self.evaluate_model_cv(model, X_train, y_train, name)

            # 2. Fit on full training set
            if isinstance(model, PyTorchDNNWrapper):
                model.fit(X_train, y_train, validation_data=(X_test, y_test))
            else:
                model.fit(X_train, y_train)

            fitted_models[name] = model

            # 3. Evaluate on Holdout Test Set
            test_preds = model.predict(X_test)
            test_probs = model.predict_proba(X_test)

            acc = float(accuracy_score(y_test, test_preds))
            prec_macro = float(precision_score(y_test, test_preds, average="macro", zero_division=0))
            rec_macro = float(recall_score(y_test, test_preds, average="macro", zero_division=0))
            f1_macro = float(f1_score(y_test, test_preds, average="macro", zero_division=0))
            conf_mat = confusion_matrix(y_test, test_preds).tolist()
            cls_report = classification_report(y_test, test_preds, target_names=STREAM_CLASSES, output_dict=True)

            # Extract Feature Importances (for tree models)
            feat_imp = {}
            if hasattr(model, "feature_importances_"):
                importances = model.feature_importances_
                top_indices = np.argsort(importances)[::-1][:15]
                feat_imp = {feature_names[i]: float(importances[i]) for i in top_indices if i < len(feature_names)}

            results[name] = {
                "model_name": name,
                "cv_results": cv_metrics,
                "test_accuracy": acc,
                "test_precision_macro": prec_macro,
                "test_recall_macro": rec_macro,
                "test_f1_macro": f1_macro,
                "confusion_matrix": conf_mat,
                "classification_report": cls_report,
                "feature_importances": feat_imp,
                "training_history": getattr(model, "training_history", None)
            }

            logger.info(
                f"{name} Performance: Test Acc = {acc*100:.2f}%, Test Macro F1 = {f1_macro*100:.2f}%, "
                f"CV F1 = {cv_metrics['cv_f1_mean']*100:.2f}% ± {cv_metrics['cv_f1_std']*100:.2f}%"
            )

        # 4. Objective Best Model Selection based on CV Macro F1
        best_model_name = max(results, key=lambda k: results[k]["cv_results"]["cv_f1_mean"])
        best_model = fitted_models[best_model_name]

        logger.info(f"\n>>> Best Model Selected by Empirical CV Macro F1: {best_model_name}")

        # Save Best Model Artifact
        artifact_path = settings.MODEL_ARTIFACTS_DIR / "best_stream_model.joblib"
        joblib.dump({
            "model_name": best_model_name,
            "model": best_model,
            "stream_classes": STREAM_CLASSES,
            "stream_to_idx": STREAM_TO_IDX,
            "random_seed": self.random_seed
        }, artifact_path)
        logger.info(f"Persisted best model artifact to: {artifact_path}")

        # Also save individual fitted models for comparative analysis
        for m_name, m_obj in fitted_models.items():
            safe_name = m_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
            joblib.dump(m_obj, settings.MODEL_ARTIFACTS_DIR / f"{safe_name}.joblib")

        return {
            "comparison_results": results,
            "best_model_name": best_model_name,
            "best_model_metrics": results[best_model_name]
        }


def train_and_compare_all_models(
    csv_path: Optional[Path] = None,
    random_seed: int = 42
) -> Dict[str, Any]:
    """Complete workflow: load data, preprocess, train 3 models, evaluate, and save."""
    X_train, X_test, y_train, y_test, preprocessor = load_and_preprocess_dataset(
        csv_path=csv_path, random_seed=random_seed
    )

    trainer = ModelTrainer(random_seed=random_seed)
    experiment_data = trainer.train_and_evaluate_all(
        X_train, X_test, y_train, y_test, feature_names=preprocessor.feature_names
    )

    # Save structured experiment results JSON
    res_path = settings.RESEARCH_RESULTS_DIR / "experiment_results.json"
    res_path.parent.mkdir(parents=True, exist_ok=True)
    with open(res_path, "w", encoding="utf-8") as f:
        json.dump(experiment_data["comparison_results"], f, indent=2)
    logger.info(f"Saved structured research experiment results to: {res_path}")

    return experiment_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and compare Random Forest, XGBoost, and DNN on A/L dataset")
    parser.add_argument("--data", type=str, default=None, help="Path to input CSV dataset")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    args = parser.parse_args()

    data_file = Path(args.data) if args.data else None
    train_and_compare_all_models(csv_path=data_file, random_seed=args.seed)
