"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "project" in data
    assert data["data_mode"] == "synthetic"


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["data_mode"] == "synthetic"


def test_pathways_endpoint():
    response = client.get("/api/pathways")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10
    # Filter by stream
    ps_resp = client.get("/api/pathways?stream=Physical%20Science")
    assert ps_resp.status_code == 200
    ps_data = ps_resp.json()
    assert len(ps_data) > 0
    assert all(p["stream"] == "Physical Science" for p in ps_data)


def test_assessment_submission():
    payload = {
        "gender": "Male",
        "district": "Colombo",
        "school_type": "1AB National School",
        "medium": "English",
        "academic": {
            "math_grade": "A",
            "science_grade": "A",
            "english_grade": "A",
            "first_lang_grade": "A",
            "history_grade": "B",
            "religion_grade": "A",
            "basket_1_subject": "ICT",
            "basket_1_grade": "A",
            "basket_2_subject": "English Literature",
            "basket_2_grade": "B",
            "basket_3_subject": "Design_Tech",
            "basket_3_grade": "A"
        },
        "extracurricular": {
            "has_sports": True,
            "has_clubs_societies": True,
            "has_coding_robotics": True,
            "has_debating_media": False,
            "has_music_performing_arts": False,
            "has_visual_arts": False,
            "has_volunteering_scouts": False,
            "has_leadership_prefect": True,
            "has_reading_writing": True,
            "has_entrepreneurship": False
        },
        "personality": {
            "score_realistic": 4.5,
            "score_investigative": 4.8,
            "score_artistic": 2.5,
            "score_social": 2.8,
            "score_enterprising": 3.2,
            "score_conventional": 4.0
        },
        "career": {
            "preferred_career_domain": "Software Architecture & AI",
            "preferred_work_style": "Team-based & Project-driven",
            "higher_education_interest": "State University Degree",
            "parental_influence_level": 4,
            "teacher_guidance_level": 4
        }
    }

    response = client.post("/api/assessment", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "student_id" in data
    assert "stream_probabilities" in data
    assert "recommendations" in data
    assert len(data["recommendations"]) == 5
    assert data["predicted_stream"] in ["Physical Science", "Technology"]
    assert len(data["stream_probabilities"]) == 5
