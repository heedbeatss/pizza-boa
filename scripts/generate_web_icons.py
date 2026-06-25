#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera ícones para PWA/navegador baseados na pizza do app Android.
Cria: favicon.ico, icon-192.png, icon-512.png, apple-touch-icon.png, mask-icon.svg
"""

import math
import os
import sys
from PIL import Image, ImageDraw

# Configurações
COR_FUNDO = "#581c87"  # Deve bater com corPrimaria do config.js
PIZZA_BASE = (255, 200, 100)
PIZZA_BORDER = (224, 168, 48)
TOPPING = (190, 30, 30)

WEB_ICONS = [
    ("icon-192.png", 192),
    ("icon-512.png", 512),
    ("apple-touch-icon.png", 180),
    ("favicon-16.png", 16),
    ("favicon-32.png", 32),
    ("favicon-48.png", 48),
]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))


def draw_pizza(size, bg_rgb, with_background=True):
    """Desenha a pizza no tamanho especificado."""
    if with_background:
        img = Image.new('RGBA', (size, size), bg_rgb + (255,))
    else:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    radius = int(size * 0.40)
    border_w = max(2, int(size * 0.02))

    # Pizza base
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=PIZZA_BASE)

    # Border ring
    for i in range(border_w):
        r = radius - i
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=PIZZA_BORDER)

    # Slice lines
    slice_len = int(radius * 0.92)
    for angle in [270, 225, 180, 135, 90, 45, 0, 315]:
        rad = math.radians(angle)
        ex = cx + int(slice_len * math.cos(rad))
        ey = cy + int(slice_len * math.sin(rad))
        draw.line([(cx, cy), (ex, ey)], fill=(245, 216, 154), width=max(1, int(size * 0.015)))

    # Recover border
    for i in range(border_w):
        r = radius - i
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=PIZZA_BORDER)

    # Pepperoni
    scale = size / 108
    positions = [
        (40, 50, 5), (55, 42, 4), (62, 58, 5), (45, 65, 4),
        (38, 42, 4), (50, 76, 4), (68, 45, 4), (30, 58, 3.5), (62, 36, 3.5)
    ]
    for tx, ty, tr in positions:
        px, py = int(tx * scale), int(ty * scale)
        scaled_tr = max(2, int(tr * scale))
        draw.ellipse([px - scaled_tr, py - scaled_tr, px + scaled_tr, py + scaled_tr], fill=TOPPING)

    # Shine
    shine_cx, shine_cy = int(44 * scale), int(30 * scale)
    shine_r = int(12 * scale)
    for i in range(int(shine_r)):
        alpha = max(0, 60 - int(i * 5))
        if alpha <= 0:
            break
        r = shine_r - i
        draw.arc([shine_cx - r, shine_cy - r, shine_cx + r, shine_cy + r],
                 200, 340, fill=(255, 255, 255, alpha), width=1)

    return img


def generate_favicon_ico(output_path, bg_rgb):
    """Gera favicon.ico com múltiplos tamanhos num único arquivo."""
    sizes = [16, 32, 48]
    images = []
    for size in sizes:
        img = draw_pizza(size, bg_rgb)
        images.append(img.convert('RGBA'))

    # ICO salva múltiplos tamanhos no mesmo arquivo
    images[0].save(
        output_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    return True


def generate_mask_icon_svg(output_path):
    """Gera mask-icon SVG (para Safari pinned tab)."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108">
  <circle cx="54" cy="54" r="54" fill="#581c87"/>
  <circle cx="54" cy="54" r="38" fill="#ffc864"/>
  <circle cx="54" cy="54" r="36" fill="none" stroke="#e0a830" stroke-width="3"/>
  <line x1="54" y1="54" x2="54" y2="18" stroke="#f5d89a" stroke-width="1.5"/>
  <line x1="54" y1="54" x2="80" y2="28" stroke="#f5d89a" stroke-width="1.5"/>
  <line x1="54" y1="54" x2="86" y2="54" stroke="#f5d89a" stroke-width="1.5"/>
  <line x1="54" y1="54" x2="80" y2="80" stroke="#f5d89a" stroke-width="1.5"/>
  <line x1="54" y1="54" x2="54" y2="90" stroke="#f5d89a" stroke-width="1.5"/>
  <line x1="54" y1="54" x2="28" y2="80" stroke="#f5d89a" stroke-width="1.5"/>
  <line x1="54" y1="54" x2="22" y2="54" stroke="#f5d89a" stroke-width="1.5"/>
  <line x1="54" y1="54" x2="28" y2="28" stroke="#f5d89a" stroke-width="1.5"/>
  <circle cx="40" cy="50" r="5" fill="#be1e1e"/>
  <circle cx="55" cy="42" r="4" fill="#be1e1e"/>
  <circle cx="62" cy="58" r="5" fill="#be1e1e"/>
  <circle cx="45" cy="65" r="4" fill="#be1e1e"/>
</svg>'''
    with open(output_path, 'w') as f:
        f.write(svg)
    return True


def main():
    # Diretório de saída: www/icons/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(project_dir, 'www', 'icons')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    bg_rgb = hex_to_rgb(COR_FUNDO)

    print("Gerando icones web...")

    # Gerar PNGs individuais
    for filename, size in WEB_ICONS:
        img = draw_pizza(size, bg_rgb)
        output_path = os.path.join(output_dir, filename)
        img.save(output_path)
        print(f"  {filename} ({size}x{size})")

    # Gerar favicon.ico
    favicon_path = os.path.join(output_dir, 'favicon.ico')
    generate_favicon_ico(favicon_path, bg_rgb)
    print(f"  favicon.ico (multi-tamanho)")

    # Gerar mask-icon.svg
    mask_path = os.path.join(output_dir, 'mask-icon.svg')
    generate_mask_icon_svg(mask_path)
    print(f"  mask-icon.svg (Safari pinned tab)")

    print(f"\nTodos os icones salvos em: {output_dir}")
    print("\nAdicione no <head> do index.html:")
    print('  <link rel="icon" type="image/x-icon" href="icons/favicon.ico">')
    print('  <link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">')
    print('  <link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">')
    print('  <link rel="apple-touch-icon" sizes="180x180" href="icons/apple-touch-icon.png">')
    print('  <link rel="mask-icon" href="icons/mask-icon.svg" color="#581c87">')


if __name__ == '__main__':
    main()
