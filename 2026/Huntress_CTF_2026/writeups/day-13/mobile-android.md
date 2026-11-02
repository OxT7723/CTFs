# Keystore Misuse

Day 13 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 13 Mobile: Keystore Misuse

Challenge: `mobile-android-day-13-keystore-misuse`

All available modes completed: Single Solve, Time Trial, and Mastery. The Game
Master status for each reports `CORRECT` and all answer IDs accepted.

### Reusable method

Use `mobile-android-tools/run_modes.py` with the challenge ID. It downloads the
current assigned APK delivery or deliveries, verifies their SHA-256 hashes,
decodes the JSON puzzle assets using their declared codec and key, matches the
decoded value to the API answer format, submits using the live answer IDs, and
records the result under `work/day-13/mobile-android/<attempt-id>/`.

Mastery provides three APK deliveries; the runner associates each question
with its matching delivery. The existing deterministic runner needed no
challenge-specific changes.

### Assigned artifact fingerprints

- Single Solve: `80795a1f9f632902e482185f75749f56b7a7a8e39b3bad590bbeb697e021c448`
- Time Trial: `99549e41a1dd1db4ec0e9e7a1bfd2f441c5fb4830f5c7592e1e026a07f15a742`
- Mastery delivery 1: `f48b9578bc10651e558f403c26a9e62e4e98006100212ab90a6aad12a64dcbbf`
- Mastery delivery 2: `d435d80ae53761c161a81fd61dd3dc9657d80e6d12be68c159245bfe3b1bbf6b`
- Mastery delivery 3: `f39b1a62a000c84af59abdcd047fb7847b03e21fe28501311d7e89cd5a76edc0`

No incorrect submissions or unresolved challenge answers.

## Retained sources

- [later/writeups/day-13/mobile-keystore-misuse.md](../../source-notes/later/writeups/day-13/mobile-keystore-misuse.md)
