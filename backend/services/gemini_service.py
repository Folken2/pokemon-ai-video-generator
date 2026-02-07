"""
Gemini Service - Image generation using Google Gemini API.
Wraps the existing generate_asset.py logic as importable functions.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import google.generativeai as genai
from PIL import Image

from backend.config import GEMINI_API_KEY
from backend.utils.logging_config import logger


class GeminiService:
    """Google Gemini image generation service."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not configured.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-3-pro-image-preview")

    def generate_image(
        self,
        prompt: str,
        output_path: str | Path,
        reference_image_paths: list[str | Path] | None = None,
    ) -> bool:
        """
        Generate an image from prompt, optionally using reference images.

        Args:
            prompt: Complete generation prompt.
            output_path: Where to save the PNG.
            reference_image_paths: Optional reference images for variations.

        Returns:
            True if successful.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if reference_image_paths:
                logger.info(f"Generating image variation with {len(reference_image_paths)} references")
                reference_images = [Image.open(p) for p in reference_image_paths]
                content = reference_images + [prompt]
                response = self.model.generate_content(content)
            else:
                logger.info(f"Generating image from prompt ({len(prompt)} chars)")
                response = self.model.generate_content(prompt)

            if not response.parts:
                logger.error("No parts in Gemini response")
                return False

            image_data = None
            for part in response.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    image_data = part.inline_data.data
                    break

            if not image_data:
                logger.error("No image data in Gemini response")
                return False

            image = Image.open(BytesIO(image_data))
            image.save(output_path, "PNG")
            logger.info(f"Image saved: {output_path} ({image.size[0]}x{image.size[1]})")
            return True

        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            return False

    def create_composite(
        self,
        character_path: str | Path,
        environment_path: str | Path,
        output_path: str | Path,
    ) -> bool:
        """Create a composite image by centering character on environment."""
        try:
            environment = Image.open(environment_path).convert("RGBA")
            character = Image.open(character_path).convert("RGBA")

            TARGET_W, TARGET_H = 1920, 1080
            env_w, env_h = environment.size
            target_aspect = TARGET_W / TARGET_H
            env_aspect = env_w / env_h

            if env_aspect > target_aspect:
                environment = environment.resize(
                    (int(env_w * TARGET_H / env_h), TARGET_H), Image.Resampling.LANCZOS
                )
                left = (environment.size[0] - TARGET_W) // 2
                environment = environment.crop((left, 0, left + TARGET_W, TARGET_H))
            else:
                scale = TARGET_W / env_w
                new_h = int(env_h * scale)
                environment = environment.resize((TARGET_W, new_h), Image.Resampling.LANCZOS)
                if new_h < TARGET_H:
                    padded = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 255))
                    padded.paste(environment, (0, (TARGET_H - new_h) // 2))
                    environment = padded
                elif new_h > TARGET_H:
                    top = (new_h - TARGET_H) // 2
                    environment = environment.crop((0, top, TARGET_W, top + TARGET_H))

            char_w, char_h = character.size
            x_off = (TARGET_W - char_w) // 2
            y_off = (TARGET_H - char_h) // 2

            composite = environment.copy()
            composite.paste(character, (x_off, y_off), character)

            final = Image.new("RGB", composite.size, (0, 0, 0))
            final.paste(composite, mask=composite.split()[3])

            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            final.save(output_path, "PNG")
            logger.info(f"Composite saved: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Composite creation failed: {e}")
            return False
