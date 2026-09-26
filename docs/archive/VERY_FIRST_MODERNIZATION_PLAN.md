# Ashtavadhanam CD-ROM Modernization Plan

## Goal Description
The objective is to modernize the legacy multimedia CD-ROM **"Ashtavadhanam - The Wonder that is Sanskrit"** (originally published by Sri Aurobindo Society, documenting the historic Ashtavadhanam performance held on 20th January 1997 in Pondicherry) into a **modern, universal web application (PWA)**. 

The original software relies on completely obsolete, dead technology stacks from 2000–2001:
1. **Macromedia Director 8 Projector** (`start.exe`, `.dxr`, `.cxt`, 32-bit `.x32` Xtras) — cannot run on Android, iOS, Smart TVs, macOS, or 64-bit non-Windows environments.
2. **Intel Indeo Video 5 (`IV50`) AVI files** (15 video clips, ~220 MB) — not supported by any modern web browser or mobile OS without legacy standalone software.
3. **Adobe Flash (`.swf`) elements** — completely deprecated and blocked by modern browsers since 2020.
4. **173 uncompressed 22 kHz WAV audio files** (~174 MB) — heavy bandwidth requirements and lack modern streaming metadata.
5. **Non-standard 8-bit Diacritical & Devanagari Fonts** (`Palatino-RomanDiac` and `VedicBrahma2`) — legacy character mapping where accented characters and Sanskrit ligatures are mapped to standard ASCII slots.

The modernization will preserve **100% of the original content** (all 25 performance pages, all Sanskrit verses, English translations, dialogues, commentaries, 15 videos, 173+ audio clips, background artworks, and educational essays) while re-architecting the system as a high-performance, responsive, responsive web application that runs flawlessly on:
- **Smartphones** (Android & iOS via Chrome/Safari/Firefox/PWA install)
- **Tablets & iPads**
- **Smart TVs** (via TV browser with remote D-pad navigation support)
- **Desktop Computers** (Windows, macOS, Linux)

---

## User Review Required

> [!IMPORTANT]
> **Media Conversion Strategy**:
> - All **15 Indeo 5 AVI videos** will be converted to web-standard **H.264 (MP4) with AAC audio**. H.264 has 100% hardware acceleration across every mobile device, browser, and Smart TV in existence.
> - All **173 WAV audio files** will be converted to **MP3 / AAC** (128 kbps), shrinking total audio footprint from 174 MB to ~25 MB with zero perceptible loss in vocal clarity, allowing instant instant streaming even on mobile 4G/5G connections.
> - Original raw WAV and AVI files will remain untouched in their original directories as archives; modern web-ready media will reside in a dedicated `build/` or `dist/` media structure.

> [!TIP]
> **Standalone, Zero-Lock-In Web Architecture**:
> We recommend building this as a **modern static Web Application / PWA** (HTML5 + CSS3 + Vanilla ES6/TypeScript modules, with no heavy cloud runtime requirement). It can either be hosted on any web server / GitHub Pages / local network, opened directly in a browser, or bundled as an offline application (PWA / Capacitor / Electron if native APK/IPA is desired later).

---

## Open Questions

> [!NOTE]
> 1. **Hosting / Distribution Target**: Would you prefer the modernized output primarily as:
>    - A **Standalone Local / Web App** (a folder with `index.html` and modern assets that you can upload to any web hosting, Netlify, GitHub Pages, or run locally)?
>    - Or would you also like an **offline standalone package** (e.g., self-contained local web server or PWA installable shortcut on home screen)?
> 2. **Sanskrit Font Preference**: Would you prefer Sanskrit rendered in standard **Devanagari script** (with modern web fonts like Noto Sans Devanagari), **IAST Roman Transliteration** (diacritics: *ā, ī, ū, ṛ, ṅ, ñ, ś, ṣ*), or an **interactive toggle allowing the user to switch between Devanagari and English/IAST**? (The original CD-ROM had a Sanskrit/English toggle).

