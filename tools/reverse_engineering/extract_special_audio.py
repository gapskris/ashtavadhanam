import struct, os

cxt_path = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\eightfold.cxt"
out_dir = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern\assets\audio\special"
os.makedirs(out_dir, exist_ok=True)

with open(cxt_path, "rb") as f:
    data = f.read()

pos = 12
chunks = []
while pos < len(data) - 8:
    tag = data[pos:pos+4][::-1].decode('latin1', errors='replace')
    size = struct.unpack("<I", data[pos+4:pos+8])[0]
    chunks.append((pos, tag, size, data[pos+8:pos+8+size]))
    pos += 8 + size + (size % 2)

mp3_idx = 1
for i, (pos, tag, size, cdata) in enumerate(chunks):
    if tag == 'ediM' and cdata.startswith(b'\xff\xfb'):
        out_file = os.path.join(out_dir, f"track_{mp3_idx:02d}.mp3")
        with open(out_file, "wb") as fp:
            fp.write(cdata)
        print(f"Extracted internal MP3 {mp3_idx}: size {len(cdata)} bytes -> {os.path.basename(out_file)}")
        mp3_idx += 1

print(f"Total special tracks extracted: {mp3_idx - 1}")
