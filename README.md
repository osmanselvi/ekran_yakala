# Screen Recorder (Ekran Yakala)

A high-performance screen recording utility for Linux (optimized for Raspberry Pi 5) with System Tray GUI, microphone support, and live timestamp overlay.

## Features
- **Multi-Platform**: Robust support for Linux (X11) and Windows (GDI).
- **Multi-Monitor**: Select specific monitors or custom capture regions on Windows.
- **Audio Support**: Configure specific audio devices (Realtek, PulseAudio, etc.).
- **System Tray GUI**: Visual status indicators (gray idle, red recording).
- **Graceful Termination**: Ensures MP4 files are finalized correctly on exit.
- **Timestamp Overlay**: Dynamic date and time overlay on video output.
- **Configurable**: Adjustable FPS, Resolution, and Formats (MP4, MKV, AVI).

## Prerequisites
- **Linux**: FFmpeg, PulseAudio, Python 3.x, `libnotify-bin`.
- **Windows**: [FFmpeg](https://ffmpeg.org/download.html) (add to PATH), Python 3.x.

## Installation

### Linux (Debian/Raspberry Pi)
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg libnotify-bin python3-tk python3-pystray python3-pil
```

### Windows
1. Install **FFmpeg** and ensure it's available in your Command Prompt (`ffmpeg -version`).
2. Install Python dependencies:
```powershell
pip install pystray Pillow
```

## Usage

### System Tray GUI (Recommended)
Launch the application:
- **Linux**: `python3 -m src.gui_main`
- **Windows**: `python -m src.gui_main`

*Note: On Linux/XRDP, ensure `DISPLAY` and `XAUTHORITY` variables are correctly set if running via SSH.*

### Command Line Interface
```bash
python3 -m src.main --output recording --mic
```

## Creating Windows Executable (.exe)
To create a standalone EXE for Windows:
1. Ensure you are on a Windows machine.
2. Install PyInstaller: `pip install pyinstaller`
3. Run the build script: `python build_exe.py`
4. The executable will be generated in the `dist/` folder.

## Configuration
Settings are stored in `config.json`. You can modify this file or use the GUI settings dialog to update format, resolution, and more.

## Development
- **Source**: `src/`
- **Tests**: `tests/`
- **Assets**: `assets/`

Run tests:
```bash
python3 -m unittest discover tests
```

---
Developed for the Raspberry Pi 5.
