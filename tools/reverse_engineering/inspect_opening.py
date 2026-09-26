import os
from PIL import Image

master_dir = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
MODERN_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"
opening_dir = os.path.join(master_dir, "jpeg", "opening")

print("=== OPENING IMAGES ===")
if os.path.exists(opening_dir):
    for f in sorted(os.listdir(opening_dir)):
        fp = os.path.join(opening_dir, f)
        if os.path.isfile(fp):
            im = Image.open(fp)
            print(f"{f:15s} size={im.size} mode={im.mode} format={im.format}")

# Let's inspect the visual elements of opening screens
print("\n=== VISUAL DETAILS OF OPENING SCREENS ===")
for fn in ["01.bmp", "02.bmp", "03.bmp", "S01.jpg", "S02.jpg", "S03.jpg", "S04.jpg", "S05.jpg", "S06.jpg"]:
    fp = os.path.join(opening_dir, fn)
    if os.path.exists(fp):
        im = Image.open(fp)
        thumb_name = f"thumb_{fn.replace('.', '_')}.jpg"
        thumb_path = os.path.join(MODERN_DIR, "assets", "images", thumb_name)
        im_copy = im.copy()
        im_copy.thumbnail((320, 240))
        im_copy.convert('RGB').save(thumb_path)
        print(f"Generated thumbnail for {fn} at assets/images/{thumb_name}")

# Check DXR text in startup.dxr and ashmain.dxr
import sys
MODERN_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"
sys.path.insert(0, os.path.join(MODERN_DIR, "tools"))
from generate_db import parse_chunks, extract_xmed_texts

for dxr_name in ["startup.dxr", "ashmain.dxr", "ashmain1.dxr", "performance.dxr"]:
    dxr_path = os.path.join(master_dir, dxr_name)
    if os.path.exists(dxr_path):
        chs = parse_chunks(dxr_path)
        texts = extract_xmed_texts(chs)
        print(f"\n--- {dxr_name} (Chunks: {len(chs)}, Text items: {len(texts)}) ---")
        for i, t in texts[:10]:
            print(f"  {repr(t[:80])}")
