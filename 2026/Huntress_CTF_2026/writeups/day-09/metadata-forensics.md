# Built Different

Day 9 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `metadata-forensics-day-09-built-different`

## Later Homebase account

### Built Different

- Single Solve, Time Trial, and the 65-question Mastery bundle were accepted.
- The answers came from the assigned metadata evidence: note hashes and byte properties, image dimensions, PDF header, nested ZIP central directory, and PE COFF machine value.
- Reusable parser: `solve.py`. It reads the assigned ZIP and emits the answer map.
- PE machine values need four hex digits (for example, `0x014c`).

The downloaded evidence archives are saved here for faster repeat runs.

## Retained sources

- [early/09-Built_Different/readme.md](../../source-notes/early/09-Built_Different/readme.md)
- [later/writeups/day-09/built-different.md](../../source-notes/later/writeups/day-09/built-different.md)
