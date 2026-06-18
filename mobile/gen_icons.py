from PIL import Image, ImageDraw
import os, math

bg_color = (10, 10, 10)
primary = (88, 28, 135)
accent = (168, 85, 247)
red_tomato = (200, 50, 30)

def draw_pizza_icon(size):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    r = int(size * 0.44)

    # Sombra
    so = int(size * 0.04)
    draw.ellipse([cx - r + so, cy - r + so, cx + r + so, cy + r + so], fill=(0, 0, 0, 60))

    # Base pizza
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=primary)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=accent, width=max(1, size // 40))

    # Fatias
    for i in range(8):
        angle = (360 / 8) * i
        rad = math.radians(angle)
        x2 = cx + int(r * 0.85 * math.cos(rad))
        y2 = cy + int(r * 0.85 * math.sin(rad))
        draw.line([(cx, cy), (x2, y2)], fill=accent, width=max(1, size // 70))

    # Pepperoni
    pr = int(size * 0.055)
    for px_pct, py_pct in [(0.35,0.25),(0.6,0.2),(0.2,0.5),(0.5,0.45),(0.75,0.55),(0.45,0.7),(0.25,0.75),(0.65,0.72)]:
        px = cx + int((px_pct - 0.5) * 2 * r * 0.7)
        py = cy + int((py_pct - 0.5) * 2 * r * 0.7)
        if math.sqrt((px-cx)**2 + (py-cy)**2) < r * 0.78:
            draw.ellipse([px-pr, py-pr, px+pr, py+pr], fill=red_tomato)

    # Brilho
    hr = int(r * 0.32)
    hl = Image.new('RGBA', (size, size), (0,0,0,0))
    ImageDraw.Draw(hl).ellipse([cx-hr, cy-int(r*0.55), cx+hr, cy-int(r*0.12)], fill=(255,255,255,20))
    img = Image.alpha_composite(img, hl)
    return img

def make_square_icon(size):
    bg = Image.new('RGBA', (size, size), bg_color)
    pizza = draw_pizza_icon(int(size * 0.8))
    off = (size - pizza.size[0]) // 2
    bg.paste(pizza, (off, off), pizza)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,size,size], radius=int(size*0.18), fill=255)
    result = Image.new('RGBA', (size, size), (0,0,0,0))
    result.paste(bg, mask=mask)
    return result

def make_round_icon(size):
    bg = Image.new('RGBA', (size, size), bg_color)
    pizza = draw_pizza_icon(int(size * 0.84))
    off = (size - pizza.size[0]) // 2
    bg.paste(pizza, (off, off), pizza)
    return bg

sizes = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
base = '/mnt/c/Users/deeh_/pizza-delivery/mobile/android/app/src/main/res'

print("Gerando icones mipmap...")
for density, px in sizes.items():
    d = f'{base}/mipmap-{density}'
    os.makedirs(d, exist_ok=True)
    make_square_icon(px).save(f'{d}/ic_launcher.png')
    make_round_icon(px).save(f'{d}/ic_launcher_round.png')
    print(f'  {density}: {px}px')

print("Gerando adaptive icon...")
fg_size = 864
fg = draw_pizza_icon(int(fg_size * 0.88))
fg_bg = Image.new('RGBA', (fg_size, fg_size), (0,0,0,0))
off = (fg_size - fg.size[0]) // 2
fg_bg.paste(fg, (off, off), fg)
dd = f'{base}/drawable-v24'
os.makedirs(dd, exist_ok=True)
fg_bg.save(f'{dd}/ic_launcher_foreground.png')
Image.new('RGBA', (fg_size, fg_size), bg_color).save(f'{dd}/ic_launcher_background.png')

with open(f'{dd}/ic_launcher.xml', 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n    <background android:drawable="@drawable/ic_launcher_background"/>\n    <foreground android:drawable="@drawable/ic_launcher_foreground"/>\n</adaptive-icon>\n')

with open(f'{base}/values/ic_launcher_background.xml', 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#0a0a0a</color>\n</resources>\n')

print('Pronto!')
