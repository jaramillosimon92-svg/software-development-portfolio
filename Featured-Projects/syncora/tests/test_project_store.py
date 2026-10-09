import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from editor.analyze import Scene
from editor.project_store import PROJECT_TTL_SECONDS, cleanup_expired, load_project, recent_projects, remove_legacy_description, save_project, workspace_paths


class ProjectStoreTests(unittest.TestCase):
    def test_workspace_paths_are_isolated_and_reject_unsafe_ids(self):
        root = Path("app_root")
        first_work, first_outputs = workspace_paths(root, "a" * 32)
        second_work, second_outputs = workspace_paths(root, "b" * 32)
        self.assertNotEqual(first_work, second_work)
        self.assertNotEqual(first_outputs, second_outputs)
        self.assertEqual(first_work, root / "work" / ("a" * 32))
        with self.assertRaisesRegex(ValueError, "Invalid workspace ID"):
            workspace_paths(root, "../shared")

    def test_old_suggested_description_is_removed_but_custom_text_is_kept(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            work = Path(directory) / "work"
            old_job, custom_job = work / "old", work / "custom"
            old_job.mkdir(parents=True)
            custom_job.mkdir()
            old_text = "legacy placeholder"
            (old_job / "project.json").write_text(json.dumps({"settings": {"video_description": old_text, "saved_description_draft": old_text}}), encoding="utf-8")
            (custom_job / "project.json").write_text(json.dumps({"settings": {"video_description": "My own words"}}), encoding="utf-8")
            with patch("editor.project_store.LEGACY_SUGGESTED_DESCRIPTION_HASH", hashlib.sha256(old_text.encode()).hexdigest()):
                self.assertEqual(remove_legacy_description(work), 2)
            old_settings = json.loads((old_job / "project.json").read_text(encoding="utf-8"))["settings"]
            custom_settings = json.loads((custom_job / "project.json").read_text(encoding="utf-8"))["settings"]
            self.assertEqual(old_settings, {})
            self.assertEqual(custom_settings, {"saved_description_draft": "My own words"})

    def test_project_survives_a_new_session_with_scene_choices_and_media(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            root = Path(directory)
            work, outputs = root / "work", root / "outputs"
            job = work / "job_1"
            previews = job / "previews"
            previews.mkdir(parents=True)
            outputs.mkdir()
            source, beat, draft, export = job / "source.mp4", job / "beat.wav", job / "draft.mp4", outputs / "syncora_result.mp4"
            thumb = previews / "scene_0000.jpg"
            for path in (source, beat, draft, export, thumb):
                path.write_bytes(b"media")
            analysis = {
                "job": str(job), "source": str(source), "beat": str(beat), "tempo": 95.0,
                "beats": np.array([0.5, 1.1]), "beat_length": 24.0,
                "scenes": [Scene(1.0, 2.5, 0.7)], "thumbnails": [str(thumb)], "excluded": 1,
            }
            save_project(
                work, outputs, analysis, [0], str(draft), ((0,), "All selected scenes"),
                str(export), {"clips": 3},
                {"draft_length": "All selected scenes", "saved_description_draft": "My own video description"},
            )
            loaded = load_project(job, work, outputs)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded["selected"], [0])
            self.assertEqual(loaded["analysis"]["scenes"], analysis["scenes"])
            self.assertEqual(loaded["analysis"]["beats"].tolist(), [0.5, 1.1])
            self.assertEqual(loaded["draft_selection"], ((0,), "All selected scenes"))
            self.assertEqual(loaded["output"], str(export))
            self.assertEqual(loaded["settings"]["saved_description_draft"], "My own video description")
            self.assertEqual(len(recent_projects(work, outputs)), 1)

    def test_cleanup_deletes_only_expired_recorded_project_files(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            root = Path(directory)
            work, outputs = root / "work", root / "outputs"
            job = work / "old_job"
            job.mkdir(parents=True)
            outputs.mkdir()
            export = outputs / "syncora_old.mp4"
            older_export = outputs / "video_studio_older.mp4"
            oldest_export = outputs / "cold_beatz_oldest.mp4"
            unrelated = outputs / "keep.mp4"
            untracked = work / "untracked"
            untracked.mkdir()
            export.write_bytes(b"old")
            older_export.write_bytes(b"older")
            oldest_export.write_bytes(b"oldest")
            unrelated.write_bytes(b"keep")
            (untracked / "source.mp4").write_bytes(b"keep")
            (job / "project.json").write_text(json.dumps({"version": 1, "updated_at": 100.0, "output": str(export), "exports": [str(older_export), str(oldest_export)]}), encoding="utf-8")
            with patch("editor.project_store.time.time", return_value=100.0 + PROJECT_TTL_SECONDS + 1):
                self.assertEqual(cleanup_expired(work, outputs), 1)
            self.assertFalse(job.exists())
            self.assertFalse(export.exists())
            self.assertFalse(older_export.exists())
            self.assertFalse(oldest_export.exists())
            self.assertTrue(unrelated.exists())
            self.assertTrue(untracked.exists())


if __name__ == "__main__":
    unittest.main()
