> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 24 Mobile: Emulator Alibi

All three modes returned `CORRECT`; filtered Game Master status confirms each
mode is solved. Time Trial and Mastery ran in the regular untimed pool
(`run_for_time: false`) with no deadline. The Game Master response did not
include a points total or a separate CourseStack scoring field.

## Method and tooling

The Single Solve asset uses a declared split codec. The randomized Time Trial
and Mastery APKs use the `analysis` codec. The existing static evaluator follows
the reachable `Release.code` method and does not execute the APK. Mastery
exposed two missing solver cases: signed `aget-byte`/`aput-byte` operations and
`objdump` continuation rows containing raw bytes but no instruction mnemonic.
Both are now handled by `mobile-android-tools/solve_analysis_codec.py`.

The Android device panel was unavailable in this environment. All answers were
recovered from the assigned APK bytes and accepted by the Game Master.

## Results

| Mode | Attempt | Accepted answer IDs | Result |
| --- | --- | --- | --- |
| Single Solve | `11cfcecc-7092-4b90-9a09-58a7cf1de3f4` | `answer` | `CORRECT` |
| Time Trial | `f00bc965-e7a1-4bef-afa2-a5073c35ced9` | `answer` | `CORRECT` |
| Mastery | `78c1d802-ff94-452d-90eb-206e2b362799` | `set1.answer`–`set8.answer` | `CORRECT` (8/8) |

## Assigned artifacts

- Single Solve — emulator_alibi.apk (retired artifact link; see artifact inventory) — SHA-256 `bd3e6f02601670af5d131cc240d7f0dde177b0751464180598a1d18943291c52`
- Time Trial — emulator_alibi_time_trial.apk (retired artifact link; see artifact inventory) — SHA-256 `ddc850616a3b1403d650a9829c43ebce3698730e787fb106b5e227c25c7a040b`
- Mastery delivery 1 — emulator_alibi_mastery_01.apk (retired artifact link; see artifact inventory) — SHA-256 `197b7ef497b0ff7d36191e0af210ca5a4505d0d63216eca22543691bc7b2707a`
- Mastery delivery 2 — emulator_alibi_mastery_02.apk (retired artifact link; see artifact inventory) — SHA-256 `ee6539c6ef0b6d0227e437f00786f16d9142ac66414e5c93eed40e6bad685dad`
- Mastery delivery 3 — emulator_alibi_mastery_03.apk (retired artifact link; see artifact inventory) — SHA-256 `8489d9049215d0f72aa762b6d24dee261b244a7ae06121cbfb69bdbb14379e3b`
- Mastery delivery 4 — emulator_alibi_mastery_04.apk (retired artifact link; see artifact inventory) — SHA-256 `cca97891b8d67d3ccb73c5df9e2c3b7d057e64dbf4359e5dfcbb98f871f47a76`
- Mastery delivery 5 — emulator_alibi_mastery_05.apk (retired artifact link; see artifact inventory) — SHA-256 `e9133bea9dc97abac4d61a615f526ee9c04e074a6172f18b48319e19de18f9a7`
- Mastery delivery 6 — emulator_alibi_mastery_06.apk (retired artifact link; see artifact inventory) — SHA-256 `34badd723eb8e9ba913f3b5bbe79fee0ffc90a6f4c80497764742a8f0f5b54b5`
- Mastery delivery 7 — emulator_alibi_mastery_07.apk (retired artifact link; see artifact inventory) — SHA-256 `12822ab696e30ce5d56ffefdeeaa60921900391ef934acecab8efb7260c7ee94`
- Mastery delivery 8 — emulator_alibi_mastery_08.apk (retired artifact link; see artifact inventory) — SHA-256 `09ccfdfe43636df1a96b4338979251e0b0a68bfa47d66815ea41778903ca86c4`
