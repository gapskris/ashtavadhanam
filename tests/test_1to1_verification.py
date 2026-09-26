#!/usr/bin/env python3
"""
Test Suite: Automated 70-Point Forensic Audit Suite
Direct wrapper executing tools/verify_1to1_mapping.py.
"""

import os
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def test_1to1():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    verify_script = os.path.join(base_dir, "tools", "verify_1to1_mapping.py")
    res = subprocess.run([sys.executable, verify_script], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode == 0 and "70 / 70 CHECKS PASSED" in res.stdout:
        print("  [PASS] 70/70 Forensic Assertions Verified (Images, Videos, Audios, Schema, UI, PWA, Search)")
        return True
    else:
        print("  [FAIL] 70-point verification failed:\n", res.stdout, res.stderr)
        return False

if __name__ == '__main__':
    ok = test_1to1()
    sys.exit(0 if ok else 1)
