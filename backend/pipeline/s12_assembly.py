"""
Step 12: Final Assembly
Combines all video clips, narration, and sound effects into the final documentary.
Input: videos/clip_XX.mp4, audio/clip_XX.mp3, audio/clip_XX_sfx.mp3
Output: final/{pokemon}_documentary.mp4
"""

from __future__ import annotations

from pathlib import Path

from backend.models import StepName
from backend.pipeline.base import PipelineStep
from backend.services.ffmpeg_service import FFmpegService


class FinalAssemblyStep(PipelineStep):
    step_name = StepName.FINAL_ASSEMBLY

    def execute(self) -> bool:
        pokemon = self.state.pokemon_name

        # Initialize FFmpeg service
        try:
            ffmpeg = FFmpegService()
        except RuntimeError as e:
            self.log(str(e), level="error")
            return False

        # Scan for required files
        videos_dir = self.project_dir / "videos"
        audio_dir = self.project_dir / "audio"
        final_dir = self.project_dir / "final"
        final_dir.mkdir(parents=True, exist_ok=True)

        # Find all clip numbers
        video_files = sorted(videos_dir.glob("clip_*.mp4"))
        if not video_files:
            self.log("No video clips found in videos/", level="error")
            return False

        clip_numbers = []
        for vf in video_files:
            import re
            match = re.search(r'clip_(\d+)', vf.stem)
            if match:
                clip_numbers.append(int(match.group(1)))

        clip_numbers.sort()
        self.log(f"Found {len(clip_numbers)} video clips: {clip_numbers}")

        # Verify all required files exist
        missing = []
        for num in clip_numbers:
            video = videos_dir / f"clip_{num:02d}.mp4"
            narration = audio_dir / f"clip_{num:02d}.mp3"
            sfx = audio_dir / f"clip_{num:02d}_sfx.mp3"

            if not video.exists():
                missing.append(f"videos/clip_{num:02d}.mp4")
            if not narration.exists():
                missing.append(f"audio/clip_{num:02d}.mp3")
            if not sfx.exists():
                missing.append(f"audio/clip_{num:02d}_sfx.mp3")

        if missing:
            self.log(f"Missing files: {', '.join(missing)}", level="error")
            self.step_state.error = f"Missing {len(missing)} files: {', '.join(missing[:5])}"
            return False

        # Stage 1: Mix each clip individually
        self.log("Stage 1: Mixing individual clips...")
        mixed_clips = []
        success_count = 0
        fail_count = 0

        for i, num in enumerate(clip_numbers, 1):
            video = videos_dir / f"clip_{num:02d}.mp4"
            narration = audio_dir / f"clip_{num:02d}.mp3"
            sfx = audio_dir / f"clip_{num:02d}_sfx.mp3"
            output = final_dir / f"clip_{num:02d}_final.mp4"

            self.log(f"[{i}/{len(clip_numbers)}] Mixing clip {num:02d}...")

            ok = ffmpeg.mix_clip(str(video), str(narration), str(sfx), str(output))
            if ok:
                success_count += 1
                mixed_clips.append(output)
            else:
                fail_count += 1
                self.log(f"Failed to mix clip {num:02d}", level="warning")

        self.log(f"Stage 1 complete: {success_count} mixed, {fail_count} failed")

        if not mixed_clips:
            self.log("No clips were mixed successfully", level="error")
            return False

        # Stage 2: Concatenate all mixed clips
        self.log("Stage 2: Concatenating all clips...")
        final_output = final_dir / f"{pokemon}_documentary.mp4"

        ok = ffmpeg.concatenate_clips(
            [str(c) for c in sorted(mixed_clips)],
            str(final_output),
        )

        if not ok:
            self.log("Concatenation failed", level="error")
            return False

        # Get final video info
        duration = ffmpeg.get_duration(str(final_output))
        file_size = final_output.stat().st_size / (1024 * 1024)  # MB

        self.step_state.artifacts.append(f"final/{pokemon}_documentary.mp4")

        self.step_state.output = (
            f"Documentary Assembly Complete!\n\n"
            f"File: final/{pokemon}_documentary.mp4\n"
            f"Duration: {duration:.1f}s ({duration/60:.1f} minutes)\n"
            f"Size: {file_size:.1f} MB\n\n"
            f"Clips mixed: {success_count}/{len(clip_numbers)}\n"
            f"Failed: {fail_count}\n"
        )

        self.log(f"Final documentary: {final_output} ({duration:.1f}s, {file_size:.1f}MB)")
        return True
