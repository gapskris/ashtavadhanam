# AGENTS.md — Ashtavadhanam Modernization & Heritage Digital Preservation: AI Agent Instructions

> **Scope**: This document provides mandatory operational principles, reverse-engineering methodology, preservation doctrines, architectural guidelines, and forensic verification protocols for all AI coding agents, autonomous subagents, and human contributors working on the **Aṣṭāvadhānam (1997 CD-ROM -> 2026 Modern Web Application)** preservation project and associated Sri Aurobindo Society digital heritage repositories.

---

## 1. Mission

This repository is a modernization and heritage preservation project for the historic 1997 Ashtavadhanam multimedia application originally implemented using:

- Macromedia Director
- Director Projectors (`.exe`, `start.exe`)
- Protected Director Movies (`.dxr`)
- Protected Director Cast Libraries (`.cxt`)
- Flash/SWF content
- WAV audio (16-bit PCM uncompressed)
- AVI video (Cinepak / Indeo codecs)
- Director Xtras
- Lingo scripts
- Director Score / Timeline
- Legacy multimedia assets

The goal is to reproduce the original application's user experience, navigation, content relationships, interactions, timing, and media behavior using modern web technologies with **100% forensic fidelity**.

The final application **MUST NOT depend on the legacy runtime**.

The target implementation is:

- Semantic HTML5
- Modular CSS3 (CSS Variables, Flexbox, Grid)
- Modern JavaScript / ES6+
- JSON & JSON Schema
- WebP / PNG / SVG / JPEG
- M4A / AAC-LC audio (High-Fidelity 192kbps) + MP3 universal fallback
- MP4 / H.264 / AAC video with `+faststart` atom alignment
- PWA capabilities (Service Worker, Web App Manifest)
- Standalone zero-install portability (works via `file:///` and local Python server)

The final production application must **NOT** require:

- Adobe/Macromedia Director
- Shockwave
- Flash Player
- SWF runtime
- Ruffle
- ActionScript runtime
- DXR/CXT runtime
- Java Applets
- Legacy Director Xtras

**Legacy files are SOURCE MATERIAL ONLY.**

---

## 2. The 4 Golden Operational Principles

> **Context • Scope • Architecture • Proof**
>
> 1. **Re-anchor Context**: Maintain strict awareness of the primary objective, previously approved archival decisions, file locations, and preservation constraints. When facing an obstacle, browser rendering bug, or media playback failure, re-anchor to the original 1997 source files (`.dxr`, `.cxt`, `media/`, `jpeg/`) before attempting speculative modern fixes.
> 2. **Enforce Scope & Non-Goals**: Explicitly define what may change, what must NOT change, and the exact stopping criterion. Never engage in unsolicited refactoring, drive-by formatting rewrites, or unapproved architectural redesigns.
> 3. **Verify Architecture & CD-ROM Source Boundaries**: Respect the original 1997 Macromedia Director structure. Understand the exact relationship between Director score channels, cast members, bitmaps, audio tracks, and the modern web presentation.
> 4. **Demand Proof & Evidence**: Never declare a task "completed" without real, verifiable proof. Execute the automated 1-to-1 forensic audit suite (`python tools/verify_1to1_mapping.py`), verify raw terminal logs, inspect git diffs, and test live browser audio/video execution.

---

## 3. PRIMARY PRINCIPLE: Never Assume Based on Filename

**NEVER implement a modern screen based only on the filename of a legacy file.**

NEVER assume that:

```
acknowledge.dxr  = one screen
ashmain.dxr      = one screen
ashtavadhanam.dxr = one page
```

A Director movie may contain:

- multiple screens
- multiple frames
- animations
- buttons
- navigation
- audio
- video
- state
- Lingo behavior
- external dependencies
- branching
- references to other movies
- references to CXT cast members
- references to external assets

Therefore every legacy module must first be reverse-engineered.

The correct sequence is:

```
DISCOVER
    ↓
INVENTORY
    ↓
REVERSE ENGINEER
    ↓
MAP
    ↓
SPECIFY
    ↓
IMPLEMENT
    ↓
VALIDATE
    ↓
MODERNIZE
```

