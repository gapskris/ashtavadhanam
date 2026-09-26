import os
import struct

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\ashmain1.dxr"
with open(fpath, 'rb') as f:
    d = f.read()

# Real VWSC chunk at 19452 + 8
score = d[19452+8:19452+8+4584]

print("Real VWSC length:", len(score))
for i in range(0, min(128, len(score)), 16):
    print(f"{i:04x}:", " ".join(f"{b:02x}" for b in score[i:i+16]))

coords = [320, 240, 800, 600, 400, 300, 180, 420]
for c in coords:
    be = struct.pack('>H', c)
    le = struct.pack('<H', c)
    print(f"Coord {c}: BE matches={score.count(be)}, LE matches={score.count(le)}")
