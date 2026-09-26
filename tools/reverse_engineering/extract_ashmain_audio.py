import os
import struct

fpath = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\ashmain.dxr"
with open(fpath, "rb") as f:
    data = f.read()

pos = 16626
size = 492356
audio_bytes = data[pos+8:pos+8+size]

out_mp3 = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern\assets\audio\special\ashmain_theme.mp3"
with open(out_mp3, "wb") as fp:
    fp.write(audio_bytes)

print(f"Extracted {len(audio_bytes)} bytes to {out_mp3}")
print("Header:", audio_bytes[:16])

# Let's probe it with ffprobe
import subprocess
r = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', out_mp3], capture_output=True, text=True)
print("ffprobe result:")
print(r.stdout)