**Never skip the reverse-engineering stage merely because the desired modern UI appears obvious.**

---

## 4. SOURCE OF TRUTH

The legacy application is the **behavioral baseline**.

The Master Plan is the **architectural baseline**.

When implementing a module:

1. Use the legacy application/files to determine actual behavior.
2. Use the Master Plan to determine the modern architecture.
3. Use extracted evidence to determine the UI and navigation.
4. **Do not invent behavior that cannot be established from the source.**
5. If behavior is uncertain, explicitly mark it as `UNKNOWN` or `NEEDS_VERIFICATION`.
6. **Never silently replace uncertain behavior with assumptions.**

---

## 5. LEGACY APPLICATION ARCHITECTURE

The legacy application generally follows this conceptual structure:

```
start.exe
    |
    v
startup / launcher
    |
    v
main navigation
    |
    +-------------------+
    |                   |
    v                   v
Director Movies      Cast Libraries
    |                   |
   DXR                 CXT
    |                   |
    +---------+---------+
              |
              v
         Media Assets
              |
    +---------+----------+
    |         |          |
   WAV       AVI        SWF
    |         |          |
    v         v          v
  Audio      Video    Animation
```

Do not confuse:

- **DXR** = Director movie / movie logic / score / sprites / behaviors
- **CXT** = Director cast library / cast members / content assets

They are related but are not interchangeable.

---

## 6. DXR ANALYSIS

For every `.dxr`, determine as much as possible about:

- movie identity
- frames
- frame ranges
- score/timeline (`VWSC` chunk)
- sprites
- channels
- sprite positions
- sprite dimensions
- sprite visibility
- cast references
- behaviors
- Lingo scripts (`Lscr`, `Lctx`, `Lnam`)
- mouse events
- keyboard events
- initialization logic
- state variables
- navigation commands
- movie transitions
- external file references
- audio references
- video references
- SWF references
- end-of-movie behavior
- return/back behavior
- looping behavior
- timing behavior

Particular attention MUST be given to:

- `go` / `go to`
- `play` / `play movie`
- `open` / `close`
- `startMovie` / `stopMovie`
- `exit` / `exitFrame`
- `mouseUp` / `mouseDown`
- `mouseEnter` / `mouseLeave`
- frame labels (`VWLB` markers)
- global variables
- properties
- handlers
- behaviors

**Do not translate Lingo mechanically.** First determine **WHAT THE BEHAVIOR DOES**, then implement the equivalent behavior in modern JavaScript.

---

## 7. CXT ANALYSIS

For every `.cxt`, inventory all useful cast members.

For each cast member determine where possible:

- cast ID
- name
- type
- dimensions
- text
- image / bitmap
- vector
- audio
- video
- Flash/SWF
- script/behavior
- font
- button state
- relationship to DXR sprites
- external dependencies

Create stable modern asset identifiers.

Example:

```
Director Cast #42  -->  acknowledge_logo  -->  assets/images/acknowledge/logo.webp
```

Do not expose Director cast IDs as the primary identifiers in the final application. Director IDs are migration metadata.

---

## 8. MODULE-BY-MODULE WORKFLOW

Every Director module MUST be processed independently before implementation.

Current known application modules include:

- `acknowledge`
- `ashmain` / `ashmain1`
- `institu`
- `glimpse`
- `eightfold`
- `ashtavadhanam`
- `performance`
- `sas`
- `avdhankala`
- `open`
- `startup`
- `exit`
- `help`

Do not assume this list is complete. The physical inventory on disk is authoritative.

For each module:

```
<module>.dxr + <module>.cxt + related media + related SWF + related external files
```

must be analyzed together.

---

## 9. REQUIRED MODULE ANALYSIS OUTPUT

For every module produce a specification containing:

### 8.1 Module Overview
- Purpose, entry point, exit point, parent module, child modules, known dependencies.

### 8.2 Screen Map
- Document every meaningful visual state. Do NOT equate Director frames automatically with modern screens. A group of Director frames may represent one modern screen, or one movie may contain multiple screens.

