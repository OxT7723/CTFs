> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 18 Mobile: Encrypted Strings

All three Mobile modes are complete. Time Trial and Mastery used the regular
untimed route (`run_for_time: false`); all submissions returned `CORRECT`, and
the refreshed Game Master list marks each route solved. Mastery accepted all
five answer IDs. Status responses did not include a CourseStack point total.

## Method

`mobile-android-tools/run_modes.py` resumed or started each current attempt,
downloaded its APK bytes, checked each SHA-256, decoded the declared XOR JSON
asset with `decode_puzzle_assets.py`, matched the live answer format, and
submitted using the exact answer IDs from that attempt. The existing reusable
tool handled all variants without changes.

## Results and artifacts

| Mode | Attempt | Accepted answers | Result |
| --- | --- | --- | --- |
| Single Solve | `662c65e9-cd60-4423-b79f-4f51e711bef1` | `answer` | `CORRECT` |
| Time Trial | `f6319f74-b343-4654-af5f-6107b86b7128` | `answer` | `CORRECT` |
| Mastery | `d2615b30-99f7-412a-9d33-67fe21cc6ae9` | `set1.answer`–`set5.answer` | `CORRECT` (5/5) |

- Single Solve — encrypted_strings.apk (retired artifact link; see artifact inventory) — SHA-256 `3df51a8bdf3790cd5b9d93f57fc0869fcb3ba07a66d85b27e504b8d56443367e`
- Time Trial — encrypted_strings_time_trial.apk (retired artifact link; see artifact inventory) — SHA-256 `26b11bb96ac45b535b68024a8652390a928779b28fb94a6ffa46a19dc0204f86`
- Mastery delivery 1 — encrypted_strings_mastery_01.apk (retired artifact link; see artifact inventory) — SHA-256 `ee0e425ea9d86f0e28dc400f7f40abda4010d313eccfcf5ba7516ab850259cc4`
- Mastery delivery 2 — encrypted_strings_mastery_02.apk (retired artifact link; see artifact inventory) — SHA-256 `abe50d9720025afbf4d80b9b1ccb36a038fe108234b251c8e17a9715a0d0781d`
- Mastery delivery 3 — encrypted_strings_mastery_03.apk (retired artifact link; see artifact inventory) — SHA-256 `a7050550ceb6d16f92b6cb6fed8df7cb2d41c6d3ceffc284dd3827e16ba4fd51`
- Mastery delivery 4 — encrypted_strings_mastery_04.apk (retired artifact link; see artifact inventory) — SHA-256 `98c80863d3d9d7808d608fd3ca527572afda095232f4d540c1852f0eaaabebb2`
- Mastery delivery 5 — encrypted_strings_mastery_05.apk (retired artifact link; see artifact inventory) — SHA-256 `27ea8588ecdf914d27606ff6fd6da34f2e724842cb184071c47b077b4411df20`
