# Ashtavadhanam v2 — Master Plan & Architectural Roadmap

> **Repository**: `Ashtavadhanam_modern`  
> **Target Version**: `v2.0.0`  
> **Status**: Approved Architectural Plan  
> **Scope**: All v2 experimental modules, design tokens, asset manifests, and components reside under the `v2/` directory tree.

---

## 1. Vision & Architectural Philosophy

The **v1 Modernization** successfully rescued and preserved the 1997 Ashtavadhanam CD-ROM with **100% forensic fidelity** across 173 recitations, 15 videos, 53 master visuals, PWA offline mobility, and a 65-point mobile test suite.

The **v2 Evolution** builds upon this immutable foundation to transform the application from a **pure digital preservation portal** into a **living, immersive cultural sanctuary**. It fuses ancient Indian aesthetics (Bhojpatra folios, golden yantra geometry, Vedic meters) with state-of-the-art web capabilities (Web Audio API, dynamic theming, interactive educational mini-games, and vector folio generation).

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ASHTAVADHANAM v2 ECOSYSTEM                      │
└────────────────────────────────────────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┼───────────────────────────────┐
    ▼                               ▼                               ▼
[AESTHETIC SANCTUARY]     [AUDIO & SCHOLARSHIP]         [GAMIFIED HERITAGE]
• Bhojpatra Micro-Texture • 0.75x/1.0x/1.25x Speed       • The Avadhani's Challenge
• 8-Petaled Lotus Yantra  • Karaoke Verse Highlighting   • Niṣiddhākṣarī Word Game
• Dual Theme Switcher     • Sanskrit Sandhi Inspector    • Memory Recall Quiz
• Double-Fillet Borders   • Web Audio Waveform Analyzer  • Printable PDF Folios
```

---

## 2. The 10 Core v2 Pillars & Technical Specifications

### Pillar 1: Organic Bhojpatra / Palm-Leaf Micro-Texture Engine
- **Objective**: Eliminate modern flat-screen digital sterility; replicate the tactile grain of aged Himalayan birch-bark (*Bhojpatra*) and South Indian talipot palm-leaf (*Tālapatra*).
- **Core Preservation Rule**:
  - The authentic 1997 CD-ROM backdrop artwork (`eightfold 01-25.jpg` oil lamps, headers, and calligraphic watermarks) remains **100% untouched and sacred**.
- **Implementation & Scope**:
  - Applied to the **surface finish of the Sanskrit recitation card containers** replacing flat solid cream (`#fffdf8`) with an authentic, organic tactile parchment finish.
  - CSS-based SVG noise synthesis (`feTurbulence` with anisotropic horizontal frequencies for birch bark, longitudinal frequencies for palm leaf).
  - Multiplied at `mix-blend-mode: multiply` / `overlay` with subtle `opacity: 0.045 - 0.065`, preserving WCAG AAA text contrast.
  - Includes a delicate inner double-fillet gold border (`rgba(212, 175, 55, 0.25)`).
  - Toggleable in Settings (`Classic Flat` vs `Tactile Bhojpatra`).
  - *Note*: Full manuscript folio card layouts are reserved for Pillar 10 (Printable Study Folios & PDF Export).

### Pillar 2: Animated Aṣṭadala Padma (8-Petaled Lotus) Sacred Watermark
- **Objective**: Symbolize the eight simultaneous cognitive facets of *Aṣṭāvadhānam* (Nishedhakshari, Samasya, Vyastakshari, Dattapadi, Chitrakavya, Pushpaganan, Ashukavita, and Aprastuta-prasangam).
- **Desktop / Widescreen Placement**:
  - **In-Canvas Placement**: Hovers in the natural open space on the left of the 1997 canvas directly above the sacred oil lamps, radiating upward like a divine aura of concentration without obstructing text.
  - **Widescreen Flanking Symmetrical Harmony**: When viewed on wide desktop monitors, the left void features the 8-Petaled Aṣṭadala Padma rotating meditatively ($120\text{s}$ period), while the right void features the complementary 12-Petaled Sri Aurobindo Society Lotus (or the Live Scholar Panel).
- **Mobile Screen Adaptation**:
  - Because vertical mobile displays have zero side gutters, the Aṣṭadala Padma adapts into:
    1. **Spinning Player Disc Emblem**: A rotating sacred lotus avatar inside the bottom floating audio player bar next to the recitation title (`Page 1 — Turn 1`), spinning gently while recitation audio plays (analogous to spinning vinyl/mandala discs in modern music apps).
    2. **Stage Watermark**: A faint $6\%$ opacity background watermark behind the canvas.

