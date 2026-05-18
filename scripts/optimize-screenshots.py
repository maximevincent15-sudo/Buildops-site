"""
Compresse les screenshots PNG du showcase vitrine.

Stratégie : conversion en palette indexée 256 couleurs (suffisant pour des
UI screenshots qui ont peu de couleurs distinctes), puis optimisation PNG.
Gain typique : 60-80% sans perte visuelle perceptible.

Avant compression, on backup les originaux dans original-screenshots/.
"""

from PIL import Image
import os
import shutil

SCREENSHOTS = [
    "dashboard.png",
    "planning.png",
    "rapports.png",
    "alertes.png",
    "clients.png",
    "techniciens.png",
    "devis.png",
    "factures.png",
    "archivage.png",
    "parametres.png",
]

BASE_DIR = "/Users/macbookair/Saas BTP"
BACKUP_DIR = os.path.join(BASE_DIR, "original-screenshots")


def humanize_size(bytes_count):
    for unit in ["B", "Ko", "Mo"]:
        if bytes_count < 1024:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024
    return f"{bytes_count:.1f} Go"


# Création du dossier de backup si nécessaire
os.makedirs(BACKUP_DIR, exist_ok=True)

total_before = 0
total_after = 0

print("─" * 70)
print(f"{'Fichier':<25} {'Avant':>12} {'Après':>12} {'Gain':>10}")
print("─" * 70)

for filename in SCREENSHOTS:
    src = os.path.join(BASE_DIR, filename)
    if not os.path.exists(src):
        print(f"⚠️  {filename} introuvable, skip.")
        continue

    # Backup de l'original (uniquement la 1ère fois)
    backup_path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(backup_path):
        shutil.copy2(src, backup_path)

    # Taille avant
    size_before = os.path.getsize(src)
    total_before += size_before

    # Conversion en palette adaptive (256 couleurs max)
    img = Image.open(backup_path)  # On part du backup pour éviter dégradation cumulée
    if img.mode != "RGB":
        img = img.convert("RGB")
    # Quantification adaptive en palette 256 couleurs
    palette_img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    # Sauvegarde optimisée
    palette_img.save(src, "PNG", optimize=True)

    # Taille après
    size_after = os.path.getsize(src)
    total_after += size_after

    gain_pct = (1 - size_after / size_before) * 100
    print(
        f"{filename:<25} {humanize_size(size_before):>12} {humanize_size(size_after):>12} {gain_pct:>8.1f}%"
    )

print("─" * 70)
gain_total = (1 - total_after / total_before) * 100 if total_before > 0 else 0
print(
    f"{'TOTAL':<25} {humanize_size(total_before):>12} {humanize_size(total_after):>12} {gain_total:>8.1f}%"
)
print("─" * 70)
print(f"📦 Originaux backupés dans : {BACKUP_DIR}")
print(f"✅ Optimisation terminée.")
