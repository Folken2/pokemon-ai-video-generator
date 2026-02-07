"""
Kling Service - Video generation using KIE.ai Kling 2.5 API.
Wraps the existing generate_video.py logic as importable functions.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import requests

from backend.config import KIE_API_KEY
from backend.utils.logging_config import logger

KIE_API_BASE = "https://api.kie.ai/api/v1"
CATBOX_UPLOAD_URL = "https://catbox.moe/user/api.php"


class KlingService:
    """KIE.ai Kling 2.5 video generation service."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or KIE_API_KEY
        if not self.api_key:
            raise ValueError("KIE_API_KEY not configured.")

    def _upload_to_catbox(self, image_path: str | Path) -> str | None:
        """Upload image to catbox.moe for Kling API access."""
        image_path = Path(image_path)
        try:
            with open(image_path, "rb") as f:
                files = {"fileToUpload": (image_path.name, f, "image/png")}
                data = {"reqtype": "fileupload"}
                response = requests.post(CATBOX_UPLOAD_URL, files=files, data=data)

            if response.status_code != 200:
                logger.error(f"Catbox upload failed: {response.status_code}")
                return None

            url = response.text.strip()
            if not url.startswith("http"):
                logger.error(f"Invalid catbox URL: {url}")
                return None

            logger.info(f"Image uploaded to catbox: {url}")
            return url
        except Exception as e:
            logger.error(f"Catbox upload error: {e}")
            return None

    def _poll_task(self, task_id: str, max_wait: int = 600) -> str | None:
        """Poll KIE.ai task until completion. Returns video URL."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        endpoint = f"{KIE_API_BASE}/jobs/recordInfo"
        start = time.time()

        while time.time() - start < max_wait:
            try:
                resp = requests.get(endpoint, headers=headers, params={"taskId": task_id})
                if resp.status_code == 200:
                    result = resp.json()
                    if result.get("code") != 200:
                        logger.error(f"Kling API error: {result.get('message')}")
                        return None

                    data = result.get("data", {})
                    state = data.get("state")

                    if state == "success":
                        result_json = json.loads(data.get("resultJson", "{}"))
                        urls = result_json.get("resultUrls", [])
                        if urls:
                            return urls[0]
                        logger.error("No video URL in result")
                        return None
                    elif state == "failed":
                        logger.error(f"Video generation failed: {data}")
                        return None
                    else:
                        elapsed = int(time.time() - start)
                        logger.info(f"Video {state}... ({elapsed}s elapsed)")
            except Exception as e:
                logger.warning(f"Polling error: {e}")

            time.sleep(5)

        logger.error(f"Video generation timed out after {max_wait}s")
        return None

    def generate_video(
        self,
        image_path: str | Path,
        prompt: str,
        output_path: str | Path,
        on_progress: callable = None,
    ) -> bool:
        """
        Generate a 10-second video from a seed image.

        Args:
            image_path: Path to seed image.
            prompt: Motion description prompt.
            output_path: Where to save the MP4.
            on_progress: Optional callback for progress updates.

        Returns:
            True if successful.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Upload image
            image_url = self._upload_to_catbox(image_path)
            if not image_url:
                return False

            # Create task
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
            payload = {
                "model": "kling/v2-5-turbo-image-to-video-pro",
                "callBackUrl": "",
                "input": {
                    "prompt": prompt,
                    "image_url": image_url,
                    "duration": "10",
                    "negative_prompt": "blur, distort, and low quality",
                    "cfg_scale": 0.5,
                },
            }

            resp = requests.post(
                f"{KIE_API_BASE}/jobs/createTask",
                headers=headers,
                data=json.dumps(payload),
            )

            if resp.status_code != 200:
                logger.error(f"Kling API error: {resp.status_code} - {resp.text}")
                return False

            result = resp.json()
            task_id = result.get("data", {}).get("taskId")
            if not task_id:
                logger.error(f"No task ID in response: {result}")
                return False

            logger.info(f"Kling task created: {task_id}")

            # Poll for completion
            video_url = self._poll_task(task_id)
            if not video_url:
                return False

            # Download video
            dl_resp = requests.get(video_url, stream=True)
            dl_resp.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in dl_resp.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Video saved: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            return False