---

## Technical Audit of Existing Assets

| Category | File Count | Raw Size | Format in CD-ROM | Modern Target Format |
|---|---|---|---|---|
| **Video Clips** | 15 files | 219.68 MB | AVI (Intel Indeo 5 `IV50`, 320x240 @ 12fps, PCM 8-bit) | MP4 (H.264 High Profile, AAC stereo/mono 44.1kHz, web-optimized faststart) |
| **Audio Tracks** | 173 WAV + 10 embedded MP3 | 173.72 MB | WAV (PCM 16-bit 22.05 kHz stereo/mono) + Director SWA | MP3 / AAC (128kbps, 44.1kHz normalized) |
| **Canvases / Backgrounds** | 50 JPGs + 3 BMPs | 7.78 MB | 800x600 SVGA JPEGs & BMPs | Optimized WebP / High-res JPEG, responsive CSS background framing |
| **UI Components** | 17 SWF files | ~0.5 MB | Adobe Flash 4/5 vectors & buttons | Modern SVG icons, CSS animations, and HTML5 button components |
| **Runtime Engine** | 2 EXEs + 14 DXRs + 13 CXTs | ~12 MB | Macromedia Director 8 Projector & Xtras | Responsive HTML5 / CSS3 / ES6 PWA |
| **Text & Transcripts** | 25 pages + 6 essays | Embedded in `.dxr` / `.cxt` | Non-standard 8-bit encoded strings (`Palatino-RomanDiac`) | Structured JSON database with Unicode UTF-8 (Devanagari + IAST + English) |

---

## Proposed Changes

```
c:\DataScience\Vijay Ji's Music Conversion\
├── Ashtavadhanam_master/       <-- (Original legacy CD-ROM source, preserved 100% untouched)
└── Ashtavadhanam_modern/       <-- (New modernized platform)
    ├── index.html              <-- Main single-page web app entry point
    ├── manifest.json           <-- PWA manifest for home-screen install (Android/iOS)
    ├── sw.js                   <-- Service Worker for offline caching & fast loading
    ├── css/
    │   ├── main.css            <-- Modern responsive styles, typography, themes
    │   ├── player.css          <-- Media player and subtitle sync styling
    │   └── tv.css              <-- Smart TV 10-foot UI & remote control navigation
    ├── js/
    │   ├── app.js              <-- Application state, router, and view controller
    │   ├── player.js           <-- Unified Audio & Video sync playback engine
    │   ├── tv-remote.js        <-- Smart TV D-pad / keyboard arrow key controller
    │   └── data.js             <-- Structured transcript, pages 1-25, and metadata
    ├── assets/
    │   ├── images/             <-- Cleaned & optimized background canvases (WebP/JPG)
    │   ├── audio/              <-- 173+ converted MP3 clips (pg1wav1.mp3 to pg25wav1.mp3)
    │   ├── video/              <-- 15 converted H.264 MP4 clips (GLIMPSE1-3, avis, montage)
    │   └── fonts/              <-- Web fonts for Sanskrit Devanagari & Latin diacritics
    └── tools/                  <-- Python extraction & conversion pipeline scripts
        ├── convert_media.py    <-- Automated FFmpeg batch transcoder
        ├── extract_content.py  <-- Automated Director text extractor & Unicode mapper
        └── generate_db.py      <-- JSON dataset compiler
```

---

### Component 1: Automated Media Transcoding Pipeline (`tools/convert_media.py`)
- **Video Conversion**:
  - Scan `media/` (including `avis/`, `opening/`, and root `GLIMPSE*.avi`).
  - Transcode using `ffmpeg`:
    `ffmpeg -i input.avi -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart output.mp4`
  - Upscale or preserve aspect ratio with clean filtering so that 320x240 clips render crisply on mobile and 4K TV displays without blurriness.
