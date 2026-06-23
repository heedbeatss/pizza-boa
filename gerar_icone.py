from PIL import Image, ImageDraw
import os
import math

# Tamanhos dos ícones Android (em pixels)
sizes = {
    'mdpi': 48,
    'hdpi': 72,
    'xhdpi': 96,
    'xxhdpi': 144,
    'xxxhdpi': 192
}

density = 'ic_launcher.png'
pastas = {
    'mdpi': 'android/app/src/main/res/mipmap-hdpi',
    'hdpi': 'android/app/src/main/res/mipmap-hdpi',
    'xhdpi': 'android/app/src/main/res/mipmap-xhdpi',
    'xxhdpi': 'android/app/src/main/res/mipmap-xxhdpi',
    'xxxhdpi': 'android/app/src/main/res/mipmap-xxxhdpi'
}

# Cria os diretórios se não existirem
for pasta in pastas.values():
    os.makedirs(pasta, exist_ok=True)

# Cria o ícone da pizza para cada tamanho
for dens, size in sizes.items():
    # Cria imagem com fundo roxo
    img = Image.new('RGBA', (size, size), (88, 28, 135, 255))
    draw = ImageDraw.Draw(img)
    
    # Desenha um círculo de fundo mais claro
    padding = int(size * 0.1)
    draw.ellipse([padding, padding, size-padding, size-padding], fill=(126, 34, 206, 255))
    
    # Desenha uma pizza estilizada
    center = size // 2
    radius = int(size * 0.3)
    
    # Círculo amarelo (massa da pizza)
    draw.ellipse([center-radius, center-radius, center+radius, center+radius], fill=(255, 200, 50, 255))
    
    # Borda da pizza (crosta)
    draw.ellipse([center-radius, center-radius, center+radius, center+radius], outline=(200, 150, 30, 255), width=max(2, size//24))
    
    # Fatias da pizza
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = math.radians(angle)
        x1 = center + int(radius * 0.2 * math.cos(rad))
        y1 = center + int(radius * 0.2 * math.sin(rad))
        x2 = center + int(radius * 0.85 * math.cos(rad))
        y2 = center + int(radius * 0.85 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=(200, 150, 30, 255), width=max(1, size//48))
    
    # Pontos de pepperoni
    for angle in [30, 90, 150, 210, 270, 330]:
        rad = math.radians(angle)
        px = center + int(radius * 0.55 * math.cos(rad))
        py = center + int(radius * 0.55 * math.sin(rad))
        r = max(2, size // 16)
        draw.ellipse([px-r, py-r, px+r, py+r], fill=(180, 50, 50, 255))
    
    # Salva o ícone
    path = f"android/app/src/main/res/mipmap-{dens}/{density}"
    img.save(path, 'PNG')
    print(f"OK - {path} ({size}x{size})")

print("\n" + "="*50)
print("ÍCÔNES CRIADOS COM SUCESSO!")
print("="*50)
print("\nAgora faça o build do APK novamente:")
print("1. Build -> Clean Project")
print("2. Build -> Rebuild Project")
print("3. Build -> Build Bundle(s) / APK(s) -> Build APK(s)")