### 8.3 Interaction Map
- Document buttons, clickable regions, navigation, hover states, pressed states, keyboard/touch interactions, back, next, exit, replay, pause, resume.

### 8.4 Navigation Map
- Document: `current screen` $\rightarrow$ `action` $\rightarrow$ `destination`. Never infer a destination merely from a filename.

### 8.5 Timeline Map
- Animation duration, frame ranges, looping, delays, audio synchronization, video synchronization, transitions, timed events.

### 8.6 Asset Map
- Document: `legacy asset` $\rightarrow$ `cast/member/reference` $\rightarrow$ `usage` $\rightarrow$ `modern asset`.

---

## 10. APPLICATION UI MAP

The modern application MUST be based on the actual discovered navigation graph.

Conceptually the application flow is:

```
START / SPLASH GATEWAY
  |
  v
OPENING CHOREOGRAPHY
  |
  +-- Phase 1: Title Calligraphy (S01 to S06 + ashmain_theme)
  |
  +-- Phase 2: Cultural Mosaic (03 -> 02 -> 01.bmp + montage.mp4)
  |
  v
MAIN PERFORMANCE PORTAL (ASHMAIN)
  |
  +------------------+------------------+------------------+
  |                  |                  |                  |
  v                  v                  v                  v
THE 25 ROUNDS      AVADHANA KALA      CONCENTRATION      HISTORICAL ARCHIVES
(173 Recitations   (7 Chapters &      (6 Pages &         (Glimpses Theater,
 + 11 Videos)       7 Canvases)        6 Canvases)        Scholars, Institutions,
                                                          Society, Master Gallery)
```

Agents MUST update the map when actual reverse-engineering evidence differs. Never preserve a hypothetical relationship as fact.

---

## 11. DIRECTOR → WEB MAPPING

Use these conceptual mappings:

| Director Concept | Modern Web Representation |
| :--- | :--- |
| **Movie (`.dxr`)** | Page / module / section component |
| **Frame** | UI state or timeline state |
| **Sprite** | Semantic HTML5 / CSS element |
| **Cast Member (`.cxt`)** | Web asset / component |
| **Score (`VWSC`)** | JS / CSS timeline controller |
| **Lingo** | Vanilla JavaScript (ES6+) |
| `mouseUp` | `click` / `pointerup` |
| `mouseDown` | `pointerdown` |
| `mouseEnter` | `pointerenter` |
| `mouseLeave` | `pointerleave` |
| **Button Cast** | Semantic HTML `<button>` |
| **Text Cast** | Semantic HTML text / typography |
| **Bitmap** | WebP / PNG / JPEG |
| **Vector** | SVG / CSS |
| **Sound Cast** | High-Fidelity M4A (192kbps AAC) + MP3 fallback |
| **Video (`.avi`)** | Universal MP4 (H.264 + AAC + `+faststart`) |
| **Flash Asset (`.swf`)**| HTML5 / Canvas / SVG / JS |
| `go to` | Application state transition |
| `play movie` | Module navigation |
| **Global Variable** | Application state model |
| **Property** | Module / element state |
| **Behavior** | JS event handler / controller |
| **Director Xtra** | Browser API or JS implementation |

---

## 12. DO NOT REPLICATE DIRECTOR'S INTERNAL ARCHITECTURE

The objective is **behavioral equivalence, NOT architectural equivalence**.

Do NOT create:

```
DirectorFrame1.js
DirectorFrame2.js
DirectorSprite17.js
```

unless there is a clear forensic reason.

Instead prefer semantic structures:

```
AcknowledgeScreen
MainMenu
InstitutionSection
GlimpseSection
EightfoldSection
AshtavadhanamSection
```

Use modern component and state architecture.

---

## 13. DATA-DRIVEN CONTENT & SCHEMA INTEGRITY

Content must be separated from presentation:

```
content/
  └── data.json           # Single source of truth: 25 rounds, treatises, metadata
```

