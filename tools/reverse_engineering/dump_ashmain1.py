import os
import re

base = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
fpath = os.path.join(base, "ashmain1.dxr")

with open(fpath, 'rb') as f:
    data = f.read()

# Let's inspect all chunks in Director file
# Macromedia Director files have RIFX / XFIR format
print(f"Header: {data[:4]}")
print(f"File size: {len(data)}")

# Let's dump all text and chunk names
chunks = re.findall(b'[A-Za-z0-9_]{4}', data)
print(f"Found {len(chunks)} 4-char sequences")

# Let's dump all strings with their context
for m in re.finditer(b'[\x20-\x7e]{3,}', data):
    txt = m.group(0).decode('latin1')
    if any(w in txt.lower() for w in ['open', 'montage', 's0', '01', '02', '03', 'sound', 'audio', 'play', 'movie', 'loop']):
        print(f"Offset {m.start():06x}: {txt}")
