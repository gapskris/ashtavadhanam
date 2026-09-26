import os
import struct

base = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
fpath = os.path.join(base, "ashmain1.dxr")

with open(fpath, 'rb') as f:
    d = f.read()

# Let's search for 'VWSC' or 'CSWV'
vwsc_pos = d.find(b'VWSC')
if vwsc_pos == -1:
    vwsc_pos = d.find(b'CSWV')
print(f"VWSC offset: {vwsc_pos}")

if vwsc_pos != -1:
    # Score chunk length
    tag = d[vwsc_pos:vwsc_pos+4]
    chunk_len = struct.unpack('<I', d[vwsc_pos+4:vwsc_pos+8])[0]
    print(f"Tag: {tag}, Length: {chunk_len}")
    score_bytes = d[vwsc_pos+8:vwsc_pos+8+chunk_len]
    print(f"Score bytes len: {len(score_bytes)}")
    # In Director 5/6, score is delta-compressed or has frame headers
    # Let's inspect the unique bytes / words
    # Print first 200 bytes in hex
    print("Score head hex:", score_bytes[:100].hex())

# Also check cast member references in ashmain1.dxr
# Look for cast IDs 1 to 10 from open.cst
for m in range(1, 15):
    # Search for cast member references
    count = d.count(struct.pack('<H', m))
    # print(f"uint16 {m} count: {count}")