### Pillar 3: Sanskrit Chandas (Meter) & Sandhi Breakdown Inspector
- **Objective**: Assist scholars, university students, and lovers of Sanskrit poetry in deciphering classical metrical patterns.
- **Desktop Widescreen Mode**:
  - Uses the right flanking void as a persistent **Live Scholar Workstation**, displaying the meter, syllable count, Laghu/Guru rhythm notation, and Sandhi split of the active verse without covering the central 1997 stage.
- **Mobile Mode (Pull-Up Bottom Sheet)**:
  - Each recitation card carries a compact, tap-friendly pill: `[📜 अनुष्टुभ् (Meter) ▾]`.
  - Tapping this pill slides up a sleek **Mobile Bottom Sheet Drawer** showing:
    - Metrical classification: *Śārdūlavikrīḍita* (19 syllables), *Mandākrāntā* (17), *Vasantatilakā* (14), *Anuṣṭubh* (8×4), *Upajāti* (11).
    - Laghu/Guru ($\smallsmile / \text{—}$) rhythm notation for each poetic quarter (*Pāda*).
    - Word-by-word Sandhi splits.
  - Tapping outside or ✕ dismisses it immediately, restoring full-screen reading.

### Pillar 4: Interactive Sanskrit Glossary & Lore Tooltips
- **Objective**: Explain rare literary techniques, historical allusions, and poetic idioms on tap.
- **Desktop Implementation**:
  - Integrated into the right companion panel for instant contextual reading.
- **Mobile Implementation**:
  - Inline Sanskrit terms (*Niṣiddhākṣarī*, *Samasyā*, *Dattapadī*, *Aprastuta-prasaṅgam*) feature subtle dotted underlays; tapping reveals an instant micro-tooltip bottom sheet.
  - Full alphabetical glossary index accessible via a dedicated entry in the top-right **Tools & Settings Drawer (⋮)**.

### Pillar 5: Variable Audio Speed Playback Engine (`0.75×`, `1.0×`, `1.25×`)
- **Objective**: Enable students to slow down rapid extempore poetic recitations to study pronunciation and Sandhi transitions.
- **Implementation (Desktop & Mobile Universal)**:
  - Built directly into the **Floating Audio Player Bar** (`#player-bar`) as an instant `⚡ 1.0×` pill button.
  - Preserves pitch using HTML5 Audio `preservesPitch = true`.
  - Single tap cycles sequentially: `1.0×` $\rightarrow$ `0.75×` (slow chanting study) $\rightarrow$ `1.25×` (rapid review) $\rightarrow$ `1.0×`.
  - Accessible on mobile with a single thumb tap without leaving the recitation view.

### Pillar 6: Active Verse Pāda (Karaoke) Highlighting & Auto-Scroll
- **Objective**: Ensure visitors and students never lose their place during rapid extempore Sanskrit recitations.
- **Architectural Rationale**: Replaces generic, distracting audio frequency equalizers with genuine poetic value—tracking the 4 quarters (*Pādas*) of the classical verse in sync with the master audio.
- **Implementation (Desktop & Mobile)**:
  - **Pāda-by-Pāda Illumination**: As the scholar chants, the exact Sanskrit line illuminates with a warm golden highlight (`background: rgba(212, 175, 55, 0.15); border-left: 3px solid #d4af37`), while the corresponding English translation phrase softly brightens.
  - **Active Card Golden Aura**: The current recitation card gains an authentic double-fillet gold glow, while non-active cards dim slightly ($80\%$ opacity) to focus attention.
  - **Smooth Auto-Scroll**: During continuous `"Play All in Page"` playback, automatically calls `card.scrollIntoView({ behavior: 'smooth', block: 'center' })` as each turn begins, keeping the active verse centered without requiring user touch.
  - **Pāda Progress Badge**: Displays real-time metrical progress (`Line 2 of 4`) in the audio player bar.

### Pillar 7: Dual Sanctuary Theme Switcher
- **Themes**:
  1. **Night Sanctuary (Current Default)**:
     - Background: `#120e0b` (Deep obsidian gold).
     - Text: `#f3ede2` / `#ffd875`.
     - Optimized for OLED displays, dark rooms, and battery saving.
  2. **Royal Palm-Leaf Sanctuary (Daylight Mode)**:
     - Background: `#fbf6ea` (Warm aged parchment).
     - Text: `#281b10` (Deep iron gall ink).
     - Borders: `#c99738` (Antique burnished brass).
     - Optimized for bright daylight reading and high-contrast accessibility.

