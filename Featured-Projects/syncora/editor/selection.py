"""Choose a varied, editable starting set of scene options."""

import math

from .analyze import Scene


def recommend_scenes(scenes: list[Scene], beat_length: float) -> list[int]:
    eligible = [index for index, scene in enumerate(scenes) if scene.length >= 0.7]
    if not eligible:
        return []

    target = min(len(eligible), max(8, min(24, math.ceil(beat_length / 6))))
    source_end = max(scene.end for scene in scenes)
    edge_margin = min(5.0, source_end * 0.04)
    middle = [
        index for index in eligible
        if scenes[index].start >= edge_margin and scenes[index].end <= source_end - edge_margin
    ]
    if len(middle) >= target:
        eligible = middle
    # Still or near-black options make poor montage material. Fall back to the
    # full pool when a source genuinely has little movement.
    moving = [index for index in eligible if scenes[index].motion_score >= 0.006]
    pool = moving if len(moving) >= target else eligible
    bucket_count = min(12, max(1, math.ceil(target / 2)))

    def quality(index: int) -> float:
        scene = scenes[index]
        # The text detector is noisy on clothing and patterned backgrounds, so
        # its score is a soft penalty rather than a reason to reject everything.
        return (
            3.0 * scene.motion_score
            + 0.25 * scene.score
            + 0.025 * min(scene.length, 3.0)
            - 0.08 * scene.text_score
            - (0.25 if scene.motion_score < 0.006 and moving else 0.0)
        )

    buckets: list[list[int]] = [[] for _ in range(bucket_count)]
    for index in pool:
        bucket = min(bucket_count - 1, int(scenes[index].start / max(source_end, 1) * bucket_count))
        buckets[bucket].append(index)
    chosen: list[int] = []
    per_bucket = math.ceil(target / bucket_count)
    for bucket in buckets:
        chosen.extend(sorted(bucket, key=quality, reverse=True)[:per_bucket])
    chosen = chosen[:target]
    if len(chosen) < target:
        chosen_set = set(chosen)
        extras = sorted((index for index in pool if index not in chosen_set), key=quality, reverse=True)
        chosen.extend(extras[:target - len(chosen)])
    return sorted(chosen)
