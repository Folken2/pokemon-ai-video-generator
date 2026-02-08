"""
Subject catalog service.
Loads curated subject lists per theme from YAML files with search/filter support.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from backend.config import DATA_DIR


@lru_cache(maxsize=8)
def load_catalog(theme: str) -> list[dict[str, Any]]:
    """Load the subject catalog for a theme. Returns empty list if file missing."""
    catalog_path = DATA_DIR / "subjects" / f"{theme}.yaml"
    if not catalog_path.exists():
        return []
    data = yaml.safe_load(catalog_path.read_text())
    return data.get("subjects", [])


def search_subjects(theme: str, query: str = "") -> list[dict[str, Any]]:
    """Search subjects by name, tags, or description. Returns all if query is empty."""
    subjects = load_catalog(theme)
    if not query:
        return subjects

    q = query.lower()
    results = []
    for s in subjects:
        # Match against name, display_name, tags, description
        if (q in s.get("name", "").lower()
                or q in s.get("display_name", "").lower()
                or any(q in tag.lower() for tag in s.get("tags", []))
                or q in s.get("description", "").lower()):
            results.append(s)
    return results
