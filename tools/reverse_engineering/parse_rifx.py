import os
import struct

base = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"

def parse_rifx(filepath):
    print("=" * 60)
    print(f"PARSING: {os.path.basename(filepath)}")
    print("=" * 60)
    with open(filepath, 'rb') as f:
        data = f.read()
    
    magic = data[:4]
    endian = '<' if magic == b'XFIR' else '>'
    print(f"Magic: {magic}, Endian: {endian}")
    
    # In RIFX, after header (4 bytes magic, 4 bytes size, 4 bytes type e.g. MV93, MC95),
    # there is an mmap or memory map table listing all chunks (fourCC tag, offset, length).
    pos = 12
    # Search for 'mmap' or 'imap'
    mmap_pos = data.find(b'mmap')
    if mmap_pos == -1:
        mmap_pos = data.find(b'pamm')
    print(f"mmap offset: {mmap_pos}")
    
    if mmap_pos != -1:
        # parse mmap
        tag = data[mmap_pos:mmap_pos+4]
        # read header
        # Usually chunk structure: 4 bytes tag, 4 bytes length, then chunk data
        hdr_len = struct.unpack(endian + 'I', data[mmap_pos+4:mmap_pos+8])[0]
        print(f"mmap length: {hdr_len}")
        
    # Let's search for cast names or text chunks (STXT, CAS*, VWSC, Lscr)
    tags = [b'VWSC', b'STXT', b'CAS*', b'CASt', b'Lscr', b'Lnam', b'SND ', b'snd ', b'Fver', b'VWFM']
    for t in tags:
        occurrences = []
        p = 0
        while True:
            idx = data.find(t, p)
            if idx == -1:
                break
            occurrences.append(idx)
            p = idx + 1
        if occurrences:
            print(f"Found tag {t}: {len(occurrences)} times at {occurrences[:5]}")

parse_rifx(os.path.join(base, "open.cxt"))
parse_rifx(os.path.join(base, "ashmain1.dxr"))
parse_rifx(os.path.join(base, "startup.dxr"))
