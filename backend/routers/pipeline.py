"""
Pipeline execution REST endpoints.
Handles running steps, approving outputs, and retrying failures.
"""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, HTTPException

from backend.models import ApproveStepRequest, RegenerateAssetRequest, RetryStepRequest, RunStepRequest, StepName, StepStatus

router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])

# Thread pool for running pipeline steps (they're synchronous/blocking)
_executor = ThreadPoolExecutor(max_workers=2)


@router.post("/{subject_name}/run")
async def run_step(subject_name: str, request: RunStepRequest) -> dict:
    """
    Run a specific pipeline step.
    Executes in a background thread to avoid blocking the server.
    """
    from backend.pipeline.orchestrator import PipelineOrchestrator

    orchestrator = PipelineOrchestrator(subject_name)
    step_state = orchestrator.state.get_step(request.step)

    if step_state.status == StepStatus.RUNNING:
        raise HTTPException(status_code=409, detail="Step is already running")

    # Run in background thread (LLM calls and API calls are blocking)
    loop = asyncio.get_event_loop()

    def _run():
        return orchestrator.run_step(request.step)

    result = await loop.run_in_executor(_executor, _run)

    # Reload state after execution
    orchestrator = PipelineOrchestrator(subject_name)
    state = orchestrator.get_state()
    step = state.get_step(request.step)

    return {
        "success": result,
        "step": request.step,
        "status": step.status,
        "output": step.output[:2000] if step.output else "",  # Truncate for response
        "logs": step.logs[-20:],  # Last 20 log entries
        "error": step.error,
    }


@router.post("/{subject_name}/approve")
async def approve_step(subject_name: str, request: ApproveStepRequest) -> dict:
    """
    Approve a step's output and optionally provide feedback.
    For story_options step, include selected_option (1-5).
    For asset_generation Phase 1, triggers Phase 2 execution.
    """
    from backend.pipeline.orchestrator import PipelineOrchestrator

    orchestrator = PipelineOrchestrator(subject_name)
    step_state = orchestrator.state.get_step(request.step)

    if step_state.status != StepStatus.AWAITING_APPROVAL:
        raise HTTPException(
            status_code=400,
            detail=f"Step {request.step} is not awaiting approval (status: {step_state.status})",
        )

    # For asset generation Phase 1, run Phase 2 in background
    if request.step == StepName.ASSET_GENERATION:
        phase = step_state.metadata.get("phase", 1)
        if phase == 1:
            loop = asyncio.get_event_loop()

            def _approve_and_run_phase2():
                return orchestrator.approve_step(request)

            result = await loop.run_in_executor(_executor, _approve_and_run_phase2)
            orchestrator = PipelineOrchestrator(subject_name)
            step = orchestrator.state.get_step(request.step)

            return {
                "success": result,
                "step": request.step,
                "status": step.status,
                "message": "Phase 1 approved, Phase 2 running...",
                "output": step.output[:2000] if step.output else "",
            }

    result = orchestrator.approve_step(request)

    # Reload state
    orchestrator = PipelineOrchestrator(subject_name)
    state = orchestrator.get_state()

    return {
        "success": result,
        "step": request.step,
        "status": state.get_step(request.step).status,
        "next_step": state.current_step,
    }


@router.post("/{subject_name}/regenerate-asset")
async def regenerate_asset(subject_name: str, request: RegenerateAssetRequest) -> dict:
    """
    Regenerate a single asset image with user feedback.
    Only valid during asset_generation step while awaiting approval (Phase 1).
    """
    from backend.pipeline.orchestrator import PipelineOrchestrator
    from backend.pipeline.s04_asset_generation import AssetGenerationStep

    orchestrator = PipelineOrchestrator(subject_name)
    step_state = orchestrator.state.get_step(request.step)

    if request.step != StepName.ASSET_GENERATION:
        raise HTTPException(status_code=400, detail="Regeneration only supported for asset_generation step")

    if step_state.status != StepStatus.AWAITING_APPROVAL:
        raise HTTPException(status_code=400, detail="Step is not awaiting approval")

    if step_state.metadata.get("phase", 1) != 1:
        raise HTTPException(status_code=400, detail="Regeneration only available during Phase 1")

    asset_step = AssetGenerationStep(
        state=orchestrator.state,
        project_dir=orchestrator.project_dir,
    )

    loop = asyncio.get_event_loop()

    def _regenerate():
        return asset_step.regenerate_asset(request.asset_filename, request.feedback)

    result = await loop.run_in_executor(_executor, _regenerate)

    return {
        "success": result,
        "asset_filename": request.asset_filename,
        "message": f"{'Regenerated' if result else 'Failed to regenerate'} {request.asset_filename}",
    }


@router.post("/{subject_name}/retry")
async def retry_step(subject_name: str, request: RetryStepRequest) -> dict:
    """Retry a failed step."""
    from backend.pipeline.orchestrator import PipelineOrchestrator

    orchestrator = PipelineOrchestrator(subject_name)

    loop = asyncio.get_event_loop()

    def _retry():
        return orchestrator.retry_step(request.step)

    result = await loop.run_in_executor(_executor, _retry)

    orchestrator = PipelineOrchestrator(subject_name)
    step = orchestrator.state.get_step(request.step)

    return {
        "success": result,
        "step": request.step,
        "status": step.status,
        "output": step.output[:2000] if step.output else "",
        "error": step.error,
    }


@router.get("/{subject_name}/status")
async def get_pipeline_status(subject_name: str) -> dict:
    """Get current pipeline status and all step states."""
    from backend.pipeline.orchestrator import PipelineOrchestrator

    orchestrator = PipelineOrchestrator(subject_name)
    state = orchestrator.get_state()
    next_step = orchestrator.get_next_step()

    return {
        "subject_name": state.subject_name,
        "theme": state.theme,
        "current_step": state.current_step,
        "next_step": next_step,
        "steps": {
            name: {
                "display_name": step.display_name,
                "status": step.status,
                "has_output": bool(step.output),
                "artifact_count": len(step.artifacts),
                "error": step.error,
                "log_count": len(step.logs),
            }
            for name, step in state.steps.items()
        },
    }


@router.get("/{subject_name}/step/{step_name}")
async def get_step_detail(subject_name: str, step_name: str) -> dict:
    """Get detailed state for a specific step including output and logs."""
    from backend.pipeline.orchestrator import PipelineOrchestrator

    try:
        step = StepName(step_name)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid step: {step_name}")

    orchestrator = PipelineOrchestrator(subject_name)
    state = orchestrator.get_state()
    step_state = state.get_step(step)
    artifacts = orchestrator.get_artifacts(step)

    return {
        "name": step_state.name,
        "display_name": step_state.display_name,
        "status": step_state.status,
        "output": step_state.output,
        "artifacts": artifacts,
        "logs": step_state.logs,
        "error": step_state.error,
        "metadata": step_state.metadata,
        "started_at": step_state.started_at,
        "completed_at": step_state.completed_at,
    }
