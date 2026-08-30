"""Student profile and feature sub-schemas."""

from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

GradeType = Literal["A", "B", "C", "S", "W"]


class AcademicProfileSchema(BaseModel):
    """GCE O/L Academic Performance."""
    math_grade: GradeType = Field(..., description="GCE O/L Mathematics grade (A, B, C, S, W)")
    science_grade: GradeType = Field(..., description="GCE O/L Science grade (A, B, C, S, W)")
    english_grade: GradeType = Field(..., description="GCE O/L English Language grade")
    first_lang_grade: GradeType = Field(..., description="GCE O/L Sinhala / Tamil grade")
    history_grade: GradeType = Field(..., description="GCE O/L History grade")
    religion_grade: GradeType = Field(..., description="GCE O/L Religion grade")

    basket_1_subject: Optional[str] = Field("ICT", description="Basket 1 (ICT, Commerce, Geography, etc.)")
    basket_1_grade: Optional[GradeType] = Field("B", description="Basket 1 grade")
    basket_2_subject: Optional[str] = Field("Art", description="Basket 2 (Music, Art, Drama, etc.)")
    basket_2_grade: Optional[GradeType] = Field("B", description="Basket 2 grade")
    basket_3_subject: Optional[str] = Field("Design_Tech", description="Basket 3 (Agriculture, Design Tech, Home Eco, etc.)")
    basket_3_grade: Optional[GradeType] = Field("B", description="Basket 3 grade")


class ExtracurricularProfileSchema(BaseModel):
    """Extracurricular Activities Participation."""
    has_sports: bool = Field(False, description="Athletics, Cricket, Badminton, etc.")
    has_clubs_societies: bool = Field(False, description="Science club, Commerce society, etc.")
    has_coding_robotics: bool = Field(False, description="IT club, coding competitions, robotics")
    has_debating_media: bool = Field(False, description="Debating team, Media club, Announcing")
    has_music_performing_arts: bool = Field(False, description="School choir, orchestra, drama")
    has_visual_arts: bool = Field(False, description="Art club, exhibitions, photography")
    has_volunteering_scouts: bool = Field(False, description="Scouts, Girl Guides, Red Cross, St. John")
    has_leadership_prefect: bool = Field(False, description="Prefect guild, team captain, president")
    has_reading_writing: bool = Field(False, description="Literary association, journalism")
    has_entrepreneurship: bool = Field(False, description="School young entrepreneurs club")


class PersonalityProfileSchema(BaseModel):
    """Holland RIASEC Personality Dimension Scores (1.0 to 5.0)."""
    score_realistic: float = Field(3.0, ge=1.0, le=5.0, description="Practical, mechanical, hands-on")
    score_investigative: float = Field(3.0, ge=1.0, le=5.0, description="Analytical, intellectual, scientific")
    score_artistic: float = Field(3.0, ge=1.0, le=5.0, description="Creative, expressive, original")
    score_social: float = Field(3.0, ge=1.0, le=5.0, description="Cooperative, helping, teaching")
    score_enterprising: float = Field(3.0, ge=1.0, le=5.0, description="Persuasive, leadership, business")
    score_conventional: float = Field(3.0, ge=1.0, le=5.0, description="Organized, detail-oriented, data-focused")


class CareerPreferenceSchema(BaseModel):
    """Career Aspirations and Preferences."""
    preferred_career_domain: Optional[str] = Field("Engineering & Technology", description="High-level career domain")
    preferred_work_style: Optional[str] = Field("Team-based & Project-driven", description="Work style preference")
    higher_education_interest: Optional[str] = Field("State University Degree", description="State University / Foreign Degree / Vocational")
    parental_influence_level: int = Field(3, ge=1, le=5, description="Perceived parental guidance level (1=Low, 5=High)")
    teacher_guidance_level: int = Field(3, ge=1, le=5, description="Teacher / school counsellor influence (1=Low, 5=High)")
    actual_al_stream: Optional[str] = Field(None, description="Actual chosen stream (for survey dataset / evaluation)")


class StudentProfileCreate(BaseModel):
    """Full student intake profile."""
    gender: Optional[str] = Field("Prefer not to say")
    district: Optional[str] = Field("Colombo")
    school_type: Optional[str] = Field("1AB School")
    medium: Optional[str] = Field("English")

    academic: AcademicProfileSchema
    extracurricular: ExtracurricularProfileSchema
    personality: PersonalityProfileSchema
    career: CareerPreferenceSchema


class StudentProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    record_id: str
    data_source: str
    created_at: datetime
    academic: AcademicProfileSchema
    extracurricular: ExtracurricularProfileSchema
    personality: PersonalityProfileSchema
    career: CareerPreferenceSchema
