# Syncora — setup

## 1. Install the program

1. If you downloaded a ZIP, choose **Extract All** and open the extracted folder. Do not run the launcher from inside the ZIP preview.
2. Install **Python 3.11 or 3.12** from python.org and enable **Add Python to PATH**.
3. Double-click `run_windows.bat`. If FFmpeg is missing, the launcher installs it using Windows Package Manager. Close and reopen the launcher when instructed.
4. The first complete launch installs the Python packages and can take several minutes.

Only upload and reuse videos you own, license, or have permission to use.

## 2. Connect your YouTube channel for uploads (one time)

1. Open Google Cloud Console and create or select a project.
2. Enable **YouTube Data API v3**.
3. Configure the OAuth consent screen. For personal testing, add your Google account as a test user.
4. Create an OAuth client ID with application type **Desktop app**.
5. Download its JSON credentials, rename the file to `client_secret.json`, and place it beside `app.py`.
6. Render a video, enter its title, and click **Upload to YouTube**.
7. Your normal browser opens. Sign into the Google account that owns your YouTube channel and approve access.

The app requests YouTube channel-management permission so it can upload a video and optionally add it to one of your playlists. It never asks for or stores your Google password. Authorization is stored locally in `youtube_token.json`; delete that file to disconnect the channel. An existing installation may open Google authorization once more after this update because playlist support needs a broader permission.

Important: YouTube generally restricts uploads from a new, unverified API project to Private. Google requires an API compliance audit before that project can upload Public or Unlisted videos.

## Normal workflow

1. Upload one authorized source video.
2. Upload your beat.
3. Confirm reuse rights and click **Find scene options**.
4. Review the scenes preselected for you, changing any checkbox you like. Click **Generate quick draft** to see every selected scene once at 360p. You can also preview the first 20 seconds or whole edit.
5. Choose **Full beat** or **First 20 seconds (test export)** under Export length. Click **Export full-quality video**, then watch the finished video.
   If the video player is silent, expand **Check the rendered beat audio**. It plays the soundtrack extracted from the MP4; also check the video's speaker control and browser tab sound.
6. Enter the title, choose visibility, and click **Upload to YouTube**.

Rendered files remain in `outputs`. Temporary source footage remains in `work` so a failed render can be diagnosed; either folder may be cleared when the app is closed.
