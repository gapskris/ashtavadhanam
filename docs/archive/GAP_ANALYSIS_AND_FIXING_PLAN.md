# GAP ANALYSIS & 1-TO-1 CONTENT MAPPING FIXING PLAN
**Project:** Ashtavadhanam (1997–2026) Legacy Modernization  
**Review Target:** Complete Utilization of All Assets from `jpeg/`, `media/`, `xtras/`, `cxt/`, and `dxr/`  
**Date:** September 2026

---

## 1. Executive Summary of Identified Gaps

Following your strict review and screenshots (`Pic 1: jpeg/` and `Pic 2: media/`), an exhaustive forensic scan was conducted across the modernized codebase. 

While all 53 images, 15 videos, and 173 audio files were converted and placed in the project assets on disk, **a significant UI integration gap was identified in how these assets were presented to the user**:

1. **Opening Animation & Montage Video Was Omitted in the UI**:
   - In the original CD-ROM, the opening consisted of:
     1. An animated sequence (`S01.jpg` to `S06.jpg`) fading in *"THE WONDER THAT IS SANSKRIT"*.
     2. The cultural photo mosaic (`01.bmp`) with the archival video `media/opening/montage.avi` playing in the central window.
   - *Current Gap*: The modernized app replaced this authentic sequence with a generic dark card, completely bypassing `S01`–`S06`, `01.bmp`, and `montage.mp4`.
2. **`ashtava01.jpg` to `ashtava06.jpg` (6 Images) Were Not Rendered in the UI**:
   - In the original CD-ROM `ashtavadhanam.dxr`, the *Concentration* treatise was split into **6 distinct pages (Page 1 of 6 to Page 6 of 6)**, with each page displayed against its specific thematic canvas (`ashtava01.jpg` to `ashtava06.jpg`).
   - *Current Gap*: The modern app dumped all paragraphs as plain unstyled text without displaying any of the 6 authentic images.
3. **`avdhankala01.jpg` to `avdhankala07.jpg` (7 Images) Were Not Rendered in the UI**:
   - In the original CD-ROM `avdhankala.dxr`, the *Avadhāna Kalā* treatise was split into **7 distinct chapters (Page 1 of 7 to Page 7 of 7)**, each framed by its authentic colored canvas (`avdhankala01.jpg` to `avdhankala07.jpg`).
   - *Current Gap*: The modern app dumped all paragraphs as plain text without rendering the 7 canvases.
4. **Scholars, Institutions, and Society Images Were Disconnected**:
   - `performance.jpg` (the historic assembly photo of Dr. Ganesh and the scholars on 20 Jan 1997) and `acknowledge/back.jpg` were not visible in the Scholars section.
   - `institution/institution .jpg` and `sas/sas.jpg` were not visible in their respective sections.

---

## 2. Complete 1-to-1 Content Mapping Matrix

This table establishes the strict, exhaustive 1-to-1 mapping for **every single master asset** from the original CD-ROM to the modern application:

### A. Opening Sequence & Introduction
| Original Master Asset | Type | Description in CD-ROM | Modern Placement & Fixing Action |
| :--- | :--- | :--- | :--- |
| `jpeg/opening/S01.jpg` to `S06.jpg` | 6 JPGs | Animated title fade-in: "The Wonder that is Sanskrit" with quill and manuscripts | **Built-in Opening Title Animation**: Plays sequentially on landing with authentic dissolve effect |
| `jpeg/opening/01.bmp` | BMP (800x600) | Cultural photo collage (Peacock, Gopuram, Dancers, Veena, Chariot) with center stage | **Opening Video Stage**: Rendered as the frame for the introductory video |
| `media/opening/montage.avi` | AVI (320x240) | Archival opening video with Sanskrit invocation and cultural footage | **`assets/video/montage.mp4`**: Plays directly inside the `01.bmp` stage with play/skip controls |
| `jpeg/opening/02.bmp`, `03.bmp` | 2 BMPs | Supplementary introductory stage artwork | Available in the Historical Gallery & opening transitions |

---

