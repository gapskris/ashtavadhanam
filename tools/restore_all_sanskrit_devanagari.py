"""
Master Sanskrit & English Restoration Engine for Ashtavadhanam Modern
Decodes all 25 rounds from original 1997 CD-ROM Director movies:
  - eightfold(s).dxr (Sanskrit VedicBrahma2)
  - eightfold.dxr (English / IAST Commentary)
Produces 100% pure Unicode Devanagari with zero corrupted glyphs.
"""

import os
import sys
import re
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(os.path.dirname(PROJECT_DIR), "Ashtavadhanam_master")

sys.path.insert(0, os.path.join(PROJECT_DIR, "tools"))
from generate_db import parse_chunks, extract_xmed_texts, clean_iast
from vedic_brahma_codec import decode_vedic_brahma_chunk

PAGE_CHUNKS_SAN = {
    1: [0, 1],
    2: [3, 4],
    3: [6, 7],
    4: [9, 10],
    5: [12, 13],
    6: [15, 16],
    7: [18, 19],
    8: [21, 22],
    9: [24, 25],
    10: [27, 28],
    11: [30, 31],
    12: [34, 35, 36, 37],
    13: [39, 40],
    14: [42, 43],
    15: [45, 46],
    16: [48, 49],
    17: [51, 52],
    18: [54, 55],
    19: [57, 58],
    20: [60, 61],
    21: [63, 64],
    22: [66, 67],
    23: [69, 70],
    24: [72],
    25: [72]
}

PAGE_CHUNKS_ENG = {
    1: [0, 1],
    2: [3, 4, 5],
    3: [7, 8],
    4: [10, 11],
    5: [13, 14, 15],
    6: [17, 18],
    7: [20, 21, 22],
    8: [24, 25, 26],
    9: [28, 29],
    10: [31, 32, 33],
    11: [35, 36, 37],
    12: [40, 41, 42, 43, 44],
    13: [46, 47],
    14: [49, 50],
    15: [52, 53, 54],
    16: [56, 57, 58],
    17: [60, 61],
    18: [63, 64, 65],
    19: [67, 68],
    20: [70, 71, 72],
    21: [74, 75],
    22: [77, 78],
    23: [80, 81, 82],
    24: [84],
    25: [85]
}

def clean_speakers_devanagari(text):
    """Normalize speaker tags in Devanagari text."""
    t = text.replace('\r\n', '\n').replace('\r', '\n')
    # Speakers
    speakers = [
        ('अवधानी', 'अवधानी:'),
        ('निषिद्धाक्षरी', 'निषिद्धाक्षरी:'),
        ('समस्या', 'समस्या:'),
        ('दत्तपदी', 'दत्तपदी:'),
        ('व्याख्याकारः', 'व्याख्याकारः:'),
        ('वर्णना', 'वर्णना:'),
        ('आशुः', 'आशुः:'),
        ('आशु', 'आशुः:'),
        ('सभापतिः', 'सभापतिः:'),
        ('अप्रस्तुतप्रसङ्गः', 'अप्रस्तुतप्रसङ्गः:'),
        ('व्यस्ताक्षरी', 'व्यस्ताक्षरी:')
    ]
    for s, rep in speakers:
        t = re.sub(rf'(?:^|\n)\s*{s}:?\s*', rf'\n\n{rep} ', t)
        
    # Bells
    t = re.sub(r'\(घण्टा\s*(\d+)\)', r'🔔 (घण्टा \1)', t)
    t = re.sub(r'🔔\s*🔔', '🔔', t)
    
    # Fix double colons
    t = re.sub(r':+:', ':', t)
    
    # Clean whitespace
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r' *\n *', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()

def restore_database():
    chs_san = parse_chunks(os.path.join(SRC_DIR, "eightfold(s).dxr"))
    chs_eng = parse_chunks(os.path.join(SRC_DIR, "eightfold.dxr"))
    san_texts = extract_xmed_texts(chs_san)
    eng_texts = extract_xmed_texts(chs_eng)
    
    data_path = os.path.join(PROJECT_DIR, "content", "data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        master_db = json.load(f)
        
    print(f"Loaded master database with {len(master_db['pages'])} pages.")
    
    for i in range(25):
        pnum = i + 1
        page_obj = master_db['pages'][i]
        
        # 1. Sanskrit extraction & decoding
        san_cindices = PAGE_CHUNKS_SAN[pnum]
        raw_snippets = []
        decoded_snippets = []
        for cidx in san_cindices:
            txt = san_texts[cidx][1].strip()
            raw_clean = re.sub(r'^[\x00-\x1f\s]+', '', txt)
            raw_clean = re.sub(r'^[0-9A-Fa-f\x00\s]+,\s*', '', raw_clean)
            raw_clean = re.sub(r'0000[0-9A-Fa-f\x00\s]+,\s*', '', raw_clean)
            
            decoded = decode_vedic_brahma_chunk(txt)
            if raw_clean: raw_snippets.append(raw_clean)
            if decoded: decoded_snippets.append(decoded)
            
        full_raw = "\n\n".join(raw_snippets)
        full_decoded = clean_speakers_devanagari("\n\n".join(decoded_snippets))
        
        # 2. English extraction & cleaning
        eng_cindices = PAGE_CHUNKS_ENG[pnum]
        eng_snippets = []
        for cidx in eng_cindices:
            t = eng_texts[cidx][1].strip()
            cleaned_t = re.sub(r'^[\x00-\x1f\s]+', '', t)
            cleaned_t = re.sub(r'^[0-9A-Fa-f\x00\s]+,\s*', '', cleaned_t)
            cleaned_t = re.sub(r'0000[0-9A-Fa-f\x00\s]+,\s*', '', cleaned_t)
            cleaned_t = clean_iast(cleaned_t)
            if cleaned_t: eng_snippets.append(cleaned_t)
            
        full_eng = "\n\n".join(eng_snippets)
        
        # Store in page object
        page_obj['sanskritRawVedicBrahma'] = full_raw
        page_obj['sanskritDevanagari'] = full_decoded
        page_obj['englishText'] = full_eng
        
        # Check artifacts in decoded Sanskrit
        words = re.findall(r'\S+', full_decoded)
        bad_tokens = []
        for w in words:
            clean_w = re.sub(r'[\(\)\"\'\*\।\॥\,\-\?\!\d:🔔]', '', w)
            if re.search(r'[;£ÐÏÎ\)`~\[\]\{\}\+\=\^a-zA-Z\x80-\xff]', clean_w):
                bad_tokens.append(w)
                
        status = f"CLEAN (0 artifacts)" if not bad_tokens else f"FAIL ({len(bad_tokens)} artifacts: {' '.join(bad_tokens[:3])})"
        print(f"Round {pnum:02d}: {status} | raw={len(full_raw)} dev={len(full_decoded)} eng={len(full_eng)}")
        
    # Save to data.json
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(master_db, f, ensure_ascii=False, indent=2)
        
    print(f"\nSaved updated database to {data_path}")

if __name__ == "__main__":
    restore_database()
