import os
import subprocess
import json

def probe(f):
    r = subprocess.run(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', '-show_format', f], capture_output=True, text=True)
    if r.stdout:
        return json.loads(r.stdout)
    return {}

master_avi = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\media\opening\montage.avi"
modern_mp4 = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern\assets\video\montage.mp4"

print("="*60)
print("ORIGINAL montage.avi:")
d1 = probe(master_avi)
print("Format:", d1.get('format', {}).get('format_name'), "Duration:", d1.get('format', {}).get('duration'))
for s in d1.get('streams', []):
    print(" Stream:", s.get('codec_type'), s.get('codec_name'), s.get('width'), "x", s.get('height'), "sample_rate:", s.get('sample_rate'))

print("="*60)
print("MODERN montage.mp4:")
d2 = probe(modern_mp4)
print("Format:", d2.get('format', {}).get('format_name'), "Duration:", d2.get('format', {}).get('duration'))
for s in d2.get('streams', []):
    print(" Stream:", s.get('codec_type'), s.get('codec_name'), s.get('width'), "x", s.get('height'), "sample_rate:", s.get('sample_rate'))

# Also let's check if there are other audio files in opening or media
print("="*60)
print("FILES IN media/opening/:")
opening_dir = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\media\opening"
if os.path.exists(opening_dir):
    for f in os.listdir(opening_dir):
        print(" ", f, os.path.getsize(os.path.join(opening_dir, f)), "bytes")

print("="*60)
print("FILES IN jpeg/opening/:")
jpeg_opening = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master\jpeg\opening"
if os.path.exists(jpeg_opening):
    for f in os.listdir(jpeg_opening):
        print(" ", f, os.path.getsize(os.path.join(jpeg_opening, f)), "bytes")
