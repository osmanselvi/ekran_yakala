import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CONFIG_FILE = 'config.json'

DEFAULT_CONFIG = {
    "format": "mp4",
    "fps": 30,
    "resolution": "1920x1080",
    "use_mic": False,
    "display": ":10.0",
    "show_timestamp": True,
    "audio_device": "default"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

class SettingsDialog:
    def __init__(self, on_save_callback):
        self.on_save_callback = on_save_callback
        self.config = load_config()
        
    def show(self):
        self.root = tk.Tk()
        self.root.title("Screen Recorder Settings")
        self.root.geometry("300x400")
        
        # Format
        tk.Label(self.root, text="Video Format:").pack(pady=5)
        self.format_var = tk.StringVar(value=self.config['format'])
        ttk.Combobox(self.root, textvariable=self.format_var, values=['mp4', 'avi', 'mkv']).pack()
        
        # FPS
        tk.Label(self.root, text="FPS:").pack(pady=5)
        self.fps_var = tk.StringVar(value=str(self.config['fps']))
        tk.Entry(self.root, textvariable=self.fps_var).pack()
        
        # Resolution
        tk.Label(self.root, text="Resolution:").pack(pady=5)
        self.res_var = tk.StringVar(value=self.config['resolution'])
        tk.Entry(self.root, textvariable=self.res_var).pack()

        # Display
        tk.Label(self.root, text="Display / Desktop:").pack(pady=5)
        self.display_var = tk.StringVar(value=self.config['display'])
        tk.Entry(self.root, textvariable=self.display_var).pack()

        # Audio Device
        tk.Label(self.root, text="Audio Device (e.g. Mikrofon ...):").pack(pady=5)
        self.audio_device_var = tk.StringVar(value=self.config.get('audio_device', 'default'))
        tk.Entry(self.root, textvariable=self.audio_device_var).pack()
        
        # Microphone
        self.mic_var = tk.BooleanVar(value=self.config['use_mic'])
        tk.Checkbutton(self.root, text="Record Microphone", variable=self.mic_var).pack(pady=5)

        # Timestamp
        self.timestamp_var = tk.BooleanVar(value=self.config.get('show_timestamp', True))
        tk.Checkbutton(self.root, text="Show Date/Time Overlay", variable=self.timestamp_var).pack(pady=5)
        
        # Save Button
        tk.Button(self.root, text="Save Settings", command=self.save).pack(pady=20)
        
        self.root.mainloop()

    def save(self):
        try:
            new_config = {
                "format": self.format_var.get(),
                "fps": int(self.fps_var.get()),
                "resolution": self.res_var.get(),
                "display": self.display_var.get(),
                "use_mic": self.mic_var.get(),
                "show_timestamp": self.timestamp_var.get(),
                "audio_device": self.audio_device_var.get()
            }
            save_config(new_config)
            self.config = new_config
            if self.on_save_callback:
                self.on_save_callback(new_config)
            self.root.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid FPS value. Please enter a number.")

if __name__ == "__main__":
    # Test dialog
    SettingsDialog(lambda c: print(f"Saved: {c}")).show()
