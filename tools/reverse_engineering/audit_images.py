import os, sys

MASTER_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
MODERN_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"

sys.stdout.reconfigure(encoding='utf-8')

m_jpeg = os.path.join(MASTER_DIR, "jpeg")
d_img = os.path.join(MODERN_DIR, "assets", "images")

master_images = {}
for root, dirs, files in os.walk(m_jpeg):
    for f in files:
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, m_jpeg)
        master_images[rel] = os.path.getsize(fp)

modern_images = {}
for root, dirs, files in os.walk(d_img):
    for f in files:
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, d_img)
        modern_images[rel] = os.path.getsize(fp)

print(f"Total Master Images in jpeg/: {len(master_images)}")
print(f"Total Modern Images in assets/images/: {len(modern_images)}")

print("\n--- MASTER IMAGES BREAKDOWN ---")
for rel, sz in sorted(master_images.items()):
    base, ext = os.path.splitext(rel)
    mod_match = modern_images.get(rel) or modern_images.get(base + ".jpg")
    status = f"PRESENT ({mod_match} B)" if mod_match else "MISSING!"
    print(f"  {rel:35s} ({sz:8d} B) -> {status}")