- Do not hard-code large amounts of educational or spiritual text inside JavaScript controllers.
- JavaScript should implement behavior and choreography.
- JSON should represent content, transcripts, translations, and metadata.

---

## 14. MODERN SCREEN MODEL

Where useful, represent screens in structured data:

```json
{
  "id": "acknowledge",
  "title": "Acknowledgement",
  "elements": [
    {
      "id": "logo",
      "type": "image",
      "asset": "acknowledge_logo"
    },
    {
      "id": "continue",
      "type": "button",
      "action": "navigate",
      "target": "ashmain"
    }
  ]
}
```

Do not force every Director detail into JSON. Use JSON where it improves separation of content and presentation. Complex behavior belongs in JavaScript modules.

---

## 15. RESPONSIVE DESIGN

The modern application must work seamlessly across:

- Windows desktop (Chrome, Edge, Firefox)
- macOS desktop (Safari, Chrome)
- Linux desktop
- Android mobile & tablets
- iOS / iPadOS Safari
- 10-Foot Smart TV interfaces

Use:

- CSS Grid & Flexbox
- Responsive units (`rem`, `vh`, `vw`, `%`)
- Fluid typography
- Pure CSS variables defined in `:root`
- Responsive media queries

Do not assume the original fixed 800×600 Director stage size is the final layout. Preserve the visual character, proportions, and information hierarchy while adapting gracefully to modern widescreen devices.

---

## 16. INPUT HANDLING

Use Pointer Events where possible:

```javascript
pointerdown, pointerup, pointerenter, pointerleave
```

rather than creating separate mouse-only and touch-only implementations.

Hover effects must not be relied upon for essential functionality. Use `@media (hover: hover)` for hover-specific visual enhancements.

---

## 17. MEDIA MODERNIZATION PROTOCOL

### Audio
- **Primary:** High-Fidelity M4A / AAC-LC (192 kbps voice recitation, 256 kbps music theme).
- **Fallback:** Universal 192kbps MP3 generated for older environments.
- **PARITY REQUIREMENT:** All 173 recitation tracks and 11 special sound tracks must exist in both M4A and MP3 formats.

### Video
- Convert legacy Cinepak / Indeo AVI to universal MP4:
  - Video: H.264 (`yuv420p`, CRF 18-20, web-optimized)
  - Audio: AAC-LC (192 kbps, stereo, 44.1 kHz)
  - Atom Alignment: `-movflags +faststart` (moov atom at start of file for zero-delay streaming).
- The final web application must not require AVI playback.

### Images & Graphics
- Original master graphics preserved without downsampling.
- Stacked GPU layers (`transform: translateZ(0)`, `will-change: opacity`) for progressive dissolve animations.
- WebP/PNG formats where applicable.

### Flash / SWF
- Do not retain SWF as a production runtime dependency. Recreate Flash interactions using HTML5, SVG, CSS, or Canvas.

---

## 18. ANIMATION PRINCIPLES

Use the simplest modern technology that preserves behavior:

1. CSS transitions / animations (`opacity`, `transform`)
2. Web Animations API
3. `requestAnimationFrame()` for frame-accurate timing

**Do not reproduce every Director frame manually if a modern CSS transition can reproduce the same dissolve behavior.**

For media-synchronized animation:

```
requestAnimationFrame()  -->  media.currentTime  -->  visual state
```

Do not rely on `timeupdate` as a frame-accurate animation clock.

---

## 19. BROWSER AUTOPLAY COMPLIANCE

Web browsers strictly enforce the **Transient Activation / Autoplay Security Policy**:

* The application **MUST** have an explicit initial user interaction:
  ```
  "▶ Play Authentic Opening Montage & Invocations"
  ```
* The initial user gesture establishes the browser interaction context needed for subsequent audio and video playback.
* Any unmuted `.play()` call must be initiated directly within the synchronous gesture call stack.
* Do not attempt to bypass browser security restrictions.

---

## 20. STATE MANAGEMENT

Translate legacy global variables into an explicit modern state model:

