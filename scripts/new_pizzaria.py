#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
�══════════════════════════════════════════════════════════════════╗
│  🍕 PIZZA BOA — Gerador de App para Nova Pizzaria              │
│  Script que automatiza a clonagem e customização do app         │
�══════════════════════════════════════════════════════════════════╝

Uso:
  python3 new_pizzaria.py --nome "Pizza Nova" --app-id "com.pizzanova.app" \
      --api-url "https://script.google.com/macros/s/SEU_ID/exec" \
      --sheet-id "1SEUSHEETID" --whatsapp "19999999999" --cor-primaria "#e11d48"

Requisitos:
  - Python 3.8+
  - Pillow (pip install Pillow)
  - Node.js 18+ instalado (para npm install)
  - Android SDK instalado (ANDROID_HOME)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# CORES E PADR�ES
# ═══════════════════════════════════════════════════════════════════

DEFAULT_COLORS = {
    "cor_primaria": "#581c87",
    "cor_accent": "#a855f7",
    "cor_fundo": "#0a0a0a",
    "cor_surface": "#1a1a1a",
    "cor_texto": "#ffffff",
    "cor_fundo_app": "#0a0a0a",
}

STATUS_MSGS = [
    ("recebido", "Recebido", "Pedido Recebido!", "Seu pedido foi recebido!"),
    ("confirmado", "Confirmado", "Pedido Confirmado!", "Seu pedido foi confirmado!"),
    ("em_preparo", "Em Preparo", "Em Preparo!", "Seu pedido está sendo preparado!"),
    ("no_forno", "No Forno", "No Forno!", "Seu pedido foi para o forno!"),
    ("saiu_entrega", "Saiu p/ Entrega", "Saiu para Entrega!", "Seu pedido saiu para entrega!"),
    ("retirou", "Retirado", "Retirado!", "Seu pedido foi retirado!"),
    ("entregue", "Entregue", "Entregue!", "Seu pedido foi entregue!"),
    ("cancelado", "Cancelado", "Cancelado!", "Seu pedido foi cancelado."),
]

# ═══════════════════════════════════════════════════════════════════
# GERAÇÃO DO ÍCONE (PIL)
# ═══════════════════════════════════════════════════════════════════

