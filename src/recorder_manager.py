import subprocess
import signal
import os
import time

class RecorderManager:
    """Manages the FFmpeg process for screen recording."""

    def __init__(self, command_generator):
        self.command_generator = command_generator
        self.process = None
        self.status = "IDLE"

    def start(self, output_path):
        """Starts the screen recording process."""
        if self.is_recording():
            raise RuntimeError("Recording is already in progress.")

        args = self.command_generator.generate_args(output_path)
        
        # Start ffmpeg in a subshell, using a new process group to allow easy termination
        self.process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            preexec_fn=os.setsid,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        self.status = "RECORDING"
        print(f"Recording started. Output: {output_path}")

    def stop(self):
        """Stops the screen recording process gracefully."""
        if not self.is_recording():
            print("No recording in progress to stop.")
            return

        # FFmpeg expects 'q' or SIGINT to stop gracefully
        try:
            # Send SIGINT to the process group
            os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
            
            # Wait for it to finish
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            print("FFmpeg did not stop in time. Forcing termination...")
            self.process.terminate()
        except Exception as e:
            print(f"Error while stopping: {e}")
        finally:
            self.process = None
            self.status = "IDLE"
            print("Recording stopped.")

    def is_recording(self):
        """Returns True if a recording is currently in progress and the process is alive."""
        if self.status == "RECORDING" and self.process:
            if self.process.poll() is None:
                return True
            else:
                # Process died unexpectedly, check stderr
                _, stderr = self.process.communicate()
                if stderr:
                    print(f"FFmpeg Error Output: {stderr.decode()}")
                self.status = "IDLE"
                self.process = None
        return False

    def get_status(self):
        """Returns a human-readable status."""
        if self.is_recording():
            return f"RECORDING (PID: {self.process.pid})"
        return "IDLE"
