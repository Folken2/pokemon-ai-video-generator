"""
Step 10: Sound Effects Prompt Engineering
Uses LLM to create per-clip sound effect prompts.
Input: 02_story_script.md
Output: 06_sound_effects_prompts.md
"""

from backend.models import StepName
from backend.pipeline.base import PipelineStep


class SFXPromptsStep(PipelineStep):
    step_name = StepName.SFX_PROMPTS
    requires_llm = True

    def execute(self) -> bool:
        subject = self.state.subject_name

        # Load the production script
        script = self.read_file("02_story_script.md")
        if not script:
            self.log("Missing 02_story_script.md", level="error")
            return False

        # Load SOP 06 prompt
        system_prompt = self.load_sop_prompt("6_sound_effects_prompt_engineering.md")

        if "## Saving Instructions" in system_prompt:
            system_prompt = system_prompt[:system_prompt.index("## Saving Instructions")].strip()

        user_message = f"""Production Script:

{script}

---

Subject: {subject}

Create the Sound Effects Prompt Table with a unique 30-50 word prompt for each clip.
Each prompt must:
1. Start with "Continuous [environment] ambience with..."
2. Include 3-4 continuous ambient sounds
3. Add action sounds on top
4. End with "subtle nature documentary sound effect"
"""

        self.log("Generating sound effects prompts...")
        result = self.llm.generate(
            system_prompt=system_prompt,
            user_message=user_message,
        )

        if not result:
            self.log("LLM returned empty response", level="error")
            return False

        self.write_file("06_sound_effects_prompts.md", result)
        self.step_state.output = result
        self.log(f"SFX prompts generated: {len(result)} characters")
        return True
