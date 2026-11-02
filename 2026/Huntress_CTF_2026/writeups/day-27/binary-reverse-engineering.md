# Compiler Says What

Day 27 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 27 — Compiler Says What

Completed the regular, untimed Single Solve, Time Trial, and Mastery modes.
The Game Master reports `CORRECT` for all three; final status shows 324/324,
324/324, and 3,564/3,564 accepted answer fields, respectively. None had a
deadline. The proxy returned no separate point total or pending scoring state.

The evidence bundles carry the Day 1–27 binary catalog plus Day 27 GCC and TCC
ELF variants. The category solver now selects the GCC/TCC specimens by filename,
classifies their parsed containers, reads `e_machine` numerically, and scans
backward for CRC32-valid HCFG records. Shared HCFG answers are used only after
the two role payloads match byte for byte. Mastery uses the same logic for each
numbered set.

Reusable tool updates are in `binary-reverse-engineering-tools/analyze_evidence.py`
and documented in that directory's README. Attempt artifacts, candidate
answers, and final status responses are preserved under `work/day-27/binary/`.

## Retained sources

- [later/writeups/day-27/binary-compiler-says-what.md](../../source-notes/later/writeups/day-27/binary-compiler-says-what.md)
