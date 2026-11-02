> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 17 Mobile: Name Collapse

The Mobile listing returned three routes for `mobile-android-day-17-name-collapse`.
Single Solve, Time Trial, and Mastery are all completed with Game Master status
`CORRECT`. Time Trial and Mastery used the regular untimed route; every status
response had no deadline. Mastery accepted all five answer IDs.

## Method and reusable tooling

`mobile-android-tools/run_modes.py` solved each assigned APK and verified its
SHA-256 before submission. Day 17 introduced the `indexed` codec, where each
input character is placed at its corresponding position in the supplied
permutation. Mastery also included a reversed-text delivery. Both codecs are
now supported by `mobile-android-tools/decode_puzzle_assets.py`; the other
deliveries used its existing XOR, hex, and Caesar decoders.

The solver matches decoded values against the live question format and submits
under the current attempt's answer IDs. Native code, when present, is scanned
as bytes and is never loaded or executed.

## Results

| Mode | Attempt | Accepted IDs | Result |
| --- | --- | --- | --- |
| Single Solve | `ff2cc016-418f-4a2f-ad8a-799c014139ab` | `answer` | `CORRECT` |
| Time Trial | `c6ff6dba-19b6-4aaf-abe7-dccef6dde74d` | `answer` | `CORRECT` |
| Mastery | `b1a59d45-0398-4c89-a4d8-e2f417c46bf7` | `set1.answer`–`set5.answer` | `CORRECT` (5/5) |

The Game Master list marks all three routes solved. Its status responses did
not include a CourseStack point total or a scoring-pending field.

## Assigned artifacts

- Single Solve — name_collapse.apk (retired artifact link; see artifact inventory) — SHA-256 `358a788a99058fcd82b457257e7738cf11b4e3965ee0093281e023feb714bf01`
- Time Trial — name_collapse_time_trial.apk (retired artifact link; see artifact inventory) — SHA-256 `1103c33d36b71daec828fbedc4b9626abceb8e36999a5d4879908b8b637d5b23`
- Mastery delivery 1 — name_collapse_mastery_01.apk (retired artifact link; see artifact inventory) — SHA-256 `9b2268e16a5fd260b1ad313207caf3b90a502d984f12c4449e82eeeb1cec9617`
- Mastery delivery 2 — name_collapse_mastery_02.apk (retired artifact link; see artifact inventory) — SHA-256 `cdc8284a08e2f3f559138393353910eea210363d4d5546f2b812849d0de1c6e8`
- Mastery delivery 3 — name_collapse_mastery_03.apk (retired artifact link; see artifact inventory) — SHA-256 `d44e55b7bf9ccb7f5c6183aa9edc2dbaed85263ba0cb8a4010a644ca8d3a8189`
- Mastery delivery 4 — name_collapse_mastery_04.apk (retired artifact link; see artifact inventory) — SHA-256 `8e89818086960424cbc7b1a7881de06bc87e0f87077a2c21fe20de997c708379`
- Mastery delivery 5 — name_collapse_mastery_05.apk (retired artifact link; see artifact inventory) — SHA-256 `4c91fcffb18327648d8268582bf792dab910d50cc05b49db05801f4da6f0460b`
