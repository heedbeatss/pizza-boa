from PIL import Image, ImageDraw
import os, math

# Generate pizza icons using PIL based on ic_launcher_foreground.xml design
PIZZA_BASE = (255, 200, 100)    # #ffc864
PIZZA_BORDER = (224, 168, 48)   # #e0a830
TOPPING = (190, 30, 30)         # #be1e1e
BG_COLOR = (88, 28, 135)        # #581c87

sizes = {
    'mdpi': 48,
    'hdpi': 72,
    'xhdpi': 96,
    'xxhdpi': 144,
    'xxxhdpi': 192,
}

base = r"C:\Users\deeh_\pizza-delivery\android\app\src\main\res"

def draw_pizza_icon(size):
    img = Image.new('RGBA', (size, size), BG_COLOR + (255,))
    draw = ImageDraw.Draw(img)
    
    cx, cy = size // 2, size // 2
    radius = int(size * 0.40)
    border_width = max(2, int(size * 0.02))
    topping_r = max(2, int(size * 0.045))
    
    # Pizza dough circle
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
    draw.ellipse(bbox, fill=PIZZA_BASE)
    
    # Border ring (crust)
    for i in range(border_width):
        r = radius - i
        ring_bbox = [cx - r, cy - r, cx + r, cy + r]
        draw.ellipse(ring_bbox, outline=PIZZA_BORDER)
    
    # Slice lines
    slice_len = int(radius * 0.92)
    slice_angles = [270, 225, 180, 135, 90, 45, 0, 315]
    line_w = max(1, int(size * 0.015))
    
    for angle in slice_angles:
        rad = math.radians(angle)
        end_x = cx + int(slice_len * math.cos(rad))
        end_y = cy + int(slice_len * math.sin(rad))
        draw.line([(cx, cy), (end_x, end_y)], fill=(245, 216, 154), width=line_w)
    
    # Recover border after lines
    for i in range(border_width):
        r = radius - i
        ring_bbox = [cx - r, cy - r, cx + r, cy + r]
        draw.ellipse(ring_bbox, outline=PIZZA_BORDER)
    
    # Pepperoni positions (from XML, scaled from 108 viewport)
    topping_positions = [
        (40, 50, 5), (55, 42, 4), (62, 58, 5), (45, 65, 4),
        (38, 42, 4), (50, 76, 4), (68, 45, 4), (30, 58, 3.5), (62, 36, 3.5)
    ]
    
    scale_factor = size / 108
    
    for tx, ty, tr in topping_positions:
        px = int(tx * scale_factor)
        py = int(ty * scale_factor)
        scaled_tr = max(2, int(tr * scale_factor))
        bbox_top = [px - scaled_tr, py - scaled_tr, px + scaled_tr, py + scaled_tr]
        draw.ellipse(bbox_top, fill=TOPPING)
    
    # Shine highlight on top-left
    shine_cx = int(44 * scale_factor)
    shine_cy = int(30 * scale_factor)
    shine_r = int(12 * scale_factor)
    
    for i in range(int(shine_r)):
        alpha = max(0, 60 - int(i * 5))
        if alpha <= 0:
            break
        r = shine_r - i
        sbbox = [shine_cx - r, shine_cy - r, shine_cx + r, shine_cy + r]
        draw.arc(sbbox, 200, 340, fill=(255, 255, 255, alpha), width=1)
    
    return img

for density, size in sizes.items():
    folder = os.path.join(base, f"mipmap-{density}")
    os.makedirs(folder, exist_ok=True)
    
    icon = draw_pizza_icon(size)
    icon.save(os.path.join(folder, "ic_launcher.png"))
    icon.save(os.path.join(folder, "ic_launcher_round.png"))
    
    print(f"Generated {density}: {size}x{size}px")

print("\nAll icons generated!")
