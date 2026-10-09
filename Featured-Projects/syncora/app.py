from __future__ import annotations

import math
import time
import uuid
from pathlib import Path

import cv2
import streamlit as st

from editor.analyze import Scene, analyze_beat, analyze_scenes, text_likelihood
from editor.media import audio_sample, require_program
from editor.render import build_scene_reel, build_timeline, render_montage
from editor.preview import export_preview
from editor.overlay import centered_logo_score
from editor.project_store import cleanup_expired, is_legacy_suggestion, recent_projects, remove_legacy_description, save_project
from editor.selection import recommend_scenes
from editor.ui import render_hero, section_heading
from editor.youtube_upload import upload_video

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work"
OUTPUTS = ROOT / "outputs"

st.set_page_config(page_title="Syncora", page_icon=":material/graphic_eq:", layout="wide")


def reset_project() -> None:
    next_upload_key = int(st.session_state.get("project_nonce", 0)) + 1
    for key in list(st.session_state):
        if key.startswith(("scene_pick_", "source_upload_", "beat_upload_")) or key in {
            "analysis", "output", "stats", "uploaded_url", "draft", "draft_audio", "draft_selection", "source_upload", "beat_upload", "rights",
            "video_title", "video_description", "saved_description_draft", "description_just_saved", "privacy", "output_quality", "playlist_input", "playlist_status", "draft_length", "export_length",
        }:
            st.session_state.pop(key, None)
    st.session_state["project_nonce"] = next_upload_key
    st.session_state["skip_restore"] = True


def return_to_scenes() -> None:
    for key in ["output", "stats", "uploaded_url"]:
        st.session_state.pop(key, None)


def restore_project(project: dict) -> None:
    reset_project()
    analysis = project["analysis"]
    st.session_state["analysis"] = analysis
    st.session_state["skip_restore"] = False
    for index in range(len(analysis["scenes"])):
        st.session_state[f"scene_pick_{index}"] = index in project["selected"]
    if project["draft"]:
        st.session_state["draft"] = project["draft"]
        st.session_state["draft_selection"] = project["draft_selection"]
    if project["output"]:
        st.session_state["output"] = project["output"]
        st.session_state["stats"] = project["stats"]
    allowed_settings = {"rights", "draft_length", "output_quality", "export_length", "video_title", "privacy", "playlist_input"}
    for key, value in project["settings"].items():
        if key in allowed_settings:
            st.session_state[key] = value
    saved_description = project["settings"].get("saved_description_draft", "")
    if is_legacy_suggestion(saved_description):
        saved_description = ""
    st.session_state["saved_description_draft"] = saved_description
    st.session_state["video_description"] = saved_description


def persist_current_project() -> None:
    analysis = st.session_state.get("analysis")
    if not analysis:
        return
    settings = {
        key: st.session_state[key]
        for key in ("rights", "draft_length", "output_quality", "export_length", "video_title", "saved_description_draft", "privacy", "playlist_input")
        if key in st.session_state
    }
    save_project(
        WORK, OUTPUTS, analysis,
        [index for index in range(len(analysis["scenes"])) if st.session_state.get(f"scene_pick_{index}", False)],
        st.session_state.get("draft"), st.session_state.get("draft_selection"),
        st.session_state.get("output"), st.session_state.get("stats"), settings,
    )


def save_description_draft() -> None:
    description = st.session_state.get("video_description", "").strip()
    if description:
        st.session_state["saved_description_draft"] = description
        st.session_state["description_just_saved"] = True
        persist_current_project()


def restore_description_draft() -> None:
    st.session_state["video_description"] = st.session_state.get("saved_description_draft", "")


def format_time(seconds: float) -> str:
    minutes, remainder = divmod(max(0, int(seconds)), 60)
    return f"{minutes}:{remainder:02d}"


def preview_audio(video: Path, stored_path: str | None) -> str:
    """Refresh older AAC check files as MP3s for in-app playback."""
    target = Path(stored_path).with_suffix(".mp3") if stored_path else video.with_name(f"{video.stem}_audio.mp3")
    if not target.exists() or target.stat().st_size == 0:
        audio_sample(video, target)
    return str(target)


