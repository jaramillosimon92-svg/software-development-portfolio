from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import librosa
import numpy as np


@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    score: float
    text_score: float = 0.0
    motion_score: float = 0.0

    @property
    def length(self) -> float:
        return self.end - self.start


def analyze_beat(beat_path: Path) -> tuple[float, np.ndarray, float]:
    audio, sample_rate = librosa.load(str(beat_path), sr=22050, mono=True)
    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sample_rate)
    beat_times = librosa.frames_to_time(beat_frames, sr=sample_rate)
    return float(np.asarray(tempo).squeeze()), beat_times, len(audio) / sample_rate


def text_likelihood(frame: np.ndarray) -> float:
    """Estimate prominent text coverage without a cloud API or OCR dependency.

    Horizontal morphological grouping catches subtitles, credit lines, and large
    title cards even when the font is outlined or animated. The result is 0..1.
    """
    height, width = frame.shape[:2]
    scale = 640 / width
    resized = cv2.resize(frame, (640, max(1, round(height * scale))))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    # Text produces repeated strong vertical strokes arranged in horizontal rows.
    gradient = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gradient = cv2.convertScaleAbs(gradient)
    _, raw_mask = cv2.threshold(gradient, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask = raw_mask.copy()
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (17, 3)))
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3)), iterations=1)

    weighted_area = 0.0
    line_count = 0
    bottom_lines = 0
    for contour in cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
        x, y, box_w, box_h = cv2.boundingRect(contour)
        aspect = box_w / max(box_h, 1)
        relative_w = box_w / w
        relative_h = box_h / h
        if not (1.8 <= aspect <= 40 and 0.035 <= relative_w <= 0.98 and 0.012 <= relative_h <= 0.28):
            continue
        region = mask[y:y + box_h, x:x + box_w]
        fill = cv2.countNonZero(region) / max(box_w * box_h, 1)
        if fill < 0.12:
            continue
        area = relative_w * relative_h
        weighted_area += area
        line_count += 1
        if y > h * 0.58:
            bottom_lines += 1

    area_score = min(1.0, weighted_area * 5.0)
    repeated_lines = min(1.0, line_count / 5.0)
    subtitle_score = min(1.0, bottom_lines / 2.0)
    return float(max(area_score, repeated_lines * 0.75, subtitle_score * 0.8))


def analyze_scenes(video_path: Path, sample_rate: float = 2.0, exclude_text: bool = True) -> list[Scene]:
    capture = cv2.VideoCapture(str(video_path))
    fps = capture.get(cv2.CAP_PROP_FPS) or 30.0
    frame_count = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    video_length = frame_count / fps
    step = max(1, round(fps / sample_rate))

    samples: list[tuple[float, float, float, float, float, float]] = []
    previous_gray = None
    previous_hist = None
    index = 0
    while True:
        if index % step:
            # Advance through unsampled frames without transferring them to Python.
            if not capture.grab():
                break
            index += 1
            continue
        ok, frame = capture.read()
        if not ok:
            break
        small = cv2.resize(frame, (320, 180))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [32], [0, 256])
        cv2.normalize(hist, hist)
        time = index / fps
        motion = float(np.mean(cv2.absdiff(gray, previous_gray))) / 255 if previous_gray is not None else 0
        change = float(cv2.compareHist(hist, previous_hist, cv2.HISTCMP_BHATTACHARYYA)) if previous_hist is not None else 0
        contrast = float(gray.std()) / 64
        sharpness = min(float(cv2.Laplacian(gray, cv2.CV_64F).var()) / 700, 1.5)
        text_score = text_likelihood(small)
        samples.append((time, motion, change, contrast, sharpness, text_score))
        previous_gray, previous_hist = gray, hist
        index += 1
    capture.release()

    if not samples:
        raise RuntimeError("No frames could be read from the source video.")

    boundaries = [0.0]
    last_boundary = 0.0
    for time, _, change, _, _, _ in samples:
        if change > 0.38 and time - last_boundary >= 1.0:
            boundaries.append(time)
            last_boundary = time
    boundaries.append(video_length)

    scenes: list[Scene] = []
    half_sample = 0.5 / sample_rate

    def add_scene(scene_start: float, scene_end: float, scene_values: list[tuple[float, float, float, float, float, float]]) -> None:
        if scene_end - scene_start < 0.75 or not scene_values:
            return
        motion = np.mean([row[1] for row in scene_values])
        change = np.mean([row[2] for row in scene_values])
        contrast = np.mean([row[3] for row in scene_values])
        sharpness = np.mean([row[4] for row in scene_values])
        # A percentile ignores a single false-positive frame while sustained
        # subtitles/credits are removed as time ranges below.
        scene_text = float(np.percentile([row[5] for row in scene_values], 80))
        score = float(0.48 * motion + 0.22 * change + 0.15 * contrast + 0.15 * sharpness)
        scenes.append(Scene(scene_start, scene_end, score, scene_text))

    for start, end in zip(boundaries, boundaries[1:]):
        if end - start < 0.75:
            continue
        values = [row for row in samples if start <= row[0] < end]
        if not values:
            continue

        raw_text = [row[5] >= 0.38 for row in values]
        # Require text in adjacent samples (roughly one second). This avoids
        # mistaking a patterned shirt, jewelry, or background edges for captions.
        confirmed_text = [
            flagged and ((index > 0 and raw_text[index - 1]) or (index + 1 < len(raw_text) and raw_text[index + 1]))
            for index, flagged in enumerate(raw_text)
        ]
        if not exclude_text:
            add_scene(start, end, values)
            continue
        if not any(confirmed_text):
            add_scene(start, end, values)
            continue

        # Keep clean portions on both sides of subtitle/credit intervals instead
        # of discarding the entire visual scene.
        run: list[tuple[float, float, float, float, float, float]] = []
        for index, row in enumerate(values):
            if confirmed_text[index]:
                if run:
                    add_scene(max(start, run[0][0] - half_sample), min(end, run[-1][0] + half_sample), run)
                    run = []
            else:
                run.append(row)
        if run:
            add_scene(max(start, run[0][0] - half_sample), min(end, run[-1][0] + half_sample), run)
    return scenes
