import tkinter as tk
from tkinter import ttk, messagebox
from src.config_utils import load_config, save_config

class SettingsDialog:
    def __init__(self, on_save_callback):
        self.on_save_callback = on_save_callback
        self.config = load_config()
        
    def show(self):
        self.root = tk.Tk()
        self.root.title("Screen Recorder Settings")
        self.root.geometry("350x550")
        
        container = tk.Frame(self.root)
        container.pack(padx=20, pady=20, fill="both", expand=True)

        # Format
        tk.Label(container, text="Video Format:").pack(pady=2)
        self.format_var = tk.StringVar(value=self.config.get('format', 'mp4'))
        ttk.Combobox(container, textvariable=self.format_var, values=['mp4', 'avi', 'mkv']).pack(fill="x")
        
        # FPS
        tk.Label(container, text="FPS:").pack(pady=2)
        self.fps_var = tk.StringVar(value=str(self.config.get('fps', 30)))
        tk.Entry(container, textvariable=self.fps_var).pack(fill="x")
        
        # Resolution
        tk.Label(container, text="Resolution (WxH):").pack(pady=2)
        self.res_var = tk.StringVar(value=self.config.get('resolution', "1920x1080"))
        tk.Entry(container, textvariable=self.res_var).pack(fill="x")

        # Monitor Selection (Windows Specific)
        tk.Label(container, text="Monitor / Area (Windows):").pack(pady=2)
        self.monitor_var = tk.StringVar(value=self.config.get('monitor_selection', 'All Screens'))
        monitor_options = ['All Screens', 'Monitor 1 (Offset 0,0)', 'Monitor 2 (Offset 1920,0)', 'Custom Area']
        self.monitor_cb = ttk.Combobox(container, textvariable=self.monitor_var, values=monitor_options)
        self.monitor_cb.pack(fill="x")

        # Offset X/Y (Advanced)
        offset_frame = tk.Frame(container)
        offset_frame.pack(pady=5, fill="x")
        
        tk.Label(offset_frame, text="Offset X:").grid(row=0, column=0)
        self.offset_x_var = tk.StringVar(value=str(self.config.get('offset_x', 0)))
        tk.Entry(offset_frame, textvariable=self.offset_x_var, width=10).grid(row=0, column=1, padx=5)
        
        tk.Label(offset_frame, text="Offset Y:").grid(row=0, column=2)
        self.offset_y_var = tk.StringVar(value=str(self.config.get('offset_y', 0)))
        tk.Entry(offset_frame, textvariable=self.offset_y_var, width=10).grid(row=0, column=3, padx=5)

        # Audio Device
        tk.Label(container, text="Audio Device:").pack(pady=2)
        self.audio_device_var = tk.StringVar(value=self.config.get('audio_device', 'default'))
        tk.Entry(container, textvariable=self.audio_device_var).pack(fill="x")
        
        # Microphone
        self.mic_var = tk.BooleanVar(value=self.config.get('use_mic', False))
        tk.Checkbutton(container, text="Record Microphone", variable=self.mic_var).pack(pady=5)

        # Timestamp
        self.timestamp_var = tk.BooleanVar(value=self.config.get('show_timestamp', True))
        tk.Checkbutton(container, text="Show Date/Time Overlay", variable=self.timestamp_var).pack(pady=5)
        
        # Save Button
        tk.Button(container, text="Save Settings", command=self.save, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=20, fill="x")
        
        # Auto-update offsets when monitor selection changes
        self.monitor_cb.bind("<<ComboboxSelected>>", self.on_monitor_change)
        
        self.root.mainloop()

    def on_monitor_change(self, event):
        sel = self.monitor_var.get()
        if 'Monitor 1' in sel:
            self.offset_x_var.set("0")
            self.offset_y_var.set("0")
        elif 'Monitor 2' in sel:
            self.offset_x_var.set("1920")
            self.offset_y_var.set("0")
        elif 'All Screens' in sel:
            self.offset_x_var.set("0")
            self.offset_y_var.set("0")

    def save(self):
        try:
            new_config = {
                "format": self.format_var.get(),
                "fps": int(self.fps_var.get()),
                "resolution": self.res_var.get(),
                "display": "desktop" if "All" in self.monitor_var.get() else "desktop", # Still uses desktop in gdigrab
                "monitor_selection": self.monitor_var.get(),
                "offset_x": int(self.offset_x_var.get()),
                "offset_y": int(self.offset_y_var.get()),
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
            messagebox.showerror("Error", "Please enter valid numeric values for FPS and Offsets.")

if __name__ == "__main__":
    SettingsDialog(lambda c: print(f"Saved: {c}")).show()
