# Hive Mind

Day 25 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 25 Metadata Forensics — Hive Mind

All three released modes completed with `CORRECT`. Game Master status confirms
every answer accepted; no response reported CourseStack scoring as pending.
The Time Trial and Mastery runs used regular untimed play
(`run_for_time: false`).

| Mode | Attempt | Accepted | Assigned artifact SHA-256 |
| --- | --- | ---: | --- |
| Single Solve | `91c7f372-4139-4e48-be4a-6638fe2488de` | 1 / 1 | `4f27b3dc62638d4ceca4c42ad5b90329083349f38188995421b809c8bbfb190a` |
| Time Trial | `a3f3c23a-1904-4dd2-af3a-b08f6dd68658` | 30 / 30 | `b2b553a1633b8be25f9580a3b0063f464f36d3a0b37b613b047ab6b003c9b7d9` |
| Mastery | `2f95c99d-d56e-48bf-816e-bd25d7e2eacd` | 270 / 270 | `e252f689bdb13e76fc67cab19c8c6e60e2d916f0a41c0824907abb089b377f30` |

Added a reusable REGF root-key-name reader and wired it into
`metadata-forensics-tools/run_challenge.py`. Installed the already-declared
`python-evtx` dependency in the metadata tools virtual environment so the
existing EVTX handler can run.

Attempt artifacts, candidate answers, submissions, and status responses are
saved under
`metadata-forensics-tools/attempt-records/metadata-forensics-day-25-hive-mind/`.

## Retained sources

- [later/writeups/day-25/metadata-forensics-hive-mind.md](../../source-notes/later/writeups/day-25/metadata-forensics-hive-mind.md)
