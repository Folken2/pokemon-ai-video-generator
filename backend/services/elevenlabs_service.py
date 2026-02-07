"""
ElevenLabs Service - Audio narration and sound effects generation.
Wraps the existing generate_audio.py and generate_sound_effects.py logic.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import requests

from backend.config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
from backend.utils.logging_config import logger

ELEVENLABS_API_BASE = "https://api.elevenlabs.io"


class ElevenLabsService:
    """ElevenLabs TTS and sound effects service."""

    def __init__(
        self,
        api_key: str | None = None,
        voice_id: str | None = None,
    ):
        self.api_key = api_key or ELEVENLABS_API_KEY
        self.voice_id = voice_id or ELEVENLABS_VOICE_ID
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not configured.")

    def generate_narration(
        self,
        text: str,
        output_path: str | Path,
        stability: float = 0.40,
        similarity_boost: float = 0.75,
        style: float = 0.12,
    ) -> bool:
        """
        Generate narrator audio using ElevenLabs TTS.

        Args:
            text: Narration text.
            output_path: Where to save the MP3.
            stability: Voice stability (0-1).
            similarity_boost: Voice similarity (0-1).
            style: Style exaggeration (0-1).

        Returns:
            True if successful.
        """
        if not self.voice_id:
            logger.error("ELEVENLABS_VOICE_ID not configured")
            return False

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json",
            }
            payload = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": stability,
                    "similarity_boost": similarity_boost,
                    "style": style,
                    "use_speaker_boost": True,
                },
            }

            endpoint = f"{ELEVENLABS_API_BASE}/v1/text-to-speech/{self.voice_id}"
            response = requests.post(endpoint, headers=headers, json=payload)

            if response.status_code != 200:
                logger.error(f"ElevenLabs TTS error: {response.status_code} - {response.text}")
                return False

            with open(output_path, "wb") as f:
                f.write(response.content)

            logger.info(f"Narration saved: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Narration generation failed: {e}")
            return False

    def generate_sound_effect(
        self,
        text: str,
        output_path: str | Path,
        duration_seconds: float = 10.0,
        prompt_influence: float = 0.3,
    ) -> bool:
        """
        Generate a sound effect using ElevenLabs Sound Effects API.

        Args:
            text: Sound effect description.
            output_path: Where to save the MP3.
            duration_seconds: Duration (0.5-30).
            prompt_influence: How strictly to follow prompt (0-1).

        Returns:
            True if successful.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json",
            }
            payload = {
                "text": text,
                "duration_seconds": duration_seconds,
                "prompt_influence": prompt_influence,
            }
            params = {"output_format": "mp3_44100_128"}

            endpoint = f"{ELEVENLABS_API_BASE}/v1/sound-generation"
            response = requests.post(endpoint, headers=headers, json=payload, params=params)

            if response.status_code != 200:
                logger.error(f"ElevenLabs SFX error: {response.status_code} - {response.text}")
                return False

            with open(output_path, "wb") as f:
                f.write(response.content)

            # Normalize audio
            self._normalize_audio(output_path)

            logger.info(f"Sound effect saved: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Sound effect generation failed: {e}")
            return False

    @staticmethod
    def get_audio_duration(audio_path: str | Path) -> float | None:
        """Get audio duration in seconds using ffprobe."""
        try:
            result = subprocess.run(
                [
                    "ffprobe", "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    str(audio_path),
                ],
                capture_output=True, text=True, check=True,
            )
            return float(result.stdout.strip())
        except Exception as e:
            logger.warning(f"Could not get audio duration: {e}")
            return None

    @staticmethod
    def _normalize_audio(audio_path: Path, target_lufs: float = -30.0) -> bool:
        """Normalize audio volume using ffmpeg."""
        try:
            temp_path = audio_path.parent / f"{audio_path.stem}_temp{audio_path.suffix}"
            subprocess.run(
                [
                    "ffmpeg", "-i", str(audio_path),
                    "-af", f"loudnorm=I={target_lufs}:TP=-2:LRA=7",
                    "-ar", "44100", "-y", str(temp_path),
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
            )
            temp_path.replace(audio_path)
            return True
        except Exception as e:
            logger.warning(f"Audio normalization failed (non-critical): {e}")
            return False
