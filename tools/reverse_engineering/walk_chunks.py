import os
import struct

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\ashmain1.dxr"
with open(fpath, 'rb') as f:
    d = f.read()

# In Director 6/7, the memory map gives the exact offset of the score chunk
# Let's inspect the mmap entries
# From earlier: mmap is at offset 44, entries start at offset 44 + 32 = 76
entries_start = 76
entry_size = 20 # or 24
# Let's find each chunk by iterating through the file and printing all 4-byte tags
# Director chunks have: 4-byte tag, 4-byte length, then chunk data
p = 12 # after XFIR header
while p < len(d) - 8:
    tag = d[p:p+4]
    length = struct.unpack('<I', d[p+4:p+8])[0]
    tag_rev = tag[::-1].decode('latin1', errors='ignore')
    tag_str = tag.decode('latin1', errors='ignore')
    # If tag looks like ascii letters
    if tag.isalnum() or tag_rev.isalnum():
        if length < len(d):
            print(f"Offset {p:6d} (0x{p:04x}): tag='{tag_str}' (rev='{tag_rev}'), len={length}")
            if tag in [b'CSWV', b'VWSC', b'tSAt', b'CAS*', b'txet', b'STXT']:
                print(f"   Data: {d[p+8:p+8+min(length, 60)]}")
            p += 8 + length
            # pad to 2 or 4 bytes
            if p % 2 != 0: p += 1
            continue
    p += 2
