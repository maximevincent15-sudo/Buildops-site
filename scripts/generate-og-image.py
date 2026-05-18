"""
Génère l'image Open Graph 1200×630 pour les preview de partage social
(LinkedIn, Twitter/X, WhatsApp, Slack, email signature, etc.).

Format : 1200×630 px (ratio 1.91:1, standard Open Graph)
Style : gradient bleu Firovia (#3A5CA8 → #5578C8) + wordmark + tagline
"""

from PIL import Image, ImageDraw, ImageFont
import os

WIDTH, HEIGHT = 1200, 630

# Couleurs Firovia
BLUE_1 = (58, 92, 168)     # #3A5CA8
BLUE_2 = (85, 120, 200)    # #5578C8
INK = (28, 33, 48)         # #1C2130
WHITE = (255, 255, 255)
WHITE_60 = (255, 255, 255, 153)


def make_gradient(width, height, color1, color2):
    """Gradient diagonal 135° (haut-gauche → bas-droite)."""
    img = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        for x in range(width):
            # Ratio diagonal
            t = (x + y) / (width + height)
            r = int(color1[0] + (color2[0] - color1[0]) * t)
            g = int(color1[1] + (color2[1] - color1[1]) * t)
            b = int(color1[2] + (color2[2] - color1[2]) * t)
            draw.point((x, y), fill=(r, g, b))
    return img


def make_gradient_fast(width, height, color1, color2):
    """Version rapide via numpy si dispo, sinon utilise PIL pure."""
    try:
        import numpy as np
        arr = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(3):
            top = color1[i]
            bot = color2[i]
            # Gradient diagonal : on combine x et y
            x_grad = np.linspace(0, 1, width).reshape(1, -1)
            y_grad = np.linspace(0, 1, height).reshape(-1, 1)
            t = (x_grad + y_grad) / 2
            arr[:, :, i] = top + (bot - top) * t
        return Image.fromarray(arr)
    except ImportError:
        return make_gradient(width, height, color1, color2)


def try_load_font(candidates, size):
    """Essaye plusieurs chemins de fonts (macOS / Linux / fallback)."""
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# ─── 1. Fond gradient ─────────────────────────────────────────────────
img = make_gradient_fast(WIDTH, HEIGHT, BLUE_1, BLUE_2)
draw = ImageDraw.Draw(img)

# ─── 2. Carré "F" en haut à gauche (rappel favicon) ──────────────────
# Carré 100×100 px avec coin arrondi
square_x, square_y = 80, 80
square_size = 100
draw.rounded_rectangle(
    [square_x, square_y, square_x + square_size, square_y + square_size],
    radius=22,
    fill=WHITE,
)
# Lettre F bleue dedans
f_font_candidates = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/Avenir.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
f_font = try_load_font(f_font_candidates, 70)
# Centre approximatif
draw.text((square_x + 28, square_y + 8), "F", fill=BLUE_1, font=f_font)

# ─── 3. Wordmark "Firovia" à côté ─────────────────────────────────────
wordmark_font = try_load_font(f_font_candidates, 56)
draw.text((square_x + square_size + 24, square_y + 24), "Firovia", fill=WHITE, font=wordmark_font)

# ─── 4. Tagline principale (en gros, centre) ──────────────────────────
title_font = try_load_font(f_font_candidates, 76)
title_line1 = "Le logiciel des PME"
title_line2 = "de maintenance incendie."
draw.text((80, 290), title_line1, fill=WHITE, font=title_font)
draw.text((80, 380), title_line2, fill=WHITE, font=title_font)

# ─── 5. Sous-tagline ─────────────────────────────────────────────────
sub_font = try_load_font(f_font_candidates, 28)
sub = "Planning · Rapports terrain · Conformité réglementaire"
draw.text((80, 490), sub, fill=(220, 230, 250), font=sub_font)

# ─── 6. URL en bas-droite ────────────────────────────────────────────
url_font = try_load_font(f_font_candidates, 24)
url = "firovia.fr"
draw.text((80, 555), url, fill=(220, 230, 250), font=url_font)

# ─── 7. Sauvegarde ───────────────────────────────────────────────────
output_path = "/Users/macbookair/Saas BTP/og-image.png"
img.save(output_path, "PNG", optimize=True)
print(f"✅ Image OG générée : {output_path}")
print(f"   Taille : {os.path.getsize(output_path) // 1024} Ko")
