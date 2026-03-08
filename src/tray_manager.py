import pystray
from PIL import Image
import threading
import os

class TrayManager:
    """Manages the system tray icon and its menu."""

    def __init__(self, start_callback, stop_callback, settings_callback, exit_callback):
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.settings_callback = settings_callback
        self.exit_callback = exit_callback
        
        # Load icons
        self.icon_idle = Image.open('assets/icon_idle.png')
        self.icon_recording = Image.open('assets/icon_recording.png')
        
        # Initial menu
        self.menu = pystray.Menu(
            pystray.MenuItem('Start Recording', self.on_start, enabled=True),
            pystray.MenuItem('Stop Recording', self.on_stop, enabled=False),
            pystray.MenuItem('Settings', self.on_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Exit', self.on_exit)
        )
        
        self.icon = pystray.Icon(
            "ScreenRecorder",
            self.icon_idle,
            "Screen Recorder",
            self.menu
        )

    def on_start(self, icon, item):
        self.start_callback()
        self.update_menu(recording=True)

    def on_stop(self, icon, item):
        self.stop_callback()
        self.update_menu(recording=False)

    def on_settings(self, icon, item):
        self.settings_callback()

    def on_exit(self, icon, item):
        self.exit_callback()
        self.icon.stop()

    def update_menu(self, recording):
        """Update the menu state and icon based on recording status."""
        new_icon = self.icon_recording if recording else self.icon_idle
        
        new_menu = pystray.Menu(
            pystray.MenuItem('Start Recording', self.on_start, enabled=not recording),
            pystray.MenuItem('Stop Recording', self.on_stop, enabled=recording),
            pystray.MenuItem('Settings', self.on_settings, enabled=not recording),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Exit', self.on_exit)
        )
        
        self.icon.icon = new_icon
        self.icon.menu = new_menu

    def run(self):
        """Run the tray icon in the main thread (or its own)."""
        self.icon.run()
