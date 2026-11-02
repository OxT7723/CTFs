#!/usr/bin/env python3
"""Read audio stream metadata from media files using MediaInfo."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile


def primary_audio_codec_name(data: bytes, suffix: str = ".bin") -> str:
    """Return the first audio stream's canonical codec name."""
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
                    "a:0",
                    "-show_entries",
                    "stream=codec_name",
                    "-of",
                    "json",
                    media_file.name,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            streams = json.loads(result.stdout).get("streams", [])
            return str(streams[0].get("codec_name") or "none") if streams else "none"
        result = subprocess.run(
            ["mediainfo", "--Output=JSON", media_file.name],
            capture_output=True,
            text=True,
            check=True,
        )
    document = json.loads(result.stdout)
    tracks = document.get("media", {}).get("track", [])
    audio_tracks = [track for track in tracks if track.get("@type") == "Audio"]
    if not audio_tracks:
        return "none"
    track = audio_tracks[0]
    format_name = str(track.get("Format") or "")
    if format_name.casefold() == "pcm":
        bits = track.get("BitDepth")
        if bits:
            bit_depth = int(bits)
            sign = (
                "s"
                if str(track.get("Format_Settings_Sign", "")).casefold() == "signed"
                else "u"
            )
            if bit_depth == 8:
                return "pcm_u8"
            endian = (
                "be"
                if str(track.get("Format_Settings_Endianness", "")).casefold()
                == "big"
                else "le"
            )
            return f"pcm_{sign}{bit_depth}{endian}"
    aliases = {
        "aac": "aac",
        "ac-3": "ac3",
        "e-ac-3": "eac3",
        "flac": "flac",
        "mpeg audio": "mp3",
        "opus": "opus",
        "vorbis": "vorbis",
        "wavpack": "wavpack",
    }
    return aliases.get(format_name.casefold(), format_name.casefold() or "none")
