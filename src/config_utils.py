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
            try:
                return {**DEFAULT_CONFIG, **json.load(f)}
            except json.JSONDecodeError:
                return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
