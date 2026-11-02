#!/usr/bin/env python3
"""Read Android APK manifest metadata using the Android Asset Packaging Tool."""
from __future__ import annotations

import re
import subprocess
import tempfile


def package_name(data: bytes) -> str:
    """Return the manifest package name from an APK, or 'none' when absent."""
    with tempfile.NamedTemporaryFile(suffix=".apk") as apk:
        apk.write(data)
        apk.flush()
        completed = subprocess.run(
            ["aapt", "dump", "badging", apk.name],
            capture_output=True,
            text=True,
        )
    if completed.returncode:
        raise ValueError(f"aapt could not read APK metadata: {completed.stderr.strip()}")
    match = re.search(r"^package: name='([^']*)'", completed.stdout, re.M)
    return match.group(1) if match else "none"
