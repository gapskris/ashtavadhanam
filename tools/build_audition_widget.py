import base64
import os

art_dir = r"C:\Users\gkpan\.gemini\antigravity\brain\455879ea-5c59-4ef5-8181-2a16441a2101"
audio_dir = "assets/audio/special"
img_path = "assets/images/opening/S06.jpg"

with open(os.path.join(audio_dir, "sparkle_01_crystal_chime.mp3"), "rb") as f:
    b64_1 = base64.b64encode(f.read()).decode("ascii")
with open(os.path.join(audio_dir, "sparkle_02_magic_shimmer.mp3"), "rb") as f:
    b64_2 = base64.b64encode(f.read()).decode("ascii")
with open(os.path.join(audio_dir, "sparkle_03_temple_bell.mp3"), "rb") as f:
    b64_3 = base64.b64encode(f.read()).decode("ascii")
with open(img_path, "rb") as f:
    b64_img = base64.b64encode(f.read()).decode("ascii")

html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @keyframes glint {{
      0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.7; filter: drop-shadow(0 0 4px #facc15); }}
      50% {{ transform: translate(-50%, -50%) scale(1.4); opacity: 1; filter: drop-shadow(0 0 14px #fff) drop-shadow(0 0 20px #eab308); }}
    }}
    .sparkle-pulse {{
      animation: glint 1.2s infinite ease-in-out;
    }}
  </style>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-3 select-none">
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-4 shadow-xl max-w-xl mx-auto">
    
    <!-- Header -->
    <div class="flex items-center justify-between mb-3">
      <div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-semibold uppercase tracking-wider text-amber-400 bg-amber-950/40 border border-amber-500/30 px-2 py-0.5 rounded-full">Title Sparkle Sound</span>
          <span class="text-xs text-[var(--muted-foreground)]">Frame S06 • ~1.0s</span>
        </div>
        <h2 class="text-base font-bold text-[var(--foreground)] mt-1">Audition Sparkle Sound Options</h2>
      </div>
      <div id="statusIndicator" class="text-xs px-2.5 py-1 rounded-md bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)] font-mono">
        Ready to audition
      </div>
    </div>

    <!-- Visual Preview Crop of Letter 'T' Sparkle -->
    <div class="relative h-28 w-full bg-black rounded-xl overflow-hidden border border-amber-500/30 mb-3 shadow-inner flex items-center justify-center">
      <img src="data:image/jpeg;base64,{b64_img}" class="absolute max-h-full object-contain pointer-events-none" alt="Title Reveal">
      <!-- Glint target highlighter over the letter T -->
      <div id="glintMarker" class="sparkle-pulse absolute top-[50.5%] left-[64.2%] w-7 h-7 rounded-full border border-amber-300 pointer-events-none"></div>
    </div>

    <!-- 3 Compact Audio Choice Cards -->
    <div class="grid grid-cols-3 gap-2 mb-3">
      
      <!-- Option 1 -->
      <div id="card1" class="group relative p-2.5 rounded-xl border border-[var(--border)] hover:border-amber-400 bg-[var(--background)] transition-all cursor-pointer flex flex-col justify-between" onclick="playOption(1)">
        <div>
          <div class="text-[10px] font-bold uppercase tracking-wider text-amber-400">Option 1</div>
          <div class="text-xs font-bold text-[var(--foreground)] mt-0.5 leading-tight">Crystal Chime</div>
          <div class="text-[11px] text-[var(--muted-foreground)] mt-1 leading-snug">Rising C6–G7 arpeggio with subtle shimmer vibrato.</div>
        </div>
        <button class="mt-2 w-full py-1 text-xs font-semibold rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/30 group-hover:bg-amber-500 group-hover:text-black transition-colors flex items-center justify-center gap-1">
          <span>▶</span> 1.0s
        </button>
      </div>

      <!-- Option 2 -->
      <div id="card2" class="group relative p-2.5 rounded-xl border border-[var(--border)] hover:border-sky-400 bg-[var(--background)] transition-all cursor-pointer flex flex-col justify-between" onclick="playOption(2)">
        <div>
          <div class="text-[10px] font-bold uppercase tracking-wider text-sky-400">Option 2</div>
          <div class="text-xs font-bold text-[var(--foreground)] mt-0.5 leading-tight">Magic Shimmer</div>
          <div class="text-[11px] text-[var(--muted-foreground)] mt-1 leading-snug">32-note micro-twinkle stardust cascade.</div>
        </div>
        <button class="mt-2 w-full py-1 text-xs font-semibold rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/30 group-hover:bg-sky-400 group-hover:text-black transition-colors flex items-center justify-center gap-1">
          <span>▶</span> 1.1s
        </button>
      </div>

      <!-- Option 3 -->
      <div id="card3" class="group relative p-2.5 rounded-xl border border-[var(--border)] hover:border-emerald-400 bg-[var(--background)] transition-all cursor-pointer flex flex-col justify-between" onclick="playOption(3)">
        <div>
          <div class="text-[10px] font-bold uppercase tracking-wider text-emerald-400">Option 3</div>
          <div class="text-xs font-bold text-[var(--foreground)] mt-0.5 leading-tight">Temple Bell</div>
          <div class="text-[11px] text-[var(--muted-foreground)] mt-1 leading-snug">Sacred bronze chime in F#6 with authentic warm partials.</div>
        </div>
        <button class="mt-2 w-full py-1 text-xs font-semibold rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 group-hover:bg-emerald-400 group-hover:text-black transition-colors flex items-center justify-center gap-1">
          <span>▶</span> 1.0s
        </button>
      </div>

    </div>

    <!-- Hidden Native Audio Elements -->
    <audio id="snd1" preload="auto" src="data:audio/mp3;base64,{b64_1}"></audio>
    <audio id="snd2" preload="auto" src="data:audio/mp3;base64,{b64_2}"></audio>
    <audio id="snd3" preload="auto" src="data:audio/mp3;base64,{b64_3}"></audio>

    <!-- Footer Note -->
    <div class="text-[11px] text-[var(--muted-foreground)] flex items-center justify-between border-t border-[var(--border)] pt-2">
      <span>💡 Click any card to audition the sound with visual glint</span>
      <span class="text-amber-400 font-medium">Dual M4A + MP3 ready</span>
    </div>

  </div>

  <script>
    const snd1 = document.getElementById('snd1');
    const snd2 = document.getElementById('snd2');
    const snd3 = document.getElementById('snd3');
    const status = document.getElementById('statusIndicator');
    const marker = document.getElementById('glintMarker');

    function stopAll() {{
      [snd1, snd2, snd3].forEach(s => {{
        s.pause();
        s.currentTime = 0;
      }});
      [1, 2, 3].forEach(i => {{
        const c = document.getElementById('card' + i);
        if (c) c.classList.remove('ring-2', 'ring-amber-400', 'ring-sky-400', 'ring-emerald-400');
      }});
    }}

    function playOption(num) {{
      stopAll();
      const snd = num === 1 ? snd1 : (num === 2 ? snd2 : snd3);
      const card = document.getElementById('card' + num);
      const ringColor = num === 1 ? 'ring-amber-400' : (num === 2 ? 'ring-sky-400' : 'ring-emerald-400');
      
      card.classList.add('ring-2', ringColor);
      const names = ['Crystal Chime', 'Magic Shimmer', 'Temple Bell Glint'];
      status.innerHTML = '✨ Playing: <strong class="text-amber-300">' + names[num - 1] + '</strong>';

      // Visual flash animation on the sparkle marker
      marker.style.transform = 'translate(-50%, -50%) scale(2.2)';
      marker.style.boxShadow = '0 0 30px #fef08a, 0 0 50px #eab308';
      setTimeout(() => {{
        marker.style.transform = 'translate(-50%, -50%) scale(1)';
        marker.style.boxShadow = 'none';
      }}, 500);

      snd.play().catch(e => {{
        status.textContent = 'Audio playback error';
        console.error(e);
      }});

      snd.onended = () => {{
        card.classList.remove('ring-2', ringColor);
        status.textContent = 'Audition complete';
      }};
    }}
  </script>
</body>
</html>
"""

target_file = os.path.join(art_dir, "sparkle_audition_player.html")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully wrote {target_file} (size: {len(html_content)} bytes)")
