"""
Step 03: Asset Planning
Uses LLM to create the asset manifest with generation prompts.
Input: 01_research.md + 02_story_script.md
Output: 03_assets.md
"""

from backend.models import StepName
from backend.pipeline.base import PipelineStep


class AssetPlanningStep(PipelineStep):
    step_name = StepName.ASSET_PLANNING
    requires_llm = True

    def execute(self) -> bool:
        pokemon = self.state.pokemon_name

        # Load prerequisites
        research = self.read_file("01_research.md")
        script = self.read_file("02_story_script.md")

        if not research:
            self.log("Missing 01_research.md", level="error")
            return False
        if not script:
            self.log("Missing 02_story_script.md", level="error")
            return False

        # Load SOP 03 prompt (asset planning guide)
        system_prompt = self.load_sop_prompt("3_character_generation.md")

        if "## Saving Instructions" in system_prompt:
            system_prompt = system_prompt[:system_prompt.index("## Saving Instructions")].strip()

        user_message = f"""Species Profile (SOP 01):

{research}

---

Production Script (SOP 02):

{script}

---

Create the complete Asset Manifest for {pokemon} including:
1. Part 1: The Manifest (cast + props list)
2. Part 2: Clip-to-Asset Mapping Table
3. Part 3: The Global Atmosphere Block
4. Part 4: Master Prompts (all code blocks with [CORE] markers and suggested filenames)"""

        self.log("Generating asset manifest (this may take a while)...")
        result = self.llm.generate_with_continuation(
            system_prompt=system_prompt,
            user_message=user_message,
            max_continuations=5,  # Asset manifests can be very long
        )

        if not result:
            self.log("LLM returned empty response", level="error")
            return False

        # Save output
        self.write_file("03_assets.md", result)
        self.step_state.output = result
        self.log(f"Asset manifest generated: {len(result)} characters")
        return True
