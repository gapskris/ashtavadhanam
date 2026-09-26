import os
import struct

base = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"

for fname in ["open.cxt", "ashmain1.dxr", "startup.dxr", "ashmain.dxr"]:
    fpath = os.path.join(base, fname)
    with open(fpath, "rb") as f:
        data = f.read()
    
    pos = 12
    found = []
    while pos < len(data) - 8:
        tag = data[pos:pos+4][::-1].decode('latin1', errors='replace')
        size = struct.unpack("<I", data[pos+4:pos+8])[0]
        if size < len(data):
            if any(k in tag.lower() for k in ['snd', 'wav', 'edim', 'mide', 'aiff', 'mp3']):
                found.append((tag, size, pos))
            # Also check if cdata looks like MP3 or RIFF/WAVE
            chunk_head = data[pos+8:pos+16]
            if chunk_head.startswith(b'RIFF') or chunk_head.startswith(b'\xff\xfb') or chunk_head.startswith(b'ID3'):
                found.append(('AUDIO_DATA', size, pos))
        pos += 8 + size + (size % 2)
    print(f"{fname:15s}: Found audio chunks: {found}")
