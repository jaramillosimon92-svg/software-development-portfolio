import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import cv2

from editor.analyze import Scene, analyze_scenes
from editor.media import audio_sample
from editor.overlay import centered_logo_score
from editor.preview import export_preview
from editor.render import build_scene_reel, build_timeline, render_montage
from editor.selection import recommend_scenes


def probe(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames,width,height,duration", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)["streams"][0]


class RenderPreviewTests(unittest.TestCase):
    def test_known_center_overlay_is_detected(self):
        reference = cv2.imread(str(Path(__file__).resolve().parents[1] / "editor" / "assets" / "drehtv_logo_reference.png"), cv2.IMREAD_GRAYSCALE)
        square = np.zeros((180, 180, 3), dtype=np.uint8)
        square[62:112, 78:105] = cv2.cvtColor(reference, cv2.COLOR_GRAY2BGR)
        self.assertGreater(centered_logo_score(square), 0.70)
        self.assertLess(centered_logo_score(np.zeros_like(square)), 0.70)

    def test_failed_audio_check_keeps_existing_sample_and_removes_partial_file(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            target = Path(directory) / "audio_check.mp3"
            target.write_bytes(b"existing sample")

            def fail_after_creating_partial(command):
                Path(command[-1]).write_bytes(b"partial")
                raise RuntimeError("Conversion failed")

            with patch("editor.media.run", side_effect=fail_after_creating_partial):
                with self.assertRaisesRegex(RuntimeError, "Conversion failed"):
                    audio_sample(Path(directory) / "video.mp4", target)
            self.assertEqual(target.read_bytes(), b"existing sample")
            self.assertEqual(list(Path(directory).glob("*.part.mp3")), [])

    def test_recommendations_are_varied_when_text_detector_is_noisy(self):
        scenes = [Scene(index * 2, index * 2 + 1.8, 0.4, 0.8, 0.04) for index in range(40)]
        picks = recommend_scenes(scenes, 140)
        self.assertEqual(len(picks), 24)
        self.assertLess(min(picks), 5)
        self.assertGreater(max(picks), 34)

    def test_scene_reel_includes_every_selection_without_padding(self):
        scenes = [Scene(index * 3, index * 3 + 1.5, 0.4) for index in range(15)]
        reel = build_scene_reel(scenes)
        self.assertEqual(len(reel), len(scenes))
        self.assertTrue(all(source_length == output_length for _, source_length, output_length in reel))
        self.assertLessEqual(sum(item[2] for item in reel), 24)

    def test_missing_intro_beats_do_not_create_a_long_hold(self):
        scenes = [Scene(0, 3, 0.5), Scene(4, 6, 0.4)]
        beats = np.array([13.93, 14.53, 15.16, 15.79, 16.39, 17.04, 17.69, 18.34, 18.99])
        timeline = build_timeline(scenes, beats, 20.0, manual_selection=True)
        self.assertAlmostEqual(sum(clip[2] for clip in timeline), 20.0)
        self.assertLessEqual(max(clip[2] for clip in timeline), 3.0)
        self.assertLessEqual(max(clip[2] - clip[1] for clip in timeline), 0.05 + 1e-6)
        self.assertGreater(len(timeline), 7)

    def test_rendered_clips_preserve_timing_without_long_freezes(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            root = Path(directory)
            source, beat, output = root / "source.mp4", root / "beat.wav", root / "draft.mp4"
            subprocess.run([
                "ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=160x90:rate=30:duration=1.5",
                "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(source),
            ], check=True)
            subprocess.run([
                "ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=440:duration=4.2", str(beat),
            ], check=True)
            self.assertTrue(analyze_scenes(source))
            events = []
            timeline = [(0 if index % 2 == 0 else 0.6, 0.6, 0.6) for index in range(7)]
            render_montage(source, beat, timeline, output, root, "draft", lambda fraction, message: events.append(fraction))
            self.assertEqual(probe(root / "clips_draft" / "clip_0000.mp4")["nb_frames"], "18")
            self.assertEqual(probe(root / "clips_draft" / "clip_0001.mp4")["nb_frames"], "18")
            result = probe(output)
            self.assertEqual((result["width"], result["height"]), (640, 360))
            self.assertEqual(result["nb_frames"], "126")
            self.assertEqual(events[-1], 1.0)
            sample_audio = audio_sample(output, root / "audio_check.mp3")
            audio_info = subprocess.run([
                "ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "default=nw=1", str(sample_audio),
            ], check=True, capture_output=True, text=True)
            self.assertIn("mp3", audio_info.stdout)
            short_output = root / "short_draft.mp4"
            render_montage(
                source, beat, timeline, short_output, root,
                "draft", max_duration=2.5,
            )
            self.assertEqual(probe(root / "clips_draft" / "clip_0004.mp4")["nb_frames"], "3")
            self.assertEqual(probe(short_output)["nb_frames"], "75")
            sample_output = root / "sample_1080p.mp4"
            render_montage(source, beat, timeline, sample_output, root, "1080p", max_duration=1.0)
            sample = probe(sample_output)
            self.assertEqual((sample["width"], sample["height"], sample["nb_frames"]), (1920, 1080, "30"))
            with self.assertRaisesRegex(ValueError, "freeze for too long"):
                render_montage(source, beat, [(0, 0.6, 2.0)], root / "invalid.mp4", root, "draft")
            short_beat = root / "short_beat.wav"
            subprocess.run([
                "ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=440:duration=0.5", str(short_beat),
            ], check=True)
            reel_output = root / "reel.mp4"
            render_montage(source, short_beat, timeline[:2], reel_output, root, "draft", audio_loop=True)
            self.assertEqual(probe(reel_output)["nb_frames"], "36")

    def test_preview_uses_centered_square_and_sidebars(self):
        frame = np.zeros((100, 200, 3), dtype=np.uint8)
        frame[:, :50] = (0, 0, 255)
        frame[:, 50:150] = (0, 255, 0)
        frame[:, 150:] = (255, 0, 0)
        preview = export_preview(frame)
        self.assertEqual(preview.shape, (180, 320, 3))
        self.assertTrue(np.all(preview[:, :70] == 0))
        self.assertTrue(np.all(preview[:, 70:250, 1] == 255))


if __name__ == "__main__":
    unittest.main()
