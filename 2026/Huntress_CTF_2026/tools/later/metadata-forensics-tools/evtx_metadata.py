#!/usr/bin/env python3
"""Read record counts from Windows EVTX event-log files."""
from __future__ import annotations

import tempfile

def record_count(data: bytes) -> int:
    """Count records the EVTX parser can read from the supplied bytes."""
    if not data.startswith(b"ElfFile\x00"):
        raise ValueError("Input does not have an EVTX file header")
    try:
        from Evtx.Evtx import Evtx
    except ImportError as exc:
        raise ImportError(
            "EVTX parsing requires python-evtx; install metadata-forensics-tools/requirements.txt"
        ) from exc
    with tempfile.NamedTemporaryFile(suffix=".evtx") as stream:
        stream.write(data)
        stream.flush()
        with Evtx(stream.name) as event_log:
            return sum(1 for _ in event_log.records())
