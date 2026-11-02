"""Read target-path metadata from Windows Shell Link (LNK) files."""
from __future__ import annotations

import io

try:
    import pylnk3
except ImportError:
    pylnk3 = None


def inspect_lnk(data: bytes) -> dict[str, str | None]:
    """Return the resolved target path and related Shell Link path fields."""
    if pylnk3 is None:
        raise RuntimeError(
            "LNK metadata support requires pylnk3; install metadata-forensics-tools/requirements.txt"
        )
    link = pylnk3.parse(io.BytesIO(data))
    return {
        "target_path_windows": link.path,
        "relative_path": link.relative_path,
        "working_directory": link.working_dir,
    }
