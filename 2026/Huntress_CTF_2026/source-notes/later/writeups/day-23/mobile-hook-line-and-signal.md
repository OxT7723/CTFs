> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 23 Mobile: Hook Line and Signal

All three modes returned `CORRECT`; timed-by-default routes used regular,
untimed play (`run_for_time: false`) and had no deadline. The final Game Master
statuses accepted every answer ID. Its responses did not include a points
total or separate CourseStack scoring field.

## Method and reusable tooling

Single Solve used an XOR-encoded JSON asset. The Time Trial and Mastery APKs
used the `analysis` codec: follow the actual `Release.code` call chain and
evaluate the reachable DEX instructions, rather than choosing similarly named
decoy methods. The Mastery bundle included seven APKs, spanning earlier mobile
cases as well as Day 23. Its Day 15 set included an x86_64 JNI arithmetic
routine; the solver statically emulates that function from `objdump` output
without loading the library.

`mobile-android-tools/decode_puzzle_assets.py` recognizes the analysis codec,
and `mobile-android-tools/solve_analysis_codec.py` evaluates its reachable
DEX/native call chain. `run_modes.py` chooses each candidate using the live
question's answer format and assigned delivery. Install the declared
requirements before using the analysis codec.

## Results

| Mode | Attempt | Accepted IDs | Result |
| --- | --- | --- | --- |
| Single Solve | `37066b2a-fb98-40b9-bfe5-d86ac101ad9c` | `answer` | `CORRECT` |
| Time Trial | `24aa2ceb-7c9a-4739-9ffb-3f8fc53ada6f` | `answer` | `CORRECT` |
| Mastery | `8a4a3625-2c69-4f0e-be54-e82fb89227fb` | `set1.answer`–`set7.answer` | `CORRECT` (7/7) |

## Assigned artifacts

- Single Solve — hook_line_and_signal.apk (retired artifact link; see artifact inventory) — SHA-256 `96e3081d96ae70312c09f73ab8d4b003e71ff0309936affe9f5aa5c29c10c155`
- Time Trial — hook_line_and_signal_time_trial.apk (retired artifact link; see artifact inventory) — SHA-256 `05a9acb4595ee95fa52236933b5a8aeadc177cca1359edb3f9107a69baf5d15c`
- Mastery delivery 1 — hook_line_and_signal_mastery_01.apk (retired artifact link; see artifact inventory) — SHA-256 `8f5510cd9a33ab38eb33e1af00bbc82c88a9a72b2fa45a044632f5f052203a45`
- Mastery delivery 2 — hook_line_and_signal_mastery_02.apk (retired artifact link; see artifact inventory) — SHA-256 `43cd67380096a2a7dee6199b043478c42e17d0bb96f4664ede409b59db2780df`
- Mastery delivery 3 — hook_line_and_signal_mastery_03.apk (retired artifact link; see artifact inventory) — SHA-256 `6226bc4ee996d563f864f6253c0e1ac32e874e51bd88a6b9b6d5345661f9a8f8`
- Mastery delivery 4 — hook_line_and_signal_mastery_04.apk (retired artifact link; see artifact inventory) — SHA-256 `ff386d23aa72b3c78e300b8e3f687756b54950fb02df3163ff1ff63e7b9f25f3`
- Mastery delivery 5 — hook_line_and_signal_mastery_05.apk (retired artifact link; see artifact inventory) — SHA-256 `bca12604d8c33899367810942838a239605d4e23a9c061671a928196c431f1d2`
- Mastery delivery 6 — hook_line_and_signal_mastery_06.apk (retired artifact link; see artifact inventory) — SHA-256 `1035c5463ac19a77cfec1c9e313a8f968a35b035de2286577c3322388c5dff12`
- Mastery delivery 7 — hook_line_and_signal_mastery_07.apk (retired artifact link; see artifact inventory) — SHA-256 `699f08eb6022d369b1301aef60a8b429b4c1622c2163080dd01f21f963f20518`
