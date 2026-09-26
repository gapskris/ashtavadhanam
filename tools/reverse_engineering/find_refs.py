import os
import glob

base = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
all_files = glob.glob(os.path.join(base, "*.dxr")) + glob.glob(os.path.join(base, "*.cxt"))

for f in sorted(all_files):
    fname = os.path.basename(f)
    with open(f, 'rb') as fp:
        data = fp.read()
    
    matches = []
    for target in [b'open', b'ashmain1', b'startup', b'montage', b'ashmain']:
        if target in data.lower():
            matches.append(target.decode('latin1'))
    if matches:
        print(f"{fname:20s}: references {matches}")
