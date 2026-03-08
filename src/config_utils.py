import json
import os
import platform

CONFIG_FILE = 'config.json'

def get_default_config():
    os_type = platform.system()
    return {
        "format": "mp4",
        "fps": 30,
        "resolution": "1920x1080",
        "use_mic": False,
        "display": ":0.0" if os_type == "Linux" else "desktop",
        "show_timestamp": True,
        "audio_device": "default" if os_type == "Linux" else "Mikrofon (Realtek(R) Audio)",
        "monitor_index": "0"  # 0: All, 1: Monitor 1, 2: Monitor 2
    }

def load_config():
    defaults = get_default_config()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            try:
                user_config = json.load(f)
                # Ensure the loaded config has all keys from defaults
                return {**defaults, **user_config}
            except json.JSONDecodeError:
                return defaults.copy()
    return defaults.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
