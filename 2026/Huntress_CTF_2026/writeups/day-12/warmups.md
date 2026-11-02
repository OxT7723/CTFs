# Back at You

Day 12 · Warmups · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `warmups-day-12`.

## Decoding approach

The prompt was “Maybe we started at the wrong end.” The retained Day 12 account says the Single Solve and Time Trial blobs were decoded by reversing their downloaded bytes. The answer was the slug on the final non-empty decoded line.

Mastery assigned a ZIP containing **58 blobs**. Its recorded layout combined twelve numbered mixed-encoding rows, with the last row reversed. The session generated a candidate map for the exact question IDs rather than reusing a previous instance’s answers.

## Recorded outcomes

| Mode | Saved result | Qualification |
| --- | --- | --- |
| Single Solve | `CORRECT` | Recorded in the Day 12 progress note |
| Time Trial | `CORRECT` | Recorded completion; no independent timing claim here |
| Mastery | `CORRECT`, 58 answers | Completed through an untimed practice continuation after the initial deadline expired |

The initial Mastery submission returned `expired` after the deadline `2026-10-12T13:01:20.548Z`. The first retry and practice requests returned `retry_variants_unavailable`; a later practice continuation had no deadline and accepted all 58 answers. The eventual completion must therefore not be presented as a successful ranked timed Mastery run.

## Recorded artifact fingerprints

| Assignment | SHA-256 |
| --- | --- |
| Single Solve | `e1143dc727cac903c8456ddb1f85c91ab88c48da6650a1bb4be1cd5c571c2ac9` |
| Time Trial | `3f4c1210fd9f4124521e09a4f4c45b7b9ee5aa80683a9913c539287abb972ef2` |
| Mastery | `e287ad6ea20e523c1b184114603d9730550a5933d063805e83c70d824b38c502` |

The original attempt directories and candidate JSON files named by the progress note were not retained in the publication package. These hashes and outcomes are attributed to that saved account; the challenge was not replayed during publication preparation.

## Retained sources

- [early/12-Back_at_You/readme.md](../../source-notes/early/12-Back_at_You/readme.md)
- [later/writeups/day-12/progress-notes.md](../../source-notes/later/writeups/day-12/progress-notes.md)
