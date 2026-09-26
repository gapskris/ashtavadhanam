import os
import re

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\startup.dxr"
with open(fpath, 'rb') as f:
    d = f.read()

print("File size:", len(d))

# Search for any image names, member names, or labels in startup.dxr
print("\nAll strings in startup.dxr >= 4 chars:")
for s in re.findall(rb'[\x20-\x7e]{4,}', d):
    t = s.decode('latin1')
    if not t.startswith('Mac:') and not t.startswith('Win:') and len(t) < 50:
        if any(k in t.lower() for k in ['jpg', 'bmp', 'avi', 's0', '01', '02', '03', 'marker', 'start', 'ashmain', 'open', 'godis']):
            print(" ", t)

# Search for VWLB in startup.dxr
vwlb_pos = d.find(b'BLWV')
if vwlb_pos != -1:
    length = int.from_bytes(d[vwlb_pos+4:vwlb_pos+8], 'little')
    print("startup.dxr VWLB:", repr(d[vwlb_pos+8:vwlb_pos+8+length]))