def show_audio_check(video: Path, stored_path: str | None = None) -> None:
    with st.expander("Check the rendered beat audio"):
        try:
            st.audio(preview_audio(video, stored_path), format="audio/mpeg")
            st.caption("This audio comes from the rendered video. If the video is silent, check its speaker control and the browser tab's sound setting.")
        except Exception as exc:
            st.caption(f"The separate audio check is unavailable: {exc}. The video preview and download are still ready.")


def split_scene_options(scenes: list[Scene], maximum_length: float = 4.0) -> list[Scene]:
    options: list[Scene] = []
    for scene in scenes:
        count = max(1, math.ceil(scene.length / maximum_length))
        chunk_length = scene.length / count
        for index in range(count):
            start = scene.start + index * chunk_length
            end = min(scene.end, start + chunk_length)
            if end - start >= 0.70:
                options.append(Scene(start, end, scene.score, scene.text_score, scene.motion_score))
    return options


def create_preview_gallery(source: Path, scenes: list[Scene], folder: Path) -> tuple[list[Scene], list[str], int]:
    folder.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(source))
    updated: list[Scene] = []
    thumbnails: list[str] = []
    excluded = 0
    for index, scene in enumerate(scenes):
        frames = []
        text_scores = []
        logo_scores = []
        for fraction in (0.15, 0.38, 0.62, 0.85):
            timestamp = scene.start + scene.length * fraction
            capture.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
            ok, frame = capture.read()
            if not ok:
                continue
            preview = export_preview(frame)
            text_scores.append(text_likelihood(preview[:, 70:250]))
            logo_scores.append(centered_logo_score(preview[:, 70:250]))
            frames.append(preview)
        if not frames:
            continue
        if max(logo_scores, default=0.0) >= 0.70:
            excluded += 1
            continue
        while len(frames) < 4:
            frames.append(frames[-1].copy())
        gray = [cv2.cvtColor(frame[:, 70:250], cv2.COLOR_BGR2GRAY) for frame in frames]
        motion = sorted(
            float(cv2.mean(cv2.absdiff(first, second))[0]) / 255
            for first, second in zip(gray, gray[1:])
        )[1]
        target = folder / f"scene_{index:04d}.jpg"
        cv2.imwrite(str(target), cv2.hconcat(frames), [cv2.IMWRITE_JPEG_QUALITY, 88])
        updated.append(Scene(scene.start, scene.end, scene.score, max(text_scores, default=0.0), motion))
        thumbnails.append(str(target))
    capture.release()
    return updated, thumbnails, excluded


remove_legacy_description(WORK)
cleanup_expired(WORK, OUTPUTS)
saved_projects = recent_projects(WORK, OUTPUTS)
if not st.session_state.get("analysis") and not st.session_state.get("skip_restore") and saved_projects:
    restore_project(saved_projects[0])

render_hero(3 if st.session_state.get("output") else 2 if st.session_state.get("analysis") else 1)

with st.sidebar:
    st.markdown("### :material/graphic_eq: Syncora")
    st.caption("Your editing workspace")
    if saved_projects:
        with st.expander("Saved projects · 6 hours", icon=":material/folder_open:"):
            for project in saved_projects[:6]:
                job = Path(project["analysis"]["job"])
                label = f"{Path(project['analysis']['beat']).stem} · {time.strftime('%I:%M %p', time.localtime(project['updated_at']))}"
                if st.button(label, key=f"restore_{job.name}", width="stretch"):
                    restore_project(project)
                    st.rerun()
    st.button("Start new project", on_click=reset_project, width="stretch", icon=":material/add:")
    st.markdown("#### Source and beat")
    project_nonce = st.session_state.get("project_nonce", 0)
    source_upload = st.file_uploader(
        "Your source video",
        type=["mp4", "mov", "m4v", "mkv", "webm", "avi"],
        key=f"source_upload_{project_nonce}",
    )
    beat_upload = st.file_uploader("Your beat", type=["mp3", "wav", "m4a", "aac", "flac"], key=f"beat_upload_{project_nonce}")
    confirmed = st.checkbox("I own or have permission to reuse the source video", key="rights")
    analyze = st.button("Find scene options", type="primary", width="stretch", icon=":material/search:")

