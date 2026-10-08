"""Short-lived, local project state for surviving Streamlit session resets."""

from __future__ import annotations

import json
import hashlib
import os
import shutil
import time
import uuid
from dataclasses import asdict
from pathlib import Path

import numpy as np

from .analyze import Scene


PROJECT_TTL_SECONDS = 6 * 60 * 60
MANIFEST = "project.json"
EXPORT_PREFIXES = ("syncora_", "video_studio_", "cold_beatz_")  # Retain legacy exports until their projects expire.
LEGACY_SUGGESTED_DESCRIPTION_HASH = "f25557d3113fcb32e8bab6d1376e5acec53ff73a989bc0d80c5279fb196e50b4"


def is_legacy_suggestion(value: object) -> bool:
    return isinstance(value, str) and hashlib.sha256(value.encode("utf-8")).hexdigest() == LEGACY_SUGGESTED_DESCRIPTION_HASH


def remove_legacy_description(work: Path) -> int:
    """Remove the old bundled description from saved jobs without losing custom text."""
    if not work.exists():
        return 0
    changed = 0
    for manifest in work.glob(f"*/{MANIFEST}"):
        if not _inside(manifest.parent, work):
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            settings = data.get("settings")
            if not isinstance(settings, dict):
                continue
            previous = settings.pop("video_description", None)
            saved = settings.get("saved_description_draft")
            old_saved = is_legacy_suggestion(saved)
            if old_saved:
                settings.pop("saved_description_draft")
                saved = None
            if not saved and isinstance(previous, str) and previous and not is_legacy_suggestion(previous):
                settings["saved_description_draft"] = previous
            if previous is not None or old_saved:
                temporary = manifest.with_name(f".{MANIFEST}.{uuid.uuid4().hex}.tmp")
                try:
                    temporary.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
                    os.replace(temporary, manifest)
                    changed += 1
                finally:
                    temporary.unlink(missing_ok=True)
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            continue
    return changed


def _inside(path: Path, parent: Path) -> bool:
    return path.resolve().parent == parent.resolve()


def save_project(
    work: Path,
    outputs: Path,
    analysis: dict,
    selected: list[int],
    draft: str | None = None,
    draft_selection: tuple[tuple[int, ...], str] | None = None,
    output: str | None = None,
    stats: dict | None = None,
    settings: dict | None = None,
) -> None:
    job = Path(analysis["job"])
    if not _inside(job, work):
        raise ValueError("Project job must be inside the work folder.")
    source = Path(analysis["source"])
    beat = Path(analysis["beat"])
    if not _inside(source, job) or not _inside(beat, job):
        raise ValueError("Project media must be inside its job folder.")
    if draft and not _inside(Path(draft), job):
        raise ValueError("Draft must be inside its job folder.")
    if output and not _inside(Path(output), outputs):
        raise ValueError("Export must be inside the outputs folder.")
    thumbnails = [str(Path(item)) for item in analysis["thumbnails"]]
    if any(not _inside(Path(item), job / "previews") for item in thumbnails):
        raise ValueError("Scene thumbnails must be inside the job folder.")
    target = job / MANIFEST
    try:
        previous = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        previous = {}
    exports = {
        item for item in [*previous.get("exports", []), previous.get("output"), output]
        if isinstance(item, str) and _inside(Path(item), outputs) and Path(item).name.startswith(EXPORT_PREFIXES)
    }
    data = {
        "version": 1,
        "updated_at": time.time(),
        "source": str(source),
        "beat": str(beat),
        "tempo": float(analysis["tempo"]),
        "beats": [float(value) for value in analysis["beats"]],
        "beat_length": float(analysis["beat_length"]),
        "scenes": [asdict(scene) for scene in analysis["scenes"]],
        "thumbnails": thumbnails,
        "excluded": int(analysis.get("excluded", 0)),
        "selected": selected,
        "draft": draft if draft and Path(draft).is_file() else None,
        "draft_selection": [list(draft_selection[0]), draft_selection[1]] if draft_selection else None,
        "output": output if output and Path(output).is_file() else None,
        "exports": sorted(exports),
        "stats": stats or {},
        "settings": settings or {},
    }
    temporary = job / f".{MANIFEST}.{uuid.uuid4().hex}.tmp"
    try:
        temporary.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def load_project(job: Path, work: Path, outputs: Path, now: float | None = None) -> dict | None:
    if not _inside(job, work):
        return None
    manifest = job / MANIFEST
    if not manifest.is_file():
        return None
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if data.get("version") != 1 or (time.time() if now is None else now) - float(data["updated_at"]) > PROJECT_TTL_SECONDS:
            return None
        source, beat = Path(data["source"]), Path(data["beat"])
        if not all(_inside(path, job) and path.is_file() for path in (source, beat)):
            return None
        thumbnails = [Path(item) for item in data["thumbnails"]]
        scenes = [Scene(**item) for item in data["scenes"]]
        if len(thumbnails) != len(scenes) or not all(_inside(path, job / "previews") and path.is_file() for path in thumbnails):
            return None
        selected = [int(index) for index in data.get("selected", []) if 0 <= int(index) < len(scenes)]
        draft = data.get("draft")
        if draft and not (_inside(Path(draft), job) and Path(draft).is_file()):
            draft = None
        output = data.get("output")
        if output and not (_inside(Path(output), outputs) and Path(output).is_file()):
            output = None
        saved_draft_selection = data.get("draft_selection")
        draft_selection = (tuple(saved_draft_selection[0]), saved_draft_selection[1]) if draft and saved_draft_selection else None
        return {
            "analysis": {
                "job": str(job), "source": str(source), "beat": str(beat),
                "tempo": float(data["tempo"]), "beats": np.asarray(data["beats"], dtype=float),
                "beat_length": float(data["beat_length"]), "scenes": scenes,
                "thumbnails": [str(path) for path in thumbnails], "excluded": int(data.get("excluded", 0)),
            },
            "selected": selected,
            "draft": draft,
            "draft_selection": draft_selection,
            "output": output,
            "stats": data.get("stats", {}),
            "settings": data.get("settings", {}),
            "updated_at": float(data["updated_at"]),
        }
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None


def recent_projects(work: Path, outputs: Path, now: float | None = None) -> list[dict]:
    if not work.exists():
        return []
    projects = []
    for manifest in work.glob(f"*/{MANIFEST}"):
        project = load_project(manifest.parent, work, outputs, now)
        if project:
            projects.append(project)
    return sorted(projects, key=lambda item: item["updated_at"], reverse=True)


def cleanup_expired(work: Path, outputs: Path, now: float | None = None) -> int:
    """Remove expired app-owned jobs and only their recorded export files."""
    if not work.exists():
        return 0
    now = time.time() if now is None else now
    removed = 0
    for manifest in work.glob(f"*/{MANIFEST}"):
        job = manifest.parent
        if not _inside(job, work):
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if data.get("version") != 1 or now - float(data["updated_at"]) <= PROJECT_TTL_SECONDS:
                continue
            for output in [*data.get("exports", []), data.get("output")]:
                if not isinstance(output, str):
                    continue
                export = Path(output)
                if _inside(export, outputs) and export.name.startswith(EXPORT_PREFIXES):
                    export.unlink(missing_ok=True)
            shutil.rmtree(job)
            removed += 1
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
            continue
    return removed
