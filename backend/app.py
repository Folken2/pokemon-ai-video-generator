"""
FastAPI Application Entry Point
Pokemon AI Documentary Pipeline - Backend Server

Run with: uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.config import FRONTEND_DIR, HOST, PORT, PROJECT_ROOT, validate_api_keys
from backend.routers import pipeline, projects

# --- App ---
app = FastAPI(
    title="Pokemon AI Documentary Pipeline",
    description="Automated video generation pipeline with human-in-the-loop approval",
    version="1.0.0",
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        return HTMLResponse(content=index_path.read_text())
    return HTMLResponse(content="""
        <html><body>
        <h1>Pokemon AI Documentary Pipeline</h1>
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
