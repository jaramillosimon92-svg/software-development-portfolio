from __future__ import annotations

import random
import math
from pathlib import Path
from collections.abc import Callable

import numpy as np

from .analyze import Scene
from .media import duration, run


def build_timeline(
    scenes: list[Scene],
    beat_times: np.ndarray,
    audio_length: float,
    manual_selection: bool = False,
) -> list[tuple[float, float, float]]:
    if manual_selection:
        usable = [scene for scene in scenes if scene.length >= 0.70]
        if not usable:
            raise RuntimeError("Select at least one usable scene.")
    else:
        usable = _automatic_scene_pool(scenes)
    rng = random.Random(24)
    rng.shuffle(usable)
    # Never ask a scene to fill more time than it contains. The extra small
    # margin covers timestamp/frame rounding without producing a visible hold.
    max_shot_length = min(3.0, max(scene.length - 0.05 for scene in usable))

    anchors = [0.0]
    if len(beat_times) >= 5:
        # Four-beat phrases give a music-video pace while keeping every cut on-grid.
        anchors.extend(float(value) for value in beat_times[4::4] if value < audio_length - 1)
    else:
        anchors.extend(np.arange(4.0, audio_length, 4.0).tolist())
    anchors.append(audio_length)

    # Beat tracking can miss a quiet intro (or a break). Fill those gaps with
    # extra cuts so a single short scene cannot freeze for many seconds.
    spaced_anchors = [anchors[0]]
    for end in anchors[1:]:
        start = spaced_anchors[-1]
        divisions = max(1, math.ceil((end - start) / max_shot_length))
        spaced_anchors.extend(start + (end - start) * part / divisions for part in range(1, divisions))
        spaced_anchors.append(end)

    result: list[tuple[float, float, float]] = []
    for index, (out_start, out_end) in enumerate(zip(spaced_anchors, spaced_anchors[1:])):
        needed = out_end - out_start
        candidates = [scene for scene in usable if scene.length >= needed]
        scene = candidates[index % len(candidates)] if candidates else max(usable, key=lambda item: item.length)
        source_length = min(needed, max(0.2, scene.length - 0.05))
        safe_scene_start = scene.start
        offset_room = max(0, scene.length - source_length)
        source_start = safe_scene_start + (offset_room * ((index * 0.37) % 1))
        result.append((source_start, source_length, needed))
    return result


def build_scene_reel(scenes: list[Scene]) -> list[tuple[float, float, float]]:
    """A short review clip that includes every selected scene exactly once."""
    usable = [scene for scene in scenes if scene.length >= 0.70]
    if not usable:
        raise RuntimeError("Select at least one usable scene.")
    target_length = max(0.70, min(1.4, 24.0 / len(usable)))
    result = []
    for scene in usable:
        length = min(target_length, scene.length - 0.05)
        start = scene.start + max(0, scene.length - length) / 2
        result.append((start, length, length))
    return result


