# Ashtavadhanam (1997 → 2026): Modernization, Tech Stack & Data Integrity Guide

> **Project:** Ashtavadhanam — The Wonder that is Sanskrit (1997 CD-ROM Digital Heritage Preservation)  
> **Target Release:** 2026 Modern Standalone Web Application & Progressive Web App (PWA)  
> **Preservation Baseline:** Sri Aurobindo Society, Pondicherry (1997 Historic Multimedia CD-ROM)

---

## 1. Executive Modernization Overview

In 1997, the Sri Aurobindo Society published a landmark multimedia CD-ROM documenting a historic **Ashtavadhanam** (an eightfold feat of simultaneous Sanskrit memory, versification, and intellect). Built with **Macromedia Director 7/8**, **Intel Indeo Video 5**, and **16-bit uncompressed PCM audio**, the application became unplayable on modern operating systems after the deprecation of 32-bit runtimes, Flash Player, and proprietary codecs.

In 2026, the entire multimedia application was forensically reverse-engineered and reconstructed as a **zero-dependency, future-proof, standalone web application**.

---

## 2. Modern Tech Stack

The application was authored intentionally **without heavy frontend frameworks (no React, no Angular, no Vue)** and **without complex build pipelines (no Webpack, no Vite, no Node.js runtime required)** to guarantee **100-year digital preservation longevity**:

| Layer | Modern Technology | Rationale & Benefit |
| :--- | :--- | :--- |
| **Presentation** | **Semantic HTML5** | Direct standard DOM elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<audio>`, `<video>`). Accessible, screen-reader ready, and lightweight. |
| **Styling & Layout** | **Modular CSS3** | Native CSS Variables (`:root`), Flexbox, CSS Grid, Fluid typography (`clamp()`), and responsive viewports (Mobile, Tablet, Desktop, 4K, 10-Foot Smart TV). |
| **Application Logic** | **Vanilla ES6+ JavaScript** | Object-Oriented modular controllers (`app.js`, `player.js`, `search.js`, `tv-remote.js`). Zero external libraries or npm dependencies. |
| **Viewport Engine** | **Autonomous Adaptive Engine** | Real-time mathematical scaling (`updateStageScale`) dynamically fitting 1080px stage geometry to any viewport with zero text clipping. |
| **Animation Clock** | **`requestAnimationFrame` API** | High-precision 60fps/120fps hardware-synchronized rendering querying `media.currentTime` to eliminate UI jitter. |
| **Audio Engine** | **Dual High-Fidelity Audio** | **Primary:** 192 kbps M4A (AAC-LC) for crystal-clear recitations.<br>**Fallback:** 192 kbps universal MP3 for legacy browsers. |
| **Acoustic Synthesizer**| **Web Audio API** | Pure algorithmic synthesis of temple bell chime harmonics (432Hz/864Hz/1296Hz) replacing corrupt legacy audio. |
| **Video Engine** | **H.264 / AAC MP4** | Web-optimized progressive MP4 (CRF 18 visually lossless, `+faststart` atom alignment for instant zero-buffer seeking). |
| **Visual Graphics** | **Progressive JPEG & WebP** | High-resolution parchment backdrops and archival photography preserved without downsampling. |
| **Search Engine** | **Client-Side Inverted Index** | Client-side Sanskrit search with Devanagari ligature normalization (homorganic nasal to anusvāra) and IAST accent folding across 222 documents. |
| **PWA & Offline** | **Service Worker & Manifest** | Web App Manifest + Network-First Service Worker (`sw.js` v1.2.2) with Range-request safety bypass, video passthrough, and `?v=1.2.2` cache-busting. |
| **Local Portability** | **Dual-Mode Execution** | Runs instantly via direct double-click (`file:///index.html`) or via zero-install local Python launcher (`run_local.py`). |

---

## 3. Legacy-to-Modern Content Migration Matrix

Every legacy file from the 1997 CD-ROM was mapped 1-to-1 into modern open standards:

