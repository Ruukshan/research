"""Explainability module for SHAP model explanations."""
from app.ml.explainability.shap_explainer import ShapExplainer, get_shap_explainer

__all__ = ["ShapExplainer", "get_shap_explainer"]
