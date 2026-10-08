from __future__ import annotations

from pathlib import Path
from urllib.parse import parse_qs, urlparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube"]


def credentials(secret_file: Path, token_file: Path) -> Credentials:
    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    has_required_scope = bool(creds and creds.has_scopes(SCOPES))
    if creds and has_required_scope and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid or not has_required_scope:
        flow = InstalledAppFlow.from_client_secrets_file(str(secret_file), SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True)
    token_file.write_text(creds.to_json(), encoding="utf-8")
    return creds


def normalize_playlist_id(value: str) -> str | None:
    value = value.strip()
    if not value:
        return None
    if "://" in value:
        playlist_id = parse_qs(urlparse(value).query).get("list", [""])[0]
        if not playlist_id:
            raise ValueError("The playlist URL does not contain a playlist ID.")
        return playlist_id
    return value


def upload_video(
    video: Path,
    title: str,
    description: str,
    privacy: str,
    secret_file: Path,
    token_file: Path,
    playlist: str = "",
) -> tuple[str, str | None]:
    playlist_id = normalize_playlist_id(playlist)
    youtube = build("youtube", "v3", credentials=credentials(secret_file, token_file))
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description, "categoryId": "10"},
            "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False},
        },
        media_body=MediaFileUpload(str(video), chunksize=8 * 1024 * 1024, resumable=True),
    )
    response = None
    while response is None:
        _, response = request.next_chunk()
    video_id = response["id"]
    playlist_status = None
    if playlist_id:
        try:
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": video_id},
                    }
                },
            ).execute()
            playlist_status = "Added to playlist successfully."
        except Exception as exc:
            playlist_status = f"Video uploaded, but it could not be added to the playlist: {exc}"
    return f"https://www.youtube.com/watch?v={video_id}", playlist_status
