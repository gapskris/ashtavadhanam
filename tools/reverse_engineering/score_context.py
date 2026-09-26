import os
import struct

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\ashmain1.dxr"
with open(fpath, 'rb') as f:
    d = f.read()

score = d[19452+8:19452+8+4584]

# Let's find every occurrence of 800 (0x0320) and 600 (0x0258)
be_800 = struct.pack('>H', 800)
be_600 = struct.pack('>H', 600)
be_400 = struct.pack('>H', 400)
be_300 = struct.pack('>H', 300)
be_320 = struct.pack('>H', 320)
be_240 = struct.pack('>H', 240)

pos = 0
while True:
    idx = score.find(be_400, pos)
    if idx == -1: break
    # print context of 32 bytes around idx
    start = max(0, idx - 16)
    end = min(len(score), idx + 24)
    print(f"Offset {idx:04x}:", " ".join(f"{b:02x}" for b in score[start:end]))
    pos = idx + 1
