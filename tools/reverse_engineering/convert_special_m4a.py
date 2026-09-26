import glob, os, subprocess

special_dir = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern\assets\audio\special"
mp3s = glob.glob(os.path.join(special_dir, "*.mp3"))
print(f"Found {len(mp3s)} mp3s to convert to m4a.")

for f in mp3s:
    m4a = os.path.splitext(f)[0] + ".m4a"
    subprocess.run(["ffmpeg", "-y", "-i", f, "-c:a", "aac", "-b:a", "256k", m4a], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Created:", os.path.basename(m4a))
