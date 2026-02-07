"""
Base pipeline step class.
All pipeline steps inherit from this for consistent logging, error handling, and state management.
"""

from __future__ import annotations

import traceback
from pathlib import Path
from typing import TYPE_CHECKING

from backend.models import PipelineState, StepName, StepStatus
from backend.utils.logging_config import logger

if TYPE_CHECKING:
    from backend.services.llm_service import LLMService


class PipelineStep:
    """Base class for all pipeline steps."""

    step_name: StepName  # Must be set by subclass
    requires_llm: bool = False

    def __init__(self, state: PipelineState, project_dir: Path, llm: LLMService | None = None):
        self.state = state
        self.project_dir = project_dir
        self.llm = llm

    @property
    def step_state(self):
        return self.state.get_step(self.step_name)

    def log(self, message: str, level: str = "info") -> None:
        """Add a log message to the step and the global logger."""
        self.state.add_log(self.step_name, message)
        getattr(logger, level, logger.info)(f"[{self.step_name.value}] {message}")

    def run(self) -> bool:
        """Execute the step. Returns True if successful."""
        self.state.set_step_status(self.step_name, StepStatus.RUNNING)
        self.log(f"Starting {self.step_name.value}...")

        try:
            result = self.execute()

            if result:
                self.state.set_step_status(self.step_name, StepStatus.AWAITING_APPROVAL)
                self.log("Completed, awaiting approval.", level="info")
            else:
                self.state.set_step_status(self.step_name, StepStatus.FAILED)
                self.log("Step failed.", level="error")

            self.state.save(self.project_dir)
            return result

        except Exception as e:
            self.state.set_step_status(self.step_name, StepStatus.FAILED)
            self.step_state.error = str(e)
            self.log(f"Exception: {e}", level="error")
            logger.error(traceback.format_exc())
            self.state.save(self.project_dir)
            return False

    def execute(self) -> bool:
        """Override in subclass. Actual step logic."""
        raise NotImplementedError

    def read_file(self, relative_path: str) -> str | None:
        """Read a file from the project directory."""
        path = self.project_dir / relative_path
        if path.exists():
            return path.read_text()
        self.log(f"File not found: {relative_path}", level="warning")
        return None

    def write_file(self, relative_path: str, content: str) -> Path:
        """Write content to a file in the project directory."""
        path = self.project_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        self.step_state.artifacts.append(str(relative_path))
        self.log(f"Wrote {relative_path}")
        return path

    def load_sop_prompt(self, prompt_filename: str) -> str:
        """Load an SOP prompt template from the prompts/ directory."""
        from backend.config import PROMPTS_DIR
        path = PROMPTS_DIR / prompt_filename
        if path.exists():
            return path.read_text()
        raise FileNotFoundError(f"SOP prompt not found: {path}")
