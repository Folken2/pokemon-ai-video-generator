"""
Step 11: Sound Effects Generation
Parses 06_sound_effects_prompts.md and generates SFX via ElevenLabs.
Input: 06_sound_effects_prompts.md
Output: audio/clip_XX_sfx.mp3
"""

from __future__ import annotations

import re

from backend.models import StepName
from backend.pipeline.base import PipelineStep
from backend.services.elevenlabs_service import ElevenLabsService


class SFXGenerationStep(PipelineStep):
    step_name = StepName.SFX_GENERATION

    def execute(self) -> bool:
        subject = self.state.subject_name

        # Load SFX prompts
        sfx_md = self.read_file("06_sound_effects_prompts.md")
        if not sfx_md:
            self.log("Missing 06_sound_effects_prompts.md", level="error")
            return False

        # Parse SFX prompts
        sfx_entries = self._parse_sfx_table(sfx_md)
        if not sfx_entries:
            self.log("No SFX entries found", level="error")
            return False

        self.log(f"Found {len(sfx_entries)} sound effects to generate")

        # Create output directory
        audio_dir = self.project_dir / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)

        # Initialize ElevenLabs service
        try:
            el = ElevenLabsService()
        except ValueError as e:
            self.log(str(e), level="error")
            return False

        success_count = 0
        fail_count = 0

        for i, entry in enumerate(sfx_entries, 1):
            clip_num = entry["clip"]
            prompt = entry["prompt"]
            output_path = audio_dir / f"clip_{clip_num:02d}_sfx.mp3"

            self.log(f"[{i}/{len(sfx_entries)}] Generating SFX for clip {clip_num:02d}...")

            ok = el.generate_sound_effect(prompt, str(output_path), duration_seconds=10.0)
            if ok:
                success_count += 1
                self.step_state.artifacts.append(f"audio/clip_{clip_num:02d}_sfx.mp3")
            else:
                fail_count += 1
                self.log(f"Clip {clip_num:02d} SFX failed", level="warning")

        self.step_state.output = (
            f"Sound Effects Generation Complete\n\n"
            f"Total clips: {len(sfx_entries)}\n"
            f"Success: {success_count}\n"
            f"Failed: {fail_count}\n"
        )

        self.log(f"SFX generation: {success_count} success, {fail_count} failed")
        return success_count > 0

    @staticmethod
    def _parse_sfx_table(sfx_md: str) -> list[dict]:
        """Parse sound effect prompts from the table."""
        entries = []
        lines = sfx_md.split("\n")
        in_table = False
        header_found = False

        for line in lines:
            stripped = line.strip()

            if re.match(r'\|\s*Clip\s*#?\s*\|', stripped, re.IGNORECASE):
                in_table = True
                header_found = False
                continue

            if in_table and stripped.startswith("|") and "---" in stripped:
                header_found = True
                continue

            if in_table and header_found and stripped.startswith("|"):
                cells = [c.strip() for c in stripped.split("|")[1:-1]]
                if len(cells) >= 3:
                    clip_match = re.search(r'(\d+)', cells[0])
                    if clip_match:
                        clip_num = int(clip_match.group(1))
                        # SFX prompt is usually in the 3rd column (after scene summary)
                        prompt = cells[2].strip().strip('"').strip("'")
                        if not prompt and len(cells) >= 2:
                            prompt = cells[1].strip().strip('"').strip("'")
                        if prompt:
                            entries.append({"clip": clip_num, "prompt": prompt})

            elif in_table and not stripped.startswith("|"):
                in_table = False

        return entries
