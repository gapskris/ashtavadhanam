import os
import re

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\ashmain1.dxr"
with open(fpath, 'rb') as f:
    d = f.read()

lscr_data = d[10738+8:10738+8+5264]
print("Strings in Lscr:")
for s in re.findall(rb'[\x20-\x7e]{3,}', lscr_data):
    print("  ", s.decode('latin1'))
