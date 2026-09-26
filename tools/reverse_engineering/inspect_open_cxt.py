import os

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\open.cxt"
with open(fpath, 'rb') as f:
    d = f.read()

# Look for cast member info in open.cxt
# In Director, cast members are in 'CAS*' or 'CASt' chunks
p = 0
while True:
    idx = d.find(b'CAS', p)
    if idx == -1:
        break
    tag = d[idx:idx+4]
    print(f"Found {tag} at offset {idx}")
    p = idx + 1

# Let's inspect all strings and adjacent bytes in open.cxt
import re
for m in re.finditer(rb'[\x20-\x7e]{3,}', d):
    s = m.group(0).decode('latin1')
    if any(k in s.lower() for k in ['bmp', 'jpg', 'avi', 'montage', 's0', '01', '02', '03']):
        print(f"Offset {m.start():04x}: {s}")
