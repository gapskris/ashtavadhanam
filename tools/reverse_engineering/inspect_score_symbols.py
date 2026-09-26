import os
import struct

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\ashmain1.dxr"
with open(fpath, 'rb') as f:
    d = f.read()

# VWSC chunk starts at 19452 + 8
score_data = d[19452+8:19452+8+4584]

# In Director 5/6, VWSC begins with a header:
# 4 bytes size, 4 bytes version, 4 bytes frameCount, 4 bytes channelCount...
print("Score header bytes (first 32):", score_data[:32])

# Director score channel frame entries:
# Let's search for cast member IDs 1, 2, 3 (which are 01.bmp, 02.bmp, 03.bmp)
# and cast member ID 4 (montage.avi)
# and cast member IDs 5, 6, 7, 8, 9, 10 (S01 to S06)
# Each sprite has a castLib (usually 2 for linked cast) and castMember (1-10)
print("\nSearching for sprite cast member entries in score:")
for i in range(len(score_data) - 4):
    w1, w2 = struct.unpack('>HH', score_data[i:i+4])
    # Also little endian
    lw1, lw2 = struct.unpack('<HH', score_data[i:i+4])
    for cast_num in range(1, 11):
        if (w1 == cast_num and w2 in [1, 2, 0]) or (lw1 == cast_num and lw2 in [1, 2, 0]):
            pass # we can check surrounding bytes

# Let's inspect the Lscr (Lingo script) in ashmain1.dxr!
# Offset 10738 (0x29f2), len=5264: tag='rcsL' (Lscr)
lscr_data = d[10738+8:10738+8+5264]
print("Lscr len:", len(lscr_data))

# Let's inspect all strings in Lscr / Lnam
lnam_data = d[16010+8:16010+8+3281]
# Lnam contains names of variables, handlers, etc.
# In Director, Lnam has a list of Pascal strings (1 byte len, then chars)
pos = 0
names = []
while pos < len(lnam_data):
    slen = lnam_data[pos]
    if 0 < slen < 50 and pos + 1 + slen <= len(lnam_data):
        s = lnam_data[pos+1:pos+1+slen].decode('latin1', errors='ignore')
        if s.isprintable():
            names.append(s)
            pos += 1 + slen
            continue
    pos += 1

print(f"Decoded {len(names)} names from Lnam:")
print(names[:60])
