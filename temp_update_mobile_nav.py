#!/usr/bin/env python3
"""
Generate a full favicon set from images/shree-shiv-divy-logo.webp

Usage:
    pip install Pillow --break-system-packages   # if not already installed
    python3 generate_favicons.py

Reads:  images/shree-shiv-divy-logo.webp   (source logo, ideally square, transparent bg)
Writes (to site root, so paths match the root-relative <link> tags):
    favicon.ico                (multi-size: 16, 32, 48)
    favicon-16x16.png
    favicon-32x32.png
    apple-touch-icon.png       (180x180, flattened onto white — iOS ignores alpha)
    android-chrome-192x192.png
    android-chrome-512x512.png
    site.webmanifest
"""

from PIL import Image
import os
import json

SRC = "images/shree-shiv-divy-logo.webp"
OUT_DIR = "."  # site root

def load_source(path):
    img = Image.open(path).convert("RGBA")
    # Pad to square first so all derived icons aren't distorted
    if img.width != img.height:
        side = max(img.width, img.height)
        square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        square.paste(img, ((side - img.width) // 2, (side - img.height) // 2), img)
        img = square
    return img

def save_png(img, size, path):
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(path, format="PNG")
    print(f"  wrote {path} ({size}x{size})")

def save_apple_touch_icon(img, size, path):
    # Apple ignores transparency and can render it oddly (e.g. black bg on some iOS
    # versions), so flatten onto white for a predictable result.
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    bg = Image.new("RGB", (size, size), (255, 255, 255))
    bg.paste(resized, mask=resized.split()[3])
    bg.save(path, format="PNG")
    print(f"  wrote {path} ({size}x{size}, flattened on white)")

def save_ico(img, path, sizes=(16, 32, 48)):
    frames = [img.resize((s, s), Image.Resampling.LANCZOS) for s in sizes]
    frames[0].save(path, format="ICO", sizes=[(s, s) for s in sizes], append_images=frames[1:])
    print(f"  wrote {path} (sizes: {sizes})")

def write_manifest(path):
    manifest = {
        "name": "Shree Shiv Divy Astrology Centre",
        "short_name": "Shree Shiv Divy",
        "icons": [
            {"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}
        ],
        "theme_color": "#A6821F",
        "background_color": "#FDF9EF",
        "display": "standalone"
    }
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  wrote {path}")

def main():
    if not os.path.exists(SRC):
        raise SystemExit(f"Source logo not found at '{SRC}'. Run this script from the site root.")

    img = load_source(SRC)
    print(f"Loaded source logo: {img.size[0]}x{img.size[1]} (padded to square, RGBA)")

    save_png(img, 16, os.path.join(OUT_DIR, "favicon-16x16.png"))
    save_png(img, 32, os.path.join(OUT_DIR, "favicon-32x32.png"))
    save_apple_touch_icon(img, 180, os.path.join(OUT_DIR, "apple-touch-icon.png"))
    save_png(img, 192, os.path.join(OUT_DIR, "android-chrome-192x192.png"))
    save_png(img, 512, os.path.join(OUT_DIR, "android-chrome-512x512.png"))
    save_ico(img, os.path.join(OUT_DIR, "favicon.ico"))
    write_manifest(os.path.join(OUT_DIR, "site.webmanifest"))

    print("\nDone. All files written to the site root.")

if __name__ == "__main__":
    main()