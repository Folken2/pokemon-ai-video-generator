"""
Project management REST endpoints.
Handles creating, listing, and managing Pokemon documentary projects.
"""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.config import PROJECT_ROOT, validate_api_keys
from backend.models import (
    CreateProjectRequest,
    PipelineState,
    ProjectSummary,
    StepStatus,
)

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/")
async def list_projects() -> list[dict]:
    """List all existing Pokemon projects."""
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
                        "pokemon_name": state.pokemon_name,
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
    """Create a new Pokemon documentary project."""
    pokemon = request.pokemon_name.lower().strip()
    if not pokemon:
        raise HTTPException(status_code=400, detail="Pokemon name required")

    from backend.pipeline.orchestrator import PipelineOrchestrator
    orchestrator = PipelineOrchestrator(pokemon)
    state = orchestrator.get_state()

    return {
        "pokemon_name": state.pokemon_name,
        "current_step": state.current_step,
        "message": f"Project created for {pokemon}",
    }


@router.get("/{pokemon_name}")
async def get_project(pokemon_name: str) -> dict:
    """Get full project state."""
    from backend.pipeline.orchestrator import PipelineOrchestrator
    orchestrator = PipelineOrchestrator(pokemon_name)
    state = orchestrator.get_state()

    return state.model_dump()


@router.get("/{pokemon_name}/artifacts/{step_name}")
async def get_step_artifacts(pokemon_name: str, step_name: str) -> list[dict]:
    """Get artifacts (generated files) for a specific step."""
    from backend.models import StepName
    from backend.pipeline.orchestrator import PipelineOrchestrator

    try:
        step = StepName(step_name)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid step: {step_name}")

    orchestrator = PipelineOrchestrator(pokemon_name)
    return orchestrator.get_artifacts(step)


@router.get("/config/api-keys")
async def check_api_keys() -> dict:
    """Check which API keys are configured."""
    return validate_api_keys()
