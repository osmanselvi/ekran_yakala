# Screen Recorder (Ekran Yakala)

A high-performance screen recording utility for Linux (optimized for Raspberry Pi 5) with System Tray GUI, microphone support, and live timestamp overlay.

## Features
- **High Performance**: Uses FFmpeg with X11 capture.
- **System Tray GUI**: Manage recordings via a tray icon (gray/red state).
- **Audio Support**: Record from the default microphone using PulseAudio.
- **Timestamp Overlay**: Live date and time display in the top-right corner.
- **Configurable**: Easily change format (MP4, AVI, MKV), FPS, and resolution.
- **Desktop Notifications**: Visual feedback for recording status.

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
