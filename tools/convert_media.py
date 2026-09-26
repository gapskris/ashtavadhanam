import os
import glob
import subprocess
import shutil
from PIL import Image

SRC_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
DST_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"

AUDIO_DST = os.path.join(DST_DIR, "assets", "audio")
VIDEO_DST = os.path.join(DST_DIR, "assets", "video")
IMAGES_DST = os.path.join(DST_DIR, "assets", "images")

os.makedirs(AUDIO_DST, exist_ok=True)
os.makedirs(VIDEO_DST, exist_ok=True)
os.makedirs(IMAGES_DST, exist_ok=True)

def copy_and_convert_images():
    print("=== Processing Images ===")
    src_jpeg = os.path.join(SRC_DIR, "jpeg")
    for root, dirs, files in os.walk(src_jpeg):
        for f in files:
            src_f = os.path.join(root, f)
            rel_dir = os.path.relpath(root, src_jpeg)
            target_sub = os.path.normpath(os.path.join(IMAGES_DST, rel_dir))
            os.makedirs(target_sub, exist_ok=True)
            
            ext = os.path.splitext(f)[1].lower()
            if ext == '.bmp':
                target_f = os.path.join(target_sub, os.path.splitext(f)[0] + ".jpg")
                if not os.path.exists(target_f):
                    im = Image.open(src_f)
                    im.convert('RGB').save(target_f, quality=95)
                    print(f"  Converted BMP -> High-Q JPG: {os.path.basename(target_f)}")
            elif ext in ['.jpg', '.jpeg', '.png']:
                target_f = os.path.join(target_sub, f)
                if not os.path.exists(target_f):
                    shutil.copy2(src_f, target_f)
                    print(f"  Copied image: {f}")

def convert_videos():
    print("\n=== Processing Videos (High-Quality H.264 CRF 18, 192k AAC) ===")
    avi_files = glob.glob(os.path.join(SRC_DIR, "**", "*.avi"), recursive=True)
    print(f"Found {len(avi_files)} AVI files to convert.")
    
    for avi in sorted(avi_files):
        fname = os.path.basename(avi)
        base_name = os.path.splitext(fname)[0]
        mp4_name = f"{base_name}.mp4"
        out_path = os.path.join(VIDEO_DST, mp4_name)
        
        if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
            print(f"  [Already converted] {mp4_name}")
            continue
            
        print(f"  Converting {fname} -> {mp4_name} (CRF 18, 192k AAC)...")
        # FFmpeg: CRF 18 (visually lossless archive grade), 192k AAC audio, faststart
        cmd = [
            "ffmpeg", "-y",
            "-i", avi,
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            "-movflags", "+faststart",
            out_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print(f"  ERROR on {fname}: {res.stderr.decode('utf-8', errors='ignore')[-300:]}")
        else:
            in_mb = os.path.getsize(avi) / (1024*1024)
            out_mb = os.path.getsize(out_path) / (1024*1024)
            print(f"  SUCCESS: {mp4_name} ({in_mb:.2f}MB -> {out_mb:.2f}MB)")

def convert_audios():
    print("\n=== Processing Audio (WAV -> High-Fidelity 192k M4A/AAC + MP3 fallback) ===")
    media_dir = os.path.join(SRC_DIR, "media")
    wav_files = glob.glob(os.path.join(media_dir, "Page *", "*.wav"))
    print(f"Found {len(wav_files)} WAV files across Page folders.")
    
    for wav in sorted(wav_files):
        rel_page = os.path.basename(os.path.dirname(wav))
        target_page_dir = os.path.join(AUDIO_DST, rel_page)
        os.makedirs(target_page_dir, exist_ok=True)
        
        fname = os.path.basename(wav)
        base = os.path.splitext(fname)[0]
        
        # 1. High-Fidelity 192 kbps M4A (AAC-LC)
        m4a_path = os.path.join(target_page_dir, f"{base}.m4a")
        if not (os.path.exists(m4a_path) and os.path.getsize(m4a_path) > 500):
            cmd_m4a = [
                "ffmpeg", "-y",
                "-i", wav,
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "44100",
                m4a_path
            ]
            subprocess.run(cmd_m4a, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
        # 2. Universal 192 kbps MP3 fallback
        mp3_path = os.path.join(target_page_dir, f"{base}.mp3")
        if not (os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 500):
            cmd_mp3 = [
                "ffmpeg", "-y",
                "-i", wav,
                "-c:a", "libmp3lame",
                "-b:a", "192k",
                "-ar", "44100",
                mp3_path
            ]
            subprocess.run(cmd_mp3, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    total_m4a = glob.glob(os.path.join(AUDIO_DST, "**", "*.m4a"), recursive=True)
    total_mp3 = glob.glob(os.path.join(AUDIO_DST, "**", "*.mp3"), recursive=True)
    print(f"Audio processing complete: {len(total_m4a)} M4A (192k AAC) files and {len(total_mp3)} MP3 files verified!")

if __name__ == "__main__":
    copy_and_convert_images()
    convert_videos()
    convert_audios()
    print("\n=== High-Fidelity Media Pipeline Complete! ===")
