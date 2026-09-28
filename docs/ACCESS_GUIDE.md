# Ashtavadhanam Modern: Complete Access & User Guide

> **Application:** Ashtavadhanam — The Wonder that is Sanskrit (1997 CD-ROM → 2026 Modern Web App)  
> **Platform Support:** Desktop (Windows, macOS, Linux), Mobile & Tablet (iOS, Android), 10-Foot Smart TV

---

## 1. How to Access and Run the Application

The modernized application is completely self-contained and supports multiple zero-friction access modes:

### Mode A: 1-Click Hosted Web Access (GitHub Pages / Online)
When hosted online, open the URL in any modern browser:
```text
https://gapskris.github.io/ashtavadhanam/
```
* **Offline Ready**: On first visit, the Progressive Web App (PWA) caches the application shell. Subsequent visits work even without an internet connection.

---

### Mode B: Zero-Install Standalone Execution (`file:///`)
No web server, build tool, or internet connection is required:
1. Navigate to the project folder `Ashtavadhanam_modern/`.
2. **Double-click `index.html`** to open it directly in your browser.
3. *Why it works*: All core database content is pre-packaged in `js/data.js` (`window.ASHTAVADHANAM_DATA`), bypassing browser local-file CORS restrictions cleanly.

---

### Mode C: High-Performance Local Launcher (`run_local.py`)
For the smoothest audio and video scrubbing on your local machine:
1. Open PowerShell or a terminal in `Ashtavadhanam_modern/`.
2. Run:
   ```powershell
   python run_local.py
   ```
3. The launcher will automatically find an open port (default `8080`), launch a custom HTTP server with **native HTTP 206 Partial Content (Byte Range)** support, and open `http://localhost:8080/index.html` in your default browser.

---

### Mode D: Mobile & Tablet (Progressive Web App - PWA)
1. Open the hosted web URL in Safari (iOS) or Chrome (Android).
2. Tap the **Install Web App** button in the header or Tools Drawer:
   - **iOS Safari**: Tap **Share** (📤) $\rightarrow$ **"Add to Home Screen"**.
   - **Android Chrome**: Tap the in-app **Install** button or browser menu (⋮) $\rightarrow$ **"Install app"**.
3. Launch directly from your home screen as a standalone, fullscreen app with the authentic circular golden scholar emblem and full offline support.

---

### Mode E: 10-Foot Smart TV Mode (Living Room Experience)
1. Open the application in your Smart TV browser (LG webOS, Samsung Tizen, Android TV, Apple TV).
2. Press **`T`** on your keyboard/remote or click the **📺 TV Mode** button in the header.
3. **Features**:
   - 1.4× scaled high-contrast typography readable from 10 feet away.
   - Glowing gold spatial focus outlines on active elements.
   - Spatial roving focus using TV Remote Arrow keys (`Up`, `Down`, `Left`, `Right`).
   - On-screen touch/mouse DPAD overlay available for touch-based Smart TV controllers.

---

## 2. Navigation Architecture & Dual Drawers

The application features a symmetrical **Dual 3-Bars Header**:

### Left 3-Bars Drawer (Sections & 25 Rounds)
* Click the **Left 3-Bars Menu Button** to open the main Navigation Drawer:
  - **The 25 Performance Rounds**: Quick links to any of the 25 rounds.
  - **Avadhana Kala Treatise**: 7 historic chapters on the history and art of Ashtavadhanam.
  - **Concentration Treatise**: 6 pages on the philosophy of mental focus (Sri Aurobindo & Vivekananda).
  - **Scholars & Assembly**: Biographies and 1997 historic photo of the 10 assembly scholars.
  - **Participating Institutions**: History of Pondicherry University and Sanskrit organizations.
  - **Sri Aurobindo Society**: Heritage context and Beach Office archives.
  - **Glimpses Theater**: 3-part video documentary.
  - **Historical Artwork Master Gallery**: Full grid of all 53 original master backdrops.

### Right 3-Bars Drawer (Tools & Settings)
* Click the **Right 3-Bars Tools Button** to access auxiliary features:
  - **Script / Display Switcher**: Toggle between pure Devanagari, Bilingual, and English IAST.
  - **Theme Switcher**: Night Sanctuary vs. Daylight mode.
  - **Search Engine**: Quick launch for Sanskrit and English search.
  - **Install Web App**: Direct 1-tap PWA installation.
  - **Multimedia Guide & Help**: CD-ROM historical manual.
  - **Acknowledgments & Credits**: 1997 digital preservation credits.
  - **Exit Module**: Quit confirmation modal.

