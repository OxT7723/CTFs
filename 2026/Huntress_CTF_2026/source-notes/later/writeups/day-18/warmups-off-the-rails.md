> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 18 Warmups: Off the Rails

The blob combines numbered mixed-codec fragments with a Rail Fence encoded
slug tail. Rows 1–17 select the codec by row number; the final short row is a
Rail Fence fragment. Decoding the mixed rows can leave adjacent hexadecimal
text inside the slug, so use the live answer format to find the hex span that
produces the required slug shape.

`warmup-tools/decode_base64_layers.py` now handles Rail Fence transpositions
and a final Rail Fence suffix row. `warmup-tools/run_modes.py` can decode
hexadecimal spans between readable slug fragments.

All modes completed:

- Single Solve: `warmups-day-18`
- Time Trial: `warmups-day-18/time_trial`
- Mastery: `warmups-day-18/mastery` (88/88 answers)

Attempt records and exact assigned bytes are under `work/day-18/warmups/`.
