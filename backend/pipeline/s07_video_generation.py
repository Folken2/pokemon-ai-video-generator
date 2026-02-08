"""
Step 07: Video Generation
Parses 04_video_prompts.md and generates video clips via Kling 2.5 API.
Input: 04_video_prompts.md + composite seed images
Output: videos/clip_XX.mp4
"""

from __future__ import annotations

import re
from pathlib import Path

from backend.models import StepName
from backend.pipeline.base import PipelineStep
from backend.services.kling_service import KlingService


class VideoGenerationStep(PipelineStep):
    step_name = StepName.VIDEO_GENERATION

    def execute(self) -> bool:
        subject = self.state.subject_name

        # Load video prompts
        prompts_md = self.read_file("04_video_prompts.md")
        if not prompts_md:
            self.log("Missing 04_video_prompts.md", level="error")
            return False

        # Parse the shot list
        shots = self._parse_shot_list(prompts_md)
        if not shots:
            self.log("No shots found in video prompts", level="error")
            return False

        self.log(f"Found {len(shots)} shots to generate")

        # Create output directory
        videos_dir = self.project_dir / "videos"
        videos_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Kling service
        try:
            kling = KlingService()
        except ValueError as e:
            self.log(str(e), level="error")
            return False

        success_count = 0
        fail_count = 0

        for i, shot in enumerate(shots, 1):
            clip_num = shot["clip"]
            asset_file = shot["asset"]
            prompt = shot["prompt"]

            # Find the seed image
            image_path = self._find_seed_image(asset_file, clip_num)
            if not image_path:
                self.log(f"Clip {clip_num:02d}: seed image not found ({asset_file})", level="warning")
                fail_count += 1
                continue

            output_path = videos_dir / f"clip_{clip_num:02d}.mp4"
            self.log(f"[{i}/{len(shots)}] Generating clip {clip_num:02d} (this takes 2-5 min)...")

            ok = kling.generate_video(str(image_path), prompt, str(output_path))
            if ok:
                success_count += 1
                self.step_state.artifacts.append(f"videos/clip_{clip_num:02d}.mp4")
                self.log(f"Clip {clip_num:02d} generated successfully")
            else:
                fail_count += 1
                self.log(f"Clip {clip_num:02d} failed", level="warning")

        self.step_state.output = (
            f"Video Generation Complete\n\n"
            f"Total clips: {len(shots)}\n"
            f"Success: {success_count}\n"
            f"Failed: {fail_count}\n"
        )

        self.log(f"Video generation: {success_count} success, {fail_count} failed")
        return success_count > 0

    def _find_seed_image(self, asset_file: str, clip_num: int) -> Path | None:
        """Find the seed image for a clip, checking composites first."""
        # Check composites first
        composite = self.project_dir / "assets" / "composites" / f"clip_{clip_num:02d}_composite.png"
        if composite.exists():
            return composite

        # Check characters directory
        for subdir in ["characters", "environments", "composites", "props"]:
            path = self.project_dir / "assets" / subdir / asset_file
            if path.exists():
                return path

            # Try with _core suffix
            stem = Path(asset_file).stem
            core_path = self.project_dir / "assets" / subdir / f"{stem}_core.png"
            if core_path.exists():
                return core_path

        # Glob for any match
        for subdir in ["composites", "characters", "environments"]:
            candidates = list((self.project_dir / "assets" / subdir).glob("*.png"))
            for c in candidates:
                if asset_file.replace(".png", "") in c.stem or c.stem in asset_file:
                    return c

        return None

    @staticmethod
    def _parse_shot_list(prompts_md: str) -> list[dict]:
        """Parse the Kling 2.5 Shot List table from the markdown."""
        shots = []
        lines = prompts_md.split("\n")
        in_table = False
        header_found = False

        for line in lines:
            stripped = line.strip()

            # Detect table header
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
                        asset_file = cells[1].strip().strip('`')
                        prompt = cells[2].strip().strip('"').strip("'")

                        shots.append({
                            "clip": clip_num,
                            "asset": asset_file,
                            "prompt": prompt,
                        })

            elif in_table and not stripped.startswith("|"):
                in_table = False

        return shots