def generate_icon(size, bg_hex, output_path):
    """Gera ícone da pizza com fundo colorido personalizado."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("  ERRO: Pillow nao instalado. Rode: pip install Pillow")
        sys.exit(1)

    bg = hex_to_rgba(bg_hex, 255)
    pizza_base = (255, 200, 100)
    pizza_border = (224, 168, 48)
    topping = (190, 30, 30)
    shine = (255, 255, 255, 64)

    img = Image.new('RGBA', (size, size), bg)
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    radius = int(size * 0.40)
    border_w = max(2, int(size * 0.02))

    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=pizza_base)
    for i in range(border_w):
        r = radius - i
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=pizza_border)

    import math
    slice_len = int(radius * 0.92)
    for angle in [270, 225, 180, 135, 90, 45, 0, 315]:
        rad = math.radians(angle)
        ex = cx + int(slice_len * math.cos(rad))
        ey = cy + int(slice_len * math.sin(rad))
        lw = max(1, int(size * 0.015))
        draw.line([(cx, cy), (ex, ey)], fill=(245, 216, 154), width=lw)

    for i in range(border_w):
        r = radius - i
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=pizza_border)

    scale = size / 108
    positions = [
        (40, 50, 5), (55, 42, 4), (62, 58, 5), (45, 65, 4),
        (38, 42, 4), (50, 76, 4), (68, 45, 4), (30, 58, 3.5), (62, 36, 3.5)
    ]
    for tx, ty, tr in positions:
        px, py = int(tx * scale), int(ty * scale)
        scaled_tr = max(2, int(tr * scale))
        draw.ellipse([px - scaled_tr, py - scaled_tr, px + scaled_tr, py + scaled_tr], fill=topping)

    shine_cx, shine_cy = int(44 * scale), int(30 * scale)
    shine_r = int(12 * scale)
    for i in range(int(shine_r)):
        alpha = max(0, 60 - int(i * 5))
        if alpha <= 0:
            break
        r = shine_r - i
        draw.arc([shine_cx - r, shine_cy - r, shine_cx + r, shine_cy + r],
                 200, 340, fill=(255, 255, 255, alpha), width=1)

    img.save(output_path)
    return True


def hex_to_rgba(hex_color, alpha=255):
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return (r, g, b, alpha)


# ═══════════════════════════════════════════════════════════════════
# FUNÇÕES DE SUBSTITUIÇÃO DE ARQUIVOS
# ═══════════════════════════════════════════════════════════════════

def replace_in_file(path, replacements):
    """Aplica uma lista de (old, new) replacements em um arquivo."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def update_config_js(config_path, args):
    """Atualiza o config.js com os dados da nova pizzaria."""
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    substitutions = [
        ('nome: "Pizza Boa"', f'nome: "{args.nome}"'),
        ('slogan: "Delivery"', f'slogan: "{args.slogan}"'),
        (
            'apiUrl: "https://script.google.com/macros/s/AKfycbxnxQ9Hj6hEbmveEPNySjkLYXRMwXIwdhV4TGeiLIJn6uf0evIUPne1X6XFJPimhi5qAQ/exec"',
            f'apiUrl: "{args.api_url}"'
        ),
        ('sheetId: "1EwtGeTtkl0WcKdl_2UZrZhLAU55xfx0hLAEkn1kN_2M"', f'sheetId: "{args.sheet_id}"'),
        ('whatsapp: "19984356289"', f'whatsapp: "{args.whatsapp}"'),
        (f'corPrimaria: "{DEFAULT_COLORS["cor_primaria"]}"', f'corPrimaria: "{args.cor_primaria}"'),
        (f'corAccent: "{DEFAULT_COLORS["cor_accent"]}"', f'corAccent: "{args.cor_accent}"'),
        (f'corFundo: "{DEFAULT_COLORS["cor_fundo"]}"', f'corFundo: "{args.cor_fundo}"'),
        (f'corSurface: "{DEFAULT_COLORS["cor_surface"]}"', f'corSurface: "{args.cor_surface}"'),
        (f'corTexto: "{DEFAULT_COLORS["cor_texto"]}"', f'corTexto: "{args.cor_texto}"'),
        (f'pedidoMinimo: {DEFAULTS["pedido_minimo"]}', f'pedidoMinimo: {args.pedido_minimo}'),
    ]

    if args.senha_admin != "1234":
        substitutions.append(('"senhaAdmin": "1234"', f'"senhaAdmin": "{args.senha_admin}"'))

    content_raw = content
    for old, new in substitutions:
        content = content.replace(old, new)

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [OK] config.js atualizado")


def update_capacitor_config(config_path, args):
    """Atualiza capacitor.config.json."""
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data['appId'] = args.app_id
    data['appName'] = args.nome
    data['android']['backgroundColor'] = args.cor_fundo
    data['plugins']['StatusBar']['backgroundColor'] = args.cor_fundo
    data['plugins']['SplashScreen']['backgroundColor'] = args.cor_fundo

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"  [OK] capacitor.config.json atualizado (appId: {args.app_id})")


def update_strings_xml(strings_path, args):
    """Atualiza strings.xml com nome e package."""
    replacements = [
        ('<string name="app_name">Pizza Boa</string>', f'<string name="app_name">{args.nome}</string>'),
        ('<string name="title_activity_main">Pizza Boa</string>', f'<string name="title_activity_main">{args.nome}</string>'),
        ('<string name="package_name">com.pizzaboa.app</string>', f'<string name="package_name">{args.app_id}</string>'),
        ('<string name="custom_url_scheme">com.pizzaboa.app</string>', f'<string name="custom_url_scheme">{args.app_id}</string>'),
    ]
    replace_in_file(strings_path, replacements)
    print(f"  [OK] strings.xml atualizado")


