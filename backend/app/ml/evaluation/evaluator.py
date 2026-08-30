"""
Research Evaluation and Visualization Module.

Generates publication-ready figures:
  1. Model Accuracy, Precision, Recall, Macro F1 comparison chart
  2. Confusion Matrix heatmaps for RF, XGBoost, and DNN
  3. 10-Fold Cross-Validation score distribution boxplots
  4. Top predictive feature importances
  5. Deep Neural Network training and validation curves
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless research plot generation
import matplotlib.pyplot as plt
import seaborn as sns

from app.ml.config.ml_config import STREAM_CLASSES
from app.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Research Visual Style Configuration
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.titlesize": 14,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight"
})

STREAM_SHORT_LABELS = ["Physical", "Biological", "Commerce", "Arts", "Technology"]


class ResearchEvaluator:
    """Generates figures and summary tables from model comparison results."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or settings.RESEARCH_RESULTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def plot_metric_comparisons(self, results: Dict[str, Any]):
        """Generates grouped bar chart comparing Accuracy, Precision, Recall, Macro F1."""
        models = list(results.keys())
        metrics = ["Accuracy", "Precision (Macro)", "Recall (Macro)", "Macro F1"]

        data = []
        for m in models:
            r = results[m]
            data.append([
                r["test_accuracy"],
                r["test_precision_macro"],
                r["test_recall_macro"],
                r["test_f1_macro"]
            ])

        x = np.arange(len(models))
        width = 0.18

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ["#4f46e5", "#06b6d4", "#10b981", "#f59e0b"]

        for i, metric in enumerate(metrics):
            vals = [data[m_idx][i] for m_idx in range(len(models))]
            rects = ax.bar(x + (i - 1.5) * width, vals, width, label=metric, color=colors[i], alpha=0.9, edgecolor="none")
            for rect in rects:
                h = rect.get_height()
                ax.annotate(f"{h*100:.1f}%",
                            xy=(rect.get_x() + rect.get_width() / 2, h),
                            xytext=(0, 3), textcoords="offset points",
                            ha="center", va="bottom", fontsize=7.5, fontweight="bold")

        ax.set_ylabel("Score (0.0 - 1.0)", fontweight="bold")
        ax.set_title("Multi-Model Performance Comparison on Sri Lankan GCE A/L Dataset", fontweight="bold", pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(models, fontweight="bold")
        ax.set_ylim(0.0, 1.15)
        ax.legend(loc="upper left", frameon=True)
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        out_path = self.output_dir / "model_metrics_comparison.png"
        fig.savefig(out_path)
        plt.close(fig)
        logger.info(f"Saved metric comparison figure to: {out_path}")

    def plot_confusion_matrices(self, results: Dict[str, Any]):
        """Generates side-by-side confusion matrix heatmaps."""
        models = [m for m in results.keys() if "confusion_matrix" in results[m]]
        num_models = len(models)
        if num_models == 0:
            return

        fig, axes = plt.subplots(1, num_models, figsize=(6 * num_models, 5))
        if num_models == 1:
            axes = [axes]

        for idx, m_name in enumerate(models):
            cm = np.array(results[m_name]["confusion_matrix"])
            ax = axes[idx]
            sns.heatmap(
                cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=STREAM_SHORT_LABELS, yticklabels=STREAM_SHORT_LABELS, ax=ax
            )
            ax.set_title(f"{m_name}\n(Acc: {results[m_name]['test_accuracy']*100:.1f}%)", fontweight="bold")
            ax.set_xlabel("Predicted Stream", fontweight="bold")
            if idx == 0:
                ax.set_ylabel("True Stream", fontweight="bold")

        plt.suptitle("Confusion Matrix Comparison Across Candidate Architectures", fontweight="bold", y=1.02)
        out_path = self.output_dir / "confusion_matrices_comparison.png"
        fig.savefig(out_path)
        plt.close(fig)
        logger.info(f"Saved confusion matrices figure to: {out_path}")

    def plot_cv_distributions(self, results: Dict[str, Any]):
        """Generates box plots and scatter points for 10-Fold CV score distributions."""
        models = list(results.keys())
        cv_f1_data = [results[m]["cv_results"]["fold_f1_scores"] for m in models]

        fig, ax = plt.subplots(figsize=(8, 5))
        bp = ax.boxplot(cv_f1_data, patch_artist=True, notch=False, showmeans=True)

        colors = ["#c7d2fe", "#a5f3fc", "#bbf7d0"]
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_edgecolor("#374151")
            patch.set_alpha(0.85)

        # Overlay individual fold scatter points with jitter
        for i, fold_scores in enumerate(cv_f1_data):
            y_pts = fold_scores
            x_pts = np.random.normal(i + 1, 0.04, size=len(y_pts))
            ax.plot(x_pts, y_pts, 'ro', alpha=0.6, markersize=5)

        ax.set_xticks(range(1, len(models) + 1))
        ax.set_xticklabels(models, fontweight="bold")
        ax.set_ylabel("Macro F1-Score", fontweight="bold")
        ax.set_title("10-Fold Stratified Cross-Validation F1-Score Distribution", fontweight="bold", pad=15)
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        out_path = self.output_dir / "cross_validation_distribution.png"
        fig.savefig(out_path)
        plt.close(fig)
        logger.info(f"Saved CV distributions figure to: {out_path}")

    def plot_feature_importances(self, results: Dict[str, Any]):
        """Generates feature importance horizontal bar charts."""
        target_model = None
        for name in ["XGBoost Multi-Class", "Random Forest (Baseline)"]:
            if name in results and results[name].get("feature_importances"):
                target_model = name
                break

        if not target_model:
            return

        feat_dict = results[target_model]["feature_importances"]
        sorted_feats = sorted(feat_dict.items(), key=lambda x: x[1], reverse=True)[:12]
        names = [item[0] for item in sorted_feats][::-1]
        scores = [item[1] for item in sorted_feats][::-1]

        fig, ax = plt.subplots(figsize=(9, 6))
        bars = ax.barh(names, scores, color="#4f46e5", alpha=0.85, edgecolor="none")

        for bar in bars:
            w = bar.get_width()
            ax.annotate(f"{w:.3f}",
                        xy=(w, bar.get_y() + bar.get_height() / 2),
                        xytext=(4, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=8, fontweight="bold")

        ax.set_xlabel("Relative Importance Score", fontweight="bold")
        ax.set_title(f"Top 12 Predictive Features ({target_model})", fontweight="bold", pad=15)
        ax.grid(axis="x", linestyle="--", alpha=0.7)

        out_path = self.output_dir / "feature_importance_rf_xgb.png"
        fig.savefig(out_path)
        plt.close(fig)
        logger.info(f"Saved feature importances figure to: {out_path}")

    def plot_dnn_learning_curves(self, results: Dict[str, Any]):
        """Plots training loss and validation accuracy curves for the Deep Neural Network."""
        dnn_name = "Deep Neural Network (Tabular MLP)"
        if dnn_name not in results or not results[dnn_name].get("training_history"):
            return

        hist = results[dnn_name]["training_history"]
        train_loss = hist.get("train_loss", [])
        val_loss = hist.get("val_loss", [])
        val_acc = hist.get("val_acc", [])

        if not train_loss:
            return

        epochs = range(1, len(train_loss) + 1)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

        # Loss Curve
        ax1.plot(epochs, train_loss, 'b-', label="Training Loss", linewidth=2)
        if val_loss:
            ax1.plot(epochs[:len(val_loss)], val_loss, 'r--', label="Validation Loss", linewidth=2)
        ax1.set_title("DNN Loss Trajectory (Cross-Entropy)", fontweight="bold")
        ax1.set_xlabel("Epoch", fontweight="bold")
        ax1.set_ylabel("Loss", fontweight="bold")
        ax1.legend()
        ax1.grid(True, linestyle="--", alpha=0.7)

        # Accuracy Curve
        if val_acc:
            ax2.plot(epochs[:len(val_acc)], [a * 100 for a in val_acc], 'g-', label="Validation Accuracy (%)", linewidth=2)
            ax2.set_title("DNN Validation Accuracy Trajectory", fontweight="bold")
            ax2.set_xlabel("Epoch", fontweight="bold")
            ax2.set_ylabel("Accuracy (%)", fontweight="bold")
            ax2.legend()
            ax2.grid(True, linestyle="--", alpha=0.7)

        out_path = self.output_dir / "dnn_training_curves.png"
        fig.savefig(out_path)
        plt.close(fig)
        logger.info(f"Saved DNN learning curves figure to: {out_path}")

    def generate_all(self, results: Dict[str, Any]):
        """Generates all 5 research figures."""
        self.plot_metric_comparisons(results)
        self.plot_confusion_matrices(results)
        self.plot_cv_distributions(results)
        self.plot_feature_importances(results)
        self.plot_dnn_learning_curves(results)


def generate_research_visualizations(results_json_path: Optional[Path] = None):
    """Entrypoint to load experiment results and render all research plots."""
    target_json = results_json_path or (settings.RESEARCH_RESULTS_DIR / "experiment_results.json")
    if not target_json.exists():
        raise FileNotFoundError(f"Experiment results JSON not found at: {target_json}")

    with open(target_json, "r", encoding="utf-8") as f:
        results = json.load(f)

    evaluator = ResearchEvaluator()
    evaluator.generate_all(results)


if __name__ == "__main__":
    generate_research_visualizations()
    print("All research figures generated successfully in: backend/app/ml/evaluation/results/")
