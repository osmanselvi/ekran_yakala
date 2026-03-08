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
- Linux OS (Tested on Raspberry Pi 5 / Debian)
- FFmpeg
- PulseAudio (for microphone support)
- Python 3.x
- Dependencies: `pystray`, `Pillow`, `libnotify-bin`, `python3-tk`

## Installation

```bash
# Clone the repository
git clone https://github.com/osmanselvi/ekran_yakala.git
cd ekran_yakala

# Install system dependencies
sudo apt-get update
sudo apt-get install -y ffmpeg libnotify-bin python3-tk python3-pystray python3-pil
```

## Usage

### System Tray GUI (Recommended)
Launch the application in your graphical session:
```bash
python3 -m src.gui_main
```
*Note: If running over SSH to a specific display (e.g., XRDP), ensure `DISPLAY` and `XAUTHORITY` are set.*

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
