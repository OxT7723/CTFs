# D-Day

Day 11 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `binary-reverse-engineering-day-11-d-collection-planner`

## Later Homebase account

### Day 11 Binary: D-Day

- Challenge ID: `binary-reverse-engineering-day-11-d-collection-planner`
- Mode: Single Solve
- Evidence archive SHA-256: `4dd58e769c65b28fe7c25e63ce94005cb181e3e552f9f80c295024bcb2d744ad`
- Questions: 110

The archive uses WinZip AES and the event password `infected`. Its samples
include ELF, PE/CLI and JAR files. The reusable analyzer recovers binary
metadata and HCFG configuration records from the extracted bytes, validates
HCFG CRCs, and builds answers directly from the current API response. Single
Solve and Time Trial each accepted all 110 answers.

The Mastery assignment contains three 110-question sets. Its timed attempt
expired during analysis before submission. The Game Master reports
`next_op: practice`, but both `op=practice` and `op=retry` return
`retry_variants_unavailable`; an explicit answer submission returns
`expired`, and the untimed start form returns HTTP 409
`timed_intent_not_available`. The live list does not advertise
`run_for_time_supported`, so this is an older timed-by-default route. Status
still says `next_op: practice` with zero fresh attempts, despite retry
returning `retry_variants_unavailable`. The analyzer now handles the assigned
PE C++ RTTI and vtable symbols and built all 330 candidate answers from the
saved evidence. They are preserved with the attempt record under
`work/day-11/binary/`. A fresh offline pass reproduced all 330 candidates
with no changes; no per-question correctness feedback is available because
the Game Master still rejects practice continuation.

## Retained sources

- [early/11-D-Day/readme.md](../../source-notes/early/11-D-Day/readme.md)
- [later/writeups/day-11/binary-d-day.md](../../source-notes/later/writeups/day-11/binary-d-day.md)
- [later/writeups/day-11/progress-notes.md](../../source-notes/later/writeups/day-11/progress-notes.md)
