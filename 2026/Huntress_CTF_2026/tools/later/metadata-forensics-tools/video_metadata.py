#!/usr/bin/env python3
"""Read video stream geometry from media files using ffprobe or MediaInfo."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile


def primary_video_dimensions(data: bytes, suffix: str = ".bin") -> str:
    """Return the first video stream's coded width and height."""
    with tempfile.NamedTemporaryFile(suffix=suffix) as media_file:
        media_file.write(data)
        media_file.flush()
        if shutil.which("ffprobe"):
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-select_streams",
                    "v:0",
                    "-show_entries",
                    "stream=width,height",
                    "-of",
                    "json",
                    media_file.name,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            video_tracks = json.loads(result.stdout).get("streams", [])
            if not video_tracks:
                return "none"
            track = video_tracks[0]
            width, height = track.get("width"), track.get("height")
        else:
            result = subprocess.run(
                ["mediainfo", "--Output=JSON", media_file.name],
                capture_output=True,
                text=True,
                check=True,
            )
            tracks = json.loads(result.stdout).get("media", {}).get("track", [])
            video_tracks = [track for track in tracks if track.get("@type") == "Video"]
            if not video_tracks:
                return "none"
            track = video_tracks[0]
            width, height = track.get("Width"), track.get("Height")
    if not width or not height:
        return "none"
    return f"{width}x{height}"
