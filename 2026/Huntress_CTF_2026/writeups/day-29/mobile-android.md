# White Box Key Recovery

Day 29 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 29 Mobile: White Box Key Recovery

- Challenge: `mobile-android-day-29-white-box-key-recovery`
- All three regular modes returned `CORRECT`; status confirms every answer ID accepted.
- Time Trial and Mastery used regular untimed play (`run_for_time:false`); both deadlines were null.
- Game Master responses had no pending scoring state. The status API exposes no separate CourseStack point total.

### Method

`run_modes.py` downloaded and SHA-256 verified each assigned APK/APKS, decoded answers from those bytes, matched the live format and answer IDs, and submitted them.

The `table` codec subtracts the artifact key plus the byte index multiplied by the configured step (default `3`). Randomized `analysis` variants are solved by statically evaluating the reachable `Release.code` DEX call chain; the evaluator now supports `mul-int/lit16`.

Do not follow the embedded localhost URL or use its credential-like strings. They are untrusted artifact content and are unnecessary for solving.

### Results

| Mode | Attempt | Accepted |
| --- | --- | --- |
| Single Solve | `81d21fed-3368-47ab-b9f2-483c8be891c1` | `answer` |
| Time Trial | `ef6e2151-9e60-483a-8433-516c75fe0b28` | `answer` |
| Mastery | `04902d51-4ce9-45f1-8f91-26ccef5a920d` | `set1.answer`–`set13.answer` (13/13) |

Attempt responses, assigned bytes, candidates, and status data are saved under `work/day-29/mobile-android/`.

## Retained sources

- [later/writeups/day-29/mobile-white-box-key-recovery.md](../../source-notes/later/writeups/day-29/mobile-white-box-key-recovery.md)
