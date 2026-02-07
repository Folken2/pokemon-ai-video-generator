"""
Step 01: Species Research
Uses LLM to generate a biological profile from Pokédex lore.
Input: Pokemon name
Output: 01_research.md
"""

from backend.models import StepName
from backend.pipeline.base import PipelineStep


class ResearchStep(PipelineStep):
    step_name = StepName.RESEARCH
    requires_llm = True

    def execute(self) -> bool:
        pokemon = self.state.pokemon_name
        self.log(f"Researching {pokemon}...")

        # Load SOP 01 prompt
        system_prompt = self.load_sop_prompt("1_research.md")

        # Remove the saving instructions (we handle file saving ourselves)
        if "## Saving Instructions" in system_prompt:
            system_prompt = system_prompt[:system_prompt.index("## Saving Instructions")].strip()

        user_message = f"Target Pokémon: {pokemon}"

        # Call LLM
        self.log("Calling Claude for species research...")
        result = self.llm.generate_with_continuation(
            system_prompt=system_prompt,
            user_message=user_message,
        )

        if not result:
            self.log("LLM returned empty response", level="error")
            return False

        # Save output
        self.write_file("01_research.md", result)
        self.step_state.output = result
        self.log(f"Research complete: {len(result)} characters")
        return True
