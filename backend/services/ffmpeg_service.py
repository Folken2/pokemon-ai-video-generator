"""
FFmpeg Service - Video assembly operations.
Wraps the existing assemble_video.py logic.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from backend.utils.logging_config import logger


class FFmpegService:
    """FFmpeg-based video assembly service."""

    def __init__(self):
        self._check_ffmpeg()

    @staticmethod
    def _check_ffmpeg() -> None:
        """Verify ffmpeg and ffprobe are installed."""
        for tool in ("ffmpeg", "ffprobe"):
            try:
                subprocess.run([tool, "-version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise RuntimeError(f"{tool} not found. Install ffmpeg first.")

    @staticmethod
    def get_duration(file_path: str | Path) -> float | None:
        """Get media file duration in seconds."""
        try:
            result = subprocess.run(
                [
                    "ffprobe", "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    str(file_path),
                ],
                capture_output=True, text=True, check=True,
            )
            return float(result.stdout.strip())
        except Exception as e:
            logger.warning(f"Could not get duration for {file_path}: {e}")
            return None

    def mix_clip(
        self,
        video_path: str | Path,
        narration_path: str | Path,
        sfx_path: str | Path,
        output_path: str | Path,
    ) -> bool:
        """
        Mix a single clip: center narration in 10s timeline, add SFX, combine with video.

        Args:
            video_path: Path to 10s video clip.
            narration_path: Path to narration audio (6-8s).
            sfx_path: Path to 10s sound effect.
            output_path: Where to save the mixed clip.

        Returns:
            True if successful.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Get narration duration
            narration_dur = self.get_duration(narration_path)
            if narration_dur is None:
                logger.error(f"Cannot determine narration duration: {narration_path}")
                return False

            padding = (10.0 - narration_dur) / 2.0
            if padding < 0:
                padding = 0

            # Step 1: Center narration in 10s timeline
            centered_path = output_path.parent / f"{output_path.stem}_centered.mp3"
            subprocess.run(
                [
                    "ffmpeg",
                    "-f", "lavfi", "-t", str(padding),
                    "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                    "-i", str(narration_path),
                    "-f", "lavfi", "-t", str(padding),
                    "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                    "-filter_complex", "[0:a][1:a][2:a]concat=n=3:v=0:a=1[centered]",
                    "-map", "[centered]", "-t", "10", "-y", str(centered_path),
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
            )

            # Step 2: Mix centered narration + SFX
            mixed_path = output_path.parent / f"{output_path.stem}_mixed.mp3"
            subprocess.run(
                [
                    "ffmpeg",
                    "-i", str(centered_path),
                    "-i", str(sfx_path),
                    "-filter_complex",
                    "[0:a]volume=1.0[narration];[1:a]volume=1.0[sfx];"
                    "[narration][sfx]amix=inputs=2:duration=first[mixed]",
                    "-map", "[mixed]", "-t", "10", "-y", str(mixed_path),
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
            )

            # Step 3: Combine mixed audio with video
            subprocess.run(
                [
                    "ffmpeg",
                    "-i", str(video_path),
                    "-i", str(mixed_path),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-t", "10", "-y", str(output_path),
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
            )

            # Clean up temp files
            centered_path.unlink(missing_ok=True)
            mixed_path.unlink(missing_ok=True)

            logger.info(f"Clip mixed: {output_path} (narration={narration_dur:.1f}s, padding={padding:.2f}s)")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg mix failed: {e.stderr.decode() if e.stderr else e}")
            return False
        except Exception as e:
            logger.error(f"Clip mixing failed: {e}")
            return False

    def concatenate_clips(
        self,
        clip_paths: list[str | Path],
        output_path: str | Path,
    ) -> bool:
        """
        Concatenate multiple mixed clips into final documentary.

        Args:
            clip_paths: Ordered list of mixed clip paths.
            output_path: Where to save the final video.

        Returns:
            True if successful.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Create concat file
            concat_file = output_path.parent / "concat_list.txt"
            with open(concat_file, "w") as f:
                for clip in clip_paths:
                    abs_path = Path(clip).resolve()
                    f.write(f"file '{abs_path}'\n")

            # Concatenate
            subprocess.run(
                [
                    "ffmpeg",
                    "-f", "concat", "-safe", "0",
                    "-i", str(concat_file),
                    "-c", "copy", "-y", str(output_path),
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
            )

            logger.info(f"Final video assembled: {output_path}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Concatenation failed: {e.stderr.decode() if e.stderr else e}")
            return False
        except Exception as e:
            logger.error(f"Assembly failed: {e}")
            return False