```javascript
class AshtavadhanamApp {
  constructor() {
    this.currentPage = 1;
    this.currentTrackIndex = 0;
    this.isPlaying = false;
    this.displayView = 'bilingual'; // 'devanagari' | 'bilingual' | 'english'
    this.isTvMode = false;
  }
}
```

Avoid uncontrolled global JavaScript variables. Prefer a centralized, encapsulated state controller.

---

## 21. EXPLICIT NAVIGATION

Navigation must be explicit and intent-driven:

```javascript
this.navigateToPage(roundNumber);
this.navigateToSection(sectionId);
```

Do not use arbitrary filename manipulation to implement navigation. Legacy filenames are migration metadata, not application routes.

---

## 22. VALIDATION AGAINST LEGACY (4 CRITERIA)

Every implemented module must be compared against legacy behavior:

1. **Visual:** Layout, typography, images, buttons, colors, spacing, animation, transitions.
2. **Functional:** Buttons, navigation, branching, back/next, replay, exit, state changes.
3. **Media:** Audio timing, video timing, synchronization, volume, looping.
4. **Content:** Text, Sanskrit verses, English translations, images, captions, labels, sequence.

The modern implementation must reproduce the legacy behavior unless a specific quality enhancement has been explicitly approved.

---

## 23. EVIDENCE AND CONFIDENCE CLASSIFICATION

Every reverse-engineered behavior must carry an evidence classification:

- `CONFIRMED`: Verified directly in decompiled Director score/Lingo bytecode.
- `PROBABLE`: Strongly supported by cast names and file structure.
- `INFERRED`: Deduced from neighboring screen logic.
- `UNKNOWN`: Unresolved behavior.
- `NEEDS_VERIFICATION`: Requires verification on physical CD-ROM or consultation with archives.

**Do not present INFERRED behavior as CONFIRMED.**

---

## 24. NO SILENT ASSUMPTIONS

If an asset cannot be identified: `UNKNOWN_ASSET`  
If a navigation target cannot be established: `UNKNOWN_NAVIGATION`  
If a Lingo handler cannot be reconstructed: `UNRESOLVED_LINGO`  
If a media relationship is unclear: `UNRESOLVED_MEDIA_REFERENCE`  

**Document the issue instead of guessing.**

---

## 25. TRACEABILITY & METADATA

Every modern asset must trace to its legacy source:

```
Legacy Asset:  Cast #4 (open.cxt) -> media/opening/montage.avi
Modern Asset:  assets/video/montage.mp4
Metadata:      H.264/AAC, +faststart, 320x240, 2m 57s soundtrack
```

Do not lose traceability between legacy and modern assets.

---

## 26. DIRECTORY STRUCTURE

The modernized application is organized as follows:

```
Ashtavadhanam_modern/
├── assets/
│   ├── audio/           # 173 M4A + 173 MP3 recitation tracks + 11 special sound tracks
│   │   ├── Page 1-25/   # Round recitations
│   │   └── special/     # Director bells + ashmain_theme opening soundtrack
│   ├── images/          # 53 master historical visuals, backdrops, and calligraphy
│   │   ├── opening/     # S01-S06.jpg, 01.jpg, 02.jpg, 03.jpg
│   │   ├── institution/ # Sanskrit institutions banner
│   │   └── sas/         # Sri Aurobindo Society Beach Office
│   └── video/           # 15 H.264 MP4 videos (1 montage + 11 rounds + 3 glimpses)
├── content/
│   └── data.json        # Single source of truth: 25 rounds, treatises, metadata
├── css/
│   ├── main.css         # Primary layout, typography, animations, responsive design
│   ├── player.css       # Floating high-fidelity audio player bar
│   └── tv.css           # 10-foot Smart TV interface styling
├── js/
│   └── app.js           # Core application controller (state, audio, animations, UI)
├── tools/
│   └── verify_1to1_mapping.py # Automated 43-point forensic verification suite
├── index.html           # Main standalone entry point
└── run_local.py         # Zero-install local HTTP launcher
```

---

## 27. AGENT WORKFLOW (9-STEP DISCIPLINE)

Every agent MUST follow this workflow:

