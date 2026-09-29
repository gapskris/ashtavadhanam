"""
Sparkle Sound Generator for Ashtavadhanam Modern
Generates 3 pristine 1-second sparkle audio effects:
  1. sparkle_01_crystal_chime.wav -> .m4a & .mp3
  2. sparkle_02_magic_shimmer.wav -> .m4a & .mp3
  3. sparkle_03_temple_bell.wav -> .m4a & .mp3
"""

import os
import math
import wave
import struct
import subprocess
import random

SAMPLE_RATE = 44100
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_DIR, "assets", "audio", "special")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def write_wav(filename, samples):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)  # Stereo
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(SAMPLE_RATE)
        
        # Normalize to peak -1.5 dB (approx 27500)
        max_val = max(abs(s) for s in samples) if samples else 1.0
        scale = 27500.0 / max_val if max_val > 0 else 1.0
        
        packed_frames = bytearray()
        for s in samples:
            val = int(max(min(s * scale, 32767), -32768))
            packed = struct.pack('<hh', val, val)  # Left & Right
            packed_frames.extend(packed)
        wf.writeframes(packed_frames)

def convert_to_m4a_mp3(wav_path, base_name):
    m4a_path = os.path.join(OUTPUT_DIR, f"{base_name}.m4a")
    mp3_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")
    
    # FFmpeg M4A (AAC-LC 192k)
    cmd_m4a = ["ffmpeg", "-y", "-i", wav_path, "-c:a", "aac", "-b:a", "192k", "-ar", "44100", m4a_path]
    subprocess.run(cmd_m4a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # FFmpeg MP3 (192k)
    cmd_mp3 = ["ffmpeg", "-y", "-i", wav_path, "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", mp3_path]
    subprocess.run(cmd_mp3, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"Generated: {base_name}.m4a & {base_name}.mp3")

# ==================== SOUND 1: CRYSTAL CHIME ====================
def generate_crystal_chime():
    duration = 1.05
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # Rising crystalline chime chord: C6, E6, G6, B6, E7, G7
    notes = [
        (0.00, 1046.50, 0.60),  # C6
        (0.04, 1318.51, 0.70),  # E6
        (0.08, 1567.98, 0.80),  # G6
        (0.12, 1975.53, 0.85),  # B6
        (0.16, 2637.02, 1.00),  # E7 (peak sparkle)
        (0.20, 3135.96, 0.90),  # G7
        (0.24, 3951.07, 0.65),  # B7
    ]
    
    for start_t, freq, amp in notes:
        start_idx = int(start_t * SAMPLE_RATE)
        for i in range(start_idx, total_samples):
            t = (i - start_idx) / SAMPLE_RATE
            # Exponential decay
            decay = math.exp(-4.2 * t)
            # Bell harmonics: fundamental + octave overtone + shimmer tremolo
            vib = 1.0 + 0.12 * math.sin(2 * math.pi * 7.5 * t)
            harm1 = math.sin(2 * math.pi * freq * t)
            harm2 = 0.35 * math.sin(2 * math.pi * freq * 2.005 * t)
            harm3 = 0.15 * math.sin(2 * math.pi * freq * 2.76 * t)
            samples[i] += amp * decay * vib * (harm1 + harm2 + harm3)
            
    return samples

# ==================== SOUND 2: MAGIC SHIMMER ====================
def generate_magic_shimmer():
    duration = 1.0
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # 28 rapid sparkling micro-twinkles cascading upwards
    random.seed(42)
    twinkles = 32
    for k in range(twinkles):
        t_start = (k / twinkles) * 0.38  # all start within first 380ms
        freq = 1800 + (k / twinkles) * 2600 + random.uniform(-80, 80)
        amp = (0.5 + 0.5 * math.sin(math.pi * k / twinkles)) * random.uniform(0.6, 1.0)
        start_idx = int(t_start * SAMPLE_RATE)
        
        for i in range(start_idx, total_samples):
            t = (i - start_idx) / SAMPLE_RATE
            # Fast initial chime decay
            decay = math.exp(-5.5 * t)
            wave = math.sin(2 * math.pi * freq * t + math.sin(2 * math.pi * 12.0 * t))
            samples[i] += amp * decay * wave
            
    # Add gentle high-pass shimmering air tail
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        noise = random.uniform(-0.04, 0.04) * math.exp(-3.5 * t) * (1.0 if t > 0.05 else t/0.05)
        samples[i] += noise

    return samples

# ==================== SOUND 3: TEMPLE BELL GLINT ====================
def generate_temple_bell():
    duration = 1.15
    total_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * total_samples
    
    # Resonant bronze bell harmonic structure (F#6 = 1479.98 Hz)
    f0 = 1479.98
    partials = [
        (f0 * 1.000, 1.00, 3.8),   # Prime
        (f0 * 1.503, 0.45, 4.2),   # Minor third / fifth partial
        (f0 * 2.002, 0.70, 4.8),   # Octave (nominal)
        (f0 * 2.760, 0.35, 5.5),   # Tierce
        (f0 * 4.070, 0.50, 6.5),   # Quint
        (f0 * 5.430, 0.25, 7.8),   # Super-high sparkle
    ]
    
    # Strike transient
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        val = 0.0
        for freq, amp, decay_rate in partials:
            decay = math.exp(-decay_rate * t)
            # Beating tremolo for authentic bronze chime warmth
            beat = 1.0 + 0.15 * math.sin(2 * math.pi * 4.5 * t)
            tone = math.sin(2 * math.pi * freq * t)
            val += amp * decay * beat * tone
        # Quick soft attack (3ms) to prevent click
        env = min(1.0, t / 0.003) if t < 0.003 else 1.0
        samples[i] = val * env

    return samples

if __name__ == "__main__":
    temp_wav1 = os.path.join(OUTPUT_DIR, "temp1.wav")
    temp_wav2 = os.path.join(OUTPUT_DIR, "temp2.wav")
    temp_wav3 = os.path.join(OUTPUT_DIR, "temp3.wav")
    
    print("Synthesizing Option 1: Crystal Chime...")
    s1 = generate_crystal_chime()
    write_wav(temp_wav1, s1)
    convert_to_m4a_mp3(temp_wav1, "sparkle_01_crystal_chime")
    
    print("Synthesizing Option 2: Magic Shimmer...")
    s2 = generate_magic_shimmer()
    write_wav(temp_wav2, s2)
    convert_to_m4a_mp3(temp_wav2, "sparkle_02_magic_shimmer")
    
    print("Synthesizing Option 3: Temple Bell Glint...")
    s3 = generate_temple_bell()
    write_wav(temp_wav3, s3)
    convert_to_m4a_mp3(temp_wav3, "sparkle_03_temple_bell")
    
    # Clean up temp wav files
    for tw in [temp_wav1, temp_wav2, temp_wav3]:
        if os.path.exists(tw):
            os.remove(tw)
            
    print("\nAll 3 sparkle sound options successfully synthesized and encoded!")
