# Hear Me Out

Day 17 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 17 Metadata Forensics — Hear Me Out

### Results

All modes returned `CORRECT`; every answer ID was accepted. The final
Game Master status checks showed no pending scoring state.

| Mode | Attempt | Accepted | Play type |
| --- | --- | ---: | --- |
| Single Solve | `06ddb090-41dc-445e-8e89-a529794d9e14` | 1 / 1 | Untimed |
| Time Trial | `03775308-e2c0-4bbb-9e0a-7ab139a894b3` | 22 / 22 | Regular, untimed |
| Mastery | `12d93ed4-2834-44a7-ad8e-c7122f9da3b7` | 110 / 110 | Regular, untimed |

The Day 17 Metadata Forensics list marks all three modes solved by the current
player. No deadline was active.

### Assigned artifacts

- Single Solve: Download metadata-day-17-evidence.zip (private download link removed) —
  SHA-256 `5bb0fc7a712253cfe26b4ec3e6d22b35fc4f3377e966143100a7a6d27719145b`.
- Time Trial: Download evidence.zip (private download link removed) —
  SHA-256 `f9b81191675fda501924d55625aef8efe4f9fc121eab692e8f6edb4a72bf74cf`.
- Mastery: Download mastery bundle (private download link removed) —
  SHA-256 `498e556977fcc6082b06ed6d67c4f446dcd6a8a01d58f23ee024613f140aff71`.
  The bundle supplied five mastery sets.

### Solver update

Added `metadata-forensics-tools/audio_metadata.py` and wired the runner to
answer `media.primary_audio_codec_name`. It uses `ffprobe`'s stream
`codec_name` when available, with a MediaInfo fallback that maps common codec
names and derives PCM names from bit depth and byte order. For the assigned
WAV, the codec name is `pcm_s16le`; MediaInfo's broader format label `PCM`
alone was rejected.

## Retained sources

- [later/writeups/day-17/metadata-forensics-hear-me-out.md](../../source-notes/later/writeups/day-17/metadata-forensics-hear-me-out.md)
