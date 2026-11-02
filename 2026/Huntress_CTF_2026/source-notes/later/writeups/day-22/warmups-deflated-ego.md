> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 22 Warmups: Deflated Ego

- Challenge ID: `warmups-day-22`
- Completed Single Solve, regular untimed Time Trial, and regular untimed Mastery.
- Mastery accepted all 108 answer IDs. Game Master status was `CORRECT` for all three modes.
- The artifacts combine the numbered mixed-codec rows with independently encoded suffix rows. Some suffixes are Base64-wrapped gzip or zlib text; others use hex-encoded UTF-16 or Rail Fence.
- `warmup-tools/decode_base64_layers.py` now inflates gzip/zlib and resolves wrapped suffixes while rejecting invalid text candidates. It also falls back to per-bundle rail decoding when the inferred rail count is ambiguous.
- Attempt records and downloaded bytes are under `work/day-22/warmups/`.
