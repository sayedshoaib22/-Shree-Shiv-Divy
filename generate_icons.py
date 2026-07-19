from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

root = Path(r"c:\Users\ss386\OneDrive\Desktop\New folder (9)")
logo = Image.open(root / 'images' / 'Shree-Shiv-Divy-Logo.webp').convert('RGBA')
logo = ImageOps.contain(logo, (512, 512))

base = Image.new('RGBA', (512, 512), (255, 255, 255, 0))
mask = Image.new('L', (512, 512), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((40, 40, 472, 472), fill=255)

bg = Image.new('RGBA', (512, 512), (166, 130, 31, 255))
logo = logo.resize((320, 320), Image.Resampling.LANCZOS)
base.paste(bg, (0, 0), mask)
base.paste(logo, ((512 - logo.size[0]) // 2, (512 - logo.size[1]) // 2), logo)

for size in [16, 32, 48, 64, 96, 128, 192, 256, 512]:
    img = base.resize((size, size), Image.Resampling.LANCZOS)
    img.save(root / f'favicon-{size}.png')

base64 = base.resize((64, 64), Image.Resampling.LANCZOS)
base64.save(root / 'favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

apple = base.resize((180, 180), Image.Resampling.LANCZOS)
apple.save(root / 'apple-touch-icon.png')

for size in [192, 512]:
    img = base.resize((size, size), Image.Resampling.LANCZOS)
    img.save(root / f'android-chrome-{size}.png')

print('generated icons')
