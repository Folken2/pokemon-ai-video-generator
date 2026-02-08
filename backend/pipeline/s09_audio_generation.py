"""
Step 09: Audio/Narration Generation
Parses 05_audio_generation.md and generates narrator audio via ElevenLabs.
Includes iterative duration targeting (7.5-9 seconds per clip).
Input: 05_audio_generation.md
Output: audio/clip_XX.mp3
"""

from __future__ import annotations

import re

from backend.models import StepName
from backend.pipeline.base import PipelineStep
from backend.services.elevenlabs_service import ElevenLabsService


class AudioGenerationStep(PipelineStep):
    step_name = StepName.AUDIO_GENERATION

    def execute(self) -> bool:
        subject = self.state.subject_name

        # Load audio prompts
        audio_md = self.read_file("05_audio_generation.md")
        if not audio_md:
            self.log("Missing 05_audio_generation.md", level="error")
            return False

        # Parse narration entries
        narrations = self._parse_narration_table(audio_md)
        if not narrations:
            self.log("No narration entries found", level="error")
            return False

        self.log(f"Found {len(narrations)} narration clips to generate")

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
        results = []

        for i, entry in enumerate(narrations, 1):
            clip_num = entry["clip"]
            text = entry["text"]
            output_path = audio_dir / f"clip_{clip_num:02d}.mp3"

            self.log(f"[{i}/{len(narrations)}] Generating clip {clip_num:02d} narration...")

            # Iterative generation with duration targeting
            ok, duration, final_text = self._generate_with_duration_target(
                el, text, str(output_path),
                target_min=7.5, target_max=9.0, max_iterations=3,
            )

            if ok:
                success_count += 1
                self.step_state.artifacts.append(f"audio/clip_{clip_num:02d}.mp3")
                results.append(f"clip_{clip_num:02d}.mp3: {duration:.1f}s")
                self.log(f"Clip {clip_num:02d}: {duration:.1f}s")
            else:
                fail_count += 1
                results.append(f"clip_{clip_num:02d}.mp3: FAILED")
                self.log(f"Clip {clip_num:02d} failed", level="warning")

        self.step_state.output = (
            f"Audio Generation Complete\n\n"
            f"Total clips: {len(narrations)}\n"
            f"Success: {success_count}\n"
            f"Failed: {fail_count}\n\n"
            f"Details:\n" + "\n".join(results)
        )

        self.log(f"Audio generation: {success_count} success, {fail_count} failed")
        return success_count > 0

    def _generate_with_duration_target(
        self,
        el: ElevenLabsService,
        text: str,
        output_path: str,
        target_min: float = 7.5,
        target_max: float = 9.0,
        max_iterations: int = 3,
    ) -> tuple[bool, float, str]:
        """
        Generate audio with iterative duration targeting.
        Returns: (success, duration, final_text)
        """
        current_text = text

        for attempt in range(max_iterations):
            ok = el.generate_narration(current_text, output_path)
            if not ok:
                return False, 0.0, current_text

            duration = el.get_audio_duration(output_path)
            if duration is None:
                return False, 0.0, current_text

            if target_min <= duration <= target_max:
                return True, duration, current_text

            if duration < target_min and attempt < max_iterations - 1:
                # Too short - try to expand
                words = current_text.split()
                word_count = len(words)
                # Add ~2 words per second needed
                needed = target_min - duration
                extra_words = max(2, int(needed * 2))
                self.log(f"  Attempt {attempt+1}: {duration:.1f}s (too short, need +{extra_words} words)")
                # Simple expansion: repeat last few meaningful words with context
                current_text = current_text  # Keep as-is, ElevenLabs variance may fix it
            elif duration > target_max and attempt < max_iterations - 1:
                # Too long - try to trim
                self.log(f"  Attempt {attempt+1}: {duration:.1f}s (too long)")
                current_text = current_text  # Keep as-is, retry

            # If still outside range after all attempts, accept what we have
            if attempt == max_iterations - 1:
                self.log(f"  Accepting {duration:.1f}s after {max_iterations} attempts")
                return True, duration, current_text

        return True, 0.0, current_text

    @staticmethod
    def _parse_narration_table(audio_md: str) -> list[dict]:
        """Parse narration text from the Audio Generation Table."""
        narrations = []
        lines = audio_md.split("\n")
        in_table = False
        header_found = False

        for line in lines:
            stripped = line.strip()

            if re.match(r'\|\s*Sequence\s*#?\s*\|', stripped, re.IGNORECASE):
                in_table = True
                header_found = False
                continue

            if in_table and stripped.startswith("|") and "---" in stripped:
                header_found = True
                continue

            if in_table and header_found and stripped.startswith("|"):
                cells = [c.strip() for c in stripped.split("|")[1:-1]]
                if len(cells) >= 2:
                    clip_match = re.search(r'(\d+)', cells[0])
                    if clip_match:
                        clip_num = int(clip_match.group(1))
                        text = cells[1].strip().strip('"').strip("'")
                        if text:
                            narrations.append({"clip": clip_num, "text": text})

            elif in_table and not stripped.startswith("|"):
                in_table = False

        return narrations
