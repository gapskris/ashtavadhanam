/**
 * Ashtavadhanam Modern — Sanskrit & Devanagari Search Engine
 * Phase 10: Client-side inverted index, Devanagari normalization, IAST folding,
 * phonetic mapping, result ranking, and deep linking.
 */

class AshtavadhanamSearch {
  constructor(app) {
    this.app = app;
    this.data = window.ASHTAVADHANAM_DATA;
    this.index = [];
    this.modal = null;
    this.input = null;
    this.resultsContainer = null;
    this.currentFilter = 'all';
    this.debounceTimer = null;

    if (this.data) {
      this.buildIndex();
    }
  }

  /* ================= NORMALIZATION PIPELINE ================= */

  /**
   * Devanagari Normalization
   * Strips daṇḍas, metrical markers, homorganic nasals to anusvāra, and whitespace
   */
  normalizeDevanagari(text) {
    if (!text) return '';
    let s = text;
    // Strip metrical markers and punctuation
    s = s.replace(/[।॥,.:;!?"'\-—()[\]{}<>/\\]/g, ' ');
    // Strip avagraha and virama variations for loose matching
    s = s.replace(/ऽ/g, '');
    // Homorganic nasal ligatures before stop consonants -> anusvāra
    s = s.replace(/ङ्([क-खग-घ])/g, 'ं$1');
    s = s.replace(/ञ्([च-छज-झ])/g, 'ं$1');
    s = s.replace(/ण्([ट-ठड-ढ])/g, 'ं$1');
    s = s.replace(/न्([त-थद-ध])/g, 'ं$1');
    s = s.replace(/म्([प-फब-भ])/g, 'ं$1');
    // Collapse whitespace
    return s.replace(/\s+/g, ' ').trim().toLowerCase();
  }

  /**
   * Latin / IAST Accent Folding
   * Folds macrons, diacritics, and case
   */
  normalizeLatin(text) {
    if (!text) return '';
    return text
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/ā/gi, 'a')
      .replace(/ī/gi, 'i')
      .replace(/ū/gi, 'u')
      .replace(/[ṛṝ]/gi, 'r')
      .replace(/[ḷḹ]/gi, 'l')
      .replace(/[ṅñṇ]/gi, 'n')
      .replace(/[ṭḍ]/gi, m => m.toLowerCase() === 'ṭ' ? 't' : 'd')
      .replace(/[śṣ]/gi, 's')
      .replace(/ḥ/gi, 'h')
      .replace(/ṃ/gi, 'm')
      .replace(/[^a-z0-9\s]/gi, ' ')
      .replace(/\s+/g, ' ')
      .trim()
      .toLowerCase();
  }

  /**
   * Phonetic mapping for Roman/ASCII query matching against Devanagari text
   */
  toPhoneticKey(text) {
    if (!text) return '';
    let s = this.normalizeLatin(text);
    // Broad phonetic classes
    s = s.replace(/sh/g, 's');
    s = s.replace(/th/g, 't');
    s = s.replace(/dh/g, 'd');
    s = s.replace(/ch/g, 'c');
    s = s.replace(/kh/g, 'k');
    s = s.replace(/gh/g, 'g');
    s = s.replace(/bh/g, 'b');
    s = s.replace(/ph/g, 'p');
    s = s.replace(/[aeiou]/g, ''); // consonant skeleton
    return s;
  }

  /* ================= INDEX GENERATION ================= */

  buildIndex() {
    this.index = [];
    const speakerPat = /^(Avadhānī|Niṣiddhākṣarī|Aprastutaprasaṅga|Aprastutaprasanga|Samasyā|Dattapadī|Vyastākṣarī|The Bell|Ghaṇṭā|President|Commentator):/i;

    // 1. Index All 25 Performance Rounds
    const pages = this.data.pages || [];
    pages.forEach((p) => {
      const pnum = p.pageNumber;
      const rawSan = (p.sanskritDevanagari || '').trim();
      const rawEng = (p.englishText || '').trim();

      const sanParas = rawSan.split(/\n\n+/).map(s => s.trim()).filter(Boolean);
      const engParas = rawEng.split(/\n\n+/).map(s => s.trim()).filter(Boolean);

      const engTurns = [];
      let curEng = [];
      for (const ep of engParas) {
        if (speakerPat.test(ep) && curEng.length > 0) {
          engTurns.push(curEng.join('\n\n'));
          curEng = [ep];
        } else {
          curEng.push(ep);
        }
      }
      if (curEng.length > 0) engTurns.push(curEng.join('\n\n'));

      const audioFiles = p.audioFiles || [];
      const maxTurns = Math.max(audioFiles.length, sanParas.length, engTurns.length, 1);

      for (let i = 0; i < maxTurns; i++) {
        const san = sanParas[i] || '';
        const eng = engTurns[i] || '';
        const audio = audioFiles[i] || null;
        const speakerInfo = this.app ? this.app.detectSpeaker(san, eng) : { name: 'Assembly', cssClass: 'speaker-default' };

        this.index.push({
          id: `round_${pnum}_turn_${i}`,
          type: 'round',
          roundNumber: pnum,
          turnIndex: i,
          title: `Page ${pnum} • Turn ${i + 1}`,
          speaker: speakerInfo.name,
          speakerClass: speakerInfo.cssClass,
          sanRaw: san,
          sanNorm: this.normalizeDevanagari(san),
          sanPhonetic: this.toPhoneticKey(san),
          engRaw: eng,
          engNorm: this.normalizeLatin(eng),
          audio: audio,
          clipIndex: i,
          hasVideo: !!p.video
        });
      }
    });

    // 2. Index Treatises: Avadhana Kala (7 Chapters)
    const avadhana = this.data.treatises && this.data.treatises.avadhanaKala;
    if (avadhana && avadhana.chapters) {
      avadhana.chapters.forEach((ch, idx) => {
        const text = (ch.content || []).join('\n\n');
        this.index.push({
          id: `treatise_avadhana_${ch.chapter}`,
          type: 'treatise',
          treatiseKey: 'avadhanaKala',
          chapterIndex: idx,
          title: `Avadhana Kalā • Chapter ${ch.chapter}: ${ch.title}`,
          speaker: '📜 Avadhana Kalā Treatise',
          speakerClass: 'speaker-president',
          sanRaw: text,
          sanNorm: this.normalizeDevanagari(text),
          sanPhonetic: this.toPhoneticKey(text),
          engRaw: ch.title,
          engNorm: this.normalizeLatin(ch.title),
          audio: null
        });
      });
    }

    // 3. Index Treatises: Concentration (6 Pages)
    const conc = this.data.treatises && this.data.treatises.concentration;
    if (conc && conc.pages) {
      conc.pages.forEach((pg, idx) => {
        const text = (pg.content || []).join('\n\n');
        this.index.push({
          id: `treatise_concentration_${pg.page}`,
          type: 'treatise',
          treatiseKey: 'concentration',
          chapterIndex: idx,
          title: `Concentration • Page ${pg.page}: ${pg.title}`,
          speaker: '🧘 Concentration Treatise',
          speakerClass: 'speaker-president',
          sanRaw: text,
          sanNorm: this.normalizeDevanagari(text),
          sanPhonetic: this.toPhoneticKey(text),
          engRaw: pg.title,
          engNorm: this.normalizeLatin(pg.title),
          audio: null
        });
      });
    }

    // 4. Index Scholars & Participants (Credits)
    const cred = this.data.credits;
    if (cred && cred.participants) {
      cred.participants.forEach((pt, idx) => {
        this.index.push({
          id: `participant_${idx}`,
          type: 'scholar',
          title: `Scholar • ${pt.role}`,
          speaker: pt.role,
          speakerClass: 'speaker-avadhani',
          sanRaw: pt.name,
          sanNorm: this.normalizeDevanagari(pt.name),
          sanPhonetic: this.toPhoneticKey(pt.name),
          engRaw: `${pt.role}: ${pt.name}`,
          engNorm: this.normalizeLatin(`${pt.role}: ${pt.name}`),
          audio: null
        });
      });
    }
  }

  /* ================= SEARCH & RANKING ALGORITHM ================= */

  search(query, filterCategory = 'all') {
    if (!query || query.trim().length === 0) {
      return [];
    }

    const qRaw = query.trim();
    const isDevanagari = /[\u0900-\u097F]/.test(qRaw);
    const qSanNorm = this.normalizeDevanagari(qRaw);
    const qEngNorm = this.normalizeLatin(qRaw);
    const qPhonetic = this.toPhoneticKey(qRaw);

    const matches = [];

    for (const doc of this.index) {
      // Filter Category Check
      if (filterCategory !== 'all') {
        if (filterCategory === 'rounds' && doc.type !== 'round') continue;
        if (filterCategory === 'treatises' && doc.type !== 'treatise') continue;
        if (filterCategory === 'scholars' && doc.type !== 'scholar') continue;
      }

      let score = 0;
      let matchField = '';
      let matchText = '';

      if (isDevanagari) {
        // Devanagari Search
        if (doc.sanRaw && doc.sanRaw.includes(qRaw)) {
          score += 100;
          matchField = 'san';
          matchText = doc.sanRaw;
        } else if (doc.sanNorm && doc.sanNorm.includes(qSanNorm)) {
          score += 80;
          matchField = 'san';
          matchText = doc.sanRaw;
        }
      } else {
        // Latin / English / Phonetic Search
        if (doc.engNorm && doc.engNorm.includes(qEngNorm)) {
          score += 85;
          matchField = 'eng';
          matchText = doc.engRaw;
        } else if (doc.sanNorm && qSanNorm && doc.sanNorm.includes(qSanNorm)) {
          score += 75;
          matchField = 'san';
          matchText = doc.sanRaw;
        } else if (doc.speaker && this.normalizeLatin(doc.speaker).includes(qEngNorm)) {
          score += 65;
          matchField = 'speaker';
          matchText = doc.speaker;
        } else if (doc.sanPhonetic && qPhonetic.length >= 3 && doc.sanPhonetic.includes(qPhonetic)) {
          score += 35;
          matchField = 'san';
          matchText = doc.sanRaw;
        }
      }

      if (score > 0) {
        matches.push({
          doc,
          score,
          matchField,
          snippet: this.generateSnippet(matchText || doc.sanRaw || doc.engRaw, qRaw)
        });
      }
    }

    // Sort by descending score
    matches.sort((a, b) => b.score - a.score);
    return matches.slice(0, 30); // Top 30 matches
  }

  generateSnippet(text, query) {
    if (!text) return '';
    const cleanText = text.replace(/\s+/g, ' ');
    const lowerText = cleanText.toLowerCase();
    const lowerQuery = query.toLowerCase().trim();

    let idx = lowerText.indexOf(lowerQuery);
    if (idx === -1) {
      // Try accent-folded match index
      const normText = this.normalizeLatin(cleanText);
      const normQuery = this.normalizeLatin(query);
      idx = normText.indexOf(normQuery);
    }

    if (idx === -1) {
      return cleanText.slice(0, 160) + (cleanText.length > 160 ? '...' : '');
    }

    const start = Math.max(0, idx - 40);
    const end = Math.min(cleanText.length, idx + query.length + 80);
    const rawSnippet = (start > 0 ? '...' : '') + cleanText.slice(start, end) + (end < cleanText.length ? '...' : '');

    // Highlight query safely
    const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    try {
      const regex = new RegExp(`(${escapedQuery})`, 'gi');
      return rawSnippet.replace(regex, '<mark class="search-highlight">$1</mark>');
    } catch (e) {
      return rawSnippet;
    }
  }

  /* ================= UI CONTROLLER ================= */

  initUI() {
    this.modal = document.getElementById('search-modal');
    this.input = document.getElementById('search-input');
    this.resultsContainer = document.getElementById('search-results');
    const btnOpen = document.getElementById('btn-search');
    const btnClose = document.getElementById('btn-close-search');
    const backdrop = document.getElementById('search-modal-backdrop');

    if (btnOpen) {
      btnOpen.addEventListener('click', () => this.open());
    }
    if (btnClose) {
      btnClose.addEventListener('click', () => this.close());
    }
    if (backdrop) {
      backdrop.addEventListener('click', () => this.close());
    }

    // Keyboard Shortcuts: '/' or 'Ctrl+K'
    document.addEventListener('keydown', (e) => {
      if ((e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') ||
          (e.key === 'k' && (e.ctrlKey || e.metaKey))) {
        e.preventDefault();
        this.open();
      } else if (e.key === 'Escape' && this.modal && !this.modal.classList.contains('hidden')) {
        this.close();
      }
    });

    // Input Debouncing
    if (this.input) {
      this.input.addEventListener('input', (e) => {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
          this.executeSearch(e.target.value);
        }, 150);
      });
    }

    // Filter Chips
    const chips = document.querySelectorAll('.search-filter-chip');
    chips.forEach(chip => {
      chip.addEventListener('click', (e) => {
        chips.forEach(c => c.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.currentFilter = e.currentTarget.dataset.filter || 'all';
        if (this.input) {
          this.executeSearch(this.input.value);
        }
      });
    });
  }

  open() {
    if (!this.modal) return;
    this.modal.classList.remove('hidden');
    if (this.input) {
      this.input.value = '';
      setTimeout(() => this.input.focus(), 80);
    }
    if (this.resultsContainer) {
      this.resultsContainer.innerHTML = '<div class="search-empty-state">Type a Sanskrit word, English topic, or scholar name to search all 25 rounds and treatises...</div>';
    }
  }

  close() {
    if (!this.modal) return;
    this.modal.classList.add('hidden');
  }

  executeSearch(query) {
    if (!this.resultsContainer) return;
    const q = query.trim();
    if (q.length === 0) {
      this.resultsContainer.innerHTML = '<div class="search-empty-state">Type a Sanskrit word, English topic, or scholar name to search all 25 rounds and treatises...</div>';
      return;
    }

    const results = this.search(q, this.currentFilter);
    if (results.length === 0) {
      this.resultsContainer.innerHTML = `
        <div class="search-empty-state">
          No matches found for "<strong>${q}</strong>".<br>
          <span style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px; display: inline-block;">
            Try typing in Devanagari (e.g. समस्या), Roman transliteration (e.g. Samasya), or English keywords (e.g. riddle, bell, cobbler).
          </span>
        </div>
      `;
      return;
    }

    this.resultsContainer.innerHTML = results.map((res, idx) => {
      const doc = res.doc;
      let playBtnHtml = '';
      if (doc.type === 'round' && doc.audio) {
        playBtnHtml = `<button class="search-action-btn search-play-btn" data-round="${doc.roundNumber}" data-clip="${doc.clipIndex}" title="Play audio recitation">▶ Listen</button>`;
      }

      let jumpBtnHtml = '';
      if (doc.type === 'round') {
        jumpBtnHtml = `<button class="search-action-btn search-jump-btn" data-round="${doc.roundNumber}" data-turn="${doc.turnIndex}">📖 Jump to Verse</button>`;
      } else if (doc.type === 'treatise') {
        jumpBtnHtml = `<button class="search-action-btn search-jump-btn" data-treatise="${doc.treatiseKey}" data-chapter="${doc.chapterIndex}">📜 View Chapter</button>`;
      } else if (doc.type === 'scholar') {
        jumpBtnHtml = `<button class="search-action-btn search-jump-btn" data-section="acknowledgments">🏛️ View in Credits</button>`;
      }

      return `
        <div class="search-result-card" data-idx="${idx}">
          <div class="search-result-header">
            <span class="search-result-title">${doc.title}</span>
            <span class="speaker-badge ${doc.speakerClass}">${doc.speaker}</span>
          </div>
          <div class="search-result-snippet">${res.snippet}</div>
          <div class="search-result-actions">
            ${jumpBtnHtml}
            ${playBtnHtml}
          </div>
        </div>
      `;
    }).join('');

    // Attach Action Listeners
    this.resultsContainer.querySelectorAll('.search-jump-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.close();
        if (btn.dataset.round) {
          const rNum = parseInt(btn.dataset.round, 10);
          const tIdx = parseInt(btn.dataset.turn, 10);
          if (this.app) {
            this.app.navigateToPage(rNum, false);
            setTimeout(() => {
              const card = document.querySelector(`.dialogue-card[data-index="${tIdx}"]`);
              if (card) {
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                card.classList.add('search-target-pulse');
                setTimeout(() => card.classList.remove('search-target-pulse'), 2500);
              }
            }, 300);
          }
        } else if (btn.dataset.treatise) {
          const tKey = btn.dataset.treatise;
          const cIdx = parseInt(btn.dataset.chapter, 10);
          if (this.app) {
            this.app.navigateToSection(tKey);
            if (tKey === 'avadhanaKala') this.app.showAvadhanaChapter(cIdx);
            if (tKey === 'concentration') this.app.showConcentrationPage(cIdx);
          }
        } else if (btn.dataset.section) {
          if (this.app) this.app.navigateToSection(btn.dataset.section);
        }
      });
    });

    this.resultsContainer.querySelectorAll('.search-play-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.close();
        const rNum = parseInt(btn.dataset.round, 10);
        const cIdx = parseInt(btn.dataset.clip, 10);
        if (this.app) {
          this.app.navigateToPage(rNum, false);
          setTimeout(() => {
            if (window.Player) window.Player.playClip(cIdx);
          }, 350);
        }
      });
    });
  }
}

window.AshtavadhanamSearch = AshtavadhanamSearch;