### Top-Center Brand & Home Button
* Click the **Home icon (🏛️)** in the center of the top header at any time to return immediately to the **Splash Landing Gateway**.

---

## 3. Navigating the 25 Rounds

The performance is structured into **25 authentic extempore rounds**:
* **Horizontal Round Bar**: Click any round pill (`R1` through `R25`) in the horizontal selector.
* **Pinned Arrow Buttons**: Click the fixed **`◀`** or **`▶`** arrow buttons on the ends of the bar for instant single-click pagination.
* **Auto-Centering**: The active round pill automatically scrolls to the center of your view upon selection.
* **Swipe Gestures**: On touchscreens and tablets, swipe left or right on the stage to switch rounds.

---

## 4. Audio & Video Playback Controls

### Dialogue Cards & Recitations
* **Play Individual Recitation**: Click the **`▶`** button on any dialogue card to begin audio recitation.
* **Web Audio Temple Bell**: In Round 1, the opening invocation bell is synthesized in real-time with authentic acoustic harmonics (432Hz/864Hz/1296Hz).
* **Pause / Resume in Place**: Click **`⏸`** while playing to pause at the exact second, and click **`▶`** to resume seamlessly.
* **Switch Cards**: Clicking any other card immediately plays that verse without lag.

### Stage Actions
* **▶ Play All in Page**: Automatically plays all recitations on the current page in sequential order.
* **🎥 Watch Video Demonstration**: Available on Rounds 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, and 15. Launches the original 1997 demonstration video with instant seeking.

### Bottom Master Audio Player Bar
* **Now Playing Banner**: Displays the active speaker, round number, and turn title.
* **Scrubber Bar**: Click or drag the gold timeline scrubber to seek anywhere in the recitation.
* **Loop Toggle (🔁)**: Enables continuous auto-advance across dialogue turns and sequential rounds.

---

## 5. Sanskrit & English Display Switcher

The application defaults to pure **Devanagari** for an authentic Sanskrit experience. Switch views at any time via the header or Tools Drawer:
* **देवनागरी (Devanagari - Default)**: Authentic Sanskrit typography restored with 142 VedicBrahma2 glyphs, proper ligatures, and verse pāda indentation.
* **Bilingual / द्विभाषी**: Displays Sanskrit Devanagari alongside English translations separated by a gold border.
* **English (IAST)**: Displays academic Roman transliteration with authentic IAST diacritical marks (*ā, ī, ū, ṛ, ṅ, ñ, ś, ṣ*).

---

## 6. Sanskrit & Devanagari Search Engine

Press **`Ctrl + K`** (or **`/`** or click **🔍** in the header / Tools Drawer) to launch the search engine:
* **Devanagari Unicode Search**: Type Sanskrit words in standard Devanagari (e.g. `सञ्जीवयत्य`, `चर्मकारः`, `समस्या`, `अमर्त्यात्मा`).
  - *Smart Normalization*: Automatically handles homorganic nasals (e.g. searching with `ङ्` matches `ं`).
* **Romanized / English Search**: Type English concepts, verse themes, or phonetic terms (e.g. `cobbler`, `riddle`, `garland`, `ashukavita`, `pranshupala`).
* **Category Filters**: Filter results by **All**, **Rounds**, **Treatises**, or **Scholars**.
* **Deep-Linking**:
  - Click **📖 Jump to Verse** on any result to navigate directly to the target round, smoothly scroll to the card, and highlight it with a pulsing gold border.
  - Click **▶ Listen** to immediately begin playing that specific recitation.

---

## 7. Keyboard Shortcuts Reference

| Shortcut | Action |
| :--- | :--- |
| **`Ctrl + K`** or **`/`** | Open Sanskrit & English Search Modal |
| **`Escape`** | Close open modals (Search, Video, Exit, Drawers) |
| **`Space`** | Toggle Play / Pause on active audio track |
| **`T`** | Toggle Smart TV 10-Foot Mode |
| **`ArrowLeft` / `ArrowRight`** | Previous / Next Page (in TV mode) |
| **`ArrowUp` / `ArrowDown`** | Move spatial focus between dialogue cards (in TV mode) |
| **`Enter`** | Activate focused card or button |
