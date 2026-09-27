#!/usr/bin/env python3
"""
Comprehensive Mobile Multi-Device Forensic Verification Test Suite
Executes the full mobile test matrix across Android & iOS viewports,
touch targets, button actions, horizontal overflow, drawer navigation,
screen switching, audio player docking, and PWA configuration.
"""

import sys
import os
import time
import socket
import threading
import http.server
from http.server import ThreadingHTTPServer
from playwright.sync_api import sync_playwright

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(TEST_DIR)

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format, *args):
        pass  # Suppress request spam

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError):
            pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError):
            pass

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run_mobile_test_suite():
    port = get_free_port()
    os.chdir(PROJECT_DIR)
    
    server = ThreadingHTTPServer(('127.0.0.1', port), QuietHTTPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    base_url = f"http://127.0.0.1:{port}/index.html"
    print(f"[*] Local test server running on {base_url}")
    
    results = []
    
    VIEWPORTS = [
        {"name": "Ultra-Compact Android (Galaxy A10/A12)", "width": 360, "height": 640, "is_mobile": True},
        {"name": "iPhone SE (Compact iOS)", "width": 375, "height": 667, "is_mobile": True},
        {"name": "Standard Modern iOS (iPhone 13/14/15)", "width": 390, "height": 844, "is_mobile": True},
        {"name": "Standard Modern Android (Pixel 7 / Galaxy S23)", "width": 412, "height": 915, "is_mobile": True},
        {"name": "Large / Pro Max iOS (iPhone 15/16 Pro Max)", "width": 430, "height": 932, "is_mobile": True},
        {"name": "Foldable Unfolded (Galaxy Z Fold)", "width": 884, "height": 1104, "is_mobile": True},
        {"name": "Tablet Portrait (iPad Mini / iPad 10th)", "width": 768, "height": 1024, "is_mobile": True},
        {"name": "Landscape Mobile (iPhone Landscape)", "width": 844, "height": 390, "is_mobile": True},
    ]

    def test(category, test_name, condition, details=""):
        status = "PASS" if condition else "FAIL"
        results.append({"category": category, "name": test_name, "status": status, "details": details})
        mark = "+" if condition else "-"
        print(f"  [{mark}] [{category}] {test_name}: {status} {details}")
        return condition

    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # -------------------------------------------------------------
        # 1. VIEWPORT OVERFLOW & LAYOUT INTEGRITY ACROSS ALL MOBILE DEVICES
        # -------------------------------------------------------------
        print("\n=== TEST GROUP 1: MOBILE VIEWPORTS & HORIZONTAL OVERFLOW (JIGGLE) ===")
        for vp in VIEWPORTS:
            context = browser.new_context(
                viewport={"width": vp["width"], "height": vp["height"]},
                is_mobile=vp["is_mobile"],
                has_touch=True
            )
            page = context.new_page()
            page.goto(base_url, wait_until="networkidle")
            
            # Dismiss splash gateway
            btn_enter = page.locator("#btn-enter")
            if btn_enter.is_visible():
                btn_enter.click()
                page.wait_for_selector("#app-shell", state="visible")
            
            # Check horizontal overflow (scrollWidth should not exceed clientWidth)
            has_overflow = page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth || document.body.scrollWidth > window.innerWidth")
            test(
                "Viewport Overflow",
                f"{vp['name']} ({vp['width']}x{vp['height']}) - Zero Horizontal Overflow",
                not has_overflow,
                f"scrollWidth <= {vp['width']}"
            )
            
            # Check Round Navigator Bar stays within screen
            bar_box = page.locator(".round-bar-container").bounding_box()
            if bar_box:
                test(
                    "Fitment",
                    f"{vp['name']} - Page Navigator Bar fits viewport",
                    bar_box["width"] <= vp["width"] + 2,
                    f"bar width = {int(bar_box['width'])}px <= {vp['width']}px"
                )
                
            # Check Stage Container stays within screen
            stage_box = page.locator("#stage-container").bounding_box()
            if stage_box:
                test(
                    "Fitment",
                    f"{vp['name']} - Stage Container fits viewport",
                    stage_box["width"] <= vp["width"] + 2,
                    f"stage width = {int(stage_box['width'])}px <= {vp['width']}px"
                )
            
            context.close()

        # -------------------------------------------------------------
        # 2. TOUCH TARGETS MINIMUM DIMENSIONS (WCAG / APPLE / ANDROID)
        # -------------------------------------------------------------
        print("\n=== TEST GROUP 2: TOUCH TARGET SIZE AUDIT (>= 38px - 44px) ===")
        context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        page = context.new_page()
        page.goto(base_url, wait_until="networkidle")
        page.locator("#btn-enter").click()
        page.wait_for_selector("#app-shell", state="visible")
        
        # Header buttons
        for btn_id in ["#btn-toggle-menu", "#btn-home", "#btn-search", "#btn-help", "#btn-tv-mode", "#btn-fullscreen"]:
            btn = page.locator(btn_id)
            if btn.is_visible():
                box = btn.bounding_box()
                min_dim = min(box["width"], box["height"]) if box else 0
                test(
                    "Touch Targets",
                    f"Header Button {btn_id} touch target >= 40px",
                    min_dim >= 40,
                    f"size = {int(box['width'])}x{int(box['height'])}px" if box else "not found"
                )
                
        # Round Navigation Arrows
        for arrow_id in ["#btn-round-prev", "#btn-round-next"]:
            arrow = page.locator(arrow_id)
            box = arrow.bounding_box()
            min_dim = min(box["width"], box["height"]) if box else 0
            test(
                "Touch Targets",
                f"Page Arrow {arrow_id} touch target >= 36px",
                min_dim >= 36,
                f"size = {int(box['width'])}x{int(box['height'])}px" if box else "not found"
            )
            
        # Round Pills
        pills = page.locator(".round-pill")
        count = pills.count()
        test("Pills Cardinality", "Exactly 25 Round Pills Rendered", count == 25, f"count = {count}")
        if count > 0:
            box = pills.first.bounding_box()
            test(
                "Touch Targets",
                "Round Pill touch height >= 36px",
                box["height"] >= 36 if box else False,
                f"height = {int(box['height'])}px" if box else "no box"
            )
            
        # Recitation Card Audio Buttons
        audio_btns = page.locator(".dialogue-audio-btn")
        if audio_btns.count() > 0:
            box = audio_btns.first.bounding_box()
            test(
                "Touch Targets",
                "Recitation Audio Play Button >= 36px",
                box["width"] >= 36 and box["height"] >= 36 if box else False,
                f"size = {int(box['width'])}x{int(box['height'])}px" if box else "no box"
            )

        # -------------------------------------------------------------
        # 3. INTERACTIVE CONTROLS & SCREEN NAVIGATION
        # -------------------------------------------------------------
        print("\n=== TEST GROUP 3: INTERACTIVE CONTROLS & SCREEN NAVIGATION ===")
        
        # 3-Way Script Switcher
        switcher_dev = page.locator('.view-btn[data-view="devanagari"]')
        switcher_bi = page.locator('.view-btn[data-view="bilingual"]')
        switcher_en = page.locator('.view-btn[data-view="english"]')
        
        switcher_en.click()
        page.wait_for_timeout(150)
        has_mode_en = page.evaluate("() => document.body.classList.contains('mode-english')")
        test("Script Switcher", "Click 'English' switches body to mode-english", has_mode_en)
        
        switcher_bi.click()
        page.wait_for_timeout(150)
        has_mode_bi = page.evaluate("() => document.body.classList.contains('mode-bilingual')")
        test("Script Switcher", "Click 'Bilingual' switches body to mode-bilingual", has_mode_bi)

        switcher_dev.click()
        page.wait_for_timeout(150)
        has_mode_dev = page.evaluate("() => document.body.classList.contains('mode-devanagari')")
        test("Script Switcher", "Click 'Devanagari' switches body to mode-devanagari", has_mode_dev)

        # Round Next & Prev Cycling
        prev_round = page.locator("#current-round-title").inner_text()
        page.locator("#btn-round-next").click()
        page.wait_for_timeout(200)
        next_round = page.locator("#current-round-title").inner_text()
        test("Page Navigation", "Click Next Page cycles from Page 1 to Page 2", "Page 2" in next_round, f"Title = {next_round}")

        page.locator("#btn-round-prev").click()
        page.wait_for_timeout(200)
        back_round = page.locator("#current-round-title").inner_text()
        test("Page Navigation", "Click Prev Page returns to Page 1", "Page 1" in back_round, f"Title = {back_round}")

        # Direct Pill Selection (Page 5)
        pills.nth(4).click()
        page.wait_for_timeout(300)
        p5_round = page.locator("#current-round-title").inner_text()
        test("Page Navigation", "Tapping Page 5 Pill loads Page 5", "Page 5" in p5_round, f"Title = {p5_round}")

        # Drawer Navigation Across All Screens
        page.locator("#btn-toggle-menu").click()
        page.wait_for_timeout(300)
        drawer_visible = page.locator("#nav-drawer").is_visible()
        test("Navigation Drawer", "Menu button opens navigation drawer", drawer_visible)

        # Navigate to Avadhana Kala Treatise
        page.locator('.nav-link[data-section="avadhanaKala"]').click()
        page.wait_for_timeout(300)
        is_avadhankala = page.locator("#section-avadhanaKala").is_visible()
        test("Section Navigation", "Drawer link navigates to Avadhana Kala Treatise", is_avadhankala)

        # Navigate to Concentration Treatise
        page.locator("#btn-toggle-menu").click()
        page.wait_for_timeout(300)
        page.locator('.nav-link[data-section="concentration"]').click()
        page.wait_for_timeout(300)
        is_ashtavadhanam = page.locator("#section-concentration").is_visible()
        test("Section Navigation", "Drawer link navigates to Concentration Treatise", is_ashtavadhanam)

        # Navigate to Glimpses Theater
        page.locator("#btn-toggle-menu").click()
        page.wait_for_timeout(300)
        page.locator('.nav-link[data-section="glimpses"]').click()
        page.wait_for_timeout(300)
        is_glimpses = page.locator("#section-glimpses").is_visible()
        test("Section Navigation", "Drawer link navigates to Glimpses Theater", is_glimpses)

        # Navigate to Scholars & Assembly
        page.locator("#btn-toggle-menu").click()
        page.wait_for_timeout(300)
        page.locator('.nav-link[data-section="scholars"]').click()
        page.wait_for_timeout(300)
        is_scholars = page.locator("#section-scholars").is_visible()
        test("Section Navigation", "Drawer link navigates to Scholars & Assembly", is_scholars)

        # Navigate to Participating Institutions
        page.locator("#btn-toggle-menu").click()
        page.wait_for_timeout(300)
        page.locator('.nav-link[data-section="institutions"]').click()
        page.wait_for_timeout(300)
        is_institutions = page.locator("#section-institutions").is_visible()
        test("Section Navigation", "Drawer link navigates to Participating Institutions", is_institutions)

        # Navigate to Sri Aurobindo Society
        page.locator("#btn-toggle-menu").click()
        page.wait_for_timeout(300)
        page.locator('.nav-link[data-section="society"]').click()
        page.wait_for_timeout(300)
        is_society = page.locator("#section-society").is_visible()
        test("Section Navigation", "Drawer link navigates to Sri Aurobindo Society", is_society)

        # Navigate to Master Gallery
        page.locator("#btn-toggle-menu").click()
        page.wait_for_timeout(300)
        page.locator('.nav-link[data-section="gallery"]').click()
        page.wait_for_timeout(300)
        is_gallery = page.locator("#section-gallery").is_visible()
        gallery_items = page.locator(".gallery-item-card").count()
        test("Section Navigation", f"Drawer link navigates to Master Gallery ({gallery_items} items)", is_gallery and gallery_items >= 50, f"items = {gallery_items}")

        # Navigate to Acknowledgments & Credits
        page.locator("#btn-toggle-menu").click()
        page.wait_for_timeout(300)
        page.locator('.nav-link[data-section="acknowledgments"]').click()
        page.wait_for_timeout(300)
        is_ack = page.locator("#section-acknowledgments").is_visible()
        test("Section Navigation", "Drawer link navigates to Acknowledgments & Credits", is_ack)

        # Navigate to Help & Guide
        page.locator("#btn-toggle-menu").click()
        page.wait_for_timeout(300)
        page.locator('.nav-link[data-section="help"]').click()
        page.wait_for_timeout(300)
        is_help = page.locator("#section-help").is_visible()
        test("Section Navigation", "Drawer link navigates to User Guide & Help", is_help)

        # Return to Performance section via drawer
        page.locator("#btn-toggle-menu").click()
        page.wait_for_timeout(300)
        page.locator('.nav-link[data-section="performance"]').click()
        page.wait_for_timeout(300)
        is_perf = page.locator("#section-performance").is_visible()
        test("Section Navigation", "Drawer link navigates back to Performance Section", is_perf)

        # Home emblem returns to Main Landing Gateway
        page.locator("#btn-home").click()
        page.wait_for_timeout(300)
        is_gateway = page.locator("#splash-gateway").is_visible()
        test("Home Navigation", "Home emblem returns to Main Landing Gateway", is_gateway)

        # Re-enter Performance portal for remaining tests
        page.locator("#btn-enter").click()
        page.wait_for_selector("#app-shell", state="visible")
        page.wait_for_timeout(300)

        # -------------------------------------------------------------
        # 4. SEARCH MODAL & QUERY EXECUTION
        # -------------------------------------------------------------
        print("\n=== TEST GROUP 4: SEARCH MODAL & INTERACTION ===")
        page.locator("#btn-search").click()
        page.wait_for_timeout(300)
        search_modal_open = page.locator("#search-modal").is_visible()
        test("Search Modal", "Search icon in header opens Search Modal", search_modal_open)

        search_input = page.locator("#search-input")
        search_input.fill("अरविन्द")
        page.wait_for_timeout(400)
        search_results_count = page.locator(".search-result-card").count()
        test("Search Execution", f"Devanagari query 'अरविन्द' returns results", search_results_count > 0, f"results = {search_results_count}")

        page.locator("#btn-close-search").click()
        page.wait_for_timeout(200)
        search_modal_closed = not page.locator("#search-modal").is_visible()
        test("Search Modal", "Close button closes Search Modal", search_modal_closed)

        # -------------------------------------------------------------
        # 5. AUDIO PLAYBACK & PLAYER DOCKING CLEARANCE
        # -------------------------------------------------------------
        print("\n=== TEST GROUP 5: AUDIO PLAYER & MOBILE DOCKING CLEARANCE ===")
        audio_btn = page.locator(".dialogue-audio-btn").first
        audio_btn.click()
        page.wait_for_timeout(400)
        
        # Audio Player Bar visibility
        player_bar = page.locator("#player-bar")
        player_visible = player_bar.is_visible()
        test("Audio Player", "Tapping verse audio button triggers persistent Player Bar", player_visible)

        # Check player bar docking
        player_box = player_bar.bounding_box()
        if player_box:
            test("Audio Player Docking", "Player bar docked at bottom of viewport", player_box["y"] + player_box["height"] >= 840, f"y={int(player_box['y'])}, h={int(player_box['height'])}")
            
            # Check content padding bottom clearance
            pb_val = page.evaluate("() => window.getComputedStyle(document.querySelector('.main-content')).paddingBottom")
            pb_int = int(''.join(filter(str.isdigit, pb_val)) or '0')
            test("Player Clearance", f"Main content padding-bottom ({pb_int}px) clears player bar ({int(player_box['height'])}px)", pb_int >= player_box["height"] - 10, f"paddingBottom={pb_val}")

        # Player Play / Pause Toggle
        play_btn = page.locator("#btn-play-pause")
        play_btn.click()
        page.wait_for_timeout(300)
        is_paused = page.evaluate("() => window.Player && window.Player.audio ? window.Player.audio.paused : true")
        test("Audio State Toggle", "Tapping player play/pause button pauses playback", is_paused)

        # -------------------------------------------------------------
        # 6. PWA & HEAD METADATA FOR MOBILE OS (ANDROID & IOS)
        # -------------------------------------------------------------
        print("\n=== TEST GROUP 6: PWA & MOBILE OS METADATA ===")
        viewport_meta = page.locator('meta[name="viewport"]').get_attribute('content') or ""
        test("Mobile Viewport Meta", "Viewport includes width=device-width & viewport-fit=cover", "width=device-width" in viewport_meta and "viewport-fit=cover" in viewport_meta, viewport_meta)

        apple_cap = page.locator('meta[name="apple-mobile-web-app-capable"]').get_attribute('content')
        test("iOS PWA Meta", "apple-mobile-web-app-capable is yes", apple_cap == "yes")

        apple_touch_icon = page.locator('link[rel="apple-touch-icon"]').get_attribute('href') or ""
        test("iOS Icon", "apple-touch-icon link is declared", "apple-touch-icon.png" in apple_touch_icon, apple_touch_icon)

        manifest_link = page.locator('link[rel="manifest"]').get_attribute('href') or ""
        test("PWA Manifest", "W3C manifest link is declared", "manifest.json" in manifest_link, manifest_link)

        theme_color = page.locator('meta[name="theme-color"]').get_attribute('content')
        test("PWA Theme Color", "theme-color is defined", theme_color is not None, f"theme-color={theme_color}")

        context.close()
        browser.close()

    server.shutdown()
    
    # -------------------------------------------------------------
    # SUMMARY & SCORECARD
    # -------------------------------------------------------------
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    
    print("\n" + "="*70)
    print(f"   MOBILE FORENSIC MULTI-DEVICE TEST SCORECARD: {passed}/{total} PASSED")
    print("="*70)
    
    if failed > 0:
        print("\nFAILED TESTS:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"  [-] [{r['category']}] {r['name']}: {r['details']}")
        return False
    else:
        print("\nALL MOBILE TESTS PASSED! 100% PRODUCTION READY FOR ANDROID & IOS!")
        return True

if __name__ == "__main__":
    success = run_mobile_test_suite()
    sys.exit(0 if success else 1)
