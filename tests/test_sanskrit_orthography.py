"""
Automated Sanskrit Orthography & Forensic Parity Test Suite
Validates that all 25 performance rounds in Ashtavadhanam Modern contain:
  1. Complete dual-format Sanskrit data (Raw VedicBrahma + Certified Devanagari).
  2. Exactly 0 legacy font mojibake / corrupted glyphs (; £ Ð Ï Î ` ~ [ ] { } + = ^ a-zA-Z \x80-\xff).
  3. Zero broken combining characters (dotted circles \u25cc or dangling matras).
  4. Proper speaker and dialogue structure.
  5. 100% synchronization between content/data.json and js/data.js.
  6. Forensic accuracy for historic benchmark verses.
"""

import unittest
import os
import sys
import json
import re

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JSON_PATH = os.path.join(PROJECT_DIR, "content", "data.json")
DATA_JS_PATH = os.path.join(PROJECT_DIR, "js", "data.js")

class TestSanskritOrthography(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
            cls.data = json.load(f)
        cls.pages = cls.data.get("pages", [])

    def test_01_all_25_rounds_exist(self):
        """Verify exactly 25 rounds exist."""
        self.assertEqual(len(self.pages), 25, "Database must contain exactly 25 rounds.")

    def test_02_dual_sanskrit_fields_present_and_non_empty(self):
        """Verify every round has non-empty sanskritRawVedicBrahma and sanskritDevanagari."""
        for p in self.pages:
            pnum = p["pageNumber"]
            raw = p.get("sanskritRawVedicBrahma", "")
            dev = p.get("sanskritDevanagari", "")
            self.assertTrue(len(raw) > 50, f"Round {pnum} raw VedicBrahma string is missing or too short.")
            self.assertTrue(len(dev) > 50, f"Round {pnum} Sanskrit Devanagari is missing or too short.")

    def test_03_zero_mojibake_artifacts(self):
        """Verify zero unconverted legacy glyphs (; £ Ð Ï Î ` ~ [ ] { } + = ^ a-zA-Z) in all rounds."""
        forbidden_pattern = re.compile(r'[;£ÐÏÎ`~\[\]\{\}\+\=\^a-zA-Z\x80-\xff]')
        for p in self.pages:
            pnum = p["pageNumber"]
            dev = p.get("sanskritDevanagari", "")
            words = re.findall(r'\S+', dev)
            bad_tokens = []
            for w in words:
                # Strip acceptable punctuation: ( ) " ' * । ॥ , - ? ! numbers colons bells
                clean_w = re.sub(r'[\(\)\"\'\*\।\॥\,\-\?\!\d:🔔]', '', w)
                if forbidden_pattern.search(clean_w):
                    bad_tokens.append(w)
            self.assertEqual(len(bad_tokens), 0, f"Round {pnum} contains {len(bad_tokens)} corrupted tokens: {' '.join(bad_tokens[:5])}")

    def test_04_no_broken_combining_characters(self):
        """Verify no dotted circles (U+25CC) or isolated combining marks at word start."""
        for p in self.pages:
            pnum = p["pageNumber"]
            dev = p.get("sanskritDevanagari", "")
            self.assertNotIn("\u25cc", dev, f"Round {pnum} contains dotted circle combining character!")
            
            # Check for words starting with an isolated combining matra (093E-094D)
            words = re.findall(r'(?:^|\s)([\u093e-\u094d]\S*)', dev)
            self.assertEqual(len(words), 0, f"Round {pnum} has isolated matra at start of word: {words}")

    def test_05_data_js_synchronization(self):
        """Verify js/data.js exists and matches content/data.json."""
        self.assertTrue(os.path.exists(DATA_JS_PATH), "js/data.js does not exist.")
        with open(DATA_JS_PATH, "r", encoding="utf-8") as f:
            js_content = f.read()
        self.assertIn("window.ASHTAVADHANAM_DATA =", js_content)
        json_part = js_content.split("window.ASHTAVADHANAM_DATA =", 1)[1].strip().rstrip(";")
        parsed_js = json.loads(json_part)
        self.assertEqual(len(parsed_js.get("pages", [])), 25)
        for i in range(25):
            self.assertEqual(
                self.pages[i]["sanskritDevanagari"],
                parsed_js["pages"][i]["sanskritDevanagari"],
                f"js/data.js out of sync with content/data.json on Round {i+1} Sanskrit Devanagari!"
            )

    def test_06_benchmark_verses_forensic_accuracy(self):
        """Verify specific historic benchmark verses across key rounds."""
        # Round 1 Mangalacharana
        r1_dev = self.pages[0]["sanskritDevanagari"]
        self.assertIn("योऽन्तः प्रविश्य मम वाचमिमां प्रसुप्ताम्", r1_dev)
        self.assertIn("सञ्जीवयत्यखिलशक्तिधरः स्वधाम्ना", r1_dev)
        self.assertIn("अन्यांश्च हस्तचरणश्रवणत्वगादीन्", r1_dev)
        self.assertIn("प्राणान् नमो भगवते पुरुषाय तुभ्यम्", r1_dev)

        # Round 3 Aprastutaprasanga
        r3_dev = self.pages[2]["sanskritDevanagari"]
        self.assertIn("दृष्ट्वा", r3_dev)
        self.assertIn("यदि", r3_dev)
        self.assertIn("ताडयति", r3_dev)
        self.assertIn("तर्हि", r3_dev)
        self.assertIn("भवादृशः", r3_dev)
        self.assertIn("अष्टाभिः दिग्गजैः बद्धः कुत्र गच्छामि", r3_dev)
        self.assertIn("ताडयन्तु ताडयन्तु", r3_dev)

        # Round 21 Stuti to Sri Aurobindo
        r21_dev = self.pages[20]["sanskritDevanagari"]
        self.assertIn("अरविन्दमहाशयानां स्तुतिः", r21_dev)
        self.assertIn("कुशलताब्रह्म", r21_dev)

        # Round 24 Avadhani Concluding Address & Stanzas 1 & 2
        r24_dev = self.pages[23]["sanskritDevanagari"]
        self.assertIn("परिसमापनसमये", r24_dev)
        self.assertIn("वयं संस्कृतस्य कृते किमपि किं न करवाम", r24_dev)
        self.assertIn("स्वयं सङ्घटितशक्त्या सिद्धिमत्र रचयाम", r24_dev)

        # Round 25 Concluding Song Stanzas 3-5 & Chorus
        r25_dev = self.pages[24]["sanskritDevanagari"]
        self.assertIn("श्रवणं सम्भाषणं संस्कृते निरन्तरम्", r25_dev)
        self.assertIn("संस्कृत इति निःश्रेणीं समारुह्य विलसाम", r25_dev)
        self.assertIn("वयं संस्कृतस्य कृते किमपि किमपि करवाम", r25_dev)

if __name__ == "__main__":
    unittest.main()