- **Audio Conversion**:
  - Scan `media/Page 1` through `media/Page 25` (173 WAV files).
  - Transcode using `ffmpeg`:
    `ffmpeg -i input.wav -c:a libmp3lame -b:a 128k -ar 44100 output.mp3`
  - Extract the 10 embedded Shockwave Audio MP3 streams directly from `eightfold.cxt`.

---

### Component 2: Content Extraction & Unicode Normalization (`tools/extract_content.py`)
- Extract all text chunks from:
  - `eightfold.dxr` & `eightfold(s).dxr` (all 25 pages of dialogues, questions, answers, and verses).
  - `avdhankala.dxr` (Avadhana Kala - the Art of Concentration history and rules).
  - `ashtavadhanam.dxr` (Concentration - Its Importance and Value).
  - `glimpse.dxr` (Glimpses notes and timings).
  - `performance.dxr` (Performers and scholars directory).
  - `institu.cxt` & `sas.cxt` (Institutions and Sri Aurobindo Society history).
- Decode legacy 8-bit diacritic mapping (`Palatino-RomanDiac` -> Standard UTF-8 Unicode IAST).
- Map Sanskrit text to clean Devanagari (देवनागरी) Unicode characters.
- Output clean, structured JSON in `js/data.js`.

---

### Component 3: Universal Modern Web / PWA App (`Ashtavadhanam_modern/`)
- **Header & Navigation Bar**:
  - Modern replacement for the Flash buttons (`sanskrit.swf`, `english.swf`, `button.swf`).
  - Seamless Sanskrit (Devanagari / IAST) ⟷ English translation toggle at any instant.
  - Section Drawer / Menu:
    1. **The Performance (Eightfold Concentration / Ashtavadhanam)** — Pages 1 to 25.
    2. **Avadhana Kala (The Art of Concentration)** — Comprehensive treatise.
    3. **Concentration: Its Importance & Value** — Philosophical & yogic foundations.
    4. **Glimpses (Video Theater)** — Video highlights with synchronized descriptions.
    5. **The Scholars & Performers** — Biographical details of participating pandits.
    6. **Participating Institutions & Sri Aurobindo Society**.
- **The Performance Stage (Core Experience)**:
  - Shows the authentic parchment canvas for each page (`eightfold 01.jpg` to `25.jpg`).
  - Dialogue flow highlighting: as audio plays, the active speaker (Avadhani, Nishidhakshari, Samasya, Dattapadi, Aprastutaprasanga, Vyastakshari, etc.) is visually highlighted.
  - Play / Pause / Next Clip / Previous Clip / Auto-advance controls.
  - Video pop-up modal or inline theater for pages with video recordings (`02A.mp4` through `15A.mp4`).
- **Smart TV & Remote Control Mode**:
  - Full D-Pad (Up, Down, Left, Right, Enter/OK, Back) navigation.
  - High-contrast visual focus rings for TV viewing distance (10-foot interface).
  - Fullscreen video playback with large, legible subtitles.
- **Offline PWA Capabilities**:
  - Installable icon on Android, iPhone/iPad, Windows, and Mac.
  - Caches visited pages and audio for offline playback anywhere.

---

## Verification Plan

### Automated Pipeline Tests
1. **Media Integrity Test**:
   - Verify all 15 AVI files convert to MP4 without missing frames or audio sync drift.
   - Verify all 173 WAV files convert to MP3 with proper durations matching the originals.
   - Verify all 10 embedded MP3 streams in `eightfold.cxt` are extracted and valid.
2. **Text Database Completeness Test**:
   - Script that validates that each of Pages 1–25 has its complete sequence of audio clips and corresponding dialog text in both Sanskrit and English.

### Cross-Device & Browser Verification
1. **Desktop Browsers**: Chrome, Edge, Safari, Firefox.
2. **Mobile Devices**: Android (Chrome) and iOS (Mobile Safari) testing responsive touch interactions, audio autoplay policies, and PWA installation.
3. **Smart TV Browser & Keyboard Navigation**: Test arrow key / D-pad navigation, auto-focus, and full-screen video playback.
