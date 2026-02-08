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
        subject = self.state.subject_name

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

            # Find character file (search both dirs as fallback)
            char_path = (self._find_asset(chars_dir, char_file) or
                         self._find_asset(envs_dir, char_file)) if char_file else None
            env_path = (self._find_asset(envs_dir, env_file) or
                        self._find_asset(chars_dir, env_file)) if env_file else None

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
        # Build description -> filename mapping from Part 4 of the manifest
        name_to_filename: dict[str, str] = {}
        sections = re.split(r'\n(?=#{2,4}\s)', manifest)
        for section in sections:
            filename_match = re.search(
                r'\*\*Suggested filename:\*\*\s*`?([a-zA-Z0-9_\-]+\.png)`?',
                section
            )
            if not filename_match:
                continue
            filename = filename_match.group(1)
            # Extract the asset name from the section header
            header = section.split("\n")[0].strip()
            header_clean = re.sub(r'^[#\d.\s]+', '', header).strip()
            # Remove [CORE] for matching purposes
            header_key = re.sub(r'\s*\[CORE\]\s*', '', header_clean).strip().lower()
            name_to_filename[header_key] = filename

        mappings = []

        # Look for the mapping table
        lines = manifest.split("\n")
        in_table = False
        header_found = False
        asset_col = 1  # Default: assets in second column

        for line in lines:
            stripped = line.strip()

            # Detect table start and determine which column has assets
            if re.match(r'\|\s*Clip\s*#?\s*\|', stripped, re.IGNORECASE):
                in_table = True
                header_found = False
                header_cells = [c.strip().lower() for c in stripped.split("|")[1:-1]]
                asset_col = next(
                    (i for i, c in enumerate(header_cells) if 'asset' in c),
                    1  # fallback to second column
                )
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
                        asset_text = cells[min(asset_col, len(cells) - 1)]

                        char_file = ""
                        env_file = ""

                        # First try to find .png filenames directly in the text
                        filenames = re.findall(r'([a-zA-Z0-9_\-]+\.png)', asset_text)
                        for fn in filenames:
                            if any(kw in fn.lower() for kw in ["env_", "forest", "cave", "station"]):
                                env_file = fn
                            else:
                                char_file = char_file or fn

                        # If no filenames, match descriptions to known asset names
                        if not char_file and not env_file:
                            # Split by + to handle multiple assets per clip
                            asset_parts = re.split(r'\s*\+\s*', asset_text)
                            for part in asset_parts:
                                part_clean = re.sub(r'\s*\[CORE\]\s*', '', part).strip().lower()
                                # Skip annotation-only parts
                                if re.search(r'\bimplied\b|\bin motion\b', part_clean):
                                    continue

                                matched = name_to_filename.get(part_clean)
                                # Fuzzy: check if any known name contains or is contained by part
                                if not matched:
                                    for key, fname in name_to_filename.items():
                                        if part_clean in key or key in part_clean:
                                            matched = fname
                                            break

                                if matched:
                                    is_env = any(kw in matched for kw in ["env_", "forest", "cave", "station"])
                                    if is_env:
                                        env_file = env_file or matched
                                    else:
                                        char_file = char_file or matched

                        mappings.append({
                            "clip": clip_num,
                            "character": char_file,
                            "environment": env_file,
                            "raw": asset_text,
                        })

            elif in_table and not stripped.startswith("|"):
                in_table = False

        return mappings
