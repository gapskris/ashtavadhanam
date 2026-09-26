# Ashtavadhanam Modern — Device-to-Device Adaptation Matrix & UI Architecture

## Overview
The modernized **Ashtavadhanam** web application is engineered as a responsive, cross-platform Progressive Web App (PWA) that dynamically adapts its layout, typography, controls, and interaction models across four distinct device categories:
1. **Mobile Phones** (Small screens, one-handed touch, portrait & landscape)
2. **Tablets & iPads** (Medium screens, touch & stylus, 2-column flexibility)
3. **Desktop & Laptop PCs** (High-DPI large screens, mouse & keyboard shortcuts)
4. **Smart TVs & 10-Foot UI** (Living-room distance, TV browser WebKit/Blink, D-pad remote control)

---

## Device Adaptation Matrix

| Gadget Category | Typical Viewport | Typography (`rem` / `clamp`) | Navigational Buttons & Controls | Touch / Remote Input Mechanism |
|---|---|---|---|---|
| **Mobile Phones** *(iPhone, Android)* | `320px – 640px` (Portrait & Landscape) | • Sanskrit: `1.15rem – 1.25rem`<br>• English: `0.95rem – 1.05rem`<br>• Fluid scaling via CSS `clamp()` | • **Two-tier Adaptive Header**: 3-Way Switcher (`देवनागरी`, `Bilingual`, `English`) drops into a dedicated full-width segmented row beneath the brand title to prevent text clipping.<br>• **Pill Navigation**: Horizontal touch carousel with momentum scrolling (`-webkit-overflow-scrolling: touch`) and active pill auto-centering.<br>• **Bottom Player**: Compact stacked layout showing the live Speaker/Turn title on top, followed by 48px play button and full-width scrubber. | • **Touch Targets**: Minimum **44×44px** (WCAG AAA compliance).<br>• **Touch Gestures**: Horizontal swipe on stage (Swipe Left = Next Round, Swipe Right = Previous Round).<br>• `@media (hover: hover)` prevents sticky hover states on touchscreens. |
| **Tablets & iPads** *(iPad, Galaxy Tab)* | `641px – 1024px` | • Sanskrit: `1.25rem – 1.45rem`<br>• English: `1.05rem – 1.15rem` | • **Header**: Single-line layout with brand on left, 3-way toggle centered, tools on right.<br>• **Stage**: Spacious parchment canvas with side-by-side button actions ("Play All Round", "Watch Video").<br>• **Player**: Expanded progress bar with prominent time indicators. | Touch & Stylus support with unified Pointer Events (`pointerdown`). Smooth swipe gestures enabled. |
| **Desktop & Laptop PCs** *(1080p, 1440p, 4K)* | `1025px – 1920px+` | • Sanskrit: `1.35rem`<br>• English: `1.10rem` | • **Full 3-Column Player**: Left (Speaker/Track info), Center (Scrubber & controls), Right (AAC 192k audio badge & Volume).<br>• **Keyboard Shortcuts**: Spacebar (Play/Pause), Left/Right Arrows (Previous/Next clip), Escape (Close dialogs), 'T' key (TV mode). | Mouse click, smooth scroll wheel, full keyboard shortcut integration. |
| **Smart TVs & 10-Foot UI** *(Samsung Tizen, LG webOS, Android TV, Apple TV)* | `1920px – 3840px` (4K / 8K at 10-foot distance) | • Base font: **22px**<br>• Sanskrit: **1.8rem (bold & crisp)**<br>• English: **1.45rem** | • **10-Foot UI Mode (`tv.css`)**: Buttons enlarge to **54px–64px** height for effortless visibility from couch.<br>• **Spatial Focus Ring**: Glowing **4px golden aura** (`#ffc45e` with pulse) around the active focused element.<br>• **D-Pad Controller (`tv-remote.js`)**: Up/Down/Left/Right remote arrows navigate between rounds, dialogue cards, and media buttons. | • **Automatic TV Detection**: Checks TV user-agents (`Tizen`, `webOS`, `Android TV`, `Bravia`, etc.) and automatically activates TV mode.<br>• Full TV remote OK/Enter and Back key support. |

