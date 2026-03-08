import sys
import os
import subprocess
import datetime
import threading
from src.recorder_manager import RecorderManager
from src.command_generator import CommandGenerator
from src.tray_manager import TrayManager
from src.settings_gui import SettingsDialog, load_config

def send_notification(title, message):
    """Sends a desktop notification using notify-send."""
    try:
        # Check if notify-send exists
        if subprocess.run(['which', 'notify-send'], capture_output=True).returncode == 0:
            subprocess.run(['notify-send', title, message], check=False)
        else:
            print(f"Notification (CLI): {title} - {message}")
    except Exception as e:
        print(f"Notification fallback: {title} - {message}")

class ScreenRecorderGUI:
    def __init__(self):
        self.config = load_config()
        self.recorder = None
        self.tray = TrayManager(
            start_callback=self.start_recording,
            stop_callback=self.stop_recording,
            settings_callback=self.open_settings,
            exit_callback=self.exit_app
        )

    def start_recording(self):
        # Always reload config before starting
        self.config = load_config()
        
        # Setup recorder
        generator = CommandGenerator(
            display=self.config['display'],
            fps=self.config['fps'],
            resolution=self.config['resolution'],
            use_mic=self.config['use_mic'],
            show_timestamp=self.config.get('show_timestamp', True)
        )
        self.recorder = RecorderManager(generator)
        
        # Generate filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"recording_{timestamp}.{self.config['format']}"
        output_path = os.path.abspath(output_file)
        
        try:
            self.recorder.start(output_path)
            send_notification("Recording Started", f"Saving to {output_file}")
        except Exception as e:
            send_notification("Error", f"Failed to start recording: {e}")
            self.tray.update_menu(recording=False)

    def stop_recording(self):
        if self.recorder:
            self.recorder.stop()
            send_notification("Recording Stopped", "Video has been saved successfully.")

    def open_settings(self):
        # Open settings in a separate thread/process if possible, 
        # but tkinter needs main thread or careful handling.
        # Since pystray is running its own loop, we'll spawn the dialog.
        dialog = SettingsDialog(on_save_callback=self.update_config)
        dialog.show()

    def update_config(self, new_config):
        self.config = new_config
        print(f"Config updated: {self.config}")

    def exit_app(self):
        if self.recorder and self.recorder.is_recording():
            self.recorder.stop()
        sys.exit(0)

    def run(self):
        self.tray.run()

if __name__ == "__main__":
    app = ScreenRecorderGUI()
    app.run()
