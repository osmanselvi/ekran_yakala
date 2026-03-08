import os

class CommandGenerator:
    """Generates FFmpeg command arguments for screen recording on Linux."""

    SUPPORTED_FORMATS = ['mp4', 'avi', 'mkv']

    def __init__(self, display=":0.0", fps=30, resolution="1920x1080", use_mic=False, show_timestamp=True):
        self.display = display
        self.fps = fps
        self.resolution = resolution
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
        args = ["ffmpeg"]

        # Input: Audio (Microphone via PulseAudio)
        if self.use_mic:
            args.extend([
                "-f", "pulse",
                "-i", "default",  # Use default input device
                "-ac", "2"       # 2 channels (stereo)
            ])

        # Input: Video (Screen capture on X11)
        args.extend([
            "-f", "x11grab",
            "-video_size", self.resolution,
            "-framerate", str(self.fps),
            "-i", self.display,
        ])

        # Video filters
        if self.show_timestamp:
            # Escape the colon in date format: %H:%M:%S -> %H\\:%M\\:%S
            # FFmpeg drawtext local time overlay in top-right
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            timestamp_filter = (
                f"drawtext=fontfile={font_path}:"
                "text='%{localtime\\:%Y-%m-%d %H\\\\\\:%M\\\\\\:%S}':"
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