def update_build_gradle(build_path, args):
    """Atualiza build.gradle com namespace e applicationId."""
    replacements = [
        ('namespace "com.pizzaboa.app"', f'namespace "{args.app_id}"'),
        ('applicationId "com.pizzaboa.app"', f'applicationId "{args.app_id}"'),
    ]
    replace_in_file(build_path, replacements)
    print(f"  [OK] build.gradle atualizado")


def update_manifest_bg(manifest_path, cor_primaria):
    """Atualiza a cor de fundo do icone no AndroidManifest."""
    if not os.path.exists(manifest_path):
        return

    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(
        r'<meta-data android:name="io\.capacitor\.launcher\.background_color" android:resource="@color/ico_app_background"/>',
        f'<meta-data android:name="io.capacitor.launcher.background_color" android:resource="@color/ico_app_background"/>',
        content
    )

    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)


def update_package_json(pkg_path, args):
    """Atualiza package.json com nome e descrição."""
    with open(pkg_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data['name'] = args.nome.lower().replace(' ', '-')
    data['description'] = f"{args.nome} - Delivery App"

    with open(pkg_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"  [OK] package.json atualizado")


def update_config_bg_vector(drawable_path, cor_primaria):
    """Atualiza cor de fundo do icone vector."""
    if not os.path.exists(drawable_path):
        return

    with open(drawable_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r'(android:fillColor=)"(#[0-9a-fA-F]{6})"', lambda m: f'{m.group(1)}"{cor_primaria}"', content)

    # Update background too - replace teal color #26A69A with new primary
    content = content.replace('#26A69A', cor_primaria)

    with open(drawable_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [OK] icone background drawable atualizado")


def update_territorio_cor(colors_xml_path, cor_primaria):
    """Atualiza cor primaria no seu_app_colors.xml."""
    if not os.path.exists(colors_xml_path):
        return
    with open(colors_xml_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'<color name="ico_app_background">#26A69A</color>',
                     f'<color name="ico_app_background">{cor_primaria}</color>', content)
    with open(colors_xml_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [OK] Cor do icone atualizada")


def update_splash_background(drawable_path, cor_fundo):
    """Atualiza cor de fundo da splash screen."""
    if not os.path.exists(drawable_path):
        return

    with open(drawable_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace solid color background lines
    content = re.sub(r'<item android:drawable="@color/bg_color"/>.*',
                      '', content, flags=re.DOTALL)
    content = re.sub(r'<solid android:color="[0-9a-fA-F#]{1,8}"\s*/?>',
                      f'<solid android:color="{cor_fundo}"/>', content)

    with open(drawable_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [OK] Splash screen atualizado")


# ═══════════════════════════════════════════════════════════════════
# ÍCONES NATIVOS (PNG)
# ═══════════════════════════════════════════════════════════════════

def generate_icons(res_dir, cor_primaria):
    """Gera os PNGs do ícone em todas as resoluções."""
    sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192,
    }

    for folder, size in sizes.items():
        folder_path = os.path.join(res_dir, folder)
        if not os.path.exists(folder_path):
            continue

        generate_icon(size, cor_primaria, os.path.join(folder_path, 'ic_launcher.png'))
        # round
        generate_icon(size, cor_primaria, os.path.join(folder_path, 'ic_launcher_round.png'))

    print("  [OK] Icones PNG gerados em todas as resolucoes")


def generate_foreground_png(res_dir, cor_primaria):
    """Gera PNG do foreground do adaptive icon."""
    sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192,
    }

    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("  ERRO: Pillow nao instalado")
        return

    for folder, size in sizes.items():
        folder_path = os.path.join(res_dir, folder)
        if not os.path.exists(folder_path):
            continue

        # Foreground: transparent background with pizza centered
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = size // 2, size // 2
        radius = int(size * 0.42)
        pizza_base = (255, 200, 100)
        pizza_border = (224, 168, 48)
        topping = (190, 30, 30)

        import math
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=pizza_base)

        border_w = max(2, int(size * 0.02))
        for i in range(border_w):
            r = radius - i
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=pizza_border)

        slice_len = int(radius * 0.92)
        for angle in [270, 225, 180, 135, 90, 45, 0, 315]:
            rad = math.radians(angle)
            ex = cx + int(slice_len * math.cos(rad))
            ey = cy + int(slice_len * math.sin(rad))
            draw.line([(cx, cy), (ex, ey)], fill=(245, 216, 154), width=max(1, int(size * 0.015)))

        for i in range(border_w):
            r = radius - i
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=pizza_border)

        scale = size / 108
        positions = [
            (40, 50, 5), (55, 42, 4), (62, 58, 5), (45, 65, 4),
            (38, 42, 4), (50, 76, 4), (68, 45, 4), (30, 58, 3.5), (62, 36, 3.5)
        ]
        for tx, ty, tr in positions:
            px, py = int(tx * scale), int(ty * scale)
            scaled_tr = max(2, int(tr * scale))
            draw.ellipse([px - scaled_tr, py - scaled_tr, px + scaled_tr, py + scaled_tr], fill=topping)

        img.save(os.path.join(folder_path, 'ic_launcher_foreground.png'))

    print("  [OK] Icones foreground PNG gerados")


