from PIL import Image, ImageDraw
import os

def create_icon(color, name):
    # Create a 64x64 image with a transparent background
    image = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a colored circle
    draw.ellipse((8, 8, 56, 56), fill=color, outline="white", width=2)
    
    # Ensure directory exists
    os.makedirs('assets', exist_ok=True)
    image.save(f'assets/{name}.png')
    print(f"Icon saved: assets/{name}.png")

if __name__ == "__main__":
    # Gray icon for idle
    create_icon((128, 128, 128, 255), "icon_idle")
    # Red icon for recording
    create_icon((255, 0, 0, 255), "icon_recording")
