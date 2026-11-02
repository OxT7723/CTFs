# Little Things

Day 19 · Warmups · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 19 Warmups: Little Things

The artifact combines numbered mixed-codec fragments with a Rail Fence
fragment and a hex-encoded, BOM-marked UTF-16LE suffix. Some decoded hex begins
immediately after a plaintext character that is also valid hex, so the solver
checks suffix boundaries against the requested slug format. Mastery uses one
shared Rail Fence setting across its bundle; the runner infers that setting
from all assigned blobs before preparing the 93 answers.

`warmup-tools/decode_base64_layers.py` handles the suffix decoding and
`warmup-tools/run_modes.py` performs bundle-level rail inference.

All modes completed:

- Single Solve: `warmups-day-19`
- Time Trial: `warmups-day-19/time_trial`
- Mastery: `warmups-day-19/mastery` (93/93 answers)

All three Game Master statuses returned `CORRECT`. Attempt records and assigned
bytes are under `work/day-19/warmups/`. The status responses had no separate
CourseStack points field and none reported pending scoring.

## Retained sources

- [later/writeups/day-19/warmups-little-things.md](../../source-notes/later/writeups/day-19/warmups-little-things.md)
