# Ashtavadhanam Modern — Device-to-Device Adaptation Matrix & Responsive Architecture

## Overview
The modernized **Ashtavadhanam** web application is engineered as a responsive, cross-platform Progressive Web App (PWA) powered by an **Autonomous Adaptive Viewport Engine**. It dynamically adapts its layout, stage scaling, typography, controls, and interaction models across four distinct device categories:
1. **Mobile Phones** (Small vertical screens, one-handed touch, portrait & landscape, zero-clipping safe scroll)
2. **Tablets & iPads** (Medium screens, touch & stylus, responsive 2-column flexibility)
3. **Desktop & Laptop PCs** (High-DPI widescreen, 1080px flush stage, mouse & keyboard shortcuts)
4. **Smart TVs & 10-Foot UI** (Living-room distance, TV browser WebKit/Blink, spatial D-pad remote control)

---

## Device Adaptation Matrix

| Gadget Category | Typical Viewport | Typography (`rem` / `clamp`) | Navigational Buttons & Controls | Touch / Remote Input Mechanism |
|---|---|---|---|---|
| **Mobile Phones** *(iPhone, Android)* | `320px – 640px` (Portrait & Landscape) | • Sanskrit: `1.15rem – 1.25rem`<br>• English: `0.95rem – 1.05rem`<br>• Fluid scaling via CSS `clamp()` | • **Symmetrical Dual 3-Bars Header**: Left 3-bars button opens the primary Navigation Drawer; Right 3-bars button opens the Tools Drawer containing language switcher and search.<br>• **Pinned Pagination Bar**: Horizontal round selector with pinned left/right arrow buttons and auto-centering.<br>• **In-Canvas Parchment Flow**: Dialogue cards positioned in the safe blank parchment area (13.2% clearance from top) with zero clipping. | • **Touch Targets**: Minimum **44×44px** (WCAG AAA compliance).<br>• **Touch Gestures**: Horizontal swipe on stage (Swipe Left = Next Round, Swipe Right = Previous Round).<br>• `@media (hover: hover)` prevents sticky hover states on touchscreens. |
| **Tablets & iPads** *(iPad Pro, Galaxy Tab)* | `641px – 1024px` | • Sanskrit: `1.25rem – 1.45rem`<br>• English: `1.05rem – 1.15rem` | • **Header**: Single-line layout with brand on left, 3-way toggle centered, tools on right.<br>• **Stage**: Spacious parchment canvas with side-by-side button actions ("Play All Round", "Watch Video").<br>• **Player**: Expanded progress bar with prominent time indicators. | Touch & Stylus support with unified Pointer Events (`pointerdown`). Smooth swipe gestures enabled. |
| **Desktop & Laptop PCs** *(1080p, 1440p, 4K)* | `1025px – 1920px+` | • Sanskrit: `1.35rem`<br>• English: `1.10rem` | • **Stage Widening**: Widened to 1080px flush alignment with the top page bar for expansive widescreen reading.<br>• **Full 3-Column Player**: Left (Speaker/Track info), Center (Scrubber & controls), Right (AAC 192k audio badge & Volume).<br>• **Keyboard Shortcuts**: Spacebar (Play/Pause), Left/Right Arrows (Previous/Next clip), Escape (Close dialogs), 'T' key (TV mode), `Ctrl+K` (Search). | Mouse click, smooth scroll wheel, full keyboard shortcut integration. |
| **Smart TVs & 10-Foot UI** *(Samsung Tizen, LG webOS, Android TV, Apple TV)* | `1920px – 3840px` (4K / 8K at 10-foot distance) | • Base font: **22px**<br>• Sanskrit: **1.8rem (bold & crisp)**<br>• English: **1.45rem** | • **10-Foot UI Mode (`tv.css`)**: Buttons enlarge to **54px–64px** height for effortless visibility from couch.<br>• **Spatial Focus Ring**: Glowing **4px golden aura** (`#ffc45e` with pulse) around the active focused element.<br>• **D-Pad Controller (`tv-remote.js`)**: Up/Down/Left/Right remote arrows navigate between rounds, dialogue cards, and media buttons. | • **Automatic TV Detection**: Checks TV user-agents (`Tizen`, `webOS`, `Android TV`, `Bravia`, etc.) and automatically activates TV mode.<br>• Full TV remote OK/Enter and Back key support. |

---

## Autonomous Adaptive Viewport Engine (`updateStageScale`)

To resolve screen clutter, background tiling, and container clipping across varying display geometries, an autonomous scaling algorithm operates continuously in `js/app.js`:

1. **Dynamic Scale Factor Calculation**:
   - Calculates the ratio between the available window width/height and the 1080px reference stage width.
   - Evaluates device pixel ratios (`window.devicePixelRatio`) to ensure text and Sanskrit ligatures remain razor-sharp.
2. **Safe Parchment Writing Area (In-Canvas Parchment Flow)**:
   - Sets dialogue card top clearance strictly to **13.2%** across all 25 slides.
   - Keeps historical top titles and sacred oil lamps (*diyas*) permanently visible and unobstructed.
