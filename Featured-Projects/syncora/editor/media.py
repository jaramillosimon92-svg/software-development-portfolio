from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path


def require_program(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"{name} was not found. Install it and restart the app.")


def run(command: list[str]) -> None:
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode != 0:
        lines = completed.stderr.strip().splitlines() if completed.stderr else []
        message = "\n".join(lines[-12:]) if lines else "Unknown error"
        raise RuntimeError(f"Media command failed: {message}")


def duration(path: Path) -> float:
    completed = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        text=True,
        capture_output=True,
        check=True,
    )
    return float(json.loads(completed.stdout)["format"]["duration"])


def audio_sample(video: Path, destination: Path, seconds: float = 15.0) -> Path:
    """Make a small, broadly supported audio preview from the rendered video."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f"{destination.stem}.{uuid.uuid4().hex}.part{destination.suffix}")
    try:
        run([
            "ffmpeg", "-y", "-i", str(video), "-t", str(seconds),
            "-map", "0:a:0", "-vn", "-c:a", "libmp3lame", "-b:a", "192k", str(temporary),
        ])
        if temporary.stat().st_size == 0:
            raise RuntimeError("The audio preview was empty.")
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def download_video(url: str, destination: Path) -> Path:
    """Download a user-authorized source using yt-dlp."""
    destination.mkdir(parents=True, exist_ok=True)
    template = str(destination / "source.%(ext)s")
    run([
        sys.executable, "-m", "yt_dlp",
        "--no-playlist",
        "--restrict-filenames",
        "-f", "bv*[height<=1080]+ba/b[height<=1080]",
        "--merge-output-format", "mp4",
        "-o", template,
        url,
    ])
    candidates = sorted(destination.glob("source.*"))
    if not candidates:
        raise RuntimeError("The source video could not be downloaded.")
    return candidates[0]
