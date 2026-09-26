import struct, os, re, json, sys

SRC_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_master"
MODERN_DIR = r"C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"

sys.path.append(os.path.join(MODERN_DIR, "tools"))
from krutidev_decoder import krutidev_to_devanagari
from sanskrit_cleaner import clean_sanskrit_text

def parse_chunks(path):
    if not os.path.exists(path): return []
    with open(path, "rb") as f:
        data = f.read()
    magic = data[:4]
    endian = '<' if magic == b'XFIR' else '>'
    pos = 12
    chunks = []
    while pos < len(data) - 8:
        tag = data[pos:pos+4][::-1].decode('latin1', errors='replace')
        size = struct.unpack(f"{endian}I", data[pos+4:pos+8])[0]
        chunks.append((pos, tag, size, data[pos+8:pos+8+size]))
        pos += 8 + size + (size % 2)
    return chunks

def extract_xmed_texts(chunks):
    results = []
    for i, (pos, tag, size, cdata) in enumerate(chunks):
        if tag == 'XMED':
            m = re.search(rb'00020000[0-9A-Fa-f]{8}', cdata)
            if m:
                sub = cdata[m.end():]
                m_end = re.search(rb'\x0300040000', sub)
                raw = sub[:m_end.start()] if m_end else sub[:3000]
                text_clean = re.sub(rb'^[^\x20-\xff\r\n]+', b'', raw)
                t = text_clean.decode('latin1', errors='replace')
                t = re.sub(r'^[\x00-\x1f\s]+', '', t.strip())
                t = re.sub(r'^[0-9A-Fa-f\x00\s]+,\s*', '', t)
                t = re.sub(r'0000[0-9A-Fa-f\x00\s]+,\s*', '', t)
                t = re.sub(r'^[\x00-\x1f\s]+', '', t)
                if len(t) > 5 and not t.startswith(';'):
                    results.append((i, t))
    return results

def clean_iast(text):
    t = text.replace('\r\n', '\n').replace('\r', '\n')
    # Smart quotes and dashes
    t = t.replace('\x91', "'").replace('\x92', "'").replace('\x93', '"').replace('\x94', '"').replace('\x96', '-').replace('\x97', '—')
    # Palatino-RomanDiac letter mappings
    diac_map = [
        ('AvadhDni', 'Avadhānī'),
        ('AvadhDna', 'Avadhāna'),
        ('avadhDna', 'avadhāna'),
        ('AvadhDnn', 'Avadhānī'),
        ('NishidhDkshari', 'Niṣiddhākṣarī'),
        ('NishidhDkshar', 'Niṣiddhākṣarī'),
        ('VyastDkshari', 'Vyastākṣarī'),
        ('SamasyD', 'Samasyā'),
        ('Dattapadn', 'Dattapadī'),
        ('Dattapadi', 'Dattapadī'),
        ('VarnanD', 'Varṇanā'),
        ('GhaKFD', 'Ghaṇṭā'),
        ('ghaKFD', 'ghaṇṭā'),
        ('pDda', 'pāda'),
        ('pDdas', 'pādas'),
        ('Qloka', 'śloka'),
        ('shloka', 'śloka'),
        ('ShDrdulavikridita', 'Śārdūlavikrīḍita'),
        ('MDlini', 'Mālinī'),
        ('MDnini', 'Māninī'),
        ('RDmDyana', 'Rāmāyaṇa'),
        ('PrDnDyDma', 'Prāṇāyāma'),
        ('PratyDh', 'Pratyāh'),
        ('amartyDtmD', 'amartyātmā'),
        ('charmakDra', 'carmakāra'),
        ('chamatkDra', 'camatkāra'),
        ('chamatkDrakDra', 'camatkārakāra'),
        ('svacchandavrittena', 'svacchandavṛttena'),
        ('vibudhD', 'vibudhā'),
        ('prDmshu', 'prāṃśu'),
        ('pDla', 'pāla'),
        ('prDmshupDla', 'prāṃśupāla'),
        ('PrabhDkara', 'Prabhākara'),
        ('AshFDvadhDna', 'Aṣṭāvadhāna'),
        ('AshFDvadhDnn', 'Aṣṭāvadhānī'),
        ('QDtavadhDna', 'Śatāvadhāna'),
        ('sahasrDvadhDna', 'Sahasrāvadhāna'),
        ('kavitvDvadhDna', 'kavitvāvadhāna'),
        ('SaOgntDvdhDna', 'Saṅgītāvadhāna'),
        ('KavitvDvadhDna', 'Kavitvāvadhāna'),
        ('prDcnnayuga', 'prācīnayuga'),
        ('madhyayuga', 'madhyayuga'),
        ('navyayuga', 'navyayuga'),
    ]
    for k, v in diac_map:
        t = t.replace(k, v)
    t = re.sub(r'0000[0-9A-Fa-f\x00\s]+,\s*', '', t)
    return t.strip()

