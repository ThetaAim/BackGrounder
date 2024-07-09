import tkinter as tk
from PIL import Image
import os
import re
import sys
import ctypes

SPI_SETDESKWALLPAPER = 20


def check_file_valid(image_path):
    if os.path.exists(image_path):
        file_name, file_extansion = os.path.splitext(image_path)
        if file_extansion.lower() in [".jpg", ".png", "jpeg", ".tif"]:
            set_wallpaper(image_path)
            print(f"\nWallpaper is set to {image_path}")
        else:
            print(f'\nFile not supported please choose .jpg .png .tif')
    else:
        print('\nNo such file, make sure file exists')


def create_rgb_wallpaper(rgb_string):
    match = re.match(r'RGB\((\d+),(\d+),(\d+)\)', rgb_string)

    if match:
        # Extract RGB values
        red = int(match.group(1))
        green = int(match.group(2))
        blue = int(match.group(3))
        background_color = (red, green, blue)

        width, height = get_screen_res()

        background_image = Image.new("RGB", (width, height), background_color)
        background_image_path = f"wallpaper.jpg"
        background_image.save(background_image_path, quality=80)
        image_path = os.path.abspath(background_image_path)

        set_wallpaper(image_path)

    else:
        print("Invalid RGB string format. Please use RGB(x,y,z) format.")


def get_screen_res():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return screen_width, screen_height


def set_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)


if len(sys.argv) < 2:

    def_wall_path = os.path.abspath('wallpaper.jpg')

    if os.path.exists(def_wall_path) and os.path.splitext(def_wall_path)[1].lower() in ['.jpg', '.jpeg', '.png', '.tif']:
        print(f"\nWallpaper is set to {def_wall_path}")
        set_wallpaper(def_wall_path)
        sys.exit(0)

    else:
        print("\nUsage: instantbkg <image_path\\file_name.extension>")
        print("\nUsage: instantbkg <RGB(red,green,blue)>  ex: instantbkg RGB(100,200,100)")
        print("\nPlease note RGB will OVERWRITE wallpaper.jpg")
        print("\n** If no argument instantbkg will set wallpaper.jpg by default (if available)")
        sys.exit(1)

if sys.argv[1][:3] == "RGB":
    rgb_string = sys.argv[1]
    create_rgb_wallpaper(rgb_string)

else:
    abs_path = os.path.abspath(sys.argv[1])
    check_file_valid(abs_path)