# ═══════════════════════════════════════════════════════════════════
# COPIAR E CUSTOMIZAR
# ═══════════════════════════════════════════════════════════════════

def clone_project(src, dest, args):
    """Copia o template para o destino e aplica customizações."""
    print(f"\n{'='*60}")
    print(f"  CLONANDO APP: {args.nome}")
    print(f"{'='*60}")

    if os.path.exists(dest):
        print(f"  AVISO: Pasta {dest} ja existe. Removendo...")
        shutil.rmtree(dest)

    shutil.copytree(src, dest,
                    ignore=shutil.ignore_patterns('node_modules', '.git', 'build', '.gradle', 'android/app/build', 'android/.gradle',
                                                  'www/capacitor.js', 'www/plugins'))
    print(f"  [OK] Template copiado para {dest}")

    dest = Path(dest)

    # Arquivos para atualizar
    config_js = dest / 'www/config.js'
    capacitor_config = dest / 'capacitor.config.json'
    strings_xml = dest / 'android/app/src/main/res/values/strings.xml'
    build_gradle = dest / 'android/app/build.gradle'
    package_json = dest / 'package.json'
    drawable_bg = dest / 'android/app/src/main/res/drawable/ic_launcher_background.xml'
    colors_xml = dest / 'android/app/src/main/res/values/your_app_colors.xml' if (dest / 'android/app/src/main/res/values/your_app_colors.xml').exists() else None
    splash_bg_path = dest / 'android/app/src/main/res/drawable/launch_background.xml'
    splash_bg = splash_bg_path if splash_bg_path.exists() else None
    res_dir = dest / 'android/app/src/main/res'

    print("\n  --- Atualizando arquivos de configuracao ---")
    update_config_js(str(config_js), args)
    update_capacitor_config(str(capacitor_config), args)
    update_strings_xml(str(strings_xml), args)
    update_build_gradle(str(build_gradle), args)
    update_package_json(str(package_json), args)
    update_config_bg_vector(str(drawable_bg), args.cor_primaria)

    if colors_xml:
        update_territorio_cor(str(colors_xml), args.cor_primaria)
    if splash_bg:
        update_splash_background(str(splash_bg), args.cor_fundo)

    if args.bg_color_xml:
        bg_xml = dest / 'android/app/src/main/res/values/bg_color.xml'
        if bg_xml.exists():
            with open(bg_xml, 'w', encoding='utf-8') as f:
                f.write(f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="bg_color">{args.cor_fundo}</color>\n</resources>\n')
            print("  [OK] bg_color.xml atualizado")

    if args.ico_bg_color:
        ico_bg = dest / 'android/app/src/main/res/values/ico_app_background.xml'
        if ico_bg.exists():
            with open(ico_bg, 'w', encoding='utf-8') as f:
                f.write(f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ico_app_background">{args.ico_bg_color}</color>\n</resources>\n')
            print("  [OK] ico_app_background.xml atualizado")

    print("\n  --- Gerando icones ---")
    generate_icons(str(res_dir), args.cor_primaria)
    generate_foreground_png(str(res_dir), args.cor_primaria)
    update_manifest_bg(
        str(dest / 'android/app/src/main/AndroidManifest.xml'),
        args.cor_primaria
    )

    return dest


def run_npm_install(dest):
    """Roda npm install no projeto destino."""
    print("\n  --- Instalando dependencias npm ---")
    try:
        result = subprocess.run(
            ['npm', 'install'],
            cwd=dest,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print("  [OK] npm install concluido")
            return True
        else:
            print(f"  [ERRO] npm install falhou: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  [ERRO] {e}")
        return False


def run_cap_sync(dest):
    """Roda cap sync android."""
    print("\n  --- Sincronizando Capacitor ---")
    try:
        result = subprocess.run(
            ['npx', 'cap', 'sync', 'android'],
            cwd=dest,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print("  [OK] cap sync android concluido")
            return True
        else:
            print(f"  [ERRO] cap sync falhou: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  [ERRO] {e}")
        return False


def build_apk(dest):
    """Build do APK via gradlew (Windows usa cmd.exe)."""
    print("\n  --- Building APK ---")
    gradle_cmd = f"{dest}/android/gradlew.bat" if sys.platform == 'win32' else f"{dest}/android/gradlew"
    if sys.platform == 'win32':
        cmd = ['cmd.exe', '/c', f'cd /d {dest}/android && gradlew assembleDebug']
    else:
        cmd = ['bash', '-c', f'cd {dest}/android && chmod +x gradlew && ./gradlew assembleDebug']

    try:
        result = subprocess.run(cmd, capture_output=result.returncode != 0, text=True, timeout=300)
        if result.returncode == 0:
            print("  [OK] APK gerado com sucesso")
            apk = dest / 'android/app/build/outputs/apk/debug/app-debug.apk'
            if apk.exists():
                print(f"  APK: {apk}")
            return True
        else:
            print(f"  [ERRO] Build falhou: {result.stderr[:300]}")
            return False
    except Exception as e:
        print(f"  [ERRO] {e}")
        return False


def print_instructions(dest, args):
    """Imprime instruções finais para o desenvolvedor."""
    print(f"""
{'='*60}
  ✅ APP CRIADO COM SUCESSO!
{'='*60}

  📁 Pasta: {dest}
  �️  Nome: {args.nome}
  📦 Package: {args.app_id}

{'─'*60}
  � PRÓXIMOS PASSOS:

  1. Configure o Google Apps Script (GAS):
     - Crie uma nova planilha Google
     - Cole o código GAS (ver README.md)
     - Substitua o sheetId pelo ID da nova planilha
     - Faça deploy da web app

  2. Edite os textos do cardápio:
     - Abra {dest}/www/index.html
     - Edite os itens do cardápio, preços, tamanhos

  3. Substitua os ícones (se desejar):
     - Coloque seu logo PNG em android/app/src/main/res/mipmap-*
     - Ou mantenha a pizza gerada automaticamente

  4. Faça o build do APK:
     cd {dest}
     npx cap sync android
     cd android && gradlew assembleDebug

  5. Instale no celular:
     adb install android/app/build/outputs/apk/debug/app-debug.apk

  6. Faça upload do site (GitHub Pages):
     cd {dest}
     npm run build
     git add -A && git commit -m "deploy"
     git push

{'─'*60}
  🔧 PERSONALIZAÇÕES ADICIONAIS:
  - Cores: altere corPrimaria em www/config.js
  - App name: altere em strings.xml e capacitor.config.json
  - Ícone: substitua os PNGs em mipmap-*
  - Splash screen: edite drawable/launch_background.xml
  - Cardápio: edite app.html + www/index.html

{'='*60}
""")


# ═══════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='🍕 Gerador de App Pizza Boa para Nova Pizzaria',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 new_pizzaria.py --nome "Pizza Nova" --app-id com.pizzanova.dep \\
      --api-url "https://script.google.com/macros/s/NOVO_GAS/exec" \\
      --sheet-id "NOVO_SHEET_ID" --whatsapp "19911112222" --cor-primaria "#e11d48"
        """
    )

    parser.add_argument('--nome', required=True, help='Nome da pizzaria (ex: "Pizza Nova")')
    parser.add_argument('--app-id', required=True, help='Package ID (ex: com.pizzanova.app)')
    parser.add_argument('--api-url', required=True, help='URL do Google Apps Script deployada')
    parser.add_argument('--sheet-id', required=True, help='ID da planilha Google')
    parser.add_argument('--whatsapp', required=True, help='Numero WhatsApp (ex: 19911112222)')
    parser.add_argument('--nome-admin', default='Admin', help='Nome do admin (default: Admin)')
    parser.add_argument('--senha-admin', default='1234', help='Senha admin (default: 1234)')

    parser.add_argument('--cor-primaria', default='#581c87', help='Cor primaria (default: #581c87)')
    parser.add_argument('--cor-accent', default='#a855f7', help='Cor accent (default: #a855f7)')
    parser.add_argument('--cor-fundo', default='#0a0a0a', help='Cor fundo (default: #0a0a0a)')
    parser.add_argument('--cor-surface', default='#1a1a1a', help='Cor surface (default: #1a1a1a)')
    parser.add_argument('--cor-texto', default='#ffffff', help='Cor texto (default: #ffffff)')
    parser.add_argument('--cor-fundo-app', default='#0a0a0a', help='Cor fundo app/android (default: #0a0a0a)')

    parser.add_argument('--pedido-minimo', type=float, default=30.0, help='Pedido minimo (default: 30.00)')

    parser.add_argument('--destino', default=None, help='Pasta destino (default: nome da pizzaria)')
    parser.add_argument('--icone-svg', default=None, help='Caminho para SVG/PNG customizado do icone')
    parser.add_argument('--skip-build', action='store_true', help='Pular npm install + cap sync + build')
    parser.add_argument('--template', default='.', help='Caminho do template fonte (default: diretorio atual)')

    args = parser.parse_args()

    # Validações
    if not re.match(r'^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$', args.app_id):
        print(f"  ERRO: app-id invalido: {args.app_id}")
        print("  Formato correto: com.nomedapizzaria.app (lowercase, sem caracteres especiais)")
        sys.exit(1)

    # Verifica se o template existe
    src = Path(args.template)
    if not (src / 'www/index.html').exists():
        print(f"  ERRO: Template invalido. {src}/www/index.html nao encontrado.")
        print("  Rode este script dentro do diretorio do projeto Pizza Boa.")
        sys.exit(1)

    # Define destino
    dest_path = Path(args.destino) if args.destino else src.parent / args.nome.replace(' ', '_').lower()

    # Clona e customiza
    dest = clone_project(src, dest_path, args)

    # npm install
    if not args.skip_build:
        run_npm_install(str(dest))
        run_cap_sync(str(dest))
        # build opcional - pode ser feito fora do script
        # build_apk(dest)

    # Instruções
    print_instructions(dest, args)


DEFAULTS = {
    "pedido_minimo": 30.00,
}


if __name__ == '__main__':
    main()
