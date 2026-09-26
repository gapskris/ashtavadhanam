import os

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\open.cxt"
with open(fpath, 'rb') as f:
    d = f.read(128)
print("Bytes 0-32:", d[:32])
print("Bytes 32-64:", d[32:64])
print("Bytes 64-128:", d[64:128])
