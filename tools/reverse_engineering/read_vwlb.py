import os

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\ashmain1.dxr"
with open(fpath, 'rb') as f:
    d = f.read()

vwlb = d[24052+8:24052+8+37]
print("VWLB raw:", repr(vwlb))
import re
print("Strings in VWLB:", re.findall(rb'[\x20-\x7e]{2,}', vwlb))

# Let's also inspect all strings in ashmain.dxr markers
ashmain_path = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\ashmain.dxr"
with open(ashmain_path, 'rb') as f:
    d2 = f.read()
vwlb_pos = d2.find(b'BLWV')
if vwlb_pos != -1:
    length = int.from_bytes(d2[vwlb_pos+4:vwlb_pos+8], 'little')
    print("ashmain.dxr VWLB len:", length)
    print("ashmain.dxr VWLB:", repr(d2[vwlb_pos+8:vwlb_pos+8+length]))
    print("Strings in ashmain VWLB:", re.findall(rb'[\x20-\x7e]{2,}', d2[vwlb_pos+8:vwlb_pos+8+length]))
