# SQLite Assumptions

Day 12 · Mobile / Android · **Evidence summary**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `mobile-android-day-12-sqlite-assumptions`.

## Challenge

Reconstruct authorization from a synthetic SQLite cache and prove server-side impact.

The saved assignment asks, for example:

- For case MOB-12-4B4FA1A323 in package com.huntress.mobile.d12.v4b4fa1a3235d: Reconstruct authorization from a synthetic SQLite cache and prove server-side impact. Submit only the exact backend answer code returned for this case.

## Recorded AI approach

The shared day notes retain the following challenge-specific account:

the APK asset declares codec `hex`; decode the
  `data` value directly from hex to recover the answer code. The existing
  Mobile solver supports this codec now. All three modes returned `CORRECT`;
  attempt records are under `work/day-12/mobile-android/`.

## Recorded result

The historical challenge-state snapshot records:

| Mode | Listed solved | Status result |
| --- | --- | --- |
| single_solve | True | CORRECT |
| time_trial | True | CORRECT |
| mastery | True | CORRECT |

These are retained service-state values, not a fresh check. They do not by themselves establish a ranked timed completion or a CourseStack points total.

## Evidence retained

- [Original challenge notes](../../source-notes/early/12-SQLite_Assumptions/readme.md)
- [Saved challenge state](../../source-notes/early/12-SQLite_Assumptions/challenge_state.json)
- [Reusable tooling guide](../../tools/later/mobile-android-tools/README.md)
- [Shared day notes](../../source-notes/later/writeups/day-12/progress-notes.md)

This short record preserves what the available material supports. The original AI transcript and a complete per-attempt command/output trail are not included here; no challenge was rerun to fill those gaps.

## Retained sources

- [early/12-SQLite_Assumptions/readme.md](../../source-notes/early/12-SQLite_Assumptions/readme.md)
- [later/writeups/day-12/progress-notes.md](../../source-notes/later/writeups/day-12/progress-notes.md)
