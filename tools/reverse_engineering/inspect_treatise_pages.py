import os, sys

MASTER_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
MODERN_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"

sys.path.insert(0, os.path.join(MODERN_DIR, "tools"))
from generate_db import parse_chunks, extract_xmed_texts

print("=== INSPECTING AVDHANKALA.DXR CHUNKS ===")
chs_avd = parse_chunks(os.path.join(MASTER_DIR, "avdhankala.dxr"))
texts_avd = extract_xmed_texts(chs_avd)
print(f"Total text blocks in avdhankala.dxr: {len(texts_avd)}")
for i, (idx, txt) in enumerate(texts_avd):
    print(f"[{i+1}] (Chunk {idx}) {repr(txt[:60])}")

print("\n=== INSPECTING ASHTAVADHANAM.DXR CHUNKS ===")
chs_ash = parse_chunks(os.path.join(MASTER_DIR, "ashtavadhanam.dxr"))
texts_ash = extract_xmed_texts(chs_ash)
print(f"Total text blocks in ashtavadhanam.dxr: {len(texts_ash)}")
for i, (idx, txt) in enumerate(texts_ash):
    print(f"[{i+1}] (Chunk {idx}) {repr(txt[:60])}")
