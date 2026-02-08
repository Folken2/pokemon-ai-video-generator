"""
Project management REST endpoints.
Handles creating, listing, and managing documentary projects.
"""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.config import PROJECT_ROOT, validate_api_keys
from backend.models import (
    AVAILABLE_THEMES,
    CreateProjectRequest,
    PipelineState,
    ProjectSummary,
    StepStatus,
)
from backend.services.subject_catalog import search_subjects

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/")
async def list_projects() -> list[dict]:
    """List all existing projects."""
    projects = []
    for path in sorted(PROJECT_ROOT.iterdir()):
        state_file = path / "pipeline_state.json"
        if path.is_dir() and state_file.exists():
            try:
                state = PipelineState.load(path)
                if state:
                    # Count completed steps
                    total = len(state.steps)
                    completed = sum(
                        1 for s in state.steps.values()
                        if s.status in (StepStatus.APPROVED, StepStatus.SKIPPED)
                    )
                    projects.append({
                        "subject_name": state.subject_name,
                        "theme": state.theme,
                        "current_step": state.current_step,
                        "progress": f"{completed}/{total}",
                        "created_at": state.created_at,
                        "updated_at": state.updated_at,
                    })
            except Exception:
                continue
    return projects


@router.post("/")
async def create_project(request: CreateProjectRequest) -> dict:
    """Create a new documentary project."""
    subject = request.subject_name.lower().strip()
    if not subject:
        raise HTTPException(status_code=400, detail="Subject name required")

    theme = request.theme
    if theme not in AVAILABLE_THEMES:
        raise HTTPException(status_code=400, detail=f"Invalid theme: {theme}. Must be one of: {AVAILABLE_THEMES}")

    from backend.pipeline.orchestrator import PipelineOrchestrator
    orchestrator = PipelineOrchestrator(subject, theme=theme)
    state = orchestrator.get_state()

    return {
        "subject_name": state.subject_name,
        "theme": state.theme,
        "current_step": state.current_step,
        "message": f"Project created for {subject} ({theme})",
    }


# Static routes MUST be defined before path parameter routes
@router.get("/themes")
async def list_themes() -> list[str]:
    """List available documentary themes."""
    return AVAILABLE_THEMES


@router.get("/subjects/{theme}")
async def list_subjects(theme: str, q: str = "") -> list[dict]:
    """List curated subjects for a theme, optionally filtered by query."""
    if theme not in AVAILABLE_THEMES:
        raise HTTPException(status_code=400, detail=f"Invalid theme: {theme}")
    return search_subjects(theme, q)


@router.get("/config/api-keys")
async def check_api_keys() -> dict:
    """Check which API keys are configured."""
    return validate_api_keys()


# Path parameter routes below
@router.get("/{subject_name}")
async def get_project(subject_name: str) -> dict:
    """Get full project state."""
    from backend.pipeline.orchestrator import PipelineOrchestrator
    orchestrator = PipelineOrchestrator(subject_name)
    state = orchestrator.get_state()

    return state.model_dump()


@router.get("/{subject_name}/artifacts/{step_name}")
async def get_step_artifacts(subject_name: str, step_name: str) -> list[dict]:
    """Get artifacts (generated files) for a specific step."""
    from backend.models import StepName
    from backend.pipeline.orchestrator import PipelineOrchestrator

    try:
        step = StepName(step_name)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid step: {step_name}")

    orchestrator = PipelineOrchestrator(subject_name)
    return orchestrator.get_artifacts(step)
