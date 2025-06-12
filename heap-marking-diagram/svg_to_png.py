#!/usr/bin/env python3

import subprocess
import sys

def convert_svg_to_png(svg_file='heap_marking.svg', png_file='heap_marking.png', scale=2):
    """Convert SVG to PNG using cairosvg or Inkscape"""
    
    # Try cairosvg first
    try:
        import cairosvg
        cairosvg.svg2png(url=svg_file, write_to=png_file, scale=scale)
        print(f"Converted {svg_file} to {png_file} using cairosvg (scale={scale})")
        return True
    except ImportError:
        print("cairosvg not found, trying Inkscape...")
    except Exception as e:
        print(f"cairosvg failed: {e}, trying Inkscape...")
    
    # Try Inkscape
    try:
        dpi = 96 * scale  # Default SVG DPI is 96
        subprocess.run([
            'inkscape',
            svg_file,
            '--export-type=png',
            f'--export-filename={png_file}',
            f'--export-dpi={dpi}'
        ], check=True)
        print(f"Converted {svg_file} to {png_file} using Inkscape (dpi={dpi})")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Inkscape not found or failed.")
    
    # Try rsvg-convert
    try:
        subprocess.run([
            'rsvg-convert',
            '-z', str(scale),
            svg_file,
            '-o', png_file
        ], check=True)
        print(f"Converted {svg_file} to {png_file} using rsvg-convert (scale={scale})")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("rsvg-convert not found or failed.")
    
    print("\nError: No SVG to PNG converter found.")
    print("Please install one of the following:")
    print("  - pip install cairosvg")
    print("  - apt install inkscape")
    print("  - apt install librsvg2-bin")
    return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        scale = float(sys.argv[1])
    else:
        scale = 2  # Default to 2x for presentations
    
    convert_svg_to_png(scale=scale)