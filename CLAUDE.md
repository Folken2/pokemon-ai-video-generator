# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-theme AI pipeline for generating hyper-realistic nature documentaries (~90 seconds, 1080p, 16:9) in the style of David Attenborough's *Planet Earth*. Supports multiple themes: **Pokemon**, **Harry Potter Animalia**, **Ancient Creatures**, and **Deep Sea Creatures**. Combines OpenRouter LLM API (story/prompts), Gemini (images), Kling 2.5 (video), ElevenLabs (narration/SFX), and FFmpeg (assembly) with a human-in-the-loop approval workflow.

## Commands

```bash
# Install dependencies
uv sync

# Run backend server (dev mode with hot reload)
uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000

# Run via entry point
uv run pipeline-server

# Individual scripts (run from project root)
python scripts/generate_asset.py --prompt "..." --output "path.png"
python scripts/generate_video.py --image "path.png" --prompt "..." --output "path.mp4"
python scripts/generate_audio.py --text "..." --output "path.mp3"
python scripts/create_composite.py --character "char.png" --environment "env.png" --output "composite.png"
python scripts/assemble_video.py --manifest "manifest.json" --output "final.mp4"
```

No test suite or linter is configured. FFmpeg must be installed as a system dependency.

## Environment Variables

API keys go in `scripts/.env` (see `scripts/.env.example`):
- `OPENROUTER_API_KEY` — OpenRouter LLM gateway (routes to Claude, GPT, etc.)
- `GEMINI_API_KEY` — Google Gemini image generation
- `KIE_API_KEY` — KIE.ai Kling 2.5 Pro video generation
- `ELEVENLABS_API_KEY` + `ELEVENLABS_VOICE_ID` — Narration and SFX
- `TELEGRAM_ENABLED` + `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` — Optional Telegram bot for mobile approvals
- `API_KEY` — Optional API key for cloud deployment. When set, all `/api/*` and `/files/*` routes require `X-API-Key` header (except `/api/health`). When empty, no auth (dev mode). The key is auto-injected into the frontend HTML.

Config is loaded in `backend/config.py`, which reads from both `scripts/.env` and project root `.env`.

## Architecture

### Smart Orchestrator + Dumb Scripts

- **Backend (FastAPI)**: Orchestrates the 12-step pipeline, manages state, calls LLMs, handles approvals
- **Scripts (CLI)**: Each script does one thing — takes complete inputs, calls one external API, returns success/failure. Kept simple and reusable.
- **Frontend (Vanilla JS + Tailwind)**: Web UI for project management and step approval. No build step — served as static files by FastAPI.

### Multi-Theme Support

Each project selects a theme at creation time. Available themes are defined in `backend/models.py` as `AVAILABLE_THEMES`:
- `pokemon` — Pokemon nature documentaries (default)
- `harry_potter` — Harry Potter magical creatures
- `ancient_creatures` — Prehistoric/paleontology creatures
- `deep_sea` — Deep sea marine creatures

The theme determines which SOP prompts are loaded from `prompts/{theme}/`. The pipeline architecture, state machine, and external API integrations are theme-agnostic.

### Pipeline Flow

The pipeline has 12 internal steps (mapped to 8 SOPs) with human approval gates between each:

1. **Research** → LLM generates subject profile → `{subject}/01_research.md`
2. **Story** → LLM generates 5 story options, user selects one → `{subject}/02_story_script.md` (18-clip script)
3. **Asset Planning** → LLM creates asset manifest from research + story
4. **Asset Generation** → Gemini generates 20-25 photorealistic seed images → `{subject}/assets/`
5. **Composite Generation** → Combines character + environment into 1920x1080 composites → `{subject}/assets/composites/`
6. **Video Prompts** → LLM generates Kling motion prompts using Priority Hierarchy (Core Action → Details → Sequence → Environment → Camera LAST)
7. **Video Generation** → Kling 2.5 Pro creates 18 × 10-second clips → `{subject}/videos/`
8. **Audio Prompts** → LLM generates narration scripts
9. **Audio Generation** → ElevenLabs narration (18 clips, 6-8s each) → `{subject}/audio/`
10. **SFX Prompts** → LLM generates SFX descriptions
11. **SFX Generation** → ElevenLabs Sound Effects API → `{subject}/sfx/`
12. **Final Assembly** → FFmpeg trims video to audio length, concatenates all clips → `{subject}/{subject}_final.mp4`

