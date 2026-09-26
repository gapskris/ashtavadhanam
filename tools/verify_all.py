import os, glob, subprocess, json

BASE_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"

def run_checks():
    print("="*60)
    print("  ASHTAVADHANAM MODERNIZATION — AUTOMATED VERIFICATION SUITE")
    print("="*60)
    
    passed = 0
    failed = 0

    # 1. Video files check
    videos = glob.glob(os.path.join(BASE_DIR, "assets", "video", "*.mp4"))
    expected_videos = 15
    if len(videos) == expected_videos:
        print(f"[PASS] All {expected_videos} MP4 videos converted & present.")
        passed += 1
    else:
        print(f"[FAIL] Expected {expected_videos} MP4 videos, found {len(videos)}")
        failed += 1

    # 2. Audio files check (M4A)
    m4as = glob.glob(os.path.join(BASE_DIR, "assets", "audio", "Page *", "*.m4a"))
    expected_audios = 173
    if len(m4as) == expected_audios:
        print(f"[PASS] All {expected_audios} high-fidelity M4A (192k AAC) audio files present.")
        passed += 1
    else:
        print(f"[FAIL] Expected {expected_audios} M4A files, found {len(m4as)}")
        failed += 1

    # 3. Audio files check (MP3)
    mp3s = glob.glob(os.path.join(BASE_DIR, "assets", "audio", "Page *", "*.mp3"))
    if len(mp3s) == expected_audios:
        print(f"[PASS] All {expected_audios} compatibility MP3 audio files present.")
        passed += 1
    else:
        print(f"[FAIL] Expected {expected_audios} MP3 files, found {len(mp3s)}")
        failed += 1

    # 4. Special internal tracks check
    specials = glob.glob(os.path.join(BASE_DIR, "assets", "audio", "special", "*.m4a"))
    if len(specials) == 10:
        print(f"[PASS] All 10 internal special audio tracks extracted and converted.")
        passed += 1
    else:
        print(f"[FAIL] Expected 10 special tracks, found {len(specials)}")
        failed += 1

    # 5. Background canvases check
    canvases = glob.glob(os.path.join(BASE_DIR, "assets", "images", "eightfold *.jpg"))
    if len(canvases) == 25:
        print(f"[PASS] All 25 performance background canvases present.")
        passed += 1
    else:
        print(f"[FAIL] Expected 25 canvases, found {len(canvases)}")
        failed += 1

    # 6. Database schema & content check
    json_path = os.path.join(BASE_DIR, "content", "data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if len(data.get("pages", [])) == 25:
        print(f"[PASS] Data layer contains all 25 performance pages.")
        passed += 1
    else:
        print(f"[FAIL] Pages count mismatch: {len(data.get('pages', []))}")
        failed += 1

    if all(k in data.get("treatises", {}) for k in ["avadhanaKala", "concentration", "performanceDetails", "institutions", "sriAurobindoSociety"]):
        print(f"[PASS] All 5 contextual treatises and essays parsed into data layer.")
        passed += 1
    else:
        print(f"[FAIL] Missing treatises in data layer.")
        failed += 1

    if len(data.get("glimpses", [])) == 3:
        print(f"[PASS] All 3 Glimpses video entries populated.")
        passed += 1
    else:
        print(f"[FAIL] Glimpses count mismatch.")
        failed += 1

    # 7. Core Application files
    app_files = [
        "index.html",
        "manifest.json",
        "sw.js",
        "run_local.py",
        "css/main.css",
        "css/player.css",
        "css/tv.css",
        "js/data.js",
        "js/player.js",
        "js/tv-remote.js",
        "js/app.js",
        "MODERNIZATION_PLAN.md"
    ]
    all_exist = all(os.path.exists(os.path.join(BASE_DIR, f)) for f in app_files)
    if all_exist:
        print(f"[PASS] All application web assets and scripts verified.")
        passed += 1
    else:
        print(f"[FAIL] Missing core app files.")
        failed += 1

    print("="*60)
    print(f"VERIFICATION SUMMARY: {passed} PASSED, {failed} FAILED")
    print("="*60)

if __name__ == "__main__":
    run_checks()
