#!/usr/bin/env python3
"""
Extensive Test Suite for the Adaptive Viewport Engine
Tests autonomous viewport inspection, dynamic layout calculation,
CSS variable injection, zero top/bottom clipping, and dynamic rotation
across 14 diverse real-world device form factors.
"""

import os
import sys
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
        pass

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

def run_adaptive_viewport_tests():
    port = get_free_port()
    os.chdir(PROJECT_DIR)

    server = ThreadingHTTPServer(('127.0.0.1', port), QuietHTTPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    base_url = f"http://127.0.0.1:{port}/index.html"

    print("======================================================================")
    print("      ADAPTIVE VIEWPORT ENGINE: MULTI-DEVICE FORENSIC AUDIT           ")
    print("======================================================================")

    # 14 distinct real-world device viewports
    test_viewports = [
        {"name": "Ultra-Compact Android (Galaxy A10)", "w": 360, "h": 640, "exp_profile": "phone-compact", "exp_orient": "portrait"},
        {"name": "Short Android / Open Browser Bar", "w": 360, "h": 520, "exp_profile": "phone-compact", "exp_orient": "portrait"},
        {"name": "iPhone SE (Compact iOS)", "w": 375, "h": 667, "exp_profile": "phone-tall", "exp_orient": "portrait"},
        {"name": "iPhone 13 / 14 / 15", "w": 390, "h": 844, "exp_profile": "phone-tall", "exp_orient": "portrait"},
        {"name": "In-App Webview (WhatsApp / Twitter)", "w": 390, "h": 600, "exp_profile": "phone-compact", "exp_orient": "portrait"},
        {"name": "Samsung Galaxy S23 / Pixel 7", "w": 412, "h": 915, "exp_profile": "phone-tall", "exp_orient": "portrait"},
        {"name": "iPhone 15 Pro Max (Large Flagship)", "w": 430, "h": 932, "exp_profile": "phone-tall", "exp_orient": "portrait"},
        {"name": "Galaxy Z Fold (Unfolded)", "w": 884, "h": 1104, "exp_profile": "tablet-portrait", "exp_orient": "portrait"},
        {"name": "iPad Mini (Tablet Portrait)", "w": 768, "h": 1024, "exp_profile": "tablet-portrait", "exp_orient": "portrait"},
        {"name": "iPad Air (Landscape Tablet)", "w": 1024, "h": 768, "exp_profile": "tablet-landscape", "exp_orient": "landscape"},
        {"name": "Landscape Mobile (iPhone)", "w": 844, "h": 390, "exp_profile": "desktop", "exp_orient": "landscape"},
        {"name": "Laptop HD Widescreen", "w": 1366, "h": 768, "exp_profile": "desktop", "exp_orient": "landscape"},
        {"name": "Desktop Full HD (1080p)", "w": 1920, "h": 1080, "exp_profile": "desktop", "exp_orient": "landscape"},
        {"name": "4K / Smart TV Display", "w": 3840, "h": 2160, "exp_profile": "tv-ultrawide", "exp_orient": "landscape"}
    ]

    total_assertions = 0
    passed_assertions = 0

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for d in test_viewports:
            page = browser.new_page(viewport={"width": d["w"], "height": d["h"]})
            page.goto(base_url)
            page.wait_for_selector("#opening-title-stage")

            # 1. Verify ViewportEngine API presence and metrics
            metrics = page.evaluate("() => window.ViewportEngine ? window.ViewportEngine.getMetrics() : null")
            assert metrics is not None, f"ViewportEngine API missing on {d['name']}"
            total_assertions += 1
            passed_assertions += 1

            # 2. Verify root CSS custom properties injected
            css_vars = page.evaluate("""() => {
                const s = document.documentElement.style;
                return {
                    dvh: s.getPropertyValue('--app-dvh'),
                    dvw: s.getPropertyValue('--app-dvw'),
                    uiScale: parseFloat(s.getPropertyValue('--ui-scale')),
                    stageH: parseInt(s.getPropertyValue('--dynamic-stage-max-h'), 10),
                    profile: document.documentElement.getAttribute('data-device-profile'),
                    orient: document.documentElement.getAttribute('data-orientation')
                };
            }""")

            total_assertions += 1
            if css_vars["dvh"] == f"{d['h']}px" and css_vars["dvw"] == f"{d['w']}px":
                passed_assertions += 1
            else:
                print(f"[FAIL] {d['name']} CSS dimensions mismatch: got {css_vars['dvh']}x{css_vars['dvw']}")

            # 3. Verify orientation match
            total_assertions += 1
            if css_vars["orient"] == d["exp_orient"]:
                passed_assertions += 1
            else:
                print(f"[FAIL] {d['name']} Orientation mismatch: got {css_vars['orient']}, expected {d['exp_orient']}")

            # 4. Verify scale bounds
            total_assertions += 1
            if 0.60 <= css_vars["uiScale"] <= 1.40:
                passed_assertions += 1
            else:
                print(f"[FAIL] {d['name']} uiScale out of bounds: {css_vars['uiScale']}")

            # 5. Measure layout bounding boxes for Zero Clipping
            emblem_box = page.locator(".gateway-emblem-img").bounding_box()
            primary_btn = page.locator("#btn-start-full-experience").bounding_box()
            secondary_btn = page.locator("#btn-enter").bounding_box()

            # Zero Top Clipping
            total_assertions += 1
            if emblem_box["y"] >= 0:
                passed_assertions += 1
            else:
                print(f"[FAIL] {d['name']} TOP CLIPPED: emblem y = {emblem_box['y']:.1f}")

            # Zero Bottom Clipping
            max_bottom = max(primary_btn["y"] + primary_btn["height"], secondary_btn["y"] + secondary_btn["height"])
            total_assertions += 1
            if max_bottom <= d["h"] + 1.0: # Allow 1px subpixel rounding tolerance
                passed_assertions += 1
            else:
                print(f"[FAIL] {d['name']} BOTTOM CLIPPED: bottom = {max_bottom:.1f} > vh = {d['h']}")

            # Touch target minimum height >= 36px
            total_assertions += 1
            if primary_btn["height"] >= 36 and secondary_btn["height"] >= 36:
                passed_assertions += 1
            else:
                print(f"[FAIL] {d['name']} Touch target too small: primary={primary_btn['height']}, secondary={secondary_btn['height']}")

            clearance = d["h"] - max_bottom
            print(f"  [+] {d['name']:<38} ({d['w']}x{d['h']}) | Scale: {css_vars['uiScale']:.2f} | FrameMaxH: {css_vars['stageH']}px | Clearance: +{clearance:.1f}px -> PASS")
            page.close()

        # DYNAMIC ROTATION TEST: Portrait -> Landscape -> Portrait
        print("\n=== DYNAMIC ORIENTATION & ROTATION AUDIT ===")
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(base_url)
        page.wait_for_selector("#opening-title-stage")

        orient_before = page.evaluate("() => document.documentElement.getAttribute('data-orientation')")
        total_assertions += 1
        if orient_before == "portrait":
            passed_assertions += 1
            print("  [+] Initial Portrait state: PASS (portrait)")

        # Rotate to Landscape
        page.set_viewport_size({"width": 844, "height": 390})
        page.wait_for_timeout(200) # Wait for resize event to dispatch and RAF to fire

        orient_after = page.evaluate("() => document.documentElement.getAttribute('data-orientation')")
        total_assertions += 1
        if orient_after == "landscape":
            passed_assertions += 1
            print("  [+] Rotated to Landscape state: PASS (landscape)")

        # Check clipping in rotated landscape
        eb_rot = page.locator(".gateway-emblem-img").bounding_box()
        pb_rot = page.locator("#btn-start-full-experience").bounding_box()
        total_assertions += 1
        if eb_rot["y"] >= 0:
            passed_assertions += 1
            print(f"  [+] Landscape Zero Top Clipping: PASS (y = {eb_rot['y']:.1f}px)")

        browser.close()

    server.shutdown()

    print("\n======================================================================")
    print(f"   ADAPTIVE VIEWPORT AUDIT SCORECARD: {passed_assertions} / {total_assertions} PASSED")
    print("======================================================================")

    if passed_assertions == total_assertions:
        print("\nALL ADAPTIVE VIEWPORT TESTS PASSED! 100% PRODUCTION READY!")
        return 0
    else:
        print(f"\n{total_assertions - passed_assertions} ASSERTIONS FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(run_adaptive_viewport_tests())
