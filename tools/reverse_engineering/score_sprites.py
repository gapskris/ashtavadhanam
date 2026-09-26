import os
import struct

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\ashmain1.dxr"
with open(fpath, 'rb') as f:
    d = f.read()

# VWSC is at 19452 + 8, len=4584
vwsc = d[19452+8:19452+8+4584]

# Director score channel frames:
# In Director 5/6, the score has frame delta blocks
# Let's search for cast member numbers 1 to 10 in the score
# In Director score, a sprite record is 16 to 24 bytes, containing:
# castLib, castMember (2 bytes or 1 byte), x, y, width, height, etc.
print("Length of VWSC:", len(vwsc))

# Let's search for castLib references or cast member IDs
# In open.cst, member 1 = 01.bmp, 2 = 02.bmp, 3 = 03.bmp, 4 = montage, 5..10 = S01..S06
for member_id in range(1, 11):
    # Search for (member_id, castLib)
    positions = []
    for i in range(0, len(vwsc)-4, 2):
        val = int.from_bytes(vwsc[i:i+2], 'little')
        val_be = int.from_bytes(vwsc[i:i+2], 'big')
        if val == member_id:
            positions.append(i)
    print(f"Member ID {member_id:2d} candidate occurrences: {len(positions)}")

# Let's inspect the entire ashmain1.dxr for any file names or strings
import re
print("\nAll strings in ashmain1.dxr >= 4 chars:")
for s in re.findall(rb'[\x20-\x7e]{4,}', d):
    t = s.decode('latin1')
    if not t.startswith('Mac:') and not t.startswith('Win:') and len(t) < 40:
        print(" ", t)
