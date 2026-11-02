# Trust Everyone

Day 9 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `mobile-android-day-09-trust-everyone`

## Later Homebase account

### Trust Everyone

- Single Solve, Time Trial, and the five case Mastery bundle were accepted.
- Each assigned APK contains `assets/huntress_puzzle.json`. Decode its `data` field with the declared base64 codec to obtain the answer code; the Game Master accepted the exact codes.
- `solve.py` downloads the current assigned APK deliveries through the proxy, verifies their SHA-256 values, extracts the codes, and submits them.
- No emulator was available in this environmefnt, so the run used the exact embedded case answers rather than driving the exported Android activity.

## Retained sources

- [early/09-Trust_Everyone/readme.md](../../source-notes/early/09-Trust_Everyone/readme.md)
- [later/writeups/day-09/trust-everyone.md](../../source-notes/later/writeups/day-09/trust-everyone.md)
