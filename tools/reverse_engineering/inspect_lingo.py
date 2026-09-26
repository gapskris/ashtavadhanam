import os
import re

base = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"

for fname in ["startup.dxr", "ashmain1.dxr", "navigation.cxt"]:
    fpath = os.path.join(base, fname)
    with open(fpath, 'rb') as f:
        d = f.read()
    
    print("=" * 60)
    print(f"FILE: {fname}")
    print("=" * 60)
    
    # In compiled DXR, names of scripts / handlers are stored in Lnam chunks
    # or embedded strings. Let's find all readable strings between 4 and 100 chars
    strings = [s.decode('ascii', errors='replace') for s in re.findall(rb'[\x20-\x7e]{4,}', d)]
    
    # Filter for movie navigation
    nav = [s for s in strings if any(w in s.lower() for w in ['go to', 'play', '.dxr', '.dir', 'ashmain', 'open', 'startup', 'exitframe', 'startmovie'])]
    print("Navigation / Movie strings:")
    for s in nav[:30]:
        print("  *", s)
