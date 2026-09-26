#!/usr/bin/env python3
"""
Test Suite: Native HTTP 206 Partial Content (Range Requests) in run_local.py
Verifies byte-range streaming for MP4 videos and AAC/MP3 audio.
"""

import urllib.request
import threading
import time
import os
import sys
import socketserver

def run_range_test():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, base_dir)
    import run_local

    Handler = run_local.RangeHTTPRequestHandler
    port = 8991
    server = socketserver.TCPServer(('127.0.0.1', port), Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    try:
        # 1. Video Range Request
        url_video = f'http://127.0.0.1:{port}/assets/video/02A.mp4'
        req = urllib.request.Request(url_video)
        req.add_header('Range', 'bytes=1000-4999')
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            cr = resp.headers.get('Content-Range')
            assert resp.status == 206, f"Expected status 206, got {resp.status}"
            assert len(data) == 4000, f"Expected 4000 bytes, got {len(data)}"
            assert cr.startswith('bytes 1000-4999/'), f"Unexpected Content-Range {cr}"
            print("  [PASS] Video HTTP 206 Range request verified (bytes 1000-4999)")

        # 2. Audio Range Request
        url_audio = f'http://127.0.0.1:{port}/assets/audio/special/ashmain_theme.m4a'
        req2 = urllib.request.Request(url_audio)
        req2.add_header('Range', 'bytes=0-1023')
        with urllib.request.urlopen(req2) as resp2:
            data2 = resp2.read()
            cr2 = resp2.headers.get('Content-Range')
            assert resp2.status == 206, f"Expected status 206, got {resp2.status}"
            assert len(data2) == 1024, f"Expected 1024 bytes, got {len(data2)}"
            print("  [PASS] Audio HTTP 206 Range request verified (bytes 0-1023)")

        # 3. Standard Non-Range Request
        url_index = f'http://127.0.0.1:{port}/index.html'
        with urllib.request.urlopen(url_index) as resp3:
            assert resp3.status == 200, f"Expected status 200, got {resp3.status}"
            assert resp3.headers.get('Accept-Ranges') == 'bytes', "Missing Accept-Ranges header"
            print("  [PASS] Standard HTTP 200 with Accept-Ranges: bytes verified")

        print("  --> ALL HTTP 206 RANGE TESTS PASSED!\n")
        return True

    finally:
        server.shutdown()

if __name__ == '__main__':
    success = run_range_test()
    sys.exit(0 if success else 1)
