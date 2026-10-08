# Syncora

A local editing app that turns one authorized video source and one original beat into a beat-synced montage, then lets the creator review and upload it to YouTube.

The editor finds scene boundaries, divides long shots into short options, and presents a manual gallery with four-frame previews of the final square crop. It excludes source segments containing the known centered DREHTV logo, then preselects a varied set of recommended scenes while allowing the creator to change every remaining choice. The selected scenes are arranged every four beats, with extra cuts where beat detection leaves a long gap. Shots are capped at three seconds, and the renderer will not add a long frozen-frame hold. The fast 360p scene review draft shows every selected scene once; additional draft views preview the first 20 seconds or whole final edit. Full-quality exports are 1080p or 1440p (2K/QHD). Drafts and exports include the uploaded beat and offer a separate rendered-audio check in the app. All versions preserve a square layout with black side bars. The finished video can be uploaded through Google's official YouTube Data API with OAuth and optionally added to a playlist.

Start on Windows by reading `SETUP.md`, then double-click `run_windows.bat`.

## Current limitations

- Automated selection is visual scoring, not semantic object recognition.
- The source must be downloadable by yt-dlp and authorized for reuse.
- Scene ranges can be manually selected, but frame-accurate trimming is not yet available.

The draft is 640x360; full-quality exports are 1920x1080 or 2560x1440 at 30 fps. For testing, the full-quality export can also be limited to the first 20 seconds while keeping the same resolution and encoding settings. The downloader currently requests footage up to 1080p, so the 1440p export may upscale its source.
