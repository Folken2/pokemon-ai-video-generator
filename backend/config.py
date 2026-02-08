"""
Configuration management for the AI Documentary Pipeline.
Loads API keys and settings from environment / .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from scripts/ directory (existing convention)
_scripts_dir = Path(__file__).parent.parent / "scripts"
load_dotenv(_scripts_dir / ".env")

# Also load from project root if exists
load_dotenv(Path(__file__).parent.parent / ".env")


# --- Paths ---
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data"

# --- API Keys ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
KIE_API_KEY = os.getenv("KIE_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# --- LLM Settings ---
LLM_MODEL = "moonshotai/kimi-k2.5"
LLM_MAX_TOKENS = 50000

# --- Telegram Bot (Optional) ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "").lower() in ("true", "1", "yes")

# --- Authentication ---
API_KEY = os.getenv("API_KEY", "")

# --- Server Settings ---
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


def get_project_dir(subject_name: str) -> Path:
    """Get the project directory for a specific subject."""
    return PROJECT_ROOT / subject_name.lower().strip()


def validate_api_keys() -> dict[str, bool]:
    """Check which API keys are configured."""
    return {
        "openrouter": bool(OPENROUTER_API_KEY),
        "gemini": bool(GEMINI_API_KEY),
        "kie": bool(KIE_API_KEY),
        "elevenlabs": bool(ELEVENLABS_API_KEY),
        "elevenlabs_voice": bool(ELEVENLABS_VOICE_ID),
    }
