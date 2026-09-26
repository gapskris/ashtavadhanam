import os
import struct

base = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"

def dump_mmap(filepath):
    print("=" * 70)
    print(f"FILE: {os.path.basename(filepath)}")
    print("=" * 70)
    with open(filepath, 'rb') as f:
        data = f.read()

    endian = '<' if data[:4] == b'XFIR' else '>'
    
    # In Director 5/6/7:
    # Header: 4 bytes (XFIR), 4 bytes length, 4 bytes type
    # offset 12 is usually 'imap' (4 bytes), length (4 bytes), count (2 bytes)...
    # mmap is found at data.find(b'mmap')
    mmap_pos = data.find(b'mmap')
    if mmap_pos == -1:
        print("No mmap found")
        return

    mmap_len = struct.unpack(endian + 'I', data[mmap_pos+4:mmap_pos+8])[0]
    # mmap header has entry count
    header = data[mmap_pos+8:mmap_pos+32]
    # In Director 5/6:
    # 2 bytes entry size (usually 20 or 24)
    # 4 bytes entry count
    entry_size, unk, count, free_count = struct.unpack(endian + 'HHII', header[:12])
    print(f"mmap offset: {mmap_pos}, len: {mmap_len}, entry_size: {entry_size}, count: {count}")
    
    entries_start = mmap_pos + 32
    chunks = []
    for i in range(count):
        e_pos = entries_start + i * entry_size
        if e_pos + entry_size > len(data):
            break
        fourcc = data[e_pos:e_pos+4]
        length, offset = struct.unpack(endian + 'II', data[e_pos+4:e_pos+12])
        chunks.append((i, fourcc, length, offset))
        
    for i, fourcc, length, offset in chunks:
        fourcc_str = fourcc.decode('latin1', errors='ignore')
        chunk_data = data[offset:offset+length]
        # Look for text strings in chunk
        import re
        txts = re.findall(b'[\x20-\x7e]{3,}', chunk_data)
        txt_summary = " | ".join(t.decode('latin1', errors='ignore') for t in txts[:4])
        print(f"[{i:02d}] {fourcc_str:4s} (len: {length:6d}, off: {offset:6x}): {txt_summary[:80]}")

dump_mmap(os.path.join(base, "open.cxt"))
dump_mmap(os.path.join(base, "ashmain1.dxr"))
