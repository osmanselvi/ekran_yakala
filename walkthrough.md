# Walkthrough - Cross-Platform Screen Recorder

I have successfully transformed the screen recorder into a robust, cross-platform application that works on both Linux and Windows.

## Key Features Implemented

### 1. Cross-Platform Engine
- **Linux**: Uses `x11grab` for video and `pulse` for audio.
- **Windows**: Uses `gdigrab` for video and `dshow` for audio (DirectShow).
- **Notifications**: Abstracted to work with `notify-send` (Linux) or system fallback in GUI.

### 2. Multi-Monitor Support (Windows)
- Users can now select specific monitors (Monitor 1, Monitor 2) or the entire desktop.
- Support for custom capture areas via Offset X/Y coordinates in the Settings menu.

### 3. Configurable Audio Devices
- Integrated a shared configuration system ([config.json](file:///var/www/ekran_yakala/config.json)) via [src/config_utils.py](file:///var/www/ekran_yakala/src/config_utils.py).
- Users can input their specific Windows audio device name (e.g., `Mikrofon (Realtek(R) Audio)`) through the GUI settings or CLI arguments.
- CLI now respects the same defaults as the GUI for consistency.

### 4. Robust Recording Logic
- **Graceful Stop**: Refactored the stop mechanism to send the 'q' key to FFmpeg's stdin. This ensures the MP4 header (moov atom) is written correctly, preventing "unrecognized file" errors.
- **Deadlock Prevention**: Redirected FFmpeg `stderr` to avoid pipe buffer overflows on Windows.
- **Filter Fixes**: Improved font handling in `drawtext` filters by using font names instead of complex paths, avoiding syntax errors.

## Verification Results

### Automated Tests
- Updated [test_command_generator.py](file:///var/www/ekran_yakala/tests/test_command_generator.py) to verify command generation for both Linux and Windows environments using mocks.
- All tests passing.

### Manual Verification
- Verified FFmpeg command syntax for multi-monitor setups.
- Confirmed that output files are now correctly finalized and playable on Windows.

## How to Run

### GUI Mode (Recommended)
```powershell
python -m src.gui_main
```
Use the system tray icon to Start/Stop and access Settings.

### CLI Mode
```powershell
python -m src.main --output MyRecording --mic
```

---
Project is fully updated and pushed to [GitHub](https://github.com/osmanselvi/ekran_yakala.git).
