"""
Pipeline Orchestrator
State machine that manages the lifecycle of a Pokemon documentary project.
Handles step execution, approval gates, and state transitions.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.config import get_project_dir
from backend.models import (
    APPROVAL_STEPS,
    LLM_STEPS,
    STEP_ORDER,
    ApproveStepRequest,
    PipelineState,
    StepName,
    StepStatus,
)
from backend.pipeline.base import PipelineStep
from backend.pipeline.s01_research import ResearchStep
from backend.pipeline.s02_story import StoryOptionsStep, StoryScriptStep
from backend.pipeline.s03_asset_planning import AssetPlanningStep
from backend.pipeline.s04_asset_generation import AssetGenerationStep
from backend.pipeline.s05_composite_generation import CompositeGenerationStep
from backend.pipeline.s06_video_prompts import VideoPromptsStep
from backend.pipeline.s07_video_generation import VideoGenerationStep
from backend.pipeline.s08_audio_prompts import AudioPromptsStep
from backend.pipeline.s09_audio_generation import AudioGenerationStep
from backend.pipeline.s10_sfx_prompts import SFXPromptsStep
from backend.pipeline.s11_sfx_generation import SFXGenerationStep
from backend.pipeline.s12_assembly import FinalAssemblyStep
from backend.services.llm_service import LLMService
from backend.utils.logging_config import logger


# Step name -> Step class mapping
STEP_CLASSES: dict[StepName, type[PipelineStep]] = {
    StepName.RESEARCH: ResearchStep,
    StepName.STORY_OPTIONS: StoryOptionsStep,
    StepName.STORY_SCRIPT: StoryScriptStep,
    StepName.ASSET_PLANNING: AssetPlanningStep,
    StepName.ASSET_GENERATION: AssetGenerationStep,
    StepName.COMPOSITE_GENERATION: CompositeGenerationStep,
    StepName.VIDEO_PROMPTS: VideoPromptsStep,
    StepName.VIDEO_GENERATION: VideoGenerationStep,
    StepName.AUDIO_PROMPTS: AudioPromptsStep,
    StepName.AUDIO_GENERATION: AudioGenerationStep,
    StepName.SFX_PROMPTS: SFXPromptsStep,
    StepName.SFX_GENERATION: SFXGenerationStep,
    StepName.FINAL_ASSEMBLY: FinalAssemblyStep,
}


class PipelineOrchestrator:
    """Manages the lifecycle of a Pokemon documentary project."""

    def __init__(self, pokemon_name: str):
        self.pokemon_name = pokemon_name.lower().strip()
        self.project_dir = get_project_dir(self.pokemon_name)
        self.state = self._load_or_create_state()
        self._llm: LLMService | None = None

    @property
    def llm(self) -> LLMService:
        if self._llm is None:
            self._llm = LLMService()
        return self._llm

    def _load_or_create_state(self) -> PipelineState:
        """Load existing state or create new."""
        existing = PipelineState.load(self.project_dir)
        if existing:
            logger.info(f"Loaded existing state for {self.pokemon_name} (step: {existing.current_step})")
            return existing

        state = PipelineState(pokemon_name=self.pokemon_name)
        self.project_dir.mkdir(parents=True, exist_ok=True)
        state.save(self.project_dir)
        logger.info(f"Created new project for {self.pokemon_name}")
        return state

    def get_state(self) -> PipelineState:
        """Get current pipeline state."""
        return self.state

    def run_step(self, step_name: StepName) -> bool:
        """
        Execute a specific pipeline step.
        Returns True if step completed successfully.
        """
        step_state = self.state.get_step(step_name)

        # Validate step can run
        if step_state.status == StepStatus.RUNNING:
            logger.warning(f"Step {step_name} is already running")
            return False

        # Check prerequisites
        step_index = STEP_ORDER.index(step_name)
        if step_index > 0:
            prev_step = STEP_ORDER[step_index - 1]
            prev_status = self.state.get_step(prev_step).status
            if prev_status not in (StepStatus.APPROVED, StepStatus.SKIPPED):
                # Special case: story_script depends on story_options approval
                if step_name == StepName.STORY_SCRIPT and prev_status != StepStatus.APPROVED:
                    logger.warning(f"Cannot run {step_name}: previous step {prev_step} not approved")
                    return False

        # Instantiate and run the step
        step_cls = STEP_CLASSES.get(step_name)
        if not step_cls:
            logger.error(f"No step class for {step_name}")
            return False

        llm = self.llm if step_name in LLM_STEPS else None
        step = step_cls(self.state, self.project_dir, llm)

        logger.info(f"Running step: {step_name}")
        result = step.run()

        # Update current step pointer
        if result:
            self.state.current_step = step_name
        self.state.save(self.project_dir)

        return result

    def approve_step(self, request: ApproveStepRequest) -> bool:
        """
        Approve a step's output, allowing the pipeline to proceed.
        Handles special cases like story selection.
        """
        step_name = request.step
        step_state = self.state.get_step(step_name)

        if step_state.status != StepStatus.AWAITING_APPROVAL:
            logger.warning(f"Step {step_name} is not awaiting approval (status: {step_state.status})")
            return False

        # Handle special cases
        if step_name == StepName.STORY_OPTIONS:
            if request.selected_option is None:
                logger.warning("Story options approval requires selected_option")
                return False
            step_state.metadata["selected_option"] = request.selected_option
            step_state.metadata["user_feedback"] = request.feedback

        if step_name == StepName.ASSET_GENERATION:
            # Check if this is Phase 1 approval (need to run Phase 2)
            phase = step_state.metadata.get("phase", 1)
            if phase == 1:
                step_state.metadata["phase1_approved"] = True
                # Run Phase 2
                logger.info("Phase 1 approved, running Phase 2...")
                step_cls = STEP_CLASSES[step_name]
                step = step_cls(self.state, self.project_dir)
                step.execute_phase2()
                # Still awaiting approval for Phase 2
                self.state.save(self.project_dir)
                return True

        # Mark as approved
        self.state.set_step_status(step_name, StepStatus.APPROVED)

        # Store any feedback
        if request.feedback:
            step_state.metadata["user_feedback"] = request.feedback

        # Advance current step
        step_index = STEP_ORDER.index(step_name)
        if step_index < len(STEP_ORDER) - 1:
            self.state.current_step = STEP_ORDER[step_index + 1]

        self.state.save(self.project_dir)
        logger.info(f"Step {step_name} approved")
        return True

    def retry_step(self, step_name: StepName) -> bool:
        """Reset a failed step and re-run it."""
        step_state = self.state.get_step(step_name)
        step_state.status = StepStatus.PENDING
        step_state.error = None
        step_state.logs = []
        step_state.output = ""
        step_state.artifacts = []
        self.state.save(self.project_dir)

        return self.run_step(step_name)

    def get_next_step(self) -> StepName | None:
        """Get the next step that should be run."""
        for step_name in STEP_ORDER:
            step = self.state.get_step(step_name)
            if step.status == StepStatus.PENDING:
                return step_name
            if step.status == StepStatus.AWAITING_APPROVAL:
                return None  # Waiting for human
            if step.status == StepStatus.FAILED:
                return step_name  # Retry
        return None  # All done

    def get_artifacts(self, step_name: StepName) -> list[dict]:
        """Get artifact info for a step (file paths, sizes, types)."""
        step = self.state.get_step(step_name)
        artifacts = []
        for rel_path in step.artifacts:
            full_path = self.project_dir / rel_path
            if full_path.exists():
                suffix = full_path.suffix.lower()
                file_type = "image" if suffix in (".png", ".jpg") else \
                           "video" if suffix in (".mp4", ".mov") else \
                           "audio" if suffix in (".mp3", ".wav") else "file"
                artifacts.append({
                    "path": rel_path,
                    "full_path": str(full_path),
                    "type": file_type,
                    "size": full_path.stat().st_size,
                })
        return artifacts