### B. The Performance Canvases & Videos (`eightfold.dxr` / `eightfold(s).dxr`)
| Original Master Canvas | Original Master Video | Master Audio Folder | Modern Round (R1 to R25) |
| :--- | :--- | :--- | :--- |
| `jpeg/eightfold 01.jpg` | *(None in original)* | `media/Page 1/` (6 WAVs) | **Round 1 (R1)**: Opening Stuti, Niṣiddhākṣarī, Aprastuta |
| `jpeg/eightfold 02.jpg` | `media/avis/02A.avi` | `media/Page 2/` (7 WAVs) | **Round 2 (R2)**: Video Button `02A.mp4` + 7 Audio recitations |
| `jpeg/eightfold 03.jpg` | `media/avis/03A.avi` | `media/Page 3/` (9 WAVs) | **Round 3 (R3)**: Video Button `03A.mp4` + 9 Audio recitations |
| `jpeg/eightfold 04.jpg` | `media/avis/04A.avi` | `media/Page 4/` (8 WAVs) | **Round 4 (R4)**: Video Button `04A.mp4` + 8 Audio recitations |
| `jpeg/eightfold 05.jpg` | *(None in original)* | `media/Page 5/` (8 WAVs) | **Round 5 (R5)**: Background canvas + 8 Audio recitations |
| `jpeg/eightfold 06.jpg` | `media/avis/06A.avi` | `media/Page 6/` (4 WAVs) | **Round 6 (R6)**: Video Button `06A.mp4` + 4 Audio recitations |
| `jpeg/eightfold 07.jpg` | `media/avis/07A.avi` | `media/Page 7/` (10 WAVs)| **Round 7 (R7)**: Video Button `07A.mp4` + 10 Audio recitations |
| `jpeg/eightfold 08.jpg` | `media/avis/08A.avi` | `media/Page 8/` (9 WAVs) | **Round 8 (R8)**: Video Button `08A.mp4` + 9 Audio recitations |
| `jpeg/eightfold 09.jpg` | `media/avis/09A.avi` | `media/Page 9/` (9 WAVs) | **Round 9 (R9)**: Video Button `09A.mp4` + 9 Audio recitations |
| `jpeg/eightfold 10.jpg` | *(None in original)* | `media/Page 10/` (7 WAVs)| **Round 10 (R10)**: Background canvas + 7 Audio recitations |
| `jpeg/eightfold 11.jpg` | `media/avis/11A.avi` | `media/Page 11/` (16 WAVs)| **Round 11 (R11)**: Video Button `11A.mp4` + 16 Audio recitations |
| `jpeg/eightfold 12.jpg` | `media/avis/12A.avi` | `media/Page 12/` (13 WAVs)| **Round 12 (R12)**: Video Button `12A.mp4` + 13 Audio recitations |
| `jpeg/eightfold 13.jpg` | `media/avis/13A.avi` | `media/Page 13/` (7 WAVs) | **Round 13 (R13)**: Video Button `13A.mp4` + 7 Audio recitations |
| `jpeg/eightfold 14.jpg` | *(None in original)* | `media/Page 14/` (8 WAVs) | **Round 14 (R14)**: Background canvas + 8 Audio recitations |
| `jpeg/eightfold 15.jpg` | `media/avis/15A.avi` | `media/Page 15/` (5 WAVs) | **Round 15 (R15)**: Video Button `15A.mp4` + 5 Audio recitations |
| `jpeg/eightfold 16.jpg` | *(None in original)* | `media/Page 16/` (2 WAVs) | **Round 16 (R16)**: Background canvas + 2 Audio recitations |
| `jpeg/eightfold 17.jpg` | *(None in original)* | `media/Page 17/` (7 WAVs) | **Round 17 (R17)**: Background canvas + 7 Audio recitations |
| `jpeg/eightfold 18.jpg` | *(None in original)* | `media/Page 18/` (10 WAVs)| **Round 18 (R18)**: Background canvas + 10 Audio recitations |
| `jpeg/eightfold 19.jpg` | *(None in original)* | `media/Page 19/` (9 WAVs) | **Round 19 (R19)**: Background canvas + 9 Audio recitations |
| `jpeg/eightfold 20.jpg` | *(None in original)* | `media/Page 20/` (5 WAVs) | **Round 20 (R20)**: Background canvas + 5 Audio recitations |
| `jpeg/eightfold 21.jpg` | *(None in original)* | `media/Page 21/` (6 WAVs) | **Round 21 (R21)**: Background canvas + 6 Audio recitations |
| `jpeg/eightfold 22.jpg` | *(None in original)* | `media/Page 22/` (2 WAVs) | **Round 22 (R22)**: Background canvas + 2 Audio recitations |
| `jpeg/eightfold 23.jpg` | *(None in original)* | `media/Page 23/` (3 WAVs) | **Round 23 (R23)**: Background canvas + 3 Audio recitations |
| `jpeg/eightfold 24.jpg` | *(None in original)* | `media/Page 24/` (2 WAVs) | **Round 24 (R24)**: Background canvas + 2 Audio recitations |
| `jpeg/eightfold 25.jpg` | *(None in original)* | `media/Page 25/` (1 WAV)  | **Round 25 (R25)**: Background canvas + Concluding Mangalam |

