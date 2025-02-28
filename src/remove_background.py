from PIL import Image, ImageSequence
import os
import sys
import re
import argparse
from PIL import UnidentifiedImageError

def hex_to_rgb(hex_color):
    """Преобразование HEX в RGB"""
    hex_color = hex_color.lstrip('#')
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError("Invalid HEX color format")

def parse_rgb_string(rgb_string):
    """Парсинг строки формата rgb(r,g,b)"""
    match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', rgb_string)
    if not match:
        raise ValueError("Invalid RGB format. Use: rgb(r,g,b)")
    r, g, b = map(int, match.groups())
    if not all(0 <= x <= 255 for x in (r, g, b)):
        raise ValueError("RGB values must be between 0 and 255")
    return (r, g, b)

def parse_colors(color_str):
    """Парсинг строки с несколькими цветами"""
    colors = []
    pattern = r'(rgb\(\d+,\s*\d+,\s*\d+\)|#[0-9A-Fa-f]{6})'
    matches = re.findall(pattern, color_str)
    if not matches:
        raise ValueError("Color must be in HEX (#RRGGBB) or rgb(r,g,b) format")
    
    for color in matches:
        if color.startswith('#'):
            colors.append(hex_to_rgb(color))
        elif color.startswith('rgb('):
            colors.append(parse_rgb_string(color))
    return colors

def remove_background(input_filename='input.gif', output_filename='output.gif', bg_colors=['#FFFFFF']):  # Белый по умолчанию
    try:
        target_colors = []
        for bg_color in bg_colors:
            if isinstance(bg_color, str):
                if bg_color.startswith('#'):
                    target_colors.append(hex_to_rgb(bg_color))
                elif bg_color.startswith('rgb('):
                    target_colors.append(parse_rgb_string(bg_color))
                else:
                    raise ValueError("Color must be in HEX (#RRGGBB) or rgb(r,g,b) format")
            else:
                target_colors.append(bg_color)
        
        if not all(all(0 <= x <= 255 for x in color) for color in target_colors):
            raise ValueError("RGB values must be between 0 and 255")

        try:
            img = Image.open(input_filename)
        except UnidentifiedImageError:
            raise ValueError("Input file must be a GIF")

        total_frames = img.n_frames
        
        if img.format != 'GIF':
            raise ValueError("Input file must be a GIF")

        print(f"Processing {input_filename} ({total_frames} frames): ", end='', flush=True)
        frames = []
        
        threshold = 10
        for i, frame in enumerate(ImageSequence.Iterator(img), 1):
            new_frame = frame.convert("RGBA")
            datas = new_frame.getdata()
            new_data = []
            
            for item in datas:
                r, g, b, a = item
                is_target = False
                for r_target, g_target, b_target in target_colors:
                    if (abs(r - r_target) <= threshold and 
                        abs(g - g_target) <= threshold and 
                        abs(b - b_target) <= threshold):
                        is_target = True
                        break
                if is_target:
                    new_data.append((0, 0, 0, 0))
                else:
                    new_data.append(item)
            
            new_frame.putdata(new_data)
            frames.append(new_frame)
            
            progress = f"{i}/{total_frames} ({(i/total_frames)*100:.1f}%)"
            print(f"\rProcessing {input_filename} ({total_frames} frames): {progress}", end='', flush=True)

        print(f"\rProcessing {input_filename} ({total_frames} frames): Saving...", end='', flush=True)
        frames[0].save(
            output_filename,
            save_all=True,
            append_images=frames[1:],
            duration=img.info.get('duration', 100),
            loop=0
        )
        print(f"\rProcessing {input_filename} ({total_frames} frames): Done. Saved to {output_filename}")

    except Exception as e:
        print(f"\rError: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove background from GIF')
    parser.add_argument('-i', '--input', default='input.gif', help='Input GIF file')
    parser.add_argument('-o', '--output', default='output.gif', help='Output GIF file')
    parser.add_argument('-c', '--color', default='#FFFFFF',  # Белый по умолчанию
                       help='Background colors to remove (comma-separated HEX #RRGGBB or rgb(r,g,b))')
    args = parser.parse_args()
    bg_colors = parse_colors(args.color)
    remove_background(args.input, args.output, bg_colors)