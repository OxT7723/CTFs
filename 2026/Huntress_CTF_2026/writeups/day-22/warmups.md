# Deflated Ego

Day 22 · Warmups · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 22 Warmups: Deflated Ego

- Challenge ID: `warmups-day-22`
- Completed Single Solve, regular untimed Time Trial, and regular untimed Mastery.
- Mastery accepted all 108 answer IDs. Game Master status was `CORRECT` for all three modes.
- The artifacts combine the numbered mixed-codec rows with independently encoded suffix rows. Some suffixes are Base64-wrapped gzip or zlib text; others use hex-encoded UTF-16 or Rail Fence.
- `warmup-tools/decode_base64_layers.py` now inflates gzip/zlib and resolves wrapped suffixes while rejecting invalid text candidates. It also falls back to per-bundle rail decoding when the inferred rail count is ambiguous.
- Attempt records and downloaded bytes are under `work/day-22/warmups/`.

## Retained sources

- [later/writeups/day-22/warmups-deflated-ego.md](../../source-notes/later/writeups/day-22/warmups-deflated-ego.md)
