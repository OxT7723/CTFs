> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Trust Everyone

- Single Solve, Time Trial, and the five case Mastery bundle were accepted.
- Each assigned APK contains `assets/huntress_puzzle.json`. Decode its `data` field with the declared base64 codec to obtain the answer code; the Game Master accepted the exact codes.
- `solve.py` downloads the current assigned APK deliveries through the proxy, verifies their SHA-256 values, extracts the codes, and submits them.
- No emulator was available in this environmefnt, so the run used the exact embedded case answers rather than driving the exported Android activity.
