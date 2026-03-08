import argparse
import sys
import time
import os
from src.command_generator import CommandGenerator
from src.recorder_manager import RecorderManager
from src.config_utils import load_config

def main():
    config = load_config()
    
    parser = argparse.ArgumentParser(description="Multi-platform Screen Recorder CLI")
    parser.add_argument("--format", type=str, choices=['mp4', 'avi', 'mkv'], default=config.get('format', 'mp4'), help="Video format (mp4, avi, mkv)")
    parser.add_argument("--output", type=str, default="recording", help="Output filename (without extension)")
    parser.add_argument("--fps", type=int, default=config.get('fps', 30), help="Frames per second")
    parser.add_argument("--res", type=str, default=config.get('resolution', "1920x1080"), help="Resolution (e.g. 1920x1080)")
    parser.add_argument("--display", type=str, default=config.get('display'), help="X11 Display or 'desktop' on Windows")
    parser.add_argument("--mic", action="store_true", default=config.get('use_mic', False), help="Enable microphone recording")
    parser.add_argument("--audio-device", type=str, default=config.get('audio_device'), help="Audio device name (Windows) or index (Linux)")
    parser.add_argument("--timestamp", action="store_true", default=config.get('show_timestamp', True), help="Show timestamp overlay")
    parser.add_argument("--no-timestamp", action="store_false", dest="timestamp", help="Disable timestamp overlay")

    args = parser.parse_args()

    full_output_path = f"{args.output}.{args.format}"
    
    # Initialize components
    generator = CommandGenerator(
        display=args.display, 
        fps=args.fps, 
        resolution=args.res,
        use_mic=args.mic,
        show_timestamp=args.timestamp,
        audio_device=args.audio_device
    )
    recorder = RecorderManager(generator)

    try:
        print(f"--- Screen Recorder ---")
        print(f"Format: {args.format}")
        print(f"Resolution: {args.res} @ {args.fps} FPS")
        print(f"Output: {full_output_path}")
        print(f"Microphone: {'ENABLED' if args.mic else 'DISABLED'}")
        if args.mic and args.audio_device:
            print(f"Audio Device: {args.audio_device}")

        if args.mic:
            answer = input("\nMicrophone recording is enabled. Do you want to proceed? [Y/n]: ").strip().lower()
            if answer not in ['', 'y', 'yes']:
                print("Recording cancelled.")
                sys.exit(0)

        print("\nPress Ctrl+C to stop recording...")
        
        recorder.start(full_output_path)
        
        while recorder.is_recording():
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping recording...")
        recorder.stop()
    except Exception as e:
        print(f"Error: {e}")
        if recorder.is_recording():
            recorder.stop()
        sys.exit(1)

    if os.path.exists(full_output_path):
        print(f"Success! Video saved to: {os.path.abspath(full_output_path)}")
    else:
        print("Error: Video file was not created. Check FFmpeg output or permissions.")

if __name__ == "__main__":
    main()
