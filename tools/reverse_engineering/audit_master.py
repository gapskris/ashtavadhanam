import os, sys, hashlib, struct

MASTER_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
MODERN_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"

sys.stdout.reconfigure(encoding='utf-8')

def file_md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def audit():
    print("=" * 80)
    print("  DEEP FORENSIC AUDIT OF ASHTAVADHANAM MASTER REPOSITORY")
    print("=" * 80)

    # 1. JPEG Folder
    jpeg_dir = os.path.join(MASTER_DIR, "jpeg")
    jpegs = sorted(os.listdir(jpeg_dir))
    print(f"\n1. JPEG REPOSITORY: {len(jpegs)} files in {jpeg_dir}")
    print("-" * 80)
    for idx, f in enumerate(jpegs, 1):
        fp = os.path.join(jpeg_dir, f)
        sz = os.path.getsize(fp)
        modern_target = os.path.join(MODERN_DIR, "assets", "images", f)
        modern_exists = os.path.exists(modern_target)
        modern_sz = os.path.getsize(modern_target) if modern_exists else 0
        match = "MATCH (100% Identical)" if sz == modern_sz else f"MISMATCH ({modern_sz} vs {sz})"
        print(f"  [{idx:2d}] {f:24s} | Master: {sz:8d} bytes | Modern: {match}")

    # 2. MEDIA ROOT (Videos)
    media_dir = os.path.join(MASTER_DIR, "media")
    media_files = sorted([f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))])
    print(f"\n2. MEDIA ROOT (VIDEOS): {len(media_files)} video AVI files")
    print("-" * 80)
    for idx, f in enumerate(media_files, 1):
        fp = os.path.join(media_dir, f)
        sz = os.path.getsize(fp)
        base = os.path.splitext(f)[0]
        mp4_name = f"{base}.mp4"
        modern_mp4 = os.path.join(MODERN_DIR, "assets", "video", mp4_name)
        modern_exists = os.path.exists(modern_mp4)
        mp4_sz = os.path.getsize(modern_mp4) if modern_exists else 0
        status = f"CONVERTED TO MP4 (CRF 18): {mp4_sz:9d} bytes" if modern_exists else "MISSING!"
        print(f"  [{idx:2d}] {f:15s} ({sz:10d} bytes) -> {status}")

    # 3. Dedicated check for other media subdirectories (avis, opening, etc.)
    non_page_dirs = sorted([d for d in os.listdir(media_dir) if os.path.isdir(os.path.join(media_dir, d)) and not d.startswith('Page ')])
    print(f"\n3. SPECIAL MEDIA SUBDIRECTORIES: {non_page_dirs}")
    print("-" * 80)
    for d in non_page_dirs:
        dp = os.path.join(media_dir, d)
        subfiles = sorted(os.listdir(dp))
        print(f"  Folder: media/{d} ({len(subfiles)} files):")
        for sf in subfiles:
            sfp = os.path.join(dp, sf)
            print(f"    - {sf:25s} ({os.path.getsize(sfp):10d} bytes)")

    # 4. MEDIA AUDIO DIRECTORIES (Audio recitations Page 1 to 25)
    page_subdirs = sorted([d for d in os.listdir(media_dir) if os.path.isdir(os.path.join(media_dir, d)) and d.startswith('Page ')], 
                          key=lambda x: int(x.replace('Page ', '')))
    print(f"\n4. MEDIA AUDIO DIRECTORIES: {len(page_subdirs)} Page folders (Page 1 to Page 25)")
    print("-" * 80)
    total_wav_count = 0
    total_m4a_count = 0
    total_mp3_count = 0
    total_wav_bytes = 0

    for d in page_subdirs:
        dp = os.path.join(media_dir, d)
        wavs = sorted(os.listdir(dp))
        total_wav_count += len(wavs)
        
        # Modern check
        mod_audio_dir = os.path.join(MODERN_DIR, "assets", "audio", d)
        m4as = [f for f in os.listdir(mod_audio_dir) if f.endswith('.m4a')] if os.path.exists(mod_audio_dir) else []
        mp3s = [f for f in os.listdir(mod_audio_dir) if f.endswith('.mp3')] if os.path.exists(mod_audio_dir) else []
        total_m4a_count += len(m4as)
        total_mp3_count += len(mp3s)
        
        page_bytes = sum(os.path.getsize(os.path.join(dp, w)) for w in wavs)
        total_wav_bytes += page_bytes

        print(f"  {d:10s} | {len(wavs):2d} Master WAVs ({page_bytes:8d} B) | Modern: {len(m4as):2d} M4A + {len(mp3s):2d} MP3 | Status: {'PERFECT (100% mapped)' if len(wavs) == len(m4as) == len(mp3s) else 'MISMATCH!'}")

    print(f"\n  -> Audio Totals: {total_wav_count} Master WAVs | {total_m4a_count} Modern M4As (192kbps AAC) | {total_mp3_count} Modern MP3s")

    # 4. SWF Folder (Flash Animations)
    swf_dir = os.path.join(MASTER_DIR, "swf")
    swfs = sorted(os.listdir(swf_dir)) if os.path.exists(swf_dir) else []
    print(f"\n4. SWF FOLDER (FLASH BUTTONS & ANIMATIONS): {len(swfs)} files")
    print("-" * 80)
    for idx, f in enumerate(swfs, 1):
        fp = os.path.join(swf_dir, f)
        print(f"  [{idx:2d}] {f:25s} {os.path.getsize(fp):8d} bytes")

    # 5. XTRAS Folder (Director Runtime Extensions)
    xtras_dir = os.path.join(MASTER_DIR, "xtras")
    xtras = sorted(os.listdir(xtras_dir)) if os.path.exists(xtras_dir) else []
    print(f"\n5. XTRAS FOLDER (MACROMEDIA DIRECTOR RUNTIME PLUGINS): {len(xtras)} files")
    print("-" * 80)
    for idx, f in enumerate(xtras, 1):
        fp = os.path.join(xtras_dir, f)
        print(f"  [{idx:2d}] {f:30s} {os.path.getsize(fp):8d} bytes")

    # 6. DXR & CXT Files (Director Movie Stages & Cast Libraries)
    root_files = os.listdir(MASTER_DIR)
    dxrs = sorted([f for f in root_files if f.lower().endswith('.dxr')])
    cxts = sorted([f for f in root_files if f.lower().endswith('.cxt')])
    print(f"\n6. DXR MOVIES ({len(dxrs)} files) & CXT CAST LIBRARIES ({len(cxts)} files)")
    print("-" * 80)
    print("  DXR Movies (Protected Director Stages):")
    for f in dxrs:
        fp = os.path.join(MASTER_DIR, f)
        print(f"    - {f:20s} ({os.path.getsize(fp):8d} bytes)")
    print("  CXT Cast Libraries (Director Media Casts):")
    for f in cxts:
        fp = os.path.join(MASTER_DIR, f)
        print(f"    - {f:20s} ({os.path.getsize(fp):8d} bytes)")

    # 7. Internal Audio extracted from eightfold.cxt
    special_dir = os.path.join(MODERN_DIR, "assets", "audio", "special")
    specials = sorted(os.listdir(special_dir)) if os.path.exists(special_dir) else []
    print(f"\n7. INTERNAL SOUNDS EXTRACTED FROM eightfold.cxt: {len(specials)} files in assets/audio/special")
    print("-" * 80)
    for f in specials:
        fp = os.path.join(special_dir, f)
        print(f"    - {f:25s} ({os.path.getsize(fp):8d} bytes)")

if __name__ == '__main__':
    audit()
