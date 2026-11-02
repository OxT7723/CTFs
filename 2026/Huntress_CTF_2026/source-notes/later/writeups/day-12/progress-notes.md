> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 12 progress

Checked the Day 12 list after a 7 second wait; it appeared on the second
request. No request used `run_for_time:true`.

## Mode status

| Challenge | Single Solve | Time Trial | Mastery |
| --- | --- | --- | --- |
| Back at You | CORRECT | CORRECT | CORRECT (practice) |
| Managed Expectations | CORRECT | CORRECT | CORRECT |
| AutoIt Takes Two | CORRECT | CORRECT | CORRECT |
| Pascal's Wager | CORRECT | CORRECT (practice) | CORRECT (practice) |
| SQLite Assumptions | CORRECT | CORRECT | CORRECT |

All fifteen modes are marked solved by the live list. The Game Master
returned `CORRECT` for those modes; it did not include point totals. No result
reported pending CourseStack scoring.

## Solving notes

- **Back at You:** the single and timed blobs decode by reversing their
  downloaded bytes. The mastery archive has 58 blobs with 12 numbered mixed
  encodings, with the last row reversed. All 58 candidates are saved in
  `work/day-12/warmups/2997aae7-5561-4371-88c5-f4d8959d4bd7/candidate-answers.json`.
  Its artifact SHA-256 is
  `e287ad6ea20e523c1b184114603d9730550a5933d063805e83c70d824b38c502`.
  The mastery deadline was `2026-10-12T13:01:20.548Z`; the eventual submit
  returned `expired`. `retry` and the first `practice` request returned
  `retry_variants_unavailable`; a later practice continuation succeeded.
  Practice attempt `8c2227b9-67ac-4623-88c3-fd46e4b54abc` had no deadline and
  returned `CORRECT` for all 58 answers.
- **Managed Expectations:** read the MVID from the CLR metadata Module row and
  its GUID heap for each assigned DLL. The MVID helper is now in
  `metadata-forensics-tools/pe_metadata.py`, and the metadata runner dispatches
  MVID questions to it. The accepted MVIDs were
  `21e410f3-c977-465c-80eb-6890ddd3085c` (Single Solve),
  `9e0e197f-d610-4ec9-bd1c-d28da985893a` (Time Trial),
  `2658bcc7-f07c-48b1-8cb9-2bb645f8680e` and
  `ecc37f87-9668-43c5-b9f4-011ee0d07c7c` (Mastery). All three modes returned
  `CORRECT`.
- **AutoIt Takes Two:** reused the static script-analysis solver on the
  encrypted evidence archive (password `infected`); specimens were analyzed as
  data and not executed. The contract contained 855 questions in Single Solve
  and Time Trial, and 1,710 in Mastery. The solver now maps an `If True Then`
  wrapper to the accepted `direct` control-flow value. All three modes returned
  `CORRECT`; attempt records and answer maps are under
  `work/day-12/script-analysis/`.
- **Pascal's Wager:** the encrypted evidence archive SHA-256 is
  `261fb7a322704944b2dba6d8638b9dc2913e0f91c1905bd2764fccc5c06582fc`.
  The reusable binary analyzer extracted and validated the HCFG records from
  the bundled specimens. The earlier 119 accepted answers were preserved; the
  remaining `d12_analysis_format` value was the lowercase string `elf`.
  Submitting it returned `CORRECT` with flag
  `26df1ff9bd1e5de5a745cd0a11a97861`. Its Time Trial's first timed attempt
  expired before answers were accepted; the same assigned archive was later
  completed in untimed practice attempt
  `0cb6ce8c-b24d-4c79-80af-235fdff8ce45` with flag
  `fb8206b1c1b31e48494e1470f1760556`.
  Mastery's first timed attempt
  `7b3940be-445e-4bee-8c06-469c93c99dc8` expired after 180 of 360 answers
  were accepted. Practice attempt `870a92bd-5ff2-4db8-b1e2-4f4c82fee1da`
  continued the same three assigned evidence sets without a deadline. Its
  initial answer map had one error: `set2.d10_analysis_has_hcfg_section` was
  `false`, but the assigned PE has a `.hcfg` section. The analyzer now parses
  PE section headers as well as ELF section headers; it produced `true` for
  that specimen. Submitting the corrected remaining 141 IDs returned
  `CORRECT` with flag `27e26280212bc562444a3dc08e84b5e7`. Attempt records,
  artifacts, answer maps and recovery submissions are under
  `work/day-12/binary/`. The mode runner checks for `pyzipper` before timed
  starts; the binary tools' `.venv` has the declared requirements installed.
- **SQLite Assumptions:** the APK asset declares codec `hex`; decode the
  `data` value directly from hex to recover the answer code. The existing
  Mobile solver supports this codec now. All three modes returned `CORRECT`;
  attempt records are under `work/day-12/mobile-android/`.

## Flags and artifact hashes

- Back at You Single Solve: flag `671c82a8b0418f0fafd630c0f5b52c61`;
  artifact SHA-256 `e1143dc727cac903c8456ddb1f85c91ab88c48da6650a1bb4be1cd5c571c2ac9`.
- Back at You Time Trial: flag `391cebab460ad762944eec6a194bc9a0`;
  artifact SHA-256 `3f4c1210fd9f4124521e09a4f4c45b7b9ee5aa80683a9913c539287abb972ef2`.
- Back at You Mastery practice: flag `a27ca6da98aba3bd978fadc579208fe4`;
  artifact SHA-256 `e287ad6ea20e523c1b184114603d9730550a5933d063805e83c70d824b38c502`.
- Managed Expectations: flags `65b65b79543c2019e0128b3ac68def5e`,
  `9d48a41b9228fb0dfd35ec81ba95b1ba`, and
  `ccfb43750320d9cf3d4f8c060e05ca2e` for Single Solve, Time Trial, and Mastery.
- AutoIt Takes Two: flags `9e0735dd3fa3c12c6edfc3576cfde54c`,
  `b0d5181cafc9eafa59901666eb5e9baf`, and
  `b48b3ec25ecbc5325fdcd009ca0a895f` for Single Solve, Time Trial, and Mastery.
- SQLite Assumptions: flags `943ff33ac74dfd5bb340ffedaef7cc7a`,
  `7097581f3f04d6ffbb990c5c62c02c4a`, and
  `3acf1f7261d53b0546f12b8a7eb2ec13` for Single Solve, Time Trial, and Mastery.
- Pascal's Wager Time Trial practice: flag `fb8206b1c1b31e48494e1470f1760556`;
  artifact SHA-256 `4b369d148d260ae171a3e758d5efd2a0013cb89d4a3770375785fa6dce5633e2`.
- Pascal's Wager Mastery practice: flag `27e26280212bc562444a3dc08e84b5e7`;
  artifact SHA-256 values `6111ef816a0097a77eeaeb47033ed7e5445d5781a40c0058a51731993510cfe7`,
  `0d8319674bee1a3fa40b088a76d27d8f5db025135e225138f0707c057d669b2b`, and
  `9ccd37df3af2575e15545f072aa05f2d3d97f176ea0722c81f98ee45bc055b0b`.

Detailed flags, deadlines, and per-variant SHA-256 values for Script Analysis
and Mobile are in the attempt `run-summary.json` files.
