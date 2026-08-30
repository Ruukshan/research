"""Career Pathway Knowledge Base Query Endpoints."""

import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.config import settings
from app.schemas.recommendation import CareerPathwaySchema

router = APIRouter()


def load_pathways_kb() -> List[dict]:
    """Load pathways from knowledge base JSON."""
    if not settings.KNOWLEDGE_BASE_PATH.exists():
        return []
    with open(settings.KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/pathways", response_model=List[CareerPathwaySchema], tags=["Pathways"])
def list_career_pathways(
    stream: Optional[str] = Query(None, description="Filter by A/L stream (e.g. 'Physical Science')"),
    degree_area: Optional[str] = Query(None, description="Filter by degree area")
):
    """Retrieve all available career pathways from the verified Sri Lankan knowledge base."""
    pathways = load_pathways_kb()
    if stream:
        pathways = [p for p in pathways if p["stream"].lower() == stream.lower()]
    if degree_area:
        pathways = [p for p in pathways if degree_area.lower() in p["degree_area"].lower()]
    return pathways


@router.get("/pathways/{pathway_id}", response_model=CareerPathwaySchema, tags=["Pathways"])
def get_career_pathway_by_id(pathway_id: str):
    """Retrieve details of a single career pathway by ID."""
    pathways = load_pathways_kb()
    for p in pathways:
        if p["pathway_id"] == pathway_id:
            return p
    raise HTTPException(status_code=404, detail=f"Pathway with ID '{pathway_id}' not found.")
