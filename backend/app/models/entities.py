"""SQLAlchemy models for research data management, predictions, and recommendations."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from app.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class StudentProfile(Base):
    """Anonymized student profile container."""
    __tablename__ = "student_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    record_id = Column(String(64), unique=True, index=True, nullable=False)
    data_source = Column(String(20), default="synthetic", nullable=False)  # "synthetic" | "real"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Demographic / General Context (No direct PII)
    gender = Column(String(20), nullable=True)
    district = Column(String(50), nullable=True)
    school_type = Column(String(50), nullable=True)  # 1AB, 1C, Type 2, Private, etc.
    medium = Column(String(20), nullable=True)       # Sinhala, Tamil, English

    # Relationships
    academic_profile = relationship("AcademicProfile", back_populates="student", uselist=False, cascade="all, delete-orphan")
    extracurricular_profile = relationship("ExtracurricularProfile", back_populates="student", uselist=False, cascade="all, delete-orphan")
    personality_profile = relationship("PersonalityProfile", back_populates="student", uselist=False, cascade="all, delete-orphan")
    career_preference = relationship("CareerPreference", back_populates="student", uselist=False, cascade="all, delete-orphan")
    predictions = relationship("StreamPrediction", back_populates="student", cascade="all, delete-orphan")


class AcademicProfile(Base):
    """GCE O/L academic performance record."""
    __tablename__ = "academic_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey("student_profiles.id"), nullable=False, unique=True)

    # Core GCE O/L subjects (A, B, C, S, W)
    math_grade = Column(String(2), nullable=False)
    science_grade = Column(String(2), nullable=False)
    english_grade = Column(String(2), nullable=False)
    first_lang_grade = Column(String(2), nullable=False)  # Sinhala / Tamil
    history_grade = Column(String(2), nullable=False)
    religion_grade = Column(String(2), nullable=False)

    # Basket Subjects
    basket_1_subject = Column(String(50), nullable=True)  # ICT, Commerce, Geography, etc.
    basket_1_grade = Column(String(2), nullable=True)
    basket_2_subject = Column(String(50), nullable=True)  # Music, Art, Drama, etc.
    basket_2_grade = Column(String(2), nullable=True)
    basket_3_subject = Column(String(50), nullable=True)  # Agri, Design Tech, Home Eco, etc.
    basket_3_grade = Column(String(2), nullable=True)

    # Summary Metrics
    num_a_grades = Column(Integer, default=0)
    gpa_approx = Column(Float, default=0.0)

    student = relationship("StudentProfile", back_populates="academic_profile")


class ExtracurricularProfile(Base):
    """Extracurricular activities and leadership experiences."""
    __tablename__ = "extracurricular_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey("student_profiles.id"), nullable=False, unique=True)

    has_sports = Column(Boolean, default=False)
    has_clubs_societies = Column(Boolean, default=False)
    has_coding_robotics = Column(Boolean, default=False)
    has_debating_media = Column(Boolean, default=False)
    has_music_performing_arts = Column(Boolean, default=False)
    has_visual_arts = Column(Boolean, default=False)
    has_volunteering_scouts = Column(Boolean, default=False)
    has_leadership_prefect = Column(Boolean, default=False)
    has_reading_writing = Column(Boolean, default=False)
    has_entrepreneurship = Column(Boolean, default=False)

    total_activities_count = Column(Integer, default=0)

    student = relationship("StudentProfile", back_populates="extracurricular_profile")


class PersonalityProfile(Base):
    """Holland RIASEC personality dimensions (1-5 scale)."""
    __tablename__ = "personality_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey("student_profiles.id"), nullable=False, unique=True)

    score_realistic = Column(Float, nullable=False, default=3.0)
    score_investigative = Column(Float, nullable=False, default=3.0)
    score_artistic = Column(Float, nullable=False, default=3.0)
    score_social = Column(Float, nullable=False, default=3.0)
    score_enterprising = Column(Float, nullable=False, default=3.0)
    score_conventional = Column(Float, nullable=False, default=3.0)

    dominant_riasec = Column(String(10), nullable=True)  # e.g., "IRC"

    student = relationship("StudentProfile", back_populates="personality_profile")


class CareerPreference(Base):
    """Career aspirations, higher education goals, and contextual influences."""
    __tablename__ = "career_preferences"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey("student_profiles.id"), nullable=False, unique=True)

    preferred_career_domain = Column(String(100), nullable=True)
    preferred_work_style = Column(String(100), nullable=True)
    higher_education_interest = Column(String(100), nullable=True)
    parental_influence_level = Column(Integer, default=3)  # 1 (Low) to 5 (High)
    teacher_guidance_level = Column(Integer, default=3)   # 1 (Low) to 5 (High)

    # Actual chosen stream (if surveyed post-decision) or target label for supervised learning
    actual_al_stream = Column(String(50), nullable=True)

    student = relationship("StudentProfile", back_populates="career_preference")


class StreamPrediction(Base):
    """Machine Learning stream probability predictions for a student assessment."""
    __tablename__ = "stream_predictions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey("student_profiles.id"), nullable=False)
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50), nullable=False)
    predicted_stream = Column(String(50), nullable=False)
    
    # Class Probabilities (Physical Science, Biological Science, Commerce, Arts, Technology)
    prob_physical_science = Column(Float, nullable=False)
    prob_biological_science = Column(Float, nullable=False)
    prob_commerce = Column(Float, nullable=False)
    prob_arts = Column(Float, nullable=False)
    prob_technology = Column(Float, nullable=False)

    probabilities_json = Column(JSON, nullable=False)
    shap_explanation_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    student = relationship("StudentProfile", back_populates="predictions")
    recommendations = relationship("PathwayRecommendation", back_populates="prediction", cascade="all, delete-orphan")


class PathwayRecommendation(Base):
    """Ranked Top-5 hybrid recommendations."""
    __tablename__ = "pathway_recommendations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    prediction_id = Column(String(36), ForeignKey("stream_predictions.id"), nullable=False)
    rank = Column(Integer, nullable=False)
    pathway_id = Column(String(64), nullable=False)
    stream = Column(String(50), nullable=False)
    degree_area = Column(String(100), nullable=False)
    degree_program = Column(String(150), nullable=False)
    career_domain = Column(String(150), nullable=False)
    recommendation_score = Column(Float, nullable=False)
    ml_stream_score = Column(Float, nullable=False)
    content_similarity_score = Column(Float, nullable=False)
    collaborative_score = Column(Float, nullable=False)
    explanation_text = Column(Text, nullable=False)

    prediction = relationship("StreamPrediction", back_populates="recommendations")


class CareerPathwayEntity(Base):
    """Knowledge base entity for Sri Lankan Degree & Career Pathways."""
    __tablename__ = "career_pathways"

    pathway_id = Column(String(64), primary_key=True)
    stream = Column(String(50), nullable=False, index=True)
    degree_area = Column(String(100), nullable=False)
    degree_program = Column(String(150), nullable=False)
    career_domain = Column(String(150), nullable=False)
    required_subjects = Column(JSON, nullable=False)
    preferred_subjects = Column(JSON, nullable=False)
    interest_tags = Column(JSON, nullable=False)
    riasec_profile = Column(JSON, nullable=False)
    skill_tags = Column(JSON, nullable=False)
    description = Column(Text, nullable=False)
    sample_job_titles = Column(JSON, nullable=True)


class ModelExperimentEntity(Base):
    """Experiment logging entity for academic research reporting."""
    __tablename__ = "model_experiments"

    experiment_id = Column(String(64), primary_key=True)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    dataset_source = Column(String(20), nullable=False)  # "synthetic" | "real" | "mixed"
    dataset_size = Column(Integer, nullable=False)
    feature_version = Column(String(50), nullable=False)
    preprocessing_version = Column(String(50), nullable=False)
    model_name = Column(String(100), nullable=False)
    hyperparameters = Column(JSON, nullable=False)
    cv_mean = Column(Float, nullable=False)
    cv_std = Column(Float, nullable=False)
    test_accuracy = Column(Float, nullable=False)
    test_precision = Column(Float, nullable=False)
    test_recall = Column(Float, nullable=False)
    test_f1 = Column(Float, nullable=False)
    random_seed = Column(Integer, nullable=False)
    is_selected = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    metrics_json = Column(JSON, nullable=True)
