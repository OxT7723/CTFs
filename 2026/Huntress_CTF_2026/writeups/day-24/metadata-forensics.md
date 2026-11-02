# Event Horizon

Day 24 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 24 Metadata Forensics — Event Horizon

All three regular modes completed with `CORRECT`; no response reported pending
CourseStack scoring. Attempts used regular untimed play.

| Mode | Attempt | Accepted | Assigned artifact SHA-256 |
| --- | --- | ---: | --- |
| Single Solve | `1cf3e937-3b8a-4410-8330-3d5b8675bf5f` | 1 / 1 | `6ded154983b3595bb2afa2112d1431a6895da7fbfd51d624ec0631f6b3db8841` |
| Time Trial | `02e35a1b-f4db-4347-ac11-79a0398c0263` | 29 / 29 | `44af5bc07aabbb4c15fc55c87011e588d117eaf53906003e5bab13a4ba804746` |
| Mastery | `f404a3ff-8fc5-481a-9164-e69abe393d00` | 232 / 232 | `1cce1297784fc5fa222356e58bd008612e5ad1fe9723f09b7163f1b80abfe235` |

Added `evtx_metadata.py` and an EVTX record-count handler to the reusable
runner. The assigned Single Solve log contains three readable event records.
Attempt artifacts, answer candidates, submissions, and status responses are
saved under `metadata-forensics-tools/attempt-records/metadata-forensics-day-24-event-horizon/`.

## Retained sources

- [later/writeups/day-24/metadata-forensics-event-horizon.md](../../source-notes/later/writeups/day-24/metadata-forensics-event-horizon.md)
