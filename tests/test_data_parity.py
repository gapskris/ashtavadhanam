#!/usr/bin/env python3
"""
Test Suite: Canonical Data Layer Parity
Verifies bit-for-bit synchronization between content/data.json and js/data.js.
"""

import os
import sys
import subprocess

def test_data_parity():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sync_script = os.path.join(base_dir, "tools", "sync_data_js.py")
    res = subprocess.run([sys.executable, sync_script, "--check"], capture_output=True, text=True)
    if res.returncode == 0 and "100% synchronized" in res.stdout:
        print("  [PASS] Canonical Data Parity: js/data.js is 100% synchronized with content/data.json")
        return True
    else:
        print("  [FAIL] Data parity check failed:", res.stdout, res.stderr)
        return False

if __name__ == '__main__':
    ok = test_data_parity()
    sys.exit(0 if ok else 1)
