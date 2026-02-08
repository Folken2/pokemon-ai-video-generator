"""
FastAPI Application Entry Point
AI Documentary Pipeline - Backend Server

Run with: uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from contextlib import asynccontextmanager

from backend.config import API_KEY, FRONTEND_DIR, HOST, PORT, PROJECT_ROOT, TELEGRAM_ENABLED, validate_api_keys


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Require X-API-Key header on /api/ and /files/ routes when API_KEY is set."""

    async def dispatch(self, request: Request, call_next):
        if not API_KEY:
            return await call_next(request)

        path = request.url.path

        # Exempt: health check, frontend, static assets, docs
        if path.startswith("/api/health"):
            return await call_next(request)
        if path.startswith("/api/") or path.startswith("/files/"):
            key = request.headers.get("X-API-Key", "")
            if key != API_KEY:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid or missing API key"},
                )
        return await call_next(request)


from backend.routers import pipeline, projects

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start/stop optional services (e.g. Telegram bot)."""
    notifier = None
    if TELEGRAM_ENABLED:
        try:
            from backend.services.telegram_service import TelegramNotifier, set_telegram_notifier
            notifier = TelegramNotifier()
            await notifier.start()
            set_telegram_notifier(notifier)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Telegram bot failed to start: {e}")
    yield
    if notifier:
        await notifier.stop()


# --- App ---
app = FastAPI(
    title="AI Documentary Pipeline",
    description="Multi-theme automated video generation pipeline with human-in-the-loop approval",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key auth (no-op when API_KEY is not set)
app.add_middleware(APIKeyMiddleware)

# --- Routers ---
app.include_router(projects.router)
app.include_router(pipeline.router)

# --- Static file serving for generated assets ---
# Serve the project directories (for image/video/audio previews)
app.mount("/files", StaticFiles(directory=str(PROJECT_ROOT)), name="project_files")

# Serve frontend static files
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend_static")


# --- Frontend ---
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the main frontend page."""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        html = index_path.read_text()
        if API_KEY:
            # Inject API key so frontend can authenticate requests
            script_tag = f'<script>window.__API_KEY__="{API_KEY}";</script>'
            html = html.replace("</head>", f"{script_tag}</head>", 1)
        return HTMLResponse(content=html)
    return HTMLResponse(content="""
        <html><body>
        <h1>AI Documentary Pipeline</h1>
        <p>Frontend not found. Place index.html in frontend/ directory.</p>
        <p><a href="/docs">API Documentation</a></p>
        </body></html>
    """)


# --- Health & Config ---
@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "api_keys": validate_api_keys(),
    }


def main():
    """Entry point for the pipeline server."""
    import uvicorn
    uvicorn.run("backend.app:app", host=HOST, port=PORT, reload=True)


if __name__ == "__main__":
    main()
