"""
Pydantic models for the Pokemon Documentary Pipeline.
Defines data structures for pipeline state, steps, and API requests/responses.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


# --- Enums ---

class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    FAILED = "failed"
    SKIPPED = "skipped"


class StepName(str, Enum):
    RESEARCH = "research"
    STORY_OPTIONS = "story_options"
    STORY_SCRIPT = "story_script"
    ASSET_PLANNING = "asset_planning"
    ASSET_GENERATION = "asset_generation"
    COMPOSITE_GENERATION = "composite_generation"
    VIDEO_PROMPTS = "video_prompts"
    VIDEO_GENERATION = "video_generation"
    AUDIO_PROMPTS = "audio_prompts"
    AUDIO_GENERATION = "audio_generation"
    SFX_PROMPTS = "sfx_prompts"
    SFX_GENERATION = "sfx_generation"
    FINAL_ASSEMBLY = "final_assembly"


STEP_ORDER = list(StepName)

STEP_DISPLAY_NAMES = {
    StepName.RESEARCH: "Species Research",
    StepName.STORY_OPTIONS: "Story Options",
    StepName.STORY_SCRIPT: "Production Script",
    StepName.ASSET_PLANNING: "Asset Planning",
    StepName.ASSET_GENERATION: "Asset Generation",
    StepName.COMPOSITE_GENERATION: "Composite Generation",
    StepName.VIDEO_PROMPTS: "Video Prompts",
    StepName.VIDEO_GENERATION: "Video Generation",
    StepName.AUDIO_PROMPTS: "Narration Prompts",
    StepName.AUDIO_GENERATION: "Narration Generation",
    StepName.SFX_PROMPTS: "Sound Effects Prompts",
    StepName.SFX_GENERATION: "Sound Effects Generation",
    StepName.FINAL_ASSEMBLY: "Final Assembly",
}

# Steps that require LLM generation
LLM_STEPS = {
    StepName.RESEARCH,
    StepName.STORY_OPTIONS,
    StepName.STORY_SCRIPT,
    StepName.ASSET_PLANNING,
    StepName.VIDEO_PROMPTS,
    StepName.AUDIO_PROMPTS,
    StepName.SFX_PROMPTS,
}

# Steps that require human approval before proceeding
APPROVAL_STEPS = {
    StepName.RESEARCH,
    StepName.STORY_OPTIONS,  # User selects a story
    StepName.STORY_SCRIPT,
    StepName.ASSET_PLANNING,
    StepName.ASSET_GENERATION,
    StepName.COMPOSITE_GENERATION,
    StepName.VIDEO_PROMPTS,
    StepName.VIDEO_GENERATION,
    StepName.AUDIO_PROMPTS,
    StepName.AUDIO_GENERATION,
    StepName.SFX_PROMPTS,
    StepName.SFX_GENERATION,
}


# --- Step State ---

class StepState(BaseModel):
    name: StepName
    display_name: str = ""
    status: StepStatus = StepStatus.PENDING
    output: str = ""  # Markdown output / LLM response
    artifacts: list[str] = Field(default_factory=list)  # Generated file paths
    logs: list[str] = Field(default_factory=list)
    error: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)  # Step-specific data

    def model_post_init(self, __context: Any) -> None:
        if not self.display_name:
            self.display_name = STEP_DISPLAY_NAMES.get(self.name, self.name.value)


# --- Pipeline State ---

class PipelineState(BaseModel):
    pokemon_name: str
    current_step: StepName = StepName.RESEARCH
    steps: dict[str, StepState] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def model_post_init(self, __context: Any) -> None:
        # Initialize all steps if empty
        if not self.steps:
            for step_name in STEP_ORDER:
                self.steps[step_name.value] = StepState(name=step_name)

    def get_step(self, name: StepName) -> StepState:
        return self.steps[name.value]

    def set_step_status(self, name: StepName, status: StepStatus) -> None:
        step = self.get_step(name)
        step.status = status
        if status == StepStatus.RUNNING:
            step.started_at = datetime.now(timezone.utc).isoformat()
        elif status in (StepStatus.AWAITING_APPROVAL, StepStatus.APPROVED, StepStatus.FAILED):
            step.completed_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def add_log(self, name: StepName, message: str) -> None:
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        self.get_step(name).logs.append(f"[{ts}] {message}")

    def save(self, project_dir: Path) -> None:
        state_file = project_dir / "pipeline_state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(self.model_dump_json(indent=2))

    @classmethod
    def load(cls, project_dir: Path) -> PipelineState | None:
        state_file = project_dir / "pipeline_state.json"
        if state_file.exists():
            data = json.loads(state_file.read_text())
            return cls(**data)
        return None


# --- API Request/Response Models ---

class CreateProjectRequest(BaseModel):
    pokemon_name: str


class RunStepRequest(BaseModel):
    step: StepName


class ApproveStepRequest(BaseModel):
    step: StepName
    feedback: str = ""  # Optional user feedback/edits
    selected_option: int | None = None  # For story selection step


class RetryStepRequest(BaseModel):
    step: StepName


class ProjectSummary(BaseModel):
    pokemon_name: str
    current_step: StepName
    status: str  # Overall project status description
    steps: dict[str, StepState]
    created_at: str
    updated_at: str


class LogMessage(BaseModel):
    step: str
    message: str
    timestamp: str
    level: str = "info"  # info, warning, error, success