```
Step 1: READ          Read AGENTS.md, Master Plan, and Verification Report.
Step 2: INSPECT       Inspect relevant legacy files (dxr, cxt, media, jpeg).
Step 3: INVENTORY     Identify all chunks, casts, audio, video, images.
Step 4: REVERSE ENG   Recover score, frames, sprites, scripts, state, navigation.
Step 5: DOCUMENT      Create/update module maps, screen maps, asset maps.
Step 6: DESIGN        Define the modern semantic representation.
Step 7: IMPLEMENT     Implement vanilla HTML5/CSS3/ES6+ code.
Step 8: VALIDATE      Run tools/verify_1to1_mapping.py and browser checks.
Step 9: RECORD        Update verification report and sync documentation.
```

---

## 28. AGENT TASK BOUNDARIES

When assigned a specific module:

- ONLY modify files within the declared scope.
- Before modifying shared architecture: explain why, identify affected modules, preserve backward compatibility, and update documentation.
- Never rewrite working, verified components unnecessarily.

---

## 29. ACCESSIBILITY & INCLUSION

- Use semantic HTML: `<button>`, `<nav>`, `<main>`, `<header>`, `<section>`, `<article>`, `<audio>`, `<video>`.
- Keyboard navigation (Tab, Enter, Space, Arrow keys).
- Clear focus indicators and ARIA landmarks.
- Meaningful `alt` text for images and transcripts for recitations.
- Multilingual support: Sanskrit Devanagari, bilingual side-by-side, and IAST English macrons.

---

## 30. STANDALONE OFFLINE-FIRST PORTABILITY

The modernization MUST run everywhere without complex build pipelines:

- Direct double-click on `index.html` via `file:///` protocol.
- Zero-install local Python launcher: `python run_local.py`.
- Static hosting: GitHub Pages, Cloudflare Pages, Netlify.
- USB thumb drive distribution.

---

## 31. MASTER ASSET & DATA MAPPING MATRIX

| Original CD-ROM Asset Category | Source Location | Modern Application Target | Total Count | Verification Rule |
| :--- | :--- | :--- | :---: | :--- |
| **Performance Rounds** | `page1.cxt` – `page25.cxt` | `content/data.json` (`pages[]`) | 25 Rounds | Exactly 25 rounds mapped 1-to-1 |
| **Performance Audio Recitations** | `media/Page 1/` – `Page 25/` | `assets/audio/Page X/*.m4a` & `*.mp3` | 173 Tracks | All 173 master audio tracks verified |
| **Round Demonstration Videos** | `media/avis/*.avi` | `assets/video/*.mp4` | 11 Videos | Rounds [2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 15] |
| **Round Backdrops (Canvases)** | `jpeg/eightfold 01-25.jpg` | `assets/images/eightfold 01-25.jpg` | 25 Images | Displayed per round & in Gallery |
| **Avadhana Kalā Treatise** | `avdhankala.dxr` & `avdhankala01-07.jpg` | 7 Chapters + 7 Canvas backdrops | 7 Chapters | Full Devanagari text + Canvas reader |
| **Concentration Treatise** | `ashtavadhanam.dxr` & `ashtava01-06.jpg` | 6 Pages + 6 Canvas backdrops | 6 Pages | Philosophy of Attention + Canvas reader |
| **Opening Title Animation** | `jpeg/opening/S01.jpg` – `S06.jpg` | `assets/images/opening/S01-S06.jpg` | 6 Frames | Stacked GPU 60fps progressive dissolve |
| **Cultural Opening Mosaic** | `jpeg/opening/01.bmp`, `02.jpg`, `03.jpg` | `assets/images/opening/01-03.jpg` | 3 Images | Color (03) -> Sepia (02) -> Cutout (01) |
| **Opening Archival Video** | `media/opening/montage.avi` | `assets/video/montage.mp4` | 1 Video | Plays in 320x240 center cutout of 01.bmp |
| **Historic Glimpses Theater** | `media/GLIMPSE1-3.avi` | `assets/video/GLIMPSE1-3.mp4` | 3 Videos | Standalone 3-part video gallery |
| **Director Sound Effects & Theme** | Embedded cast in `.dxr` / `.cxt` | `assets/audio/special/*.m4a` & `*.mp3` | 11 Tracks | 10 bells/effects + 1 opening master theme |
| **Historical Assembly & Photos** | `performance.jpg`, `institution`, `sas` | `assets/images/` | 3 Photos | Scholars 1997 photo, Banner, SAS Office |
| **Total Master Visuals** | All verified graphical assets | Reader, Canvases, & Master Gallery | 53 Images | 100% active in UI & Gallery Grid |

