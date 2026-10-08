@echo off
setlocal
cd /d "%~dp0"
if not exist "requirements.txt" (
  echo.
  echo ERROR: The app is being run from inside the ZIP file.
  echo.
  echo 1. Close this window.
  echo 2. Right-click the downloaded ZIP and choose Extract All.
  echo 3. Open the extracted folder and double-click run_windows.bat.
  echo.
  pause
  exit /b 1
)
where python >nul 2>nul
if errorlevel 1 (
  echo Python is not installed. Install Python 3.11 or 3.12 from python.org.
  pause
  exit /b 1
)
where ffmpeg >nul 2>nul
if errorlevel 1 goto install_ffmpeg
where ffprobe >nul 2>nul
if errorlevel 1 goto install_ffmpeg
goto ffmpeg_ready

:install_ffmpeg
echo.
echo FFmpeg is required for video editing but is not installed.
where winget >nul 2>nul
if errorlevel 1 (
  echo Install FFmpeg from https://ffmpeg.org and then restart this launcher.
  pause
  exit /b 1
)
echo Installing FFmpeg with Windows Package Manager...
winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements
if errorlevel 1 (
  echo FFmpeg installation failed. Try running this launcher as Administrator.
  pause
  exit /b 1
)
echo.
echo FFmpeg was installed successfully.
echo Close this window, then double-click run_windows.bat again so Windows can refresh PATH.
pause
exit /b 0

:ffmpeg_ready
if not exist ".venv\Scripts\python.exe" (
  echo Setting up Syncora...
  python -m venv .venv
  .venv\Scripts\python.exe -m pip install --upgrade pip
  .venv\Scripts\python.exe -m pip install -r requirements.txt
)
.venv\Scripts\python.exe -m streamlit run app.py
pause
