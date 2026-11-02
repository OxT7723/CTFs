# Eighty-Five Alive

Day 23 · Warmups · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Eighty-Five Alive — Warmups, Day 23

Completed Single Solve, regular untimed Time Trial, and regular untimed
Mastery. Game Master status returned `CORRECT` for all three modes; Mastery
accepted all 113 answer IDs. No Hall of Fame timed attempt was requested.

The main artifact uses Adobe ASCII85. Mastery combines numbered mixed-codec
rows with separately encoded trailing fragments: Rail Fence text, BOM-marked
UTF-16 hex, Base64-wrapped gzip/zlib, and ASCII85. Decode the trailing pieces
without continuing into a second encoding just because a short plaintext word
looks like Base64. For ambiguous fragments, try the available Rail Fence
counts and prefer the assembled instruction context `Game Master: ` before
selecting the final slug.

The reusable decoder and runner are in `warmup-tools/`. The runner now retries
an incorrect multi-answer batch one answer at a time to preserve accepted
answers and isolate unresolved IDs. Attempt records and downloaded artifacts
are under `work/day-23/warmups/`.

The Game Master responses expose completion and flags but no CourseStack
points or scoring-pending field, so points were not independently confirmed
from the scoreboard.

## Retained sources

- [later/writeups/day-23/warmups-eighty-five-alive.md](../../source-notes/later/writeups/day-23/warmups-eighty-five-alive.md)