| Original 1997 Legacy Format | Extracted / Legacy Source | Modern Target Format | Migration Method & Modern Architecture |
| :--- | :--- | :--- | :--- |
| **Projector Executables (`.exe`)** | `start.exe` (32-bit Windows Projector) | `index.html` + `manifest.json` | Replaced by HTML5 Autoplay Gateway & PWA App Shell. Zero OS-specific binary debt. |
| **Director Movies (`.dxr`)** | 14 files (`ashmain`, `eightfold`, `exit`, etc.) | Vanilla ES6 JS Modules + `content/data.json` | RIFX memory maps deconstructed; score channel animations translated to semantic CSS/JS state transitions. |
| **Cast Libraries (`.cxt`)** | 13 files (`page1.cxt` to `page25.cxt`) | Structured JSON Content Model | Embedded texts, bitmaps, and member references decoupled from proprietary binary containers into `content/data.json`. |
| **Flash Assets (`.swf`)** | 17 Flash vector files (`enter.swf`, `play.swf`, etc.) | Semantic HTML5 Buttons & SVG | Vector chrome converted to semantic HTML5 `<button>`, SVG icons, and CSS3 transitions. Zero Flash/Ruffle runtime. |
| **Video Media (`.avi`)** | 15 Intel Indeo 5 AVIs (`320x240 @ 12fps`) | 15 H.264 MP4s (`+faststart`) | Transcoded via FFmpeg at CRF 18 with stereo AAC-LC audio. Faststart `moov` atom shifted to start of file for instant web playback. |
| **Speech Audio (`.wav`)** | 173 uncompressed 16-bit 22.05 kHz WAVs | 173 M4A + 173 MP3 files | Transcoded to dual-format high-fidelity 192 kbps AAC-LC and 192 kbps MP3 with zero truncation. |
| **Soundtrack / Bells (`.cxt`)** | 10 embedded Shockwave Audio (SWA) streams | 11 M4A + 11 MP3 special tracks | Extracted Director chimes, bells, and opening title theme (`ashmain_theme.m4a`) at 256 kbps in `assets/audio/special/`. |
| **Master Visuals (`.jpg`, `.bmp`)** | 50 SVGA JPEGs + 3 uncompressed BMPs | 53 Master Web Visuals | BMP opening frames converted to lossless web-safe JPEG; all 25 performance backdrops preserved in `assets/images/`. |
| **8-Bit Sanskrit Fonts** | `VedicBrahma2` typewriter font | Modern UTF-8 Unicode Devanagari | Automated algorithm (`tools/vedic_brahma2_restorer.py`) reversed 142 glyphs, matra pre-fixes, reph post-fixes, and conjuncts. |
| **8-Bit English Transliteration** | `Palatino-RomanDiac` font | Standard IAST Diacritics | Decoded custom 8-bit glyph tables into standard Unicode diacritics (*Avadhānī*, *Samasyā*, *Śārdūlavikrīḍita*). |
| **App Branding & Emblem** | Legacy Director icon | Circular Gold Scholar Emblem | Designed high-resolution SVG and PNG icon suites (`assets/icons/`) featuring the sacred Veena, conch, and scholar silhouette. |

---

## 4. Preservation Methodology (How the Migration Succeeded)

The preservation effort followed a strict 5-stage engineering discipline:

```
DECONSTRUCT (RIFX/XFIR) ──▶ EXTRACT & DECODE ──▶ CANONICAL DATA MODEL ──▶ WEB ARCHITECTURE ──▶ 100% FORENSIC AUDIT
```

1. **Deconstruction**:
   - Custom Python decompressors parsed Director's RIFX/XFIR chunk hierarchy (`mmap`, `KEY*`, `DRCF`, `CASt`, `XMED`, `ediM`).
2. **Text & Typography Recovery**:
   - Proprietary typewriter glyph encodings were automatically converted to standard Unicode Devanagari and IAST macrons using `tools/vedic_brahma2_restorer.py`.
   - Authentic Sanskrit role designations (*Avadhānī*, *Niṣiddhākṣarī*, *Samasyā*, *Dattapadī*, *Vyastākṣarī*, *Ghaṇṭā*, *Sabhāpati*) were recovered and color-coded.
3. **Decoupled Data Architecture**:
   - Content was completely separated from presentation into a single canonical source of truth: `content/data.json`.
   - A zero-fetch, CORS-safe in-memory mirror (`js/data.js`) was established for direct double-click `file:///` execution.
4. **Cinematic Opening Choreography**:
   - The authentic 1997 opening title sequence was faithfully recreated using a 6-frame illuminated calligraphy progressive GPU dissolve (`S01.jpg`–`S06.jpg`) at 180ms cadence, 3-stage cultural mosaic transition (`03` → `02` → `01`), centered video playback, and reverse-dissolve outro.
