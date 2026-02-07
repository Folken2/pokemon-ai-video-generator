"""
Step 06: Video Prompt Engineering
Uses LLM to create Kling 2.5 shot list with motion prompts.
Input: 02_story_script.md + 03_assets.md
Output: 04_video_prompts.md
"""

from backend.models import StepName
from backend.pipeline.base import PipelineStep


class VideoPromptsStep(PipelineStep):
    step_name = StepName.VIDEO_PROMPTS
    requires_llm = True

    def execute(self) -> bool:
        pokemon = self.state.pokemon_name

        # Load prerequisites
        script = self.read_file("02_story_script.md")
        assets = self.read_file("03_assets.md")

        if not script:
            self.log("Missing 02_story_script.md", level="error")
            return False
        if not assets:
            self.log("Missing 03_assets.md", level="error")
            return False

        # Load SOP 04 prompt
        system_prompt = self.load_sop_prompt("4_video_prompt_engineering.md")

        if "## Saving Instructions" in system_prompt:
            system_prompt = system_prompt[:system_prompt.index("## Saving Instructions")].strip()

        user_message = f"""Production Script (SOP 02):

{script}

---

Asset Manifest (SOP 03):

{assets}

---

Generate the complete Kling 2.5 Shot List for {pokemon}. Include:
- Character Asset column (specific .png filename)
- Motion + Context Prompt column (action-first, camera-last)
- Notes column (action shots, two-character scenes, etc.)"""

        self.log("Generating video shot list...")
        result = self.llm.generate_with_continuation(
            system_prompt=system_prompt,
            user_message=user_message,
        )

        if not result:
            self.log("LLM returned empty response", level="error")
            return False

        self.write_file("04_video_prompts.md", result)
        self.step_state.output = result
        self.log(f"Video prompts generated: {len(result)} characters")
        return True
