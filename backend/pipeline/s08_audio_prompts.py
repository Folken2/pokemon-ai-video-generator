"""
Step 08: Audio/Narration Prompt Engineering
Uses LLM to create the narration text table from the production script.
Input: 02_story_script.md
Output: 05_audio_generation.md
"""

from backend.models import StepName
from backend.pipeline.base import PipelineStep


class AudioPromptsStep(PipelineStep):
    step_name = StepName.AUDIO_PROMPTS
    requires_llm = True

    def execute(self) -> bool:
        pokemon = self.state.pokemon_name

        # Load the production script
        script = self.read_file("02_story_script.md")
        if not script:
            self.log("Missing 02_story_script.md", level="error")
            return False

        # Load SOP 05 prompt
        system_prompt = self.load_sop_prompt("5_voice_prompt_engineer.md")

        if "## Saving Instructions" in system_prompt:
            system_prompt = system_prompt[:system_prompt.index("## Saving Instructions")].strip()

        user_message = f"""Production Script (SOP 02):

{script}

---

Create the Audio Generation Table for {pokemon}. For each scene:
1. Extract the narration text
2. Count words and punctuation marks
3. Calculate duration using the formula: Duration = (words / 2) + (total_punctuation * 2) + 1
4. Verify each narration line is exactly 8 seconds
5. Adjust text if needed to hit the 8-second target"""

        self.log("Generating narration text table...")
        result = self.llm.generate(
            system_prompt=system_prompt,
            user_message=user_message,
        )

        if not result:
            self.log("LLM returned empty response", level="error")
            return False

        self.write_file("05_audio_generation.md", result)
        self.step_state.output = result
        self.log(f"Audio prompts generated: {len(result)} characters")
        return True
