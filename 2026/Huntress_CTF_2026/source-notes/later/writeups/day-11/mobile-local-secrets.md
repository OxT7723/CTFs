> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 11 Mobile Android: Local Secrets

- Challenge ID: `mobile-android-day-11-local-secrets`
- Mode: Single Solve
- Artifact SHA-256: `e049a89781d24c62cdb6b83c6a2d202810088f22c27d00f1951bbc091fc78cbd`
- Answer ID: `answer`

The APK's JSON puzzle asset stores Base64 data followed by single-byte XOR.
The generic decoder scans encoded JSON assets, applies the declared codec and
key, and prints the decoded value. The mode runner maps each Mastery answer
to the APK delivery named by its set. Single Solve, Time Trial, and the
three-case Mastery bundle all returned `CORRECT`.