---

## 32. AUTOMATED VERIFICATION SUITE

Before declaring any ticket complete, run the automated 43-point audit suite:

```powershell
python tools/verify_1to1_mapping.py
```

### Verification Criteria Checklist:
- [x] All 53 Master Visuals exist on disk and are active in UI
- [x] All 15 Master Videos exist in H.264/AAC MP4 format with `+faststart`
- [x] All 173 recitations exist in dual M4A (192kbps) and MP3 formats
- [x] All 11 Director internal sound effects and themes extracted and converted
- [x] All 25 rounds mapped 1-to-1 in `content/data.json`
- [x] All 7 Avadhāna Kalā chapters & 6 Concentration pages mapped to canvases
- [x] All required DOM elements present and responsive
- [x] Verification report confirms **43 / 43 CHECKS PASSED (100% PASS)**

---

## 33. STANDARD COMMANDS

```powershell
# 1. Run the 43-Point 1-to-1 Automated Verification Audit Suite
python tools/verify_1to1_mapping.py

# 2. Launch Local Zero-Install Web Server
python run_local.py
# (Automatically opens http://localhost:8080/index.html in your default web browser)

# 3. Direct Local Launch via File Protocol
start index.html

# 4. Check for Audio/Video File Integrity
python -c "import glob, os; print('M4As:', len(glob.glob('assets/audio/**/*.m4a', recursive=True)), 'MP3s:', len(glob.glob('assets/audio/**/*.mp3', recursive=True)), 'Videos:', len(glob.glob('assets/video/*.mp4')))"

# 5. Sync Master Verification Report & AGENTS.md to Root
Copy-Item "COMPREHENSIVE_1TO1_VERIFICATION_REPORT.md" -Destination "..\COMPREHENSIVE_1TO1_VERIFICATION_REPORT.md" -Force
Copy-Item "AGENTS.md" -Destination "..\AGENTS.md" -Force
```

---

## 34. FINAL PRODUCTION RULE

The production application must contain **ZERO runtime dependency** on:

- `start.exe`
- Director / Shockwave
- Flash / SWF
- DXR / CXT
- Director Xtras
- ActionScript
- Java Applets

These legacy files may remain in source archives, but they must never be required to execute the modernized application.

---

## 35. THE MOST IMPORTANT RULE

> **WHEN IN DOUBT: DO NOT GUESS.**
>
> 1. Inspect the legacy source.
> 2. Trace the behavior.
> 3. Document the evidence.
> 4. Implement the modern equivalent.
> 5. Validate with automated tests.
>
> ```
> ORIGINAL APPLICATION  -->  UNDERSTAND EXACTLY  -->  DOCUMENT  -->  REIMPLEMENT  -->  VALIDATE  -->  MODERN PWA
> ```
>
> **NOT:**
> ```
> ORIGINAL APPLICATION  -->  GUESS WHAT IT DID   -->  BUILD SOMETHING SIMILAR
> ```

---

## 36. FINAL PRESERVATION PLEDGE FOR AUTONOMOUS AGENTS

Every agent working in this repository signs off on the following core pledge:

> *"I pledge to preserve the authentic 1997 cultural and musical heritage of Sri Vijay Ji, Dr. Ganesh, and the Sri Aurobindo Society with 100% forensic fidelity. I will never manufacture, synthesize, or hallucinate content. I will ensure every original graphic, video, audio recitation, and treatise page is preserved, active, verified, and accessible for generations to come."*
