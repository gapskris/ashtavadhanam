"""
Unit Test Suite for the 7 UI & Navigation Refinements
"""
import unittest
import os
import re

class TestUIRefinements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.html_path = os.path.join(base_dir, 'index.html')
        cls.main_css_path = os.path.join(base_dir, 'css', 'main.css')
        cls.player_css_path = os.path.join(base_dir, 'css', 'player.css')
        cls.app_js_path = os.path.join(base_dir, 'js', 'app.js')

        with open(cls.html_path, encoding='utf-8') as f:
            cls.html = f.read()
        with open(cls.main_css_path, encoding='utf-8') as f:
            cls.main_css = f.read()
        with open(cls.player_css_path, encoding='utf-8') as f:
            cls.player_css = f.read()
        with open(cls.app_js_path, encoding='utf-8') as f:
            cls.app_js = f.read()

    def test_refinement_1_responsive_sidebar(self):
        """Refinement 1: Responsive Docking on Desktop >= 1280px with collapse toggle"""
        self.assertIn('btn-collapse-sidebar', self.html, "btn-collapse-sidebar missing in HTML")
        self.assertIn('sidebar-docked', self.main_css, "sidebar-docked CSS missing in main.css")
        self.assertIn('sidebar-collapsed', self.main_css, "sidebar-collapsed CSS missing in main.css")
        self.assertIn('@media (min-width: 1280px)', self.main_css, "Desktop media query missing in main.css")
        self.assertIn('initSidebarState', self.app_js, "Sidebar state init logic missing in app.js")

    def test_refinement_2_thematic_categories_and_bilingual_titles(self):
        """Refinement 2: 4 Thematic categories with bilingual Sanskrit-English titles"""
        categories = ['मुख्यप्रयोगाः', 'शास्त्रग्रन्थाः', 'ऐतिहासिकाभिलेखाः', 'साधनानि']
        for cat in categories:
            self.assertIn(cat, self.html, f"Category '{cat}' missing in nav-drawer HTML")
        
        # Check all 13 destinations exist
        expected_sections = [
            'performance', 'avadhanaKala', 'concentration', 'glimpses',
            'scholars', 'institutions', 'society', 'gallery', 'acknowledgments',
            'help', 'btn-nav-search', 'btn-replay-opening', 'btn-exit'
        ]
        for sec in expected_sections:
            self.assertTrue(sec in self.html, f"Section/ID '{sec}' missing in nav-drawer")
        
        # Check bilingual label structure
        self.assertIn('text-primary-label', self.html)
        self.assertIn('text-secondary-label', self.html)

    def test_refinement_3_drawer_overlay_scrim(self):
        """Refinement 3: Drawer backdrop scrim on mobile/tablet"""
        self.assertIn('id="nav-drawer-backdrop"', self.html)
        self.assertIn('.nav-drawer-backdrop', self.main_css)
        self.assertIn('.nav-drawer-backdrop.active', self.main_css)
        self.assertIn('closeDrawerMobile', self.app_js)

    def test_refinement_4_verse_pাদা_indentation(self):
        """Refinement 4: Classical Sanskrit pāda rhythmic indentation"""
        self.assertIn('.verse-line.pada-even', self.player_css)
        self.assertIn('formatSanskritVerse', self.app_js)
        self.assertIn('pada-even', self.app_js)

    def test_refinement_5_dialogue_cards_double_fillet(self):
        """Refinement 5: Dialogue cards double-fillet manuscript folio border"""
        self.assertIn('inset 0 0 0 3px', self.player_css, "Double-fillet inset shadow missing")
        self.assertIn('rgba(255, 252, 242', self.player_css, "Warm parchment background missing")

    def test_refinement_6_single_letter_cards(self):
        """Refinement 6: Single-letter akṣara hero card layout"""
        self.assertIn('akshara-hero', self.player_css)
        self.assertIn('compact-turn-subtitle', self.player_css)
        self.assertIn('✦ प्रथमाक्षरम् • First Syllable Turn', self.app_js)

    def test_refinement_7_speaker_badges_seals(self):
        """Refinement 7: Traditional manuscript seal / stamp badges"""
        self.assertIn('.speaker-seal', self.player_css)
        self.assertIn('〔 ${speakerInfo.name} 〕', self.app_js)

    def test_refinement_8_workspace_centering_and_treatise(self):
        """Centering in workspace and treatise contrast / Sanskrit titles"""
        self.assertIn('align-items: center', self.main_css)
        self.assertIn('avadhana-chapter-title-sa', self.html)
        self.assertIn('concentration-chapter-title-sa', self.html)
        self.assertIn('avadhanaTitlesSa', self.app_js)

if __name__ == '__main__':
    unittest.main()