### Pillar 8: "The Avadhani's Challenge" (Interactive Memory Mini-Game)
- **Objective**: Gamify the cognitive art of concentration; allow visitors to test their own memory against the 1997 scholars!
- **Game Modes**:
  1. *The Forbidden Letter Game*: In Round 1, can you compose a sentence without using the letter given by the interrogator?
  2. *The 4-Word Dattapadi Memory*: The game gives you 4 words; after 3 distraction questions, can you recall the 4 words in correct order?
  3. *Sound the Bell Counter*: Count the random temple bell rings while answering a poetry quiz!

### Pillar 9: Printable Royal Manuscript Folio Generator (PDF Export)
- **Objective**: Enable schools, ashrams, universities, and scholars to print and archive authentic study sheets of any round.
- **Header Architecture & Official App Icon**:
  - **Top Centered App Emblem**: Every downloaded / printed A4 PDF folio MUST feature the official circular golden **Ashtavadhanam Application Icon** (`assets/icons/icon-192.png` / `apple-touch-icon.png`) prominently centered at the top of the header.
  - **Archival Header Typography**: Directly below the emblem, the folio displays:
    - *Sri Aurobindo Society Heritage Archives • 1997*
    - Classical calligraphic title *AṢṬĀVADHĀNAM*
    - Extempore round title, interrogator (*Pṛcchaka*), and poetic subject.
- **Implementation & Page Content**:
  - Client-side vector folio renderer with standard `@media print` CSS layout and instant vector PDF download.
  - Sanskrit Devanagari verse in classical calligraphic font with Anuṣṭubh / Śārdūlavikrīḍita metrical breakdown.
  - English IAST transliteration, word-for-word Sandhi splits, and poetic translation.
  - Authentic dual archival stamps: Sri Aurobindo Society seal (Pondicherry) and Ashtavadhanam 1997 Heritage Preservation seal.
  - Single-page A4 format per round (total 25 folios), with optional full 25-round bound anthology export.

---

## 2.1 Multi-Device Responsive Adaptation Matrix (Desktop vs. Mobile)

To resolve screen clutter and ensure 100% feature accessibility across both desktop monitors and vertical mobile screens:

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

---

## 3. Directory Layout in `v2/`

All future development, assets, and component modules for version 2 will strictly reside within the `v2/` directory:

```
Ashtavadhanam_modern/
├── v2/
│   ├── V2_MASTER_PLAN_AND_ROADMAP.md   # This master specification document
│   ├── css/
│   │   ├── v2-parchment-texture.css    # Bhojpatra micro-texture & lotus mandala styles
│   │   ├── v2-themes.css               # Night Sanctuary vs Royal Palm-Leaf themes
│   │   └── v2-audio-visualizer.css     # Waveform & speed selector styles
│   ├── js/
│   │   ├── v2-audio-fx.js              # Web Audio API visualizer & speed controller
│   │   ├── v2-chandas-inspector.js     # Sanskrit metrical scan & Sandhi breakdown
│   │   ├── v2-memory-game.js           # "The Avadhani's Challenge" mini-game controller
│   │   └── v2-folio-export.js          # Printable PDF folio generator
│   ├── content/
│   │   └── data_v2.json                # Extended schema with Chandas & glossary annotations
│   └── tests/
│       └── test_v2_features.py         # Dedicated test suite for v2 modules
```

---

## 4. Phase-by-Phase Release Milestones

| Milestone | Target Scope | Key Deliverables |
|:---|:---|:---|
| **Phase 2.1** | *Audio & Immersion* | Playback speed control (`0.75×-1.25×`), Real-time waveform visualizer, Verse karaoke auto-scroll |
| **Phase 2.2** | *Visual Atmosphere* | Bhojpatra micro-texture engine, Rotating lotus watermark, Dual Theme switcher |
| **Phase 2.3** | *Scholarship & Poetry* | Sanskrit Chandas (Meter) inspector, Word-by-word Sandhi splits, Interactive glossary |
| **Phase 2.4** | *Gamified Heritage* | "The Avadhani's Challenge" concentration mini-game, Sound-the-bell memory test |
| **Phase 2.5** | *Publishing & Distribution* | Printable royal folio PDF generator, Offline institutional bundle |

---

## 5. Backward Compatibility & Preservation Doctrine

- **Rule 1**: The v1 production baseline (`index.html`, `js/app.js`, `js/player.js`) remains completely functional, self-contained, and backward-compatible.
- **Rule 2**: All new v2 capabilities must be progressively enhanced: devices with older browsers or disabled JavaScript will cleanly fall back to the v1 baseline without errors.
- **Rule 3**: Zero external dependencies: all v2 modules will remain vanilla ES6+ and pure CSS without npm or framework bloat, adhering strictly to `AGENTS.md`.
