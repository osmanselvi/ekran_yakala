import os
import subprocess
import sys

def build():
    print("--- Ekran Yakala EXE Build Script ---")
    
    # Check if pyinstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Error: PyInstaller is not installed. Please run: pip install pyinstaller")
        return

    # Using the .spec file is more reliable for pystray and assets
    spec_file = "screen_recorder.spec"
    
    if not os.path.exists(spec_file):
        print(f"Error: {spec_file} not found.")
        return

    cmd = ["pyinstaller", "--noconfirm", spec_file]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\nSuccess! Your executable is in the 'dist' folder.")
    else:
        print("\nError: Build failed. Check the output above.")

if __name__ == "__main__":
    build()
