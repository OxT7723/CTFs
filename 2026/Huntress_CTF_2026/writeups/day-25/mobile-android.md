# Integrity Signals

Day 25 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 25 Mobile: Integrity Signals

- Challenge: `mobile-android-day-25-integrity-signals`
- Modes completed: Single Solve, regular Time Trial, regular Mastery (9 answers)
- All submissions returned `CORRECT`; the Day 25 Mobile listing marks all
  three modes solved.
- The Game Master responses contained no CourseStack points total or pending
  scoring status.

### Method and tooling

The assigned APKs use the `analysis` codec. The existing static evaluator now
handles immediate integer shifts, DEX packed-switch dispatch, reflected class
and method calls, and two-argument JNI `nativeShare` methods with conditional
branches. APKs and native libraries were inspected as data; no challenge code
was loaded or executed.

The runner verified each artifact's SHA-256 against the current attempt before
decoding and submitted answers under the live answer IDs. Mastery used
`set1.answer` through `set9.answer`.

### Results

| Mode | Attempt | Answers | Result |
| --- | --- | --- | --- |
| Single Solve | `60f7503a-222d-4b1f-8094-3bcd3b173827` | `answer` | `CORRECT` |
| Time Trial | `d5fe8dbc-38e2-4cbc-a00e-04f2a6008f29` | `answer` | `CORRECT` |
| Mastery | `3cd6e70f-1252-4199-b4b2-16fe6ab15044` | `set1.answer`–`set9.answer` | `CORRECT` (9/9) |

All attempts used the regular untimed pool (`run_for_time: false`); each
response had no deadline.

### Assigned artifacts

- Single Solve — integrity_signals.apk (private download link removed) — SHA-256 `799f97a4917a2232edeec0985720501412cf3cefe2f56143d427f0421562ea1d`
- Time Trial — integrity_signals_time_trial.apk (private download link removed) — SHA-256 `8f5be995c81c3eda6e5d9cf3020b1fdc6f3fff1fcaeacf33b4b2e215031a1b17`
- Mastery delivery 1 — integrity_signals_mastery_01.apk (private download link removed) — SHA-256 `324d29edbdfab28169291d29b11a133bff5e14d41c3592b6d1b9058d315a69fa`
- Mastery delivery 2 — integrity_signals_mastery_02.apk (private download link removed) — SHA-256 `a2097290b2d0553e56ee89ba2ef9a5f22054574001ca2c2935559b39163fbf67`
- Mastery delivery 3 — integrity_signals_mastery_03.apk (private download link removed) — SHA-256 `b2d410e7f6fe7013557d576e502bb657a9b632d0982b68507cc3150d802fc466`
- Mastery delivery 4 — integrity_signals_mastery_04.apk (private download link removed) — SHA-256 `5817818a32425881af830638fc53a9d222cc58af5b9d423da9aa334c27de549c`
- Mastery delivery 5 — integrity_signals_mastery_05.apk (private download link removed) — SHA-256 `d2495808e6e4622280795a83e49b2175834dcbfd56111a9e5cb9f49f0acdf734`
- Mastery delivery 6 — integrity_signals_mastery_06.apk (private download link removed) — SHA-256 `6488060b9ed40b939f3ef6d6394a7a00951fe955e8804b6e2e96ac30ac0dc3b4`
- Mastery delivery 7 — integrity_signals_mastery_07.apk (private download link removed) — SHA-256 `67b7d727d495392e67d7381104bd6bed1d0258dba1854134c9a872603fcafa85`
- Mastery delivery 8 — integrity_signals_mastery_08.apk (private download link removed) — SHA-256 `c2485a7fd1353d6fe624e5876a6dfeb3ab77b0656c884c3d236e84e81bd7f3c6`
- Mastery delivery 9 — integrity_signals_mastery_09.apk (private download link removed) — SHA-256 `73f74181774d33b838ed507949b7fe3542e7a3480c874bc7035579666fb99c35`

## Retained sources

- [later/writeups/day-25/mobile-integrity-signals.md](../../source-notes/later/writeups/day-25/mobile-integrity-signals.md)
