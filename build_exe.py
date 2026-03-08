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

    # Assets to include: (source, destination)
    # destination 'assets' means it will be at the same level as the exe if we use --onefile
    # or inside the folder if we use --onedir.
    # We'll use a .spec file for more control, but for a simple start:
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed", # No console window
        "--name", "EkranYakala",
        "--icon", "assets/icon_idle.png",
        "--add-data", "assets;assets", # Include assets folder
        "src/gui_main.py"
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\nSuccess! Your executable is in the 'dist' folder.")
    else:
        print("\nError: Build failed. Check the output above.")

if __name__ == "__main__":
    build()
