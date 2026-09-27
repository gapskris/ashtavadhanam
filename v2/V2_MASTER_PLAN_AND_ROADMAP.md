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
- **Implementation**:
  - CSS-based SVG noise synthesis with subtle parchment fiber grain overlay.
  - Multiplied at `mix-blend-mode: overlay` with `opacity: 0.045` so it does not degrade text legibility or increase network payload.
  - Zero heavy raster bitmaps; computed completely on the GPU via CSS `feTurbulence` filter.

### Pillar 2: Animated Aṣṭadala Padma (8-Petaled Lotus) Sacred Watermark
- **Objective**: Symbolize the eight simultaneous cognitive facets of *Aṣṭāvadhānam* (Nishedhakshari, Samasya, Vyastakshari, Dattapadi, Chitrakavya, Pushpaganan, Ashukavita, and Aprastuta-prasangam).
- **Implementation**:
  - High-precision SVG golden geometric mandala centered behind the main performance stage.
  - Slow, meditative 120-second rotational animation (`transform: rotate(360deg)` with `animation-timing-function: linear`).
  - Subtle breathing glow pulsing on audio play.

### Pillar 3: Sanskrit Chandas (Meter) & Sandhi Breakdown Inspector
- **Objective**: Assist scholars, university students, and lovers of Sanskrit poetry in deciphering classical metrical patterns.
- **Implementation**:
  - Data expansion in `v2/data_v2.json`:
    - Metrical classification for every verse: *Śārdūlavikrīḍita* (19 syllables), *Mandākrāntā* (17 syllables), *Vasantatilakā* (14 syllables), *Anuṣṭubh* (8×4), *Upajāti* (11 syllables).
    - Laghu/Guru ($\smallsmile / \text{—}$) rhythm notation for each poetic quarter (*Pāda*).
  - Floating pill on recitation cards: `[📜 Meter: Śārdūlavikrīḍita]` $\rightarrow$ taps to reveal the syllabic scan and Sandhi splits.

### Pillar 4: Interactive Sanskrit Glossary & Lore Tooltips
- **Objective**: Explain rare literary techniques, historical allusions, and poetic idioms on tap.
- **Implementation**:
  - Micro-tooltips integrated into Devanagari text for key terms.
  - Interactive cards explaining:
    - *Niṣiddhākṣarī*: The forbidden-letter challenge.
    - *Samasyā-pūraṇam*: Solving the paradoxical poetic riddle.
    - *Dattapadī*: Composing verses using four unrelated words given by the interrogator.
    - *Aprastuta-prasaṅgam*: The witty distraction clown attempting to break the Avadhani's concentration.

### Pillar 5: Variable Audio Speed Playback Engine (`0.75×`, `1.0×`, `1.25×`)
- **Objective**: Enable students to slow down rapid extempore poetic recitations to study pronunciation and Sandhi transitions.
- **Implementation**:
  - Integrated into the persistent bottom player bar (`#player-bar`).
  - Preserves pitch using HTML5 Audio `preservesPitch = true`.
  - Step selector: `[ 0.75× | 1.0× | 1.25× ]` with instant state feedback.

### Pillar 6: Real-time Audio Waveform Frequency Visualizer
- **Objective**: Bring voice recitations visually to life.
- **Implementation**:
  - Utilizes Web Audio API `AudioContext` and `AnalyserNode` (`fftSize = 64`).
  - Renders 16 golden vertical frequency bars pulsing in real-time inside the player bar badge whenever recitation audio is active.
  - Gracefully falls back to a CSS pulsing wave if Web Audio is unsupported or restricted by strict browser permissions.

### Pillar 7: Active Verse Karaoke Sync & Smooth Auto-Scrolling
- **Objective**: Ensure visitors never lose their place during multi-verse recitations.
- **Implementation**:
  - During continuous `"Play All in Page"` playback, the active recitation card illuminates with a warm gold fillet border.
  - Smoothly calls `card.scrollIntoView({ behavior: 'smooth', block: 'nearest' })` as each track starts, keeping the spoken Sanskrit verse centered in the viewport.

### Pillar 8: Dual Sanctuary Theme Switcher
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

### Pillar 9: "The Avadhani's Challenge" (Interactive Memory Mini-Game)
- **Objective**: Gamify the cognitive art of concentration; allow visitors to test their own memory against the 1997 scholars!
- **Game Modes**:
  1. *The Forbidden Letter Game*: In Round 1, can you compose a sentence without using the letter given by the interrogator?
  2. *The 4-Word Dattapadi Memory*: The game gives you 4 words; after 3 distraction questions, can you recall the 4 words in correct order?
  3. *Sound the Bell Counter*: Count the random temple bell rings while answering a poetry quiz!

### Pillar 10: Printable Royal Manuscript Folio Generator (PDF Export)
- **Objective**: Enable schools, ashrams, and universities to print authentic study sheets of any round.
- **Implementation**:
  - Client-side vector folio renderer.
  - Clean `@media print` CSS layout and optional PDF download containing:
    - Ashtavadhanam royal emblem at head.
    - Round title, interrogator (*Pṛcchaka*), and poetic art.
    - Sanskrit Devanagari verse in classical calligraphic font.
    - English IAST translation and metrical analysis.

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