3. **Zero-Clipping Mobile Containment**:
   - Enforces `overflow-x: hidden` on viewport bodies while permitting frictionless vertical scrolling within the dialogue container.
   - Eliminates background image repeat tiling with `background-repeat: no-repeat; background-size: contain`.

---

## Detailed UI & Interaction Breakdown

### 1. Symmetrical Dual-Header Architecture
* **Desktop / Large Screens**: Symmetrical layout featuring Left Menu (Sections & 25 Rounds), Center Brand with Home icon, and Right Tools Drawer (Themes, Views, Search, PWA Install, Help, Exit).
* **Mobile (< 640px)**: Language view-switcher pills drop out of the top header into the Right Tools Drawer, eliminating header overflow while maintaining instant single-tap access.

### 2. 25-Round Page Navigation Bar (`R1` to `R25`)
* **Pinned Navigational Arrows**: Left (`◀`) and Right (`▶`) navigation arrow buttons are pinned to the ends of the bar for single-click round pagination.
* **Touch-Optimized Carousel**: Smooth horizontal scroll container with antique gold-themed scrollbar (`::-webkit-scrollbar`).
* **Active Pill Auto-Centering**: Whenever a round is selected—or when the player auto-advances to the next round—the active pill executes `scrollIntoView({ behavior: 'smooth', inline: 'center' })` to keep the user oriented.

### 3. Dialogue Cards & Typography
* **Devanagari Font Hierarchy**: Rendered in clean Unicode using Noto Sans Devanagari / Tiro Devanagari Sanskrit with 142 restored VedicBrahma2 glyphs.
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

## 65-Point Automated Multi-Device Verification Suite (`tests/test_mobile_responsive.py`)

A comprehensive Playwright test suite validates layout stability across 5 canonical device profiles:

| Target Device Profile | Viewport Geometry | Key Verification Assertions | Status |
|:---|:---|:---|:---:|
| **Desktop 1080p** | `1920 × 1080` | Flush 1080px stage width, 3-column player bar, zero horizontal scroll, header alignment | **PASS (13/13)** |
| **iPad Pro (12.9")** | `1024 × 1366` | Aspect-ratio scaling, 2-column dialogue layout, touch target sizes, drawer overlay | **PASS (13/13)** |
| **iPhone SE** | `375 × 667` | Zero text clipping, stacked 2-tier audio bar, 44px touch targets, mobile drawer menu | **PASS (13/13)** |
| **Google Pixel 7** | `412 × 915` | Fluid typography clamp scaling, pinned pagination arrows, safe scroll containment | **PASS (13/13)** |
| **Samsung Galaxy S20** | `360 × 800` | Minimum mobile width stability, splash gateway halo scaling, zero element overlaps | **PASS (13/13)** |
| **TOTAL VERIFICATION** | **All 5 Profiles** | **65 Programmatic Assertions** | **65 / 65 PASS (100%)** |

---

## Version 2 Multi-Device Adaptation Matrix (The 9 Pillars)

| Feature / Pillar | Desktop Widescreen Display (≥ 1024px) | Mobile Portrait Phone (< 600px) |
|:---|:---|:---|
| **Pillar 1: Bhojpatra Micro-Texture** | Organic parchment grain on card containers + subtle aged vignette | Identical organic grain on card containers with zero legibility degradation |
| **Pillar 2: Aṣṭadala Padma Lotus** | Open space above oil lamps on canvas OR Left Flanking Space (paired with Sri Aurobindo Lotus on Right Flank) | Spinning sacred lotus disc avatar inside the Floating Audio Player Bar next to track title + 6% background watermark |
| **Pillar 3: Sanskrit Meter (*Chandas*)** | Persistent Right Companion Workstation with real-time Laghu/Guru scan & Sandhi splits | Tap-friendly `[📜 Meter ▾]` pill on each card $\rightarrow$ slides up a sleek Pull-Up Bottom Sheet Drawer |
| **Pillar 4: Glossary & Lore** | Persistent Right Companion Panel card | Inline term tap tooltip bottom-sheet + complete glossary in top-right Tools Drawer (⋮) |
| **Pillar 5: Audio Speed Control** | Instant speed selector in audio player bar | Single-thumb `⚡ 1.0×` button in floating audio player bar cycling `0.75×`, `1.0×`, `1.25×` |
| **Pillar 6: Active Verse Pāda Highlighting** | Golden card aura + real-time line-by-line Pāda illumination synchronized with audio | Real-time line highlight + smooth card auto-scroll centering active verse |
| **Pillar 7: Dual Sanctuary Themes** | Dedicated Sun/Moon switch on header and audio bar | Quick-tap toggle inside top-right Tools Drawer (⋮) and Settings sheet |
| **Pillar 8: The Avadhani's Challenge** | High-visibility gold beacon banner on round header (`[🧠 Test Your Memory in Round 1]`) | Compact sticky challenge pill on round header + slide-up interactive quiz bottom sheet |
| **Pillar 9: PDF Royal Folio Export** | Instant `[📄 Export A4 Folio]` button $\rightarrow$ side-by-side print preview studio with toggleable annotations | `[📥 Save PDF]` in mobile action bar $\rightarrow$ downloads clean A4 single-sheet folio with top app icon |
