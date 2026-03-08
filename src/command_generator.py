import platform
import os

class CommandGenerator:
    """
    Generates FFmpeg command-line arguments based on parameters and OS.
    """

    SUPPORTED_FORMATS = ['mp4', 'avi', 'mkv']

    def __init__(self, display=None, fps=30, resolution="1920x1080", use_mic=False, show_timestamp=True, audio_device=None, offset_x=0, offset_y=0):
        self.os_type = platform.system()
        # Default display/input based on OS
        if display is None:
            self.display = ":0.0" if self.os_type == "Linux" else "desktop"
        else:
            self.display = display
            
        # Default audio device based on OS
        if not audio_device or audio_device == "default":
            if self.os_type == "Linux":
                self.audio_device = "default"
            else:
                self.audio_device = "audio=Mikrofon (Realtek(R) Audio)"
        else:
            # Add 'audio=' prefix for Windows dshow if not present
            if self.os_type == "Windows" and not audio_device.startswith("audio="):
                self.audio_device = f"audio={audio_device}"
            else:
                self.audio_device = audio_device

        self.fps = fps
        self.resolution = resolution
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.use_mic = use_mic
        self.show_timestamp = show_timestamp

    def generate_args(self, output_path):
        """
        Constructs the FFmpeg command list.
        Args:
            output_path (str): The path to save the video file.
        Returns:
            list: A list of command-line arguments for FFmpeg.
        """
        extension = output_path.split('.')[-1].lower()
        if extension not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {extension}. Supported formats: {self.SUPPORTED_FORMATS}")

        # Base command
        args = ["ffmpeg", "-y"] # -y to overwrite by default

        # Input: Audio
        if self.use_mic:
            if self.os_type == "Linux":
                args.extend(["-f", "pulse", "-i", self.audio_device, "-ac", "2"])
            elif self.os_type == "Windows":
                args.extend(["-f", "dshow", "-i", self.audio_device, "-ac", "2"])

        # Input: Video
        if self.os_type == "Linux":
            args.extend([
                "-f", "x11grab",
                "-video_size", self.resolution,
                "-framerate", str(self.fps),
                "-i", self.display,
            ])
        elif self.os_type == "Windows":
            args.extend([
                "-f", "gdigrab",
                "-framerate", str(self.fps),
                "-video_size", self.resolution,
                "-offset_x", str(self.offset_x),
                "-offset_y", str(self.offset_y),
                "-i", self.display,
            ])

        # Video filters
        if self.show_timestamp:
            if self.os_type == "Windows":
                # On Windows, using the font name 'Arial' is more reliable than path escaping
                # especially with colons in C:\
                timestamp_filter = (
                    "drawtext=font='Arial':"
                    "text='%{localtime\\:%Y-%m-%d %H\\\\\\:%M\\\\\\:%S}':"
                    "x=w-tw-10:y=10:fontsize=24:fontcolor=white:"
                    "box=1:boxcolor=black@0.5"
                )
            else:
                font_path = self._get_font_path()
                timestamp_filter = (
                    f"drawtext=fontfile='{font_path}':"
                    "text='%{{localtime\\:%Y-%m-%d %H\\\\\\:%M\\\\\\:%S}}':"
                    "x=w-tw-10:y=10:fontsize=24:fontcolor=white:"
                    "box=1:boxcolor=black@0.5"
                )
            args.extend(["-vf", timestamp_filter])

        # Add codec and quality settings
        if extension == 'mp4':
            args.extend(["-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac"])
        elif extension == 'avi':
            args.extend(["-c:v", "libxvid", "-qscale:v", "2", "-c:a", "libmp3lame"])
        elif extension == 'mkv':
            args.extend(["-c:v", "libx264", "-crf", "23", "-c:a", "libopus"])

        # Sync audio and video
        if self.use_mic:
            args.extend(["-af", "aresample=async=1"])

        # Output path must be the last argument
        args.append(output_path)
        
        return args

    def _get_font_path(self):
        """Returns a valid system font path based on the OS."""
        if self.os_type == "Linux":
            paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
            ]
        elif self.os_type == "Windows":
            # This is a fallback now as we try 'Arial' name first
            paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/segoeui.ttf"
            ]
        else:
            return "arial.ttf"

        for p in paths:
            return p
        return "arial.ttf"
