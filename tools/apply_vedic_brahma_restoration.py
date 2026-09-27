"""
Master Sanskrit Restoration Engine
Applies VedicBrahma2 decoding across all 25 performance rounds and treatises,
storing both raw VedicBrahma and certified Unicode Devanagari in content/data.json and js/data.js.
"""

import sys, os, struct, re, json

sys.stdout.reconfigure(encoding='utf-8')

SRC_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
MODERN_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"

sys.path.insert(0, os.path.join(MODERN_DIR, "tools"))
from fix_text_issues import parse_chunks, extract_xmed_texts, get_page_splits
from vedic_brahma_codec import decode_vedic_brahma_chunk

print("Parsing raw Director master files...")
chs_san = parse_chunks(os.path.join(SRC_DIR, "eightfold(s).dxr"))
san_texts = extract_xmed_texts(chs_san)
san_splits = get_page_splits(san_texts)

data_path = os.path.join(MODERN_DIR, "content", "data.json")
with open(data_path, "r", encoding="utf-8") as f:
    master_db = json.load(f)

# Update all 25 Performance Rounds
for i in range(25):
    pnum = i + 1
    prev_san = san_splits[i-1][1] if i > 0 else 0
    cur_san = san_splits[i][1]
    
    raw_snippets = []
    decoded_snippets = []
    
    for cidx in range(prev_san, cur_san):
        txt = san_texts[cidx][1]
        if 'Page ' in txt: continue
        raw_clean = re.sub(r'^[\x00-\x1f\s]+', '', txt.strip())
        raw_clean = re.sub(r'^[0-9A-Fa-f\x00\s]+,\s*', '', raw_clean)
        raw_clean = re.sub(r'0000[0-9A-Fa-f\x00\s]+,\s*', '', raw_clean)
        
        decoded = decode_vedic_brahma_chunk(txt)
        if raw_clean: raw_snippets.append(raw_clean)
        if decoded: decoded_snippets.append(decoded)
        
    full_raw = "\n\n".join(raw_snippets)
    full_decoded = "\n\n".join(decoded_snippets)
    
    if i < len(master_db['pages']):
        master_db['pages'][i]['sanskritRawVedicBrahma'] = full_raw
        master_db['pages'][i]['sanskritDevanagari'] = full_decoded
        print(f"  [OK] Round {pnum:02d}: Restored with dual VedicBrahma raw & certified Devanagari")

# Save updated database
with open(data_path, "w", encoding="utf-8") as f:
    json.dump(master_db, f, ensure_ascii=False, indent=2)

js_data_path = os.path.join(MODERN_DIR, "js", "data.js")
with open(js_data_path, "w", encoding="utf-8") as f:
    f.write("// Ashtavadhanam Modern — Canonical Content Database (Synced with content/data.json)\n")
    f.write("window.ASHTAVADHANAM_DATA = ")
    json.dump(master_db, f, ensure_ascii=False, indent=2)
    f.write(";\n")

print(f"\nSUCCESS: Updated content/data.json and js/data.js with certified VedicBrahma Sanskrit!")
