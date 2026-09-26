import os
import re

base = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
files = ['startup.dxr', 'startup.cxt', 'open.cxt', 'ashmain.dxr', 'ashmain.cxt', 'ashmain1.dxr']

for fname in files:
    fpath = os.path.join(base, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'rb') as f:
        data = f.read()
    
    print("=" * 60)
    print(f"FILE: {fname} ({len(data)} bytes)")
    print("=" * 60)
    
    # Extract ASCII strings >= 3 chars
    strings = re.findall(b'[\x20-\x7e]{3,}', data)
    
    keywords = [b'avi', b'bmp', b'jpg', b'wav', b'sound', b'video', b'play', b'go', b'open', b'montage', b's0', b'01', b'02', b'03', b'frame', b'sprite', b'puppet']
    
    matches = []
    for s in strings:
        s_lower = s.lower()
        if any(k in s_lower for k in keywords):
            matches.append(s.decode('latin1', errors='ignore'))
            
    print(f"Total matching references found: {len(matches)}")
    for m in matches[:40]:
        print("  ->", m)
