# Local Secrets

Day 11 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `mobile-android-day-11-local-secrets`

## Later Homebase account

### Day 11 Mobile Android: Local Secrets

- Challenge ID: `mobile-android-day-11-local-secrets`
- Mode: Single Solve
- Artifact SHA-256: `e049a89781d24c62cdb6b83c6a2d202810088f22c27d00f1951bbc091fc78cbd`
- Answer ID: `answer`

The APK's JSON puzzle asset stores Base64 data followed by single-byte XOR.
The generic decoder scans encoded JSON assets, applies the declared codec and
key, and prints the decoded value. The mode runner maps each Mastery answer
to the APK delivery named by its set. Single Solve, Time Trial, and the
three-case Mastery bundle all returned `CORRECT`.

## Retained sources

- [early/11-Local_Secrets/readme.md](../../source-notes/early/11-Local_Secrets/readme.md)
- [later/writeups/day-11/mobile-local-secrets.md](../../source-notes/later/writeups/day-11/mobile-local-secrets.md)
- [later/writeups/day-11/progress-notes.md](../../source-notes/later/writeups/day-11/progress-notes.md)
