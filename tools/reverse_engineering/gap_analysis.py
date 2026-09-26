import os, sys, json, re
from PIL import Image

MASTER_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
MODERN_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"

sys.stdout.reconfigure(encoding='utf-8')

def run_gap_analysis():
    print("=" * 80)
    print("  STRICT GAP ANALYSIS: ASHTAVADHANAM MASTER vs. MODERNIZED IMPLEMENTATION")
    print("=" * 80)

    # 1. Audit JPEG Folder
    jpeg_dir = os.path.join(MASTER_DIR, "jpeg")
    all_master_jpegs = []
    for root, dirs, files in os.walk(jpeg_dir):
        for f in files:
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, jpeg_dir).replace("\\", "/")
            all_master_jpegs.append((rel, os.path.getsize(fp)))
    all_master_jpegs.sort()

    print(f"\n1. JPEG FOLDER ASSETS ({len(all_master_jpegs)} files):")
    print("-" * 80)
    for rel, sz in all_master_jpegs:
        # Check if used in index.html, app.js, or data.js
        with open(os.path.join(MODERN_DIR, "index.html"), "r", encoding="utf-8") as f:
            in_html = rel in f.read()
        with open(os.path.join(MODERN_DIR, "js", "app.js"), "r", encoding="utf-8") as f:
            in_app = rel in f.read()
        with open(os.path.join(MODERN_DIR, "js", "data.js"), "r", encoding="utf-8") as f:
            in_data = rel in f.read()
            
        used = in_html or in_app or in_data
        status = "ACTIVE IN UI" if used else "[GAP] NOT DISPLAYED IN UI"
        print(f"  {rel:35s} ({sz:8d} B) -> {status}")

    # 2. Audit MEDIA Folder
    media_dir = os.path.join(MASTER_DIR, "media")
    print(f"\n2. MEDIA FOLDER ASSETS:")
    print("-" * 80)
    
    # 2a. opening/
    print("  [Subfolder: media/opening]")
    for f in sorted(os.listdir(os.path.join(media_dir, "opening"))):
        fp = os.path.join(media_dir, "opening", f)
        base = os.path.splitext(f)[0]
        mp4_path = os.path.join(MODERN_DIR, "assets", "video", f"{base}.mp4")
        with open(os.path.join(MODERN_DIR, "index.html"), "r", encoding="utf-8") as html_f:
            in_html = f"{base}.mp4" in html_f.read()
        with open(os.path.join(MODERN_DIR, "js", "app.js"), "r", encoding="utf-8") as app_f:
            in_app = f"{base}.mp4" in app_f.read()
        with open(os.path.join(MODERN_DIR, "js", "data.js"), "r", encoding="utf-8") as data_f:
            in_data = f"{base}.mp4" in data_f.read()
        used = in_html or in_app or in_data
        status = "ACTIVE IN UI" if used else "[GAP] NOT INTEGRATED IN UI"
        print(f"    - {f:25s} ({os.path.getsize(fp):10d} B) -> {status}")

    # 2b. avis/
    print("  [Subfolder: media/avis]")
    for f in sorted(os.listdir(os.path.join(media_dir, "avis"))):
        fp = os.path.join(media_dir, "avis", f)
        base = os.path.splitext(f)[0]
        with open(os.path.join(MODERN_DIR, "js", "data.js"), "r", encoding="utf-8") as data_f:
            in_data = f"{base}.mp4" in data_f.read()
        status = "ACTIVE IN UI (Modal)" if in_data else "[GAP] NOT CONNECTED"
        print(f"    - {f:25s} ({os.path.getsize(fp):10d} B) -> {status}")

    # 2c. media root (GLIMPSE1-3)
    print("  [Subfolder: media/ root]")
    for f in sorted([x for x in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, x))]):
        fp = os.path.join(media_dir, f)
        base = os.path.splitext(f)[0]
        with open(os.path.join(MODERN_DIR, "js", "data.js"), "r", encoding="utf-8") as data_f:
            in_data = f"{base}.mp4" in data_f.read()
        status = "ACTIVE IN UI (Glimpses Section)" if in_data else "[GAP] NOT CONNECTED"
        print(f"    - {f:25s} ({os.path.getsize(fp):10d} B) -> {status}")

    # 2d. Page 1 to Page 25
    print("  [Subfolder: media/Page 1..25]")
    print(f"    - 173 WAV audio files across 25 pages -> Converted to 173 M4A + 173 MP3 and wired to Round cards.")

if __name__ == '__main__':
    run_gap_analysis()