---

### C. The Avadhāna Kalā Treatise (`avdhankala.dxr` — 7 Chapters)
| Original Master Canvas | Chapter Marker in `avdhankala.dxr` | Thematic Subject | Modern Presentation |
| :--- | :--- | :--- | :--- |
| `jpeg/avdhankala01.jpg` | Chapter 1 (Page 1 of 7) | Introduction: Definition & Origins of Avadhāna | **Page 1 Canvas + Text** |
| `jpeg/avdhankala02.jpg` | Chapter 2 (Page 2 of 7) | Oral Tradition & Historical Pandits (13th–14th Century) | **Page 2 Canvas + Text** |
| `jpeg/avdhankala03.jpg` | Chapter 3 (Page 3 of 7) | Types of Avadhāna (Caturanga, Ganita, Ashtavadhana) | **Page 3 Canvas + Text** |
| `jpeg/avdhankala04.jpg` | Chapter 4 (Page 4 of 7) | Eightfold Division: Nishiddhakshari, Samasya, Dattapadi | **Page 4 Canvas + Text** |
| `jpeg/avdhankala05.jpg` | Chapter 5 (Page 5 of 7) | Rules of Metre, Word-play, and Poetic Composition | **Page 5 Canvas + Text** |
| `jpeg/avdhankala06.jpg` | Chapter 6 (Page 6 of 7) | Vyastakshari & Aprastutaprasanga (Distractions) | **Page 6 Canvas + Text** |
| `jpeg/avdhankala07.jpg` | Chapter 7 (Page 7 of 7) | The Role of Ghanta (Bell), Personality, and Conclusion | **Page 7 Canvas + Text** |

---

### D. The Concentration Treatise (`ashtavadhanam.dxr` — 6 Chapters)
| Original Master Canvas | Page Marker in `ashtavadhanam.dxr` | Thematic Subject | Modern Presentation |
| :--- | :--- | :--- | :--- |
| `jpeg/ashtava01.jpg` | Page 1 of 6 | Sri Aurobindo & The Mother on Concentration | **Page 1 Canvas + Text** |
| `jpeg/ashtava02.jpg` | Page 2 of 6 | Swami Vivekananda on the Science of Concentration | **Page 2 Canvas + Text** |
| `jpeg/ashtava03.jpg` | Page 3 of 6 | Mind Control, Willpower, and Mental Focus | **Page 3 Canvas + Text** |
| `jpeg/ashtava04.jpg` | Page 4 of 6 | Spiritual Concentration & Christ’s Teachings | **Page 4 Canvas + Text** |
| `jpeg/ashtava05.jpg` | Page 5 of 6 | Nature & Meaning of Concentration (Single-pointedness)| **Page 5 Canvas + Text** |
| `jpeg/ashtava06.jpg` | Page 6 of 6 | Yogic Postures, Meditation, and Practical Steps | **Page 6 Canvas + Text** |