if analyze:
    if source_upload is None or not beat_upload or not confirmed:
        st.error("Add a source video and beat, then confirm you have permission to reuse the video.")
    else:
        try:
            require_program("ffmpeg")
            require_program("ffprobe")
            for key in list(st.session_state):
                if key.startswith("scene_pick_") or key in {"analysis", "output", "stats", "uploaded_url", "draft", "draft_audio", "draft_selection"}:
                    st.session_state.pop(key, None)
            job = WORK / f"{int(time.time())}_{uuid.uuid4().hex[:8]}"
            job.mkdir(parents=True, exist_ok=True)
            beat = job / Path(beat_upload.name).name
            beat.write_bytes(beat_upload.getbuffer())
            progress = st.progress(0, "Saving source video…")
            suffix = Path(source_upload.name).suffix.lower() or ".mp4"
            source = job / f"source{suffix}"
            source.write_bytes(source_upload.getbuffer())
            progress.progress(25, "Detecting the beat…")
            tempo, beats, beat_length = analyze_beat(beat)
            progress.progress(45, "Finding scene changes…")
            detected = analyze_scenes(source, exclude_text=False)
            options = split_scene_options(detected)
            progress.progress(65, "Creating scene preview strips…")
            options, thumbnails, excluded = create_preview_gallery(source, options, job / "previews")
            if not options:
                raise RuntimeError("No scene options could be created from this video.")
            st.session_state["analysis"] = {
                "job": str(job), "source": str(source), "beat": str(beat), "tempo": tempo,
                "beats": beats, "beat_length": beat_length, "scenes": options, "thumbnails": thumbnails,
                "excluded": excluded,
            }
            picks = set(recommend_scenes(options, beat_length))
            for index in range(len(options)):
                st.session_state[f"scene_pick_{index}"] = index in picks
            st.session_state["skip_restore"] = False
            persist_current_project()
            progress.progress(100, "Choose your scenes below")
        except Exception as exc:
            st.exception(exc)

analysis_data = st.session_state.get("analysis")
output_value = st.session_state.get("output")

