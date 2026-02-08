"""
Step 04: Asset Generation
Parses 03_assets.md and generates images via Gemini API.
Phase 1: Core assets + environments (prompt-to-image)
Phase 2: Character variations (image-to-image using cores as reference)
Input: 03_assets.md
Output: assets/characters/*.png, assets/environments/*.png
"""

from __future__ import annotations

import re
from pathlib import Path

from backend.models import StepName
from backend.pipeline.base import PipelineStep
from backend.services.gemini_service import GeminiService


class AssetGenerationStep(PipelineStep):
    step_name = StepName.ASSET_GENERATION

    def execute(self) -> bool:
        subject = self.state.subject_name

        # Load asset manifest
        manifest = self.read_file("03_assets.md")
        if not manifest:
            self.log("Missing 03_assets.md - run asset planning first", level="error")
            return False

        # Parse the manifest
        global_atmosphere = self._extract_global_atmosphere(manifest)
        assets = self._parse_asset_prompts(manifest)

        if not assets:
            self.log("No assets found in manifest", level="error")
            return False

        self.log(f"Found {len(assets)} assets in manifest")
        self.log(f"Global atmosphere: {len(global_atmosphere)} chars")

        # Categorize assets
        core_assets = [a for a in assets if a["is_core"]]
        variation_assets = [a for a in assets if not a["is_core"] and a["category"] == "characters"]
        env_assets = [a for a in assets if a["category"] == "environments"]
        prop_assets = [a for a in assets if a["category"] == "props"]

        self.log(f"Cores: {len(core_assets)}, Variations: {len(variation_assets)}, "
                 f"Environments: {len(env_assets)}, Props: {len(prop_assets)}")

        # Create directories
        project_dir = self.project_dir
        (project_dir / "assets" / "characters").mkdir(parents=True, exist_ok=True)
        (project_dir / "assets" / "environments").mkdir(parents=True, exist_ok=True)
        (project_dir / "assets" / "props").mkdir(parents=True, exist_ok=True)
        (project_dir / "assets" / "composites").mkdir(parents=True, exist_ok=True)

        # Initialize Gemini service
        try:
            gemini = GeminiService()
        except ValueError as e:
            self.log(str(e), level="error")
            return False

        # --- Phase 1: Core assets + environments + props ---
        phase1_assets = core_assets + env_assets + prop_assets
        self.log(f"Phase 1: Generating {len(phase1_assets)} assets (cores + envs + props)...")

        success_count = 0
        fail_count = 0

        for i, asset in enumerate(phase1_assets, 1):
            filename = asset["filename"]
            category = asset["category"]
            prompt = asset["prompt"]

            # Prepend global atmosphere for prompt-to-image
            full_prompt = f"{global_atmosphere}\n\n{prompt}"
            output_path = project_dir / "assets" / category / filename

            self.log(f"[Phase 1 {i}/{len(phase1_assets)}] Generating {filename}...")

            ok = gemini.generate_image(full_prompt, output_path)
            if ok:
                success_count += 1
                self.step_state.artifacts.append(f"assets/{category}/{filename}")
            else:
                fail_count += 1
                self.log(f"Failed to generate {filename}", level="warning")

        self.log(f"Phase 1 complete: {success_count} success, {fail_count} failed")

        # Store phase info in metadata for the approval step
        self.step_state.metadata["phase"] = 1
        self.step_state.metadata["phase1_success"] = success_count
        self.step_state.metadata["phase1_failed"] = fail_count
        self.step_state.metadata["variation_assets"] = [
            {"filename": a["filename"], "prompt": a["prompt"], "core_ref": a.get("core_ref", "")}
            for a in variation_assets
        ]

        # Phase 2 runs after user approval of Phase 1 cores
        # The orchestrator will call execute_phase2() after approval
        self.step_state.output = (
            f"Phase 1 Complete\n\n"
            f"Core Characters: {len(core_assets)} generated\n"
            f"Environments: {len(env_assets)} generated\n"
            f"Props: {len(prop_assets)} generated\n\n"
            f"Success: {success_count}, Failed: {fail_count}\n\n"
            f"Please review the core character assets before proceeding to Phase 2 "
            f"(character variations)."
        )

        return True

    def execute_phase2(self) -> bool:
        """Run Phase 2: Generate character variations using cores as references."""
        variation_assets = self.step_state.metadata.get("variation_assets", [])
        if not variation_assets:
            self.log("No variation assets to generate in Phase 2")
            return True

        try:
            gemini = GeminiService()
        except ValueError as e:
            self.log(str(e), level="error")
            return False

        self.log(f"Phase 2: Generating {len(variation_assets)} character variations...")

        success_count = 0
        fail_count = 0

        for i, asset in enumerate(variation_assets, 1):
            filename = asset["filename"]
            prompt = asset["prompt"]
            core_ref = asset.get("core_ref", "")

            # Find the core reference image
            ref_path = None
            if core_ref:
                ref_candidate = self.project_dir / "assets" / "characters" / core_ref
                if ref_candidate.exists():
                    ref_path = ref_candidate

            output_path = self.project_dir / "assets" / "characters" / filename
            self.log(f"[Phase 2 {i}/{len(variation_assets)}] Generating {filename}...")

            if ref_path:
                ok = gemini.generate_image(prompt, output_path, reference_image_paths=[str(ref_path)])
            else:
                # Fallback to prompt-only if no reference found
                self.log(f"No core reference found for {filename}, using prompt-only", level="warning")
                manifest = self.read_file("03_assets.md") or ""
                atmosphere = self._extract_global_atmosphere(manifest)
                full_prompt = f"{atmosphere}\n\n{prompt}"
                ok = gemini.generate_image(full_prompt, output_path)

            if ok:
                success_count += 1
                self.step_state.artifacts.append(f"assets/characters/{filename}")
            else:
                fail_count += 1
                self.log(f"Failed to generate {filename}", level="warning")

        self.step_state.metadata["phase"] = 2
        self.step_state.metadata["phase2_success"] = success_count
        self.step_state.metadata["phase2_failed"] = fail_count

        self.log(f"Phase 2 complete: {success_count} success, {fail_count} failed")
        self.step_state.output += (
            f"\n\nPhase 2 Complete\n"
            f"Character Variations: {success_count} success, {fail_count} failed"
        )
        return True

    def regenerate_asset(self, filename: str, feedback: str) -> bool:
        """Regenerate a single asset with user feedback."""
        manifest = self.read_file("03_assets.md")
        if not manifest:
            self.log("Missing 03_assets.md for regeneration", level="error")
            return False

        # Find the original prompt for this filename
        assets = self._parse_asset_prompts(manifest)
        target = None
        for asset in assets:
            if asset["filename"] == filename:
                target = asset
                break

        if not target:
            self.log(f"Asset '{filename}' not found in manifest", level="error")
            return False

        global_atmosphere = self._extract_global_atmosphere(manifest)
        full_prompt = f"{global_atmosphere}\n\n{target['prompt']}\n\nUser feedback: {feedback}"

        output_path = self.project_dir / "assets" / target["category"] / filename
        self.log(f"Regenerating {filename} with feedback: {feedback[:80]}...")

        try:
            gemini = GeminiService()
        except ValueError as e:
            self.log(str(e), level="error")
            return False

        ok = gemini.generate_image(full_prompt, output_path)
        if ok:
            self.log(f"Successfully regenerated {filename}")
        else:
            self.log(f"Failed to regenerate {filename}", level="warning")

        self.state.save(self.project_dir)
        return ok

    @staticmethod
    def _extract_global_atmosphere(manifest: str) -> str:
        """Extract the Global Atmosphere Block from the manifest."""
        # Look for the atmosphere section
        patterns = [
            r"(?:Part 3|Global Atmosphere Block)[^\n]*\n+([\s\S]*?)(?=\n(?:Part 4|#{1,4} |$))",
            r"```\n((?:(?!```)[\s\S])*?(?:cinematic|documentary|photography)[\s\S]*?)```",
        ]

        for pattern in patterns:
            match = re.search(pattern, manifest, re.IGNORECASE)
            if match:
                text = match.group(1).strip()
                if len(text) > 50:  # Sanity check
                    return text

        return ""

    @staticmethod
    def _parse_asset_prompts(manifest: str) -> list[dict]:
        """Parse all asset prompts from code blocks in the manifest."""
        assets = []

        # Find all code blocks with their preceding headers and following filenames
        # Pattern: ### Header (possibly with [CORE])\n\n```\nprompt\n```\n**Suggested filename:** name.png
        sections = re.split(r'\n(?=#{2,4}\s)', manifest)

        # First pass: collect core filenames indexed by species name
        core_by_species: dict[str, str] = {}
        for section in sections:
            if "[CORE]" not in section.split("```")[0]:
                continue
            filename_match = re.search(
                r'\*\*Suggested filename:\*\*\s*`?([a-zA-Z0-9_\-]+\.png)`?',
                section
            )
            if filename_match:
                filename = filename_match.group(1)
                species = filename.split("_")[0]
                core_by_species[species] = filename

        # Second pass: build full asset list with correct core references
        for section in sections:
            # Check if this section has a code block
            code_match = re.search(r'```\n?([\s\S]*?)```', section)
            if not code_match:
                continue

            prompt = code_match.group(1).strip()
            if len(prompt) < 20:  # Skip tiny code blocks
                continue

            # Extract filename
            filename_match = re.search(
                r'\*\*Suggested filename:\*\*\s*`?([a-zA-Z0-9_\-]+\.png)`?',
                section
            )
            if not filename_match:
                continue

            filename = filename_match.group(1)

            # Check for [CORE] marker
            is_core = "[CORE]" in section.split("```")[0]

            # Determine category from filename and context
            header = section.split("\n")[0].lower()
            if any(kw in header for kw in ["environment", "forest", "cave", "station", "exterior"]):
                category = "environments"
            elif any(kw in header for kw in ["prop", "beetle", "insect", "debris"]):
                category = "props"
            else:
                category = "characters"

            # Find core reference for variations by matching species prefix
            core_ref = ""
            if not is_core and category == "characters":
                species = filename.split("_")[0]
                core_ref = core_by_species.get(species, "")

            assets.append({
                "filename": filename,
                "prompt": prompt,
                "category": category,
                "is_core": is_core,
                "core_ref": core_ref,
                "header": section.split("\n")[0].strip(),
            })

        return assets
