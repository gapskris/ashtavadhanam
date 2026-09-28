#!/usr/bin/env python3
"""
Ashtavadhanam Modern — Master Automated Test Runner
Executes all unit, integration, parity, and forensic verification test suites.
"""

import os
import sys
import subprocess
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def main():
    print("=" * 70)
    print("   ASHTAVADHANAM MODERN: EXECUTING COMPLETE TEST SUITE")
    print("=" * 70)

    tests_dir = os.path.dirname(os.path.abspath(__file__))
    suites = [
        ("Canonical Data Parity Test", [sys.executable, os.path.join(tests_dir, "test_data_parity.py")]),
        ("Native HTTP 206 Range Seeking Test", [sys.executable, os.path.join(tests_dir, "test_range_requests.py")]),
        ("Audio Player Logic & State Toggle Test", ["node", os.path.join(tests_dir, "test_player_logic.js")]),
        ("Sanskrit Typography & Card Cardinality Test", [sys.executable, os.path.join(tests_dir, "test_sanskrit_alignment.py")]),
        ("70-Point Forensic Audit Verification Suite", [sys.executable, os.path.join(tests_dir, "test_1to1_verification.py")]),
        ("Mobile Multi-Device Forensic Verification Suite (Playwright)", [sys.executable, os.path.join(tests_dir, "test_mobile_matrix.py")]),
        ("Adaptive Viewport Engine Multi-Device Forensic Test", [sys.executable, os.path.join(tests_dir, "test_adaptive_viewport_engine.py")]),
    ]

    all_passed = True
    start_time = time.time()

    for name, cmd in suites:
        print(f"\n--- RUNNING: {name} ---")
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            if res.stdout:
                print(res.stdout.strip())
            if res.returncode == 0:
                print(f"--> [PASS] {name}")
            else:
                if res.stderr:
                    print(res.stderr.strip())
                print(f"--> [FAIL] {name} (Exit code: {res.returncode})")
                all_passed = False
        except Exception as e:
            print(f"--> [ERROR] Could not execute {name}: {e}")
            all_passed = False

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    if all_passed:
        print(f"  ALL TEST SUITES PASSED (100% GREEN) in {elapsed:.2f}s")
        print("  STATUS: 100% PRODUCTION READY FOR RELEASE")
    else:
        print(f"  SOME TESTS FAILED in {elapsed:.2f}s")
    print("=" * 70 + "\n")

    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