def _automatic_scene_pool(scenes: list[Scene]) -> list[Scene]:
    # Very low visual scores are fades or nearly blank frames. Never build a
    # montage from them, even when they are technically text-free.
    visible_scenes = [scene for scene in scenes if scene.score >= 0.025]
    clean_scenes = [
        scene for scene in visible_scenes
        if scene.text_score < 0.38
        and not (scene.start < 8.0 and scene.text_score >= 0.10)
    ]
    # A detector must never turn a valid source into an all-black render. If it
    # flags everything, fall back to the least text-like visible scenes while
    # still avoiding common opening and closing credit regions.
    if not clean_scenes:
        video_end = max((scene.end for scene in scenes), default=0.0)
        middle = [scene for scene in visible_scenes if scene.start >= 8.0 and scene.end <= video_end - 4.0]
        fallback_pool = middle or visible_scenes
        clean_scenes = sorted(fallback_pool, key=lambda scene: (scene.text_score, -scene.score))[: max(6, len(fallback_pool) // 3)]
    ranked = sorted(clean_scenes, key=lambda scene: scene.score, reverse=True)
    # Keep most clean scenes for variety, while dropping only the weakest tail.
    keep = min(len(ranked), max(24, math.ceil(len(ranked) * 0.80)))
    usable = ranked[:keep]
    if not usable:
        raise RuntimeError("No visible scenes were detected in this source video.")
    return usable


def render_montage(
    source: Path,
    beat: Path,
    timeline: list[tuple[float, float, float]],
    output: Path,
    work: Path,
    quality: str = "1080p",
    on_progress: Callable[[float, str], None] | None = None,
    max_duration: float | None = None,
    audio_loop: bool = False,
) -> None:
    if not timeline:
        raise ValueError("The timeline is empty.")
    if max_duration is not None:
        if max_duration <= 0:
            raise ValueError("Preview duration must be positive.")
        shortened = []
        remaining = max_duration
        for start, source_length, output_length in timeline:
            if remaining <= 0:
                break
            used = min(output_length, remaining)
            shortened.append((start, min(source_length, used), used))
            remaining -= used
        timeline = shortened
    if quality == "draft":
        canvas_width, canvas_height, square_size = 640, 360, 360
    elif quality == "1440p":
        canvas_width, canvas_height, square_size = 2560, 1440, 1440
    elif quality == "1080p":
        canvas_width, canvas_height, square_size = 1920, 1080, 1080
    else:
        raise ValueError(f"Unsupported render quality: {quality}")
    preset, crf = ("ultrafast", "28") if quality == "draft" else ("veryfast", "19")
    clips = work / f"clips_{quality}"
    clips.mkdir(parents=True, exist_ok=True)
    clip_paths: list[Path] = []
    elapsed = 0.0
    previous_frame = 0
    for index, (start, source_length, output_length) in enumerate(timeline):
        if start < 0 or source_length <= 0 or output_length <= 0:
            raise ValueError("Timeline clips must have positive durations and nonnegative start times.")
        if output_length - source_length > 0.12:
            raise ValueError("A timeline clip would freeze for too long. Rebuild the timeline from the selected scenes.")
        # Quantize absolute cut positions, so rounding never accumulates across clips.
        elapsed += output_length
        end_frame = round(elapsed * 30)
        frame_count = end_frame - previous_frame
        previous_frame = end_frame
        if frame_count <= 0:
            continue
        target = clips / f"clip_{index:04d}.mp4"
        if on_progress:
            on_progress(0.9 * index / len(timeline), f"Rendering clip {index + 1} of {len(timeline)}")
        run([
            "ffmpeg", "-y", "-ss", f"{start:.6f}", "-i", str(source),
            "-an", "-vf", f"trim=duration={source_length:.6f},setpts=PTS-STARTPTS,scale={square_size}:{square_size}:force_original_aspect_ratio=increase,crop={square_size}:{square_size},pad={canvas_width}:{canvas_height}:(ow-iw)/2:0:black,setsar=1,fps=30,tpad=stop_mode=clone:stop=-1,trim=end_frame={frame_count}",
            "-frames:v", str(frame_count), "-c:v", "libx264", "-preset", preset, "-crf", crf, "-pix_fmt", "yuv420p", str(target),
        ])
        clip_paths.append(target)

    concat_file = clips / "concat.txt"
    concat_file.write_text("".join(f"file '{path.resolve().as_posix()}'\n" for path in clip_paths), encoding="utf-8")
    if not clip_paths:
        raise ValueError("The timeline is shorter than one video frame.")
    silent = work / f"silent_montage_{quality}.mp4"
    if on_progress:
        on_progress(0.9, "Assembling clips")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(silent)])
    output.parent.mkdir(parents=True, exist_ok=True)
    beat_length = sum(item[2] for item in timeline) if audio_loop else min(duration(beat), sum(item[2] for item in timeline))
    if on_progress:
        on_progress(0.95, "Adding your beat")
    audio_input = ["-stream_loop", "-1"] if audio_loop else []
    run([
        "ffmpeg", "-y", "-i", str(silent), *audio_input, "-i", str(beat), "-map", "0:v:0", "-map", "1:a:0",
        "-t", f"{beat_length:.6f}", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", str(output),
    ])
    if on_progress:
        on_progress(1.0, "Finished")