---

### E. Scholars, Institutions, Society & Glimpses
| Original Master Asset | Source File | Description | Modern Presentation |
| :--- | :--- | :--- | :--- |
| `jpeg/performance.jpg` | `performance.jpg` | Historic stage photo of Dr. Ganesh and all Pracchakas on 20 Jan 1997 | **Scholars Header Banner**: Displayed prominently above biographical notes |
| `jpeg/acknowledge/back.jpg` | `acknowledge/` | Parchment background for scholar acknowledgments | **Section Canvas**: Framing the scholars & participants directory |
| `jpeg/institution/institution .jpg` | `institution/` | Sri Aurobindo Society & Pondicherry University visual | **Institutions Canvas**: Displayed at top of the Institutions section |
| `jpeg/sas/sas.jpg` | `sas/` | Sri Aurobindo Society headquarters & symbol | **Society Canvas**: Displayed at top of the Society section |
| `media/GLIMPSE1.avi` | Root `media/` | Video Glimpse 1: Dr. Ganesh's Preparation | **Glimpse 1 Player** in Glimpses Video Theater |
| `media/GLIMPSE2.avi` | Root `media/` | Video Glimpse 2: Pracchakas & The Assembly | **Glimpse 2 Player** in Glimpses Video Theater |
| `media/GLIMPSE3.avi` | Root `media/` | Video Glimpse 3: Spontaneous Verse Creation | **Glimpse 3 Player** in Glimpses Video Theater |

---

## 3. Step-by-Step Fixing Plan

```
[Fix 1: Authentic Opening]    ──► Replace dark splash card with S01-S06 animation + 01.bmp & montage.mp4
[Fix 2: Avadhana Kala Pages]  ──► Re-slice avdhankala text into 7 pages framed by avdhankala01-07.jpg
[Fix 3: Concentration Pages]  ──► Re-slice concentration text into 6 pages framed by ashtava01-06.jpg
[Fix 4: Visual Heritage]      ──► Embed performance.jpg, institution.jpg, sas.jpg, and acknowledge/back.jpg
[Fix 5: Database Refinement]  ──► Update data.js with chapter-level image associations
```

1. **Step 1: Build the Authentic Opening Sequence**:
   - When the user first visits, show the authentic title animation (`S01.jpg` fading smoothly into `S06.jpg` via CSS dissolve, displaying *"THE WONDER THAT IS SANSKRIT"*).
   - Followed by the cultural photo collage (`01.bmp`) featuring the central playback of `montage.mp4` (with play/pause/skip buttons).
   - Clicking "Enter Performance" transitions gracefully to the Main Performance Stage.
2. **Step 2: Update `generate_db.py` to Structure the Treatises by Chapter**:
   - Re-parse `avdhankala.dxr` using the `Page 1 of 7` to `Page 7 of 7` boundary markers and pair each page with its specific image (`avdhankala01.jpg` to `07.jpg`).
   - Re-parse `ashtavadhanam.dxr` using the `Page 1 of 6` to `Page 6 of 6` boundary markers and pair each page with its specific image (`ashtava01.jpg` to `06.jpg`).
3. **Step 3: Update `app.js` and `index.html` to Render the Paged Readers**:
   - In the **Avadhāna Kalā** section, render a book-style reader with page pills (`Ch 1` to `Ch 7`), previous/next navigation buttons, and the authentic colored background canvas.
   - In the **Concentration** section, render a book-style reader with page pills (`Page 1` to `Page 6`), previous/next navigation buttons, and the authentic thematic background canvas.
4. **Step 4: Embed the Photos for Scholars, Institutions, and Society**:
   - Insert `performance.jpg` into `#content-scholars` with caption.
   - Insert `institution/institution .jpg` into `#content-institutions`.
   - Insert `sas/sas.jpg` into `#content-society`.
5. **Step 5: Verify 100% Asset Utilization**:
   - Re-run `tools/gap_analysis.py` to verify that all 53 images, all 15 videos, and all 173 audio tracks register as **ACTIVE IN UI**.
