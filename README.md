# Aṣṭāvadhānam — The Wonder that is Sanskrit (अष्टावधानम्)

[![Verification Audit](https://img.shields.io/badge/Forensic%20Audit-70%2F70%20PASS%20(100%25)-success?style=for-the-badge&logo=checkmarx)](docs/FINAL_AUDIT_REPORT.md)
[![Zero Runtime Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Vanilla%20ES6%2B)-blue?style=for-the-badge)](docs/MIGRATION_AND_TECH_STACK.md)
[![PWA Ready](https://img.shields.io/badge/PWA-Offline%20Ready-purple?style=for-the-badge&logo=pwa)](manifest.json)
[![Platform](https://img.shields.io/badge/Platform-Web%20%7C%20Mobile%20%7C%20Smart%20TV-gold?style=for-the-badge)](docs/ACCESS_GUIDE.md)

A modern, universal Progressive Web Application (PWA) preserving and presenting the historic Sanskrit **Aṣṭāvadhānam** performance held on **20th January 1997** at Pondicherry, organized by **Sri Aurobindo Society** and the **Department of Sanskrit, Pondicherry University**.

Forensically reverse-engineered from the original 1997 Macromedia Director CD-ROM into open, future-proof web standards with **100% content fidelity and zero data loss**.

---

## 🌟 Key Highlights

- **25 Performance Pages**: Complete eightfold concentration feat by **Śatāvadhānī Dr. R. Ganesh** facing 8 challenging scholars.
- **173 Master Voice Recitations**: High-fidelity 192 kbps AAC-LC voice audio (+ 192 kbps MP3 fallback) with interactive playback controls, in-place pausing, and dialogue synchronisation.
- **15 Archival Video Demonstrations**: Universally playable H.264 (CRF 18) videos with `+faststart` atom alignment for instant seeking.
- **3-Way Live Sanskrit & English Switcher**:
  1. *Devanagari (देवनागरी)* — Pure classical Sanskrit script.
  2. *Bilingual Side-by-Side* — Sanskrit verse on top, English commentary beneath.
  3. *English + IAST* — Academic transliteration with macrons (*ā, ī, ū, ṛ, ṅ, ñ, ś, ṣ*).
- **Interactive Sanskrit Search Engine**: Client-side inverted index searching 253 corpus documents with Devanagari ligature normalization, phonetic Romanization, and deep-linking.
- **53 Master Visual Artworks**: All original illuminated canvases and archival photographs active across readers and in the **Historical Artwork Master Gallery Grid**.
- **Smart TV 10-Foot UI**: Built-in spatial D-pad remote control navigation, key bindings, and high-contrast gold focus outlines.
- **Zero-Dependency Architecture**: Pure Semantic HTML5, Modular CSS3, and Vanilla ES6+. Zero build steps, zero npm packages, zero proprietary runtimes.

---

## 🚀 Live Demo on GitHub Pages

The application is deployed directly via GitHub Pages:  
👉 **`https://gapskris.github.io/ashtavadhanam/`**

*(To enable GitHub Pages in your fork: Repository **Settings → Pages → Source: Deploy from a branch (`main` / root)**)*.

---

## 💻 Quick Start & Running Locally

The modernized application is completely portable and requires no build pipeline:

### Option 1: Direct Double-Click (`file:///`)
Double-click **`index.html`** in any web browser. Data is pre-packaged synchronously in `js/data.js` to bypass local-file CORS restrictions cleanly.

### Option 2: High-Performance Local Launcher
Run the embedded Python HTTP server with **native HTTP 206 Partial Content (Range Seeking)** for smooth video scrubbing:
```bash
# Clone the repository
git clone https://github.com/gapskris/ashtavadhanam.git
cd ashtavadhanam

# Launch the local HTTP runner (opens browser at http://localhost:8080)
python run_local.py
```

---

## 🧪 Automated Test & Verification Suite

Run the master test runner to verify all parity, range seeking, player logic, and forensic audit assertions:

```bash
python tests/run_all_tests.py
```

```text
======================================================================
   ASHTAVADHANAM MODERN: EXECUTING COMPLETE TEST SUITE
======================================================================
--- RUNNING: Canonical Data Parity Test ---
  [PASS] Canonical Data Parity: js/data.js is 100% synchronized with content/data.json
--- RUNNING: Native HTTP 206 Range Seeking Test ---
  [PASS] Video HTTP 206 Range request verified (bytes 1000-4999)
  [PASS] Audio HTTP 206 Range request verified (bytes 0-1023)
--- RUNNING: Audio Player Logic & State Toggle Test ---
  [PASS] Initial play starts audio recitation
  [PASS] Second click pauses recitation in place (without restarting)
  [PASS] Third click resumes recitation smoothly
--- RUNNING: 70-Point Forensic Audit Verification Suite ---
  [PASS] 70/70 Forensic Assertions Verified (Images, Videos, Audios, Schema, UI, PWA, Search)
======================================================================
  ALL TEST SUITES PASSED (100% GREEN) in 1.93s
  STATUS: 100% PRODUCTION READY FOR RELEASE
======================================================================
```

---

## 📁 Repository Structure

```text
├── index.html                      # Main single-page web app entry point (root for GitHub Pages)
├── manifest.json                   # Web App Manifest for mobile & desktop install
├── sw.js                           # Progressive Web App Service Worker (v1.1.3)
├── run_local.py                    # Local HTTP server with native HTTP 206 Range support
├── README.md                       # Repository overview & quick start
│
├── docs/                           # 📚 Documentation & User Guides
│   ├── MIGRATION_AND_TECH_STACK.md # 🛠️ Tech Stack, Migration Process & Zero-Data-Loss Guide
│   ├── ACCESS_GUIDE.md             # 📖 Complete User Access Guide (Web, file:///, Mobile, TV, Search)
│   ├── FINAL_AUDIT_REPORT.md       # 🔍 100% Complete Forensic Audit Report (Sections A–T)
│   ├── GITHUB_PAGES_HOSTING_GUIDE.md # 🌐 Web Hosting & Custom Domain Deployment Guide
│   ├── DEVICE_ADAPTATION_MATRIX.md # 📱 Responsive & Multi-Device Compatibility Matrix
│   └── archive/                    # 🗄️ Historical intermediate planning documents
│
├── tests/                          # 🧪 Automated Test Suites
│   ├── run_all_tests.py            # Master test runner
│   ├── test_1to1_verification.py   # 70-point forensic assertions
│   ├── test_data_parity.py         # Canonical JSON vs JS mirror sync check
│   ├── test_range_requests.py      # HTTP 206 Range byte-slicing test
│   └── test_player_logic.js        # Audio player toggle and state machine test
│
├── tools/                          # 🛠️ Extraction, Transcoding & Pipeline Scripts
│   ├── sync_data_js.py             # Database synchronizer
│   ├── convert_media.py            # FFmpeg audio/video transcoding pipeline
│   ├── krutidev_decoder.py         # 8-bit font to Unicode Devanagari decoder
│   ├── sanskrit_cleaner.py         # Sanskrit text normalization utility
│   ├── generate_db.py              # Canonical JSON database builder
│   └── reverse_engineering/        # Macromedia Director RIFX/XFIR decompilers
│
├── css/                            # 🎨 Design System (main.css, player.css, tv.css)
├── js/                             # ⚡ Vanilla ES6+ Controllers (app, player, search, tv-remote, data)
├── content/                        # 📄 Single Source of Truth database (data.json)
└── assets/                         # 🎨 Web Media (audio/, video/, images/, icons/)
```

---

## 📚 Further Documentation

- **[Migration & Tech Stack Guide](docs/MIGRATION_AND_TECH_STACK.md)**: Detailed breakdown of the technologies used, legacy-to-modern mapping, and precautions ensuring zero data loss.
- **[User Access Guide](docs/ACCESS_GUIDE.md)**: Step-by-step instructions for running via `file:///`, local server, PWA installation, and Smart TV remote controls.
- **[Final Forensic Audit Report](docs/FINAL_AUDIT_REPORT.md)**: Complete 20-section independent audit proving 100% parity across all 299 legacy CD-ROM files.

---

## 📜 Credits & Heritage Provenance

- **Original Performance**: 20th January 1997, Sri Aurobindo Society Beach Office, Pondicherry.
- **Avadhānī**: Śatāvadhānī Dr. R. Ganesh
- **Organizers**: Sri Aurobindo Society & Pondicherry University (Department of Sanskrit).
- **Digital Preservation & Modernization**: Converted from the 1997 CD-ROM release into open web standards with 100% forensic fidelity.