---

## Detailed UI & Interaction Breakdown

### 1. Header & 3-Way Language Switcher
* **Desktop / Large Screens**: Rendered as a single horizontal flexbar. Brand on the left, 3-way segmented toggle (`[देवनागरी]`, `[Bilingual / द्विभाषी]`, `[English (IAST)]`) centered, and TV / Fullscreen tools on the right.
* **Mobile (< 640px)**: The 3-way toggle breaks into a second full-width row (`order: 3; width: 100%;`), allowing each button to have large touch areas and legible labels without squishing the title.

### 2. Round Selector Pills (`R1` to `R25`)
* **Touch-Optimized Carousel**: Smooth horizontal scroll container with scroll snapping (`scroll-snap-type: x proximity`).
* **Active Pill Auto-Centering**: Whenever a round is selected—or when the player auto-advances to the next round—the active pill executes `scrollIntoView({ behavior: 'smooth', inline: 'center' })` to keep the user oriented.

### 3. Dialogue Cards & Typography
* **Devanagari Font Hierarchy**: Rendered in clean Unicode using Noto Sans Devanagari / Tiro Devanagari Sanskrit with clear conjuncts and ligatures.
* **English / IAST Hierarchy**: Academic Roman transliteration with authentic diacritical macrons (*ā, ī, ū, ṛ, ṅ, ñ, ś, ṣ*).
* **3-Way Display Modes**:
  - `mode-devanagari`: Shows only Sanskrit verses.
  - `mode-english`: Shows only English translation and commentary.
  - `mode-bilingual`: Shows the Sanskrit verse on top and the English translation directly beneath with a dashed gold separator.

### 4. Bottom Master Player
* **Desktop**: 3-column fixed bar: Now Playing details (left) | Scrubber & playback controls (center) | Codec badge & mute (right).
* **Mobile (< 768px)**: Converts into an efficient 2-tier stacked player:
  1. Live Turn/Speaker banner centered on top (`Round 1 — Turn 1 • अवधानी`).
  2. Playback controls (48px main play button, prev, next, auto-advance).
  3. Full-width touch-seekable scrubber with timestamps.

### 5. Smart TV 10-Foot UI & Remote Control Engine
* **Automatic Detection**: `tv-remote.js` inspects `navigator.userAgent` for TV platforms (`Tizen`, `webOS`, `Android TV`, `Apple TV`, `Bravia`, etc.) and engages TV mode automatically on page load.
* **Spatial D-Pad Navigation**:
  - `ArrowDown` / `ArrowUp`: Navigates between focusable dialogue cards and controls.
  - `ArrowLeft` / `ArrowRight`: Navigates previous/next round pills and controls.
  - `Enter` / `OK`: Activates current button or starts recitation.
  - `Spacebar`: Toggles Play / Pause.
  - `'T'` key: Manual toggle for TV mode.
  - `Escape` / `Back`: Closes video modal or drawer.
* **High-Contrast Focus Indicators**: Active element gains a 4px golden halo (`#ffc45e`) with a subtle scale transform (`1.02x`) so the viewer never loses cursor position from across the room.

---

## Automated Verification Suite Results

```
============================================================
  ASHTAVADHANAM MODERNIZATION — AUTOMATED VERIFICATION SUITE
============================================================
[PASS] All 15 MP4 videos converted & present (H.264 CRF 18, 192k AAC).
[PASS] All 173 high-fidelity M4A (192k AAC) audio files present.
[PASS] All 173 compatibility MP3 audio files present.
[PASS] All 10 internal special audio tracks extracted and converted.
[PASS] All 25 performance background canvases present.
[PASS] Data layer contains all 25 performance pages.
[PASS] All 5 contextual treatises and essays parsed into data layer.
[PASS] All 3 Glimpses video entries populated.
[PASS] All application web assets and scripts verified.
============================================================
VERIFICATION SUMMARY: 9 PASSED, 0 FAILED (100% SUCCESS)
============================================================
```