# Video mapping for specific pages
PAGE_VIDEOS = {
    2: "02A.mp4",
    3: "03A.mp4",
    4: "04A.mp4",
    6: "06A.mp4",
    7: "07A.mp4",
    8: "08A.mp4",
    9: "09A.mp4",
    11: "11A.mp4",
    12: "12A.mp4",
    13: "13A.mp4",
    15: "15A.mp4"
}

def build_database():
    print("Parsing Director files...")
    chs_eng = parse_chunks(os.path.join(SRC_DIR, "eightfold.dxr"))
    chs_san = parse_chunks(os.path.join(SRC_DIR, "eightfold(s).dxr"))
    
    eng_texts = extract_xmed_texts(chs_eng)
    san_texts = extract_xmed_texts(chs_san)
    
    # Slice texts by Page markers
    pages_data = []
    
    # Find page marker indices in eng_texts
    page_splits = []
    for idx, (c_idx, txt) in enumerate(eng_texts):
        m = re.search(r'Page\s+(\d+)\s+of\s+25', txt)
        if m:
            page_splits.append((int(m.group(1)), idx))
            
    print(f"Detected {len(page_splits)} page boundary markers.")
    
    # Corresponding audio files in Ashtavadhanam_modern/assets/audio/Page X/
    for i, (pnum, split_idx) in enumerate(page_splits):
        # The dialogue texts for this page are between the previous split and this split
        prev_idx = page_splits[i-1][1] if i > 0 else 0
        
        # English snippets for this page (stripping chunk header prefixes)
        eng_snippets = []
        for t in eng_texts[prev_idx:split_idx]:
            if 'Page ' in t[1]: continue
            cleaned_t = re.sub(r'^[\x00-\x1f\s]+', '', t[1].strip())
            cleaned_t = re.sub(r'^[0-9A-Fa-f\x00\s]+,\s*', '', cleaned_t)
            cleaned_t = re.sub(r'0000[0-9A-Fa-f\x00\s]+,\s*', '', cleaned_t)
            cleaned_t = re.sub(r'^[\x00-\x1f\s]+', '', cleaned_t)
            cleaned_t = clean_iast(cleaned_t)
            if cleaned_t: eng_snippets.append(cleaned_t)

        # Sanskrit snippets for this page
        san_snippets = []
        for t in san_texts[prev_idx:split_idx]:
            if 'Page ' in t[1]: continue
            cleaned_s = clean_sanskrit_text(t[1])
            if cleaned_s: san_snippets.append(cleaned_s)
        
        # Audio directory
        audio_page_dir = os.path.join(MODERN_DIR, "assets", "audio", f"Page {pnum}")
        audio_files = []
        if os.path.exists(audio_page_dir):
            def sort_key(fn):
                m = re.search(r'pg\d+wav(\d+)', fn)
                return int(m.group(1)) if m else 999
            
            m4as = sorted([f for f in os.listdir(audio_page_dir) if f.endswith('.m4a')], key=sort_key)
            for m4a in m4as:
                base = os.path.splitext(m4a)[0]
                audio_files.append({
                    "id": base,
                    "m4a": f"assets/audio/Page {pnum}/{base}.m4a",
                    "mp3": f"assets/audio/Page {pnum}/{base}.mp3"
                })
                
        # Join snippets and split into speaker dialogues
        full_eng = "\n\n".join(eng_snippets)
        full_san = "\n\n".join(san_snippets)
        
        # Assign video if available
        video_file = PAGE_VIDEOS.get(pnum)
        
        page_obj = {
            "pageNumber": pnum,
            "title": f"Round / Page {pnum}",
            "canvas": f"assets/images/eightfold {pnum:02d}.jpg",
            "video": f"assets/video/{video_file}" if video_file else None,
            "audioCount": len(audio_files),
            "audioFiles": audio_files,
            "englishText": full_eng,
            "sanskritDevanagari": full_san
        }
        pages_data.append(page_obj)

    # Educational essays
    print("Extracting educational treatises and essays...")
    
    # 1. Avadhana Kala (7 Chapters with avdhankala01-07.jpg)
    chs_avdh = parse_chunks(os.path.join(SRC_DIR, "avdhankala.dxr"))
    raw_avdh = extract_xmed_texts(chs_avdh)
    avdh_pages = []
    cur_avdh = []
    ch_num = 1
    for _, txt in raw_avdh:
        m = re.search(r'Page\s+(\d+)\s+of\s+7', txt)
        if m:
            if cur_avdh:
                avdh_pages.append({
                    "chapter": ch_num,
                    "title": f"Chapter {ch_num} of 7",
                    "canvas": f"assets/images/avdhankala{ch_num:02d}.jpg",
                    "content": cur_avdh
                })
                ch_num += 1
                cur_avdh = []
        else:
            cleaned = clean_iast(txt).strip()
            if cleaned and not cleaned.startswith('AvadhDnakalD'):
                cur_avdh.append(cleaned)
    if cur_avdh and ch_num <= 7:
        avdh_pages.append({
            "chapter": ch_num,
            "title": f"Chapter {ch_num} of 7",
            "canvas": f"assets/images/avdhankala{ch_num:02d}.jpg",
            "content": cur_avdh
        })

    # 2. Concentration (6 Pages with ashtava01-06.jpg)
    chs_ash = parse_chunks(os.path.join(SRC_DIR, "ashtavadhanam.dxr"))
    raw_ash = extract_xmed_texts(chs_ash)
    ash_pages = []
    cur_ash = []
    pg_num = 1
    for _, txt in raw_ash:
        m = re.search(r'Page\s+(\d+)\s+of\s+6', txt)
        if m:
            if cur_ash:
                ash_pages.append({
                    "page": pg_num,
                    "title": f"Page {pg_num} of 6",
                    "canvas": f"assets/images/ashtava{pg_num:02d}.jpg",
                    "content": cur_ash
                })
                pg_num += 1
                cur_ash = []
        else:
            cleaned = clean_iast(txt).strip()
            if cleaned and not cleaned.startswith('Concentration: Its Importance'):
                cur_ash.append(cleaned)
    if cur_ash and pg_num <= 6:
        ash_pages.append({
            "page": pg_num,
            "title": f"Page {pg_num} of 6",
            "canvas": f"assets/images/ashtava{pg_num:02d}.jpg",
            "content": cur_ash
        })
    
    # 3. Performance & Scholars
    chs_perf = parse_chunks(os.path.join(SRC_DIR, "performance.dxr"))
    perf_texts = [clean_iast(t[1]) for t in extract_xmed_texts(chs_perf)]
    
    # 4. Institutions
    chs_inst = parse_chunks(os.path.join(SRC_DIR, "institu.cxt"))
    inst_texts = [clean_iast(t[1]) for t in extract_xmed_texts(chs_inst)]
    
    # 5. Sri Aurobindo Society
    chs_sas = parse_chunks(os.path.join(SRC_DIR, "sas.cxt"))
    sas_texts = [clean_iast(t[1]) for t in extract_xmed_texts(chs_sas)]
    
    # 6. Glimpses
    glimpses = [
        {
            "id": 1,
            "title": "Glimpse 1 — Opening & Invocations",
            "video": "assets/video/GLIMPSE1.mp4",
            "description": "Highlights of the commencement of the Ashtavadhanam and initial invocatory recitations."
        },
        {
            "id": 2,
            "title": "Glimpse 2 — Rounds & Distractions",
            "video": "assets/video/GLIMPSE2.mp4",
            "description": "Demonstrations of simultaneous poetic composition amid the humorous interruptions of the Aprastutaprasanga."
        },
        {
            "id": 3,
            "title": "Glimpse 3 — Completion & Benediction",
            "video": "assets/video/GLIMPSE3.mp4",
            "description": "Concluding verses, full shloka recitals from memory, and the final remarks of the President and scholars."
        }
    ]

    # 7. Opening Sequence & Historical Assets
    opening_data = {
        "title": "Opening Sequence",
        "titleAnimation": [
            "assets/images/opening/S01.jpg",
            "assets/images/opening/S02.jpg",
            "assets/images/opening/S03.jpg",
            "assets/images/opening/S04.jpg",
            "assets/images/opening/S05.jpg",
            "assets/images/opening/S06.jpg"
        ],
        "mosaicCanvas": "assets/images/opening/01.jpg",
        "montageVideo": "assets/video/montage.mp4",
        "supplementaryCanvases": [
            "assets/images/opening/02.jpg",
            "assets/images/opening/03.jpg"
        ]
    }

    master_db = {
        "metadata": {
            "title": "Ashtavadhanam — The Wonder that is Sanskrit",
            "eventDate": "20th January 1997",
            "location": "Sri Aurobindo Society Beach Office, Pondicherry",
            "organizers": ["Sri Aurobindo Society", "Department of Sanskrit, Pondicherry University"],
            "totalPerformancePages": 25,
            "totalVideos": 15,
            "totalAudioTracks": 173
        },
        "opening": opening_data,
        "pages": pages_data,
        "treatises": {
            "avadhanaKala": {
                "title": "Avadhanakala — The Art of Concentration",
                "chapters": avdh_pages,
                "content": [p for page in avdh_pages for p in page["content"]]
            },
            "concentration": {
                "title": "Concentration: Its Importance & Value",
                "pages": ash_pages,
                "content": [p for page in ash_pages for p in page["content"]]
            },
            "performanceDetails": {
                "title": "The Historic Performance & Scholars",
                "image": "assets/images/performance.jpg",
                "backgroundImage": "assets/images/acknowledge/back.jpg",
                "content": perf_texts
            },
            "institutions": {
                "title": "Participating Sanskrit Institutions",
                "image": "assets/images/institution/institution .jpg",
                "content": inst_texts
            },
            "sriAurobindoSociety": {
                "title": "Sri Aurobindo Society",
                "image": "assets/images/sas/sas.jpg",
                "content": sas_texts
            }
        },
        "glimpses": glimpses
    }

    # Write JS file
    js_path = os.path.join(MODERN_DIR, "js", "data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// Ashtavadhanam Modernized Master Database\n")
        f.write("window.ASHTAVADHANAM_DATA = ")
        json.dump(master_db, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print(f"Generated {js_path} (size {os.path.getsize(js_path)} bytes)")

    # Also write JSON in content/
    content_dir = os.path.join(MODERN_DIR, "content")
    os.makedirs(content_dir, exist_ok=True)
    json_path = os.path.join(content_dir, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(master_db, f, ensure_ascii=False, indent=2)
    print(f"Generated {json_path} (size {os.path.getsize(json_path)} bytes)")

if __name__ == "__main__":
    build_database()
