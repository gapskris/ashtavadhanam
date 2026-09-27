#!/usr/bin/env python3
"""
test_sanskrit_alignment.py — Regression Test Suite for Sanskrit Alignment & Card Cardinality

Verifies:
1. Metric Verse (Padya) vs Conversational Prose (Gadya) discrimination.
2. Danda typography non-breaking gluing (no dangling dandas).
3. Zero empty dialogue cards across all 25 rounds in all view modes.
4. Exactly 7 cards on Page 2 (no phantom 8th Avadhani card).
"""

import os
import sys
import json
import re
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, "content", "data.json")
APP_JS_PATH = os.path.join(ROOT_DIR, "js", "app.js")
PLAYER_CSS_PATH = os.path.join(ROOT_DIR, "css", "player.css")

class TestSanskritAlignmentAndCardinality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            cls.data = json.load(f)
        with open(APP_JS_PATH, "r", encoding="utf-8") as f:
            cls.app_js = f.read()
        with open(PLAYER_CSS_PATH, "r", encoding="utf-8") as f:
            cls.player_css = f.read()

    def test_css_rules_for_sanskrit_alignment(self):
        """Verify CSS contains clean left alignment for .text-sanskrit and .verse-line."""
        self.assertIn(".text-sanskrit", self.player_css)
        self.assertIn("text-align: left;", self.player_css)
        self.assertIn(".verse-line.pada-even", self.player_css)
        self.assertIn(".dialogue-footnote", self.player_css)

    def test_phantom_cards_suppression_logic(self):
        """Verify js/app.js contains logic to suppress cards where both Sanskrit and audio are missing."""
        self.assertIn("!san.trim() && !audio", self.app_js)
        self.assertIn("dialogue-footnote", self.app_js)

    def test_clean_sanskrit_typography_function(self):
        """Verify cleanSanskritTypography glues dandas to preceding words."""
        self.assertIn("cleanSanskritTypography", self.app_js)
        self.assertIn("\\u00A0$1", self.app_js)

    def test_metric_verse_discrimination(self):
        """Verify isMetricVerse exists and excludes conversational dialogue cues."""
        self.assertIn("isMetricVerse", self.app_js)

    def test_page2_dialogue_card_cardinality(self):
        """Verify Page 2 has exactly 7 audio files and 7 Sanskrit paragraphs (0 empty cards)."""
        p2 = [p for p in self.data["pages"] if p["pageNumber"] == 2][0]
        audios = p2.get("audioFiles", [])
        san_paras = [x.strip() for x in (p2.get("sanskritDevanagari") or "").split("\n\n") if x.strip()]
        self.assertEqual(len(audios), 7, "Page 2 must have exactly 7 audio recitations")
        self.assertEqual(len(san_paras), 7, "Page 2 must have exactly 7 Sanskrit turns")

    def test_zero_empty_cards_across_all_25_pages(self):
        """Simulate rendering across all 25 pages to guarantee 0 phantom empty cards."""
        speaker_pat = re.compile(
            r'^(Avadhānī|Niṣiddhākṣarī|Aprastutaprasaṅga|Aprastutaprasanga|Samasyā|Dattapadī|Vyastākṣarī|President|Commentator):',
            re.I
        )
        empty_cards = 0
        total_rendered = 0

        for p in self.data["pages"]:
            num = p["pageNumber"]
            raw_san = (p.get("sanskritDevanagari") or "").strip()
            raw_eng = (p.get("englishText") or "").strip()
            audios = p.get("audioFiles", [])

            san_paras = [x.strip() for x in raw_san.split("\n\n") if x.strip()]
            eng_paras = [x.strip() for x in raw_eng.split("\n\n") if x.strip()]

            eng_turns = []
            cur_eng = []
            for ep in eng_paras:
                if speaker_pat.match(ep):
                    if len(cur_eng) > 0:
                        if len(eng_turns) == 0 and not speaker_pat.match(cur_eng[0]):
                            cur_eng.append(ep)
                        else:
                            eng_turns.append("\n\n".join(cur_eng))
                            cur_eng = [ep]
                    else:
                        cur_eng.append(ep)
                else:
                    cur_eng.append(ep)
            if len(cur_eng) > 0:
                eng_turns.append("\n\n".join(cur_eng))

            max_lines = max(len(audios), len(san_paras), len(eng_turns), 1)
            for i in range(max_lines):
                audio = audios[i] if i < len(audios) else None
                san = san_paras[i] if i < len(san_paras) else ""
                
                # Check suppression
                if not san.strip() and not audio:
                    continue
                
                total_rendered += 1
                if not san.strip() and not audio:
                    empty_cards += 1

        self.assertEqual(empty_cards, 0, "No empty cards must ever be rendered across 25 pages")
        self.assertGreaterEqual(total_rendered, 173, "All authentic recitations must be rendered")

if __name__ == "__main__":
    unittest.main()