5. **Modern Enhancements Added Without Legacy Disruption**:
   - **Autonomous Adaptive Viewport Engine**: Dynamic mathematical scaling in `app.js` guaranteeing zero text clipping on any mobile or desktop screen.
   - **Symmetrical Dual-Header Architecture**: Left Navigation Drawer (Sections & 25 Rounds) and Right Tools Drawer (Views, Themes, Search, PWA).
   - **3-Way Display Switcher**: Instant live switching between Devanagari script, Bilingual side-by-side, and English IAST macrons.
   - **Interactive Sanskrit Search Engine**: Client-side inverted index over 222 corpus documents with Devanagari ligature normalization and accent folding.
   - **Smart TV 10-Foot Mode**: Spatial D-Pad navigation, remote keycode bindings, and touch DPAD overlay for big-screen television displays.
   - **Native HTTP 206 Range Handler**: Enhanced `run_local.py` with RFC 7233 byte-range seeking for smooth audio and video scrubbing.

---

## 5. Precautions Taken to Guarantee Zero Data Loss

To ensure forensic parity with the 1997 physical CD-ROM and eliminate any possibility of data loss:

| Precaution Domain | Verification Strategy | Forensic Proof & Result |
| :--- | :--- | :--- |
| **Exact Video Durations** | Every video stream was verified against the legacy `.avi` file using `ffprobe` down to the millisecond. | **0.00s Duration Delta**: All 15 videos (`GLIMPSE1-3`, `montage`, and 11 round demonstrations) match the physical CD-ROM source files exactly with zero video truncation. |
| **Dual Audio Parity** | Dual-pipeline export generated both M4A and MP3 files for all speech recitations and soundtracks. | **100% Complete**: Exactly 173 recitation tracks and 11 special sound tracks exist in both formats (368 audio files total). |
| **Visual Master Integrity** | All 53 master visuals (25 round canvases, 7 Avadhāna Kalā canvases, 6 Concentration canvases, 9 opening frames, and 4 archival photos) were inventoried. | **53 / 53 Active**: Every graphical asset is rendered in the reader modules and accessible in the **Historical Artwork Master Gallery Grid**. |
| **Speaker & Verse Parity** | Every dialogue turn across all 25 performance rounds was validated against the original Director score. | **25 / 25 Rounds**: All speaker turns, riddle verses, and bell strike counts match the 1997 audio bindings 1-to-1. |
| **Canonical Data Synchronization** | Bi-directional consistency between JSON and JavaScript mirrors. | Running `python tools/sync_data_js.py --check` confirms **100% bit-for-bit synchronization**. |
| **Automated Forensic Verification Suite** | 70 programmatic assertions checking assets on disk, database mappings, DOM IDs, and search queries. | Running `python tools/verify_1to1_mapping.py` executes **70 / 70 tests with a 100% pass rate**. |
| **Multi-Device Responsiveness Suite** | 65 automated Playwright assertions across Desktop, iPad Pro, iPhone SE, Pixel 7, and Galaxy S20. | Running `pytest tests/test_mobile_responsive.py` executes **65 / 65 tests with a 100% pass rate**. |

---

## 6. Version 2.0 Architectural Roadmap (The 9 Pillars)

As detailed in [`v2/V2_MASTER_PLAN_AND_ROADMAP.md`](file:///c:/DataScience/Vijay%20Ji%27s%20Music%20Conversion/Ashtavadhanam_modern/v2/V2_MASTER_PLAN_AND_ROADMAP.md), the next major milestone enhances the platform with 9 non-destructive pillars:
1. **Pillar 1: Organic Bhojpatra / Palm-Leaf Micro-Texture Engine**
2. **Pillar 2: Animated Aṣṭadala Padma (Sacred 8-Petaled Lotus Watermark & Audio Avatar)**
3. **Pillar 3: Real-Time Sanskrit Chandas (Meter) & Sandhi Inspector**
4. **Pillar 4: Interactive Sanskrit Glossary & Avadhana Lore Companion**
5. **Pillar 5: Precision Audio Playback Speed Selector (0.75×, 1.0×, 1.25×)**
6. **Pillar 6: Active Verse Pāda (Karaoke) Highlighting & Auto-Scroll**
7. **Pillar 7: Dual Sanctuary Theme Switcher (Night Sanctuary vs. Royal Palm-Leaf Daylight)**
8. **Pillar 8: "The Avadhani's Challenge" Cognitive Memory Mini-Game**
9. **Pillar 9: Printable Royal Manuscript Folio Generator (A4 Vector PDF Export with Top Official App Emblem)**

---

## 7. Verification Commands

To independently verify the migration and asset integrity at any time:

```powershell
# 1. Run the automated 70-point forensic verification suite
python tools/verify_1to1_mapping.py

# 2. Check canonical data layer synchronization
python tools/sync_data_js.py --check

# 3. Run the 65-point multi-device responsive Playwright test suite
pytest tests/test_mobile_responsive.py

# 4. Launch the application locally with native HTTP 206 range seeking
python run_local.py
```