if not analysis_data:
    legacy_drafts = sorted(
        (path for path in WORK.glob("*/draft*.mp4") if path.is_file() and path.stat().st_size > 0 and not (path.parent / "project.json").exists()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if legacy_drafts:
        latest = legacy_drafts[0]
        section_heading("Recovered draft", "Your recent preview", "A finished draft is ready from your last session.")
        st.caption("This draft was made before project saving was enabled. You can review or download it now; its scene choices were not saved.")
        st.video(str(latest), muted=False, alt="Recently generated video draft")
        with latest.open("rb") as draft_file:
            st.download_button("Download recent draft", draft_file, file_name=latest.name, mime="video/mp4")

if analysis_data and not output_value:
    scenes: list[Scene] = analysis_data["scenes"]
    thumbnails: list[str] = analysis_data["thumbnails"]
    section_heading("Step 02 · Curate", "Choose your scenes", "Find the strongest moments. Every preview shows four points from the finished crop.")
    st.caption(f"{len(scenes)} scene options found · Choose the clips you want in the edit.")
    if analysis_data.get("excluded"):
        st.caption(f"Excluded {analysis_data['excluded']} scene option(s) containing the centered DREHTV logo.")

    controls = st.columns(3, gap="medium")
    if controls[0].button("Select recommended", width="stretch", icon=":material/auto_awesome:"):
        picks = set(recommend_scenes(scenes, analysis_data["beat_length"]))
        for index, scene in enumerate(scenes):
            st.session_state[f"scene_pick_{index}"] = index in picks
    if controls[1].button("Select all", width="stretch", icon=":material/select_all:"):
        for index in range(len(scenes)):
            st.session_state[f"scene_pick_{index}"] = True
    if controls[2].button("Clear all", width="stretch", icon=":material/deselect:"):
        for index in range(len(scenes)):
            st.session_state[f"scene_pick_{index}"] = False

    columns = st.columns(3, gap="medium")
    for index, (scene, thumbnail) in enumerate(zip(scenes, thumbnails)):
        with columns[index % 3]:
            with st.container(border=True, key=f"scene_card_{index}"):
                st.image(thumbnail, width="stretch", alt=f"Preview frames for scene {index + 1}")
                label = f"Scene {index + 1} · {format_time(scene.start)}–{format_time(scene.end)}"
                st.checkbox(label, key=f"scene_pick_{index}")
                if scene.text_score >= 0.88:
                    st.caption("Check for visible text")

    selected = [scene for index, scene in enumerate(scenes) if st.session_state.get(f"scene_pick_{index}", False)]
    selection = tuple(index for index in range(len(scenes)) if st.session_state.get(f"scene_pick_{index}", False))
    draft_length = st.selectbox(
        "Quick draft view",
        ["All selected scenes", "First 20 seconds of edit", "Whole beat"],
        key="draft_length",
    )
    draft_key = (selection, draft_length)
    if st.session_state.get("draft_selection") != draft_key:
        st.session_state.pop("draft", None)
        st.session_state.pop("draft_audio", None)
        st.session_state.pop("draft_selection", None)
    st.caption(f"{len(selected)} of {len(scenes)} scenes selected")
    st.caption("All selected scenes gives each choice a short turn. Use the other views to check the edit's actual cut order and timing.")
    draft_name = {
        "All selected scenes": "draft_scene_reel.mp4",
        "First 20 seconds of edit": "draft_20s.mp4",
        "Whole beat": "draft_full.mp4",
    }[draft_length]
    draft_path = Path(analysis_data["job"]) / draft_name
    if st.button("Generate quick draft", disabled=not selected, width="stretch", icon=":material/movie_edit:"):
        try:
            scene_reel = draft_length == "All selected scenes"
            timeline = (
                build_scene_reel(selected) if scene_reel else
                build_timeline(selected, analysis_data["beats"], analysis_data["beat_length"], manual_selection=True)
            )
            draft = draft_path
            progress = st.progress(0, "Starting draft")
            render_montage(
                Path(analysis_data["source"]), Path(analysis_data["beat"]), timeline, draft,
                Path(analysis_data["job"]), quality="draft",
                on_progress=lambda fraction, message: progress.progress(fraction, message),
                max_duration=20.0 if draft_length == "First 20 seconds of edit" else None,
                audio_loop=scene_reel,
            )
            st.session_state["draft"] = str(draft)
            st.session_state.pop("draft_audio", None)
            st.session_state["draft_selection"] = draft_key
            persist_current_project()
        except Exception as exc:
            st.exception(exc)
    if not st.session_state.get("draft") and draft_path.exists() and draft_path.stat().st_size > 0:
        if st.button("Open the completed draft from the last attempt", width="stretch", icon=":material/history:"):
            st.session_state["draft"] = str(draft_path)
            st.session_state["draft_selection"] = draft_key
            persist_current_project()
    draft_value = st.session_state.get("draft")
    if draft_value and Path(draft_value).exists():
        section_heading("Preview", "Quick draft", "Check pace, crop, and your selected moments before the final render.")
        st.video(draft_value, muted=False, alt="Quick draft of selected scenes")
        st.caption("No sound in the player? Turn on its speaker control and check whether your browser tab or site is muted.")
        show_audio_check(Path(draft_value), st.session_state.get("draft_audio"))
        st.caption(
            "360p review of every selected scene; the final edit uses beat timing and a different order."
            if draft_length == "All selected scenes" else
            f"360p draft · {draft_length} · Same scene order, crop, and cut timing as the final export"
        )
    quality_label = st.selectbox(
        "Export quality",
        ["1080p Full HD", "1440p (2K/QHD)"],
        key="output_quality",
        help="2K is sharper but takes longer to render and creates a larger file.",
    )
    quality = "1440p" if quality_label.startswith("1440p") else "1080p"
    export_length = st.selectbox(
        "Export length",
        ["Full beat", "First 20 seconds (test export)"],
        key="export_length",
        help="A test export uses the same resolution, encoding quality, crop, and timing as the full video.",
    )
    test_export = export_length.startswith("First 20 seconds")
    generate = st.button("Export full-quality video", type="primary", width="stretch", disabled=not selected, icon=":material/auto_awesome_motion:")
    if generate:
        try:
            progress = st.progress(0, "Building the beat-synced timeline…")
            timeline = build_timeline(selected, analysis_data["beats"], analysis_data["beat_length"], manual_selection=True)
            suffix = "_sample" if test_export else ""
            output = OUTPUTS / f"syncora_{quality}{suffix}_{int(time.time())}.mp4"
            progress.progress(15, "Rendering your selected scenes…")
            render_montage(
                Path(analysis_data["source"]), Path(analysis_data["beat"]), timeline, output,
                Path(analysis_data["job"]), quality=quality,
                on_progress=lambda fraction, message: progress.progress(fraction, message),
                max_duration=20.0 if test_export else None,
            )
            progress.progress(100, "Finished")
            st.session_state["output"] = str(output)
            st.session_state["stats"] = {
                "tempo": round(analysis_data["tempo"]), "scenes": len(selected), "clips": len(timeline),
                "quality": quality,
                "length": "20-second test export" if test_export else "full beat",
            }
            persist_current_project()
            st.rerun()
        except Exception as exc:
            st.exception(exc)

output_value = st.session_state.get("output")
if output_value and Path(output_value).exists():
    output = Path(output_value)
    stats = st.session_state.get("stats", {})
    section_heading("Step 03 · Review", "Your edit is ready", "Watch the full render, download it, or return to your scene choices.")
    st.success(
        f"Render ready · {stats.get('quality', '1080p')} · {stats.get('length', 'full beat')} · {stats.get('tempo')} BPM · "
        f"{stats.get('clips')} cuts using {stats.get('scenes')} selected scenes"
    )
    st.video(str(output), muted=False, alt="Final rendered music video")
    st.caption("No sound in the player? Turn on its speaker control and check whether your browser tab or site is muted.")
    show_audio_check(output, stats.get("audio_sample"))
    actions = st.columns(2, gap="medium")
    with output.open("rb") as video_file:
        actions[0].download_button("Download MP4", video_file, file_name=output.name, mime="video/mp4", width="stretch", icon=":material/download:")
    actions[1].button("Change scene selection", width="stretch", on_click=return_to_scenes, icon=":material/arrow_back:")

    section_heading("Share", "Publish when you're ready", "Add a title and description, then send your finished video to YouTube.")
    title = st.text_input("Video title", key="video_title")
    if "saved_description_draft" not in st.session_state:
        previous_description = st.session_state.get("video_description", "")
        st.session_state["saved_description_draft"] = previous_description if not is_legacy_suggestion(previous_description) else ""
        if is_legacy_suggestion(previous_description):
            st.session_state["video_description"] = ""
    if is_legacy_suggestion(st.session_state.get("saved_description_draft")):
        st.session_state["saved_description_draft"] = ""
    if is_legacy_suggestion(st.session_state.get("video_description")):
        st.session_state["video_description"] = st.session_state["saved_description_draft"]
    if "video_description" not in st.session_state:
        st.session_state["video_description"] = st.session_state.get("saved_description_draft", "")
    description = st.text_area("Description", height=280, key="video_description", placeholder="Write your video description here…")
    description_actions = st.columns(2, gap="small")
    description_actions[0].button("Save draft", width="stretch", icon=":material/save:", disabled=not description.strip(), on_click=save_description_draft)
    description_actions[1].button(
        "Restore saved", width="stretch", icon=":material/history:",
        disabled=not st.session_state.get("saved_description_draft") or description == st.session_state.get("saved_description_draft"),
        on_click=restore_description_draft,
    )
    if st.session_state.pop("description_just_saved", False):
        st.success("Description draft saved with this project.")
    elif st.session_state.get("saved_description_draft"):
        st.caption("Saved draft available · Save again after editing to keep your changes.")
    else:
        st.caption("Your description starts blank. Save a draft to restore it when you reopen this project.")
    privacy = st.selectbox("Visibility", ["private", "unlisted", "public"], index=0, key="privacy")
    playlist = st.text_input(
        "Add to playlist (optional)",
        placeholder="Paste a YouTube playlist URL or playlist ID",
        key="playlist_input",
    )
    secret = ROOT / "client_secret.json"
    if not secret.exists():
        st.info("Add client_secret.json to this app folder to connect your YouTube channel. See SETUP.md.")
    if st.button("Upload to YouTube", type="primary", disabled=not title or not secret.exists()):
        try:
            with st.spinner("Uploading to your YouTube channel…"):
                video_url, playlist_status = upload_video(
                    output, title, description, privacy, secret, ROOT / "youtube_token.json", playlist
                )
            st.session_state["uploaded_url"] = video_url
            st.session_state["playlist_status"] = playlist_status
        except Exception as exc:
            st.exception(exc)

    uploaded_url = st.session_state.get("uploaded_url")
    if uploaded_url:
        st.success("Uploaded successfully")
        if st.session_state.get("playlist_status"):
            st.info(st.session_state["playlist_status"])
        st.link_button("Open video on YouTube", uploaded_url)
        st.button("Generate new", type="primary", width="stretch", on_click=reset_project)

persist_current_project()
