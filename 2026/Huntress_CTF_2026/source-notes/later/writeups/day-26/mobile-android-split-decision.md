> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 26 Mobile: Split Decision

- Challenge: `mobile-android-day-26-split-decision`
- Prompt: Reassemble evidence distributed across base and configuration splits.
- Answer format for every question: `ANS-` followed by exactly 16 uppercase
  hexadecimal characters; no spaces or explanatory text.
- Single Solve and Time Trial each asked for one exact backend answer code.
  Mastery asked for ten codes under `set1.answer` through `set10.answer`.
- All three regular submissions returned `CORRECT`; the Day 26 Mobile listing
  marks all three modes solved. The status API exposed no pending scoring state
  or points total.
- No attempt had a deadline. No `run_for_time:true` request was used.

## Method and tooling

Single Solve split the answer between `base.apk` and an indexed feature asset.
Time Trial used the `analysis` codec: the static DEX evaluator followed
`Release.code`, resolved `Assets.readSplit` from the assigned configuration
APK, and emulated long shift instructions. Mastery contained ten independently
assigned deliveries. All APK and APKS content was read as data; no challenge
code was installed or executed.

`mobile-android-tools/run_modes.py` verified the current attempt's artifact
hashes, matched each decoded value against that attempt's answer format, and
submitted using its exact answer IDs.

## Results

| Mode | Attempt | Answers | Result |
| --- | --- | --- | --- |
| Single Solve | `4643bbe3-4aef-40dd-9e69-94fdf8203a2a` | `answer` | `CORRECT` |
| Time Trial | `05a1a615-1562-41e3-a7f6-3adc9af36f5a` | `answer` | `CORRECT` |
| Mastery | `28542a12-8a40-4aeb-8d39-3c33b63209a5` | `set1.answer`–`set10.answer` | `CORRECT` (10/10) |

Mastery cases were `MOB-02-6F54C6EBFD`, `MOB-03-EDD4F0CB41`,
`MOB-06-67B8465AD3`, `MOB-11-D3FC05DEC5`, `MOB-13-3F0FC41C60`,
`MOB-16-C743CFEEF1`, `MOB-19-63406CAED4`, `MOB-21-CF04E410EA`,
`MOB-25-207F6FAC45`, and `MOB-26-704CE43289`. Each asked the same
split-evidence question and used the answer format above.

## Assigned artifacts

These packages contain the base and configuration-split evidence for their
corresponding attempt or Mastery delivery.

- Single Solve — split_decision.apks (retired artifact link; see artifact inventory) — SHA-256 `98b2c4c91ede6808501aede0045d98f34bed1a1809938061d20a5a2f1dee1449`
- Time Trial — split_decision_time_trial.apks (retired artifact link; see artifact inventory) — SHA-256 `6cedb3399706d58e1d39f3ceb9f76aa65ac9feec04e7c5e4e1c7bf49aefce9d6`
- Mastery delivery 1 — split_decision_mastery_01.apk (retired artifact link; see artifact inventory) — SHA-256 `bdbdab34d724eebc01f5276a802a24607be046c1390cea9b138f20c375e85fa3`
- Mastery delivery 2 — split_decision_mastery_02.apk (retired artifact link; see artifact inventory) — SHA-256 `94f90352719de7d6c58baa22a0c42ed18640aaa4d65d75ecc309ad58934d5563`
- Mastery delivery 3 — split_decision_mastery_03.apk (retired artifact link; see artifact inventory) — SHA-256 `54a2f23c3cd9efe8251143ed26944c15de14b5627094d58c69556bbe61b4d27d`
- Mastery delivery 4 — split_decision_mastery_04.apk (retired artifact link; see artifact inventory) — SHA-256 `8b02513c302c65553afb7f9719990aa899d669dd348d2dacc7b3e201aca54ae3`
- Mastery delivery 5 — split_decision_mastery_05.apk (retired artifact link; see artifact inventory) — SHA-256 `1883d02c7f9cd8eed176d096608c60131ad70fc9914463cf298d3092748c446f`
- Mastery delivery 6 — split_decision_mastery_06.apk (retired artifact link; see artifact inventory) — SHA-256 `7a811843b6b558d2b344a2e4041c3d5896c149e477db256531bf610738eba019`
- Mastery delivery 7 — split_decision_mastery_07.apk (retired artifact link; see artifact inventory) — SHA-256 `486d3a2ed81b0f316216d57d2da9542b823191589046314838870008af3cdc88`
- Mastery delivery 8 — split_decision_mastery_08.apk (retired artifact link; see artifact inventory) — SHA-256 `cce9fa39988444942bb8706ba81e4f09d04cee448bf359605de09dcdada16acc`
- Mastery delivery 9 — split_decision_mastery_09.apk (retired artifact link; see artifact inventory) — SHA-256 `1bf8cef2953937ac1b12b8a8f916292410feca6155c77dab97cd102e1761fe55`
- Mastery delivery 10 — split_decision_mastery_10.apks (retired artifact link; see artifact inventory) — SHA-256 `a2d7c021f9c86c4c81af8d7929df44059d7fe78dc1515b88366b9e635ed355da`
