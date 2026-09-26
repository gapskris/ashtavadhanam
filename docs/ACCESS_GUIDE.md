# Ashtavadhanam Modern: Complete Access & User Guide

> **Application:** Ashtavadhanam — The Wonder that is Sanskrit (1997 CD-ROM → 2026 Modern Web App)  
> **Platform Support:** Desktop (Windows, macOS, Linux), Mobile & Tablet (iOS, Android), 10-Foot Smart TV

---

## 1. How to Access and Run the Application

The modernized application is completely self-contained and supports multiple zero-friction access modes:

### Mode A: 1-Click Hosted Web Access (GitHub Pages / Online)
When hosted online (e.g. on GitHub Pages), open the URL in any modern browser:
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
2. Tap the browser menu:
   - **iOS Safari**: Tap **Share** (📤) $\rightarrow$ **"Add to Home Screen"**.
   - **Android Chrome**: Tap **Settings** (⋮) $\rightarrow$ **"Install app"** or **"Add to Home screen"**.
3. Launch directly from your home screen as a standalone, fullscreen app with offline support.

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

## 2. Navigating the Performance

The performance is structured as **25 authentic Pages** documenting the interaction between the *Avadhānī* (scholar performing the feat) and the 8 *Pṛcchakas* (scholars challenging him).

### Navigation Controls
* **Page Selector**: Click any pill (`Page 1` through `Page 25`) in the top horizontal bar to jump directly to that page.
* **Page Arrows**: Click **`◀`** or **`▶`** on the ends of the page bar to turn pages sequentially.
* **Swipe Gestures**: On touchscreens and tablets, swipe left or right on the stage to turn pages.
* **Keyboard Shortcuts**: Press `ArrowLeft` or `ArrowRight` while in Smart TV mode to change pages.

---

## 3. Audio & Video Playback Controls

### Dialogue Cards
* **Play Individual Recitation**: Click the **`▶`** button on the right side of any dialogue card to play its audio recitation.
* **Pause in Place**: Click the **`⏸`** button while a recitation is playing to **pause** at the exact current position.
* **Resume**: Click the **`▶`** button on a paused card to **resume** right where you left off.
* **Switch Cards**: Click any other card's play button to switch to that track instantly.

### Stage Actions
* **▶ Play All in Page**: Automatically plays all recitations on the current page in sequential order.
* **🎥 Watch Video Demonstration**: Available on Pages 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, and 15. Opens an authentic video demonstration modal recorded in 1997.

### Bottom Sticky Audio Bar
* Shows the currently playing speaker name, verse title, time elapsed, and total duration.
* Click the scrubber timeline bar to jump to any point in the recitation.
* Toggle the **Loop (🔁)** button to enable continuous auto-advance across all recitations and pages.

---

## 4. 3-Way Sanskrit & English Display Switcher

In the top header, use the language switcher buttons to change the display view in real-time:
* **देवनागरी (Devanagari)**: Shows the pure Sanskrit Devanagari verses and dialogue turns.
* **Bilingual / द्विभाषी (Default)**: Shows Sanskrit Devanagari alongside English translations and explanations.
* **English (IAST)**: Shows the English explanation with standardized International Alphabet of Sanskrit Transliteration (IAST) diacritics.

---

## 5. Sanskrit & Devanagari Search Engine

Press **`Ctrl + K`** (or **`/`** or click **🔍** in the header) to open the interactive search engine:
* **Devanagari Unicode Search**: Type Sanskrit words in standard Devanagari (e.g. `सञ्जीवयत्य`, `चर्मकारः`, `समस्या`, `अमर्त्यात्मा`).
  - *Smart Normalization*: The engine automatically handles homorganic nasals (e.g. searching with `ङ्` matches `ं`).
* **Romanized / English Search**: Type English concepts, verse themes, or phonetic terms (e.g. `cobbler`, `riddle`, `garland`, `ashukavita`, `pranshupala`).
* **Category Filters**: Filter results by **All**, **Pages (Rounds)**, **Treatises**, or **Scholars**.
* **Deep-Linking**:
  - Click **📖 Jump to Verse** on any result to navigate directly to the target page, scroll to the card, and highlight it with a pulsing gold border.
  - Click **▶ Listen** to immediately begin playing that specific recitation.

---

## 6. Keyboard Shortcuts Reference

| Shortcut | Action |
| :--- | :--- |
| **`Ctrl + K`** or **`/`** | Open Sanskrit & English Search |
| **`Escape`** | Close open modals (Search, Video, Exit, Help, Navigation Drawer) |
| **`Space`** | Toggle Play / Pause on active audio track |
| **`T`** | Toggle Smart TV 10-Foot Mode |
| **`ArrowLeft` / `ArrowRight`** | Previous / Next Page (in TV mode) |
| **`ArrowUp` / `ArrowDown`** | Move focus between dialogue cards (in TV mode) |
| **`Enter`** | Activate focused card or button |
