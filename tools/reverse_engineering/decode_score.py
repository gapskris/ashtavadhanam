import os
import struct

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\ashmain1.dxr"
with open(fpath, 'rb') as f:
    d = f.read()

vwsc_pos = d.find(b'CSWV')
chunk_len = struct.unpack('<I', d[vwsc_pos+4:vwsc_pos+8])[0]
score = d[vwsc_pos+8:vwsc_pos+8+chunk_len]

print("Score chunk length:", len(score))

# In Director 5/6 (VWSC):
# Bytes 0-3: Total length or header
# Bytes 4-5: Frame count or similar
# Let's inspect the first 64 bytes
for i in range(0, min(128, len(score)), 16):
    print(f"{i:04x}:", " ".join(f"{b:02x}" for b in score[i:i+16]))

# Let's search for references to cast members 1 to 10
# In Director, sprite records have:
# byte 0: script ID (or flags)
# byte 1: blend / ink
# byte 2-3: cast member ID (big-endian in some, little-endian in others)
# byte 4-5: y (locV)
# byte 6-7: x (locH)
# byte 8-9: height
# byte 10-11: width
# Let's check for sprite coordinates around 320x240, 800x600, 400, 300, etc.
coords = [320, 240, 800, 600, 400, 300, 180, 420]
for c in coords:
    # search big endian and little endian
    be = struct.pack('>H', c)
    le = struct.pack('<H', c)
    print(f"Coord {c}: BE matches={score.count(be)}, LE matches={score.count(le)}")