### State Management

- Pipeline state persisted as `pipeline_state.json` in each project directory
- State includes `subject_name` and `theme` fields
- Step statuses: `pending → running → awaiting_approval → approved → next step` (or `failed` for retry)
- `backend/models.py` defines all Pydantic models (`StepState`, `PipelineState`, `StepStatus`, `StepName`)
- Backward compatible: loads legacy `pokemon_name` field as `subject_name`

### API Structure

- `GET/POST /api/projects/` — Project CRUD (`backend/routers/projects.py`)
- `GET /api/projects/themes` — List available themes
- `GET /api/projects/subjects/{theme}?q=` — Search curated subject catalog for a theme (`backend/services/subject_catalog.py`)
- `POST /api/pipeline/{subject_name}/run|approve|retry` — Step execution (`backend/routers/pipeline.py`)
- Steps execute in a `ThreadPoolExecutor` (2 workers) to avoid blocking async endpoints
- Frontend polls every 2 seconds during execution

### Key Constraints

- Kling 2.5 generates fixed 10-second clips; FFmpeg trims them to match audio duration (6-8s)
- "Breathing photograph" approach: each clip animates one static image with one micro-movement
- Images uploaded to catbox.moe for free URLs required by Kling API
- Hard cuts between clips (no transitions)
- LLM calls go through OpenRouter (OpenAI-compatible API); model configured in `backend/config.py` as `LLM_MODEL`

### Prompt SOPs

SOP prompts are organized by theme under `prompts/{theme}/`:

```
prompts/
├── pokemon/           # Pokemon-specific SOPs (1-3) + shared SOPs (4-7)
├── harry_potter/      # Harry Potter creature SOPs (1-3)
├── ancient_creatures/ # Paleontology SOPs (1-3)
├── deep_sea/          # Deep-sea biology SOPs (1-3)
├── 4_video_prompt_engineering.md   # Shared (theme-agnostic)
├── 5_voice_prompt_engineer.md      # Shared
├── 6_sound_effects_prompt_engineering.md  # Shared
├── 7_assemble_final_agent.md       # Shared
└── ... (other shared agent prompts)
```

**Theme-specific SOPs (1-3):** Research framework, story rules, and asset design vary by theme.
**Shared SOPs (4-7):** Video prompts, audio, SFX, and assembly are universal across themes.

The `load_sop_prompt()` method in `backend/pipeline/base.py` tries `prompts/{theme}/` first, then falls back to `prompts/` root.

### Character Catalogs

Curated subject lists per theme live in `data/subjects/{theme}.yaml`. Each entry has `name`, `display_name`, `tags`, `cinematic_rating` (1-5), and `description`. The frontend shows a searchable dropdown when creating projects — users can pick a curated subject or type a custom name.

- `data/subjects/pokemon.yaml` — ~51 Gen 1 Pokemon
- `data/subjects/harry_potter.yaml` — ~20 magical creatures
- `data/subjects/ancient_creatures.yaml` — ~25 prehistoric creatures
- `data/subjects/deep_sea.yaml` — ~25 marine creatures
- `backend/services/subject_catalog.py` — `load_catalog(theme)` (cached with `@lru_cache`), `search_subjects(theme, query)`

### Telegram Bot (Optional)

Mobile approval workflow via Telegram. Sends notifications with inline Approve/Reject buttons when steps complete. Disabled by default — enable with `TELEGRAM_ENABLED=true` in `.env`.

- `backend/services/telegram_service.py` — `TelegramNotifier` class, singleton pattern via `get_telegram_notifier()`
- Bot commands: `/status`, `/projects`, `/new <subject> [theme]`
- Inline callbacks for approve, retry, and story selection
- Started/stopped via FastAPI `lifespan` in `backend/app.py`
- Notifications fired from `backend/pipeline/base.py` after step status changes
- Requires optional dependency: `uv sync --extra telegram`
- `python-telegram-bot` is imported lazily — the app runs fine without it

### Dependencies

```toml
# Core (always installed)
pyyaml>=6.0  # Character catalogs

# Optional
[project.optional-dependencies]
telegram = ["python-telegram-bot>=21.0"]
```

### Example Projects

Complete documentary examples live in `docs/examples/` (haunter, bulbasaur, charizard, pikachu) showing expected outputs at each step.
