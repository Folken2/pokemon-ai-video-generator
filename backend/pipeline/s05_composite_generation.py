"""
Step 05: Composite Generation
Creates composite seed images by combining characters + environments.
Input: Generated character and environment assets + 03_assets.md mapping
Output: assets/composites/clip_XX_composite.png
"""

from __future__ import annotations

import re
from pathlib import Path

from backend.models import StepName
from backend.pipeline.base import PipelineStep
from backend.services.gemini_service import GeminiService


class CompositeGenerationStep(PipelineStep):
    step_name = StepName.COMPOSITE_GENERATION

    def execute(self) -> bool:
        pokemon = self.state.pokemon_name

        # Load asset manifest for clip-to-asset mapping
        manifest = self.read_file("03_assets.md")
        if not manifest:
            self.log("Missing 03_assets.md", level="error")
            return False

        # Parse clip-to-asset mapping table
        clip_mappings = self._parse_clip_mapping(manifest)
        if not clip_mappings:
            self.log("No clip-to-asset mappings found in manifest", level="error")
            return False

        self.log(f"Found {len(clip_mappings)} clip mappings")

        # Create composites directory
        composites_dir = self.project_dir / "assets" / "composites"
        composites_dir.mkdir(parents=True, exist_ok=True)

        gemini = GeminiService()
        success_count = 0
        fail_count = 0

        chars_dir = self.project_dir / "assets" / "characters"
        envs_dir = self.project_dir / "assets" / "environments"

        for i, mapping in enumerate(clip_mappings, 1):
            clip_num = mapping["clip"]
            char_file = mapping.get("character", "")
            env_file = mapping.get("environment", "")

            output_path = composites_dir / f"clip_{clip_num:02d}_composite.png"

            # Find character file (try with and without _core suffix)
            char_path = self._find_asset(chars_dir, char_file) if char_file else None
            env_path = self._find_asset(envs_dir, env_file) if env_file else None

            if char_path and env_path:
                self.log(f"[{i}/{len(clip_mappings)}] Creating composite for clip {clip_num:02d}...")
                ok = gemini.create_composite(str(char_path), str(env_path), str(output_path))
            elif char_path and not env_path:
                # Character-only: just copy
                self.log(f"[{i}/{len(clip_mappings)}] Clip {clip_num:02d}: character-only (copying)")
                import shutil
                shutil.copy2(char_path, output_path)
                ok = True
            elif env_path and not char_path:
                # Environment-only: just copy
                self.log(f"[{i}/{len(clip_mappings)}] Clip {clip_num:02d}: environment-only (copying)")
                import shutil
                shutil.copy2(env_path, output_path)
                ok = True
            else:
                self.log(f"Clip {clip_num:02d}: no assets found (char={char_file}, env={env_file})", level="warning")
                ok = False

            if ok:
                success_count += 1
                self.step_state.artifacts.append(f"assets/composites/clip_{clip_num:02d}_composite.png")
            else:
                fail_count += 1

        self.step_state.output = (
            f"Composite Generation Complete\n\n"
            f"Total clips: {len(clip_mappings)}\n"
            f"Success: {success_count}\n"
            f"Failed: {fail_count}\n"
        )

        self.log(f"Composites: {success_count} success, {fail_count} failed")
        return success_count > 0

    @staticmethod
    def _find_asset(directory: Path, filename: str) -> Path | None:
        """Find an asset file, trying with and without _core suffix."""
        if not filename:
            return None

        # Direct match
        path = directory / filename
        if path.exists():
            return path

        # Try adding _core
        stem = Path(filename).stem
        core_path = directory / f"{stem}_core.png"
        if core_path.exists():
            return core_path

        # Try removing _core
        if "_core" in stem:
            no_core = directory / f"{stem.replace('_core', '')}.png"
            if no_core.exists():
                return no_core

        # Fuzzy match - find closest
        candidates = list(directory.glob("*.png"))
        for candidate in candidates:
            if stem.replace("_core", "") in candidate.stem or candidate.stem in stem:
                return candidate

        return None

    @staticmethod
    def _parse_clip_mapping(manifest: str) -> list[dict]:
        """Parse the clip-to-asset mapping table from the manifest."""
        mappings = []

        # Look for the mapping table
        lines = manifest.split("\n")
        in_table = False
        header_found = False

        for line in lines:
            stripped = line.strip()

            # Detect table start
            if re.match(r'\|\s*Clip\s*#?\s*\|', stripped, re.IGNORECASE):
                in_table = True
                header_found = False
                continue

            if in_table and stripped.startswith("|") and "---" in stripped:
                header_found = True
                continue

            if in_table and header_found and stripped.startswith("|"):
                # Parse table row
                cells = [c.strip() for c in stripped.split("|")[1:-1]]
                if len(cells) >= 2:
                    clip_match = re.search(r'(\d+)', cells[0])
                    if clip_match:
                        clip_num = int(clip_match.group(1))
                        asset_text = " ".join(cells[1:])

                        # Extract character and environment references
                        char_file = ""
                        env_file = ""

                        # Look for filenames
                        filenames = re.findall(r'([a-zA-Z0-9_\-]+\.png)', asset_text)
                        for fn in filenames:
                            if any(kw in fn.lower() for kw in ["env_", "forest", "cave", "station"]):
                                env_file = fn
                            else:
                                char_file = fn

                        # If no explicit filenames, try to extract from descriptions
                        if not char_file and not env_file:
                            char_file = f"clip_{clip_num:02d}_asset.png"

                        mappings.append({
                            "clip": clip_num,
                            "character": char_file,
                            "environment": env_file,
                            "raw": asset_text,
                        })

            elif in_table and not stripped.startswith("|"):
                in_table = False

        return mappings
