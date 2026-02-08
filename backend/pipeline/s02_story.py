"""
Step 02: Story Development
Phase 1: Generate 5 story options (awaits user selection)
Phase 2: Generate full production script from selected option
Input: 01_research.md + subject name
Output: Story options (phase 1), then 02_story_script.md (phase 2)
"""

from backend.models import StepName
from backend.pipeline.base import PipelineStep


class StoryOptionsStep(PipelineStep):
    """Phase 1: Generate 5 story options for user to choose from."""
    step_name = StepName.STORY_OPTIONS
    requires_llm = True

    def execute(self) -> bool:
        subject = self.state.subject_name

        # Load research
        research = self.read_file("01_research.md")
        if not research:
            self.log("Missing 01_research.md - run research step first", level="error")
            return False

        # Load SOP 02 prompt (Phase 1 only - up to "STOP HERE")
        full_prompt = self.load_sop_prompt("2_story_generator.md")

        # Extract just Phase 1 (concept development) by stopping at the script section
        # The SOP says "STOP HERE. Do not write the script yet."
        if "SOP 02.5: Production Scripting" in full_prompt:
            phase1_prompt = full_prompt[:full_prompt.index("SOP 02.5: Production Scripting")].strip()
        else:
            phase1_prompt = full_prompt

        if "## Saving Instructions" in phase1_prompt:
            phase1_prompt = phase1_prompt[:phase1_prompt.index("## Saving Instructions")].strip()

        user_message = f"""Species Profile for {subject}:

{research}

Generate 5 story options for a 90-second nature documentary about {subject}."""

        self.log("Generating 5 story options...")
        result = self.llm.generate_with_continuation(
            system_prompt=phase1_prompt,
            user_message=user_message,
        )

        if not result:
            self.log("LLM returned empty response", level="error")
            return False

        self.step_state.output = result
        self.step_state.metadata["story_options_raw"] = result
        self.log("Story options generated. User must select one.")
        return True


class StoryScriptStep(PipelineStep):
    """Phase 2: Generate full production script from selected story option."""
    step_name = StepName.STORY_SCRIPT
    requires_llm = True

    def execute(self) -> bool:
        subject = self.state.subject_name

        # Get the selected option from story_options step metadata
        options_step = self.state.get_step(StepName.STORY_OPTIONS)
        selected_option = options_step.metadata.get("selected_option")
        story_options_raw = options_step.metadata.get("story_options_raw", "")
        user_feedback = options_step.metadata.get("user_feedback", "")

        if selected_option is None:
            self.log("No story option selected", level="error")
            return False

        # Load research
        research = self.read_file("01_research.md")
        if not research:
            self.log("Missing 01_research.md", level="error")
            return False

        # Load the scripting section of SOP 02
        full_prompt = self.load_sop_prompt("2_story_generator.md")

        # Extract Phase 2 (scripting) prompt
        if "SOP 02.5: Production Scripting" in full_prompt:
            script_prompt = full_prompt[full_prompt.index("SOP 02.5: Production Scripting"):]
        else:
            script_prompt = full_prompt

        if "## Saving Instructions" in script_prompt:
            script_prompt = script_prompt[:script_prompt.index("## Saving Instructions")].strip()

        user_message = f"""Species Profile for {subject}:

{research}

Story Options Previously Generated:
{story_options_raw}

Selected Option: Option {selected_option}
{f"User feedback: {user_feedback}" if user_feedback else ""}

Generate the full production script for Option {selected_option}. Create exactly 18 scenes, each with 8-second narration."""

        self.log(f"Generating production script for Option {selected_option}...")
        result = self.llm.generate_with_continuation(
            system_prompt=script_prompt,
            user_message=user_message,
        )

        if not result:
            self.log("LLM returned empty response", level="error")
            return False

        # Save to file
        self.write_file("02_story_script.md", result)
        self.step_state.output = result
        self.log(f"Production script generated: {len(result)} characters")
        return True
