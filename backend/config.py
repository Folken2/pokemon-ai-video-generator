"""
Configuration management for the Pokemon Documentary Pipeline.
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

# --- API Keys ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
KIE_API_KEY = os.getenv("KIE_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# --- LLM Settings ---
LLM_MODEL = "claude-sonnet-4-20250514"
LLM_MAX_TOKENS = 8192

# --- Server Settings ---
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


def get_project_dir(pokemon_name: str) -> Path:
    """Get the project directory for a specific Pokemon."""
    return PROJECT_ROOT / pokemon_name.lower().strip()


def validate_api_keys() -> dict[str, bool]:
    """Check which API keys are configured."""
    return {
        "anthropic": bool(ANTHROPIC_API_KEY),
        "gemini": bool(GEMINI_API_KEY),
        "kie": bool(KIE_API_KEY),
        "elevenlabs": bool(ELEVENLABS_API_KEY),
        "elevenlabs_voice": bool(ELEVENLABS_VOICE_ID),
    }
