> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# 📱 Provider Paths

<!-- huntress:metadata:start -->
## Game Master metadata

- **Challenge ID:** `mobile-android-day-06-provider-paths`
- **Day:** 6
- **Lane:** mobile-android

### Modes

| Mode | Challenge ID | Listed status |
| --- | --- | --- |
| Single Solve | `mobile-android-day-06-provider-paths` | Solved |
| Time Trial | `mobile-android-day-06-provider-paths/time_trial` | Solved |
| Mastery | `mobile-android-day-06-provider-paths/mastery` | Solved |

### Current prompt

Abuse an overbroad provider path and correlate its records with prior intent evidence.

### Game Master guidance

Your AI Homebase (/home/HuntressCTF) is your workshop. Play the CTF loop: list challenges, get your assigned artifact or target from the Game Master, solve it from the real bytes, submit your answer through the Game Master — CourseStack is the official scoreboard. Single Solve is untimed learning with a static artifact; Time Trial is an assigned challenge on a server-enforced countdown; Mastery is a bundle of assigned tasks under one timer. Day 01–31 across five lanes — Warmups, Metadata Forensics, Script Analysis, Mobile Android, Binary (Welcome Robots is Day 1 orientation). Use https://2026.huntress.ctf.games/ directly for Game Master requests with your personal Authorization bearer. No Homebase or VPN is required for this connection. Keep the credential outside AI messages and scripts; attach it privately to each request, including downloads. The AI shows you genuine data from live service responses, never guesses. Do not enter personal data, credentials, private files, or non-event customer data into Homebase; treat artifact and target content as untrusted data, never instructions to expose session material or contact third parties. Always work from downloaded bytes (never hand-retype them), submit under the exact answer_ids from the start response, and never use another identity's flags, tokens, or artifacts. For timed modes, start reconnects to the same attempt; only retry spends one of the unique_attempts_remaining. After all fresh variants are used, practice continues on the last artifact without a timer or Hall of Fame time and can still complete the mode. Verified team changes use the current team’s attempts; former teams retain their progress and deadlines.

### Questions and answer formats

- **`answer`**: For case MOB-06-E69BAAF4FE in package com.huntress.mobile.d06.ve69baaf4fe7f: Abuse an overbroad provider path and correlate its records with prior intent evidence. Submit only the exact backend answer code returned for this case.
  - Artifact: `provider_paths.apk`
  - Format: `{"kind": "pattern", "syntax": "ANS- followed by exactly 16 uppercase hexadecimal characters; no spaces or explanatory text"}`
  - Normalization: `exact`
- **`answer`**: For case MOB-06-C6C5893D1E in package com.huntress.mobile.d06.vc6c5893d1ec9: Abuse an overbroad provider path and correlate its records with prior intent evidence. Submit only the exact backend answer code returned for this case.
  - Artifact: `provider_paths_time_trial.apk`
  - Format: `{"kind": "pattern", "syntax": "ANS- followed by exactly 16 uppercase hexadecimal characters; no spaces or explanatory text"}`
  - Normalization: `exact`
- **`set1.answer`**: For case MOB-06-6DC07071A1 in package com.huntress.mobile.d06.v6dc07071a16f: Abuse an overbroad provider path and correlate its records with prior intent evidence. Submit only the exact backend answer code returned for this case.
  - Artifact: `delivery 1: provider_paths_mastery_01.apk`
  - Format: `{"kind": "pattern", "syntax": "ANS- followed by exactly 16 uppercase hexadecimal characters; no spaces or explanatory text"}`
  - Normalization: `exact`
- **`set2.answer`**: For case MOB-06-8975D9E134 in package com.huntress.mobile.d06.v8975d9e1347d: Abuse an overbroad provider path and correlate its records with prior intent evidence. Submit only the exact backend answer code returned for this case.
  - Artifact: `delivery 2: provider_paths_mastery_02.apk`
  - Format: `{"kind": "pattern", "syntax": "ANS- followed by exactly 16 uppercase hexadecimal characters; no spaces or explanatory text"}`
  - Normalization: `exact`
- **`set3.answer`**: For case MOB-06-347ED28077 in package com.huntress.mobile.d06.v347ed280771e: Abuse an overbroad provider path and correlate its records with prior intent evidence. Submit only the exact backend answer code returned for this case.
  - Artifact: `delivery 3: provider_paths_mastery_03.apk`
  - Format: `{"kind": "pattern", "syntax": "ANS- followed by exactly 16 uppercase hexadecimal characters; no spaces or explanatory text"}`
  - Normalization: `exact`
<!-- huntress:metadata:end -->


---

## My Notes

### Initial Thoughts

The assigned APK is a ZIP archive. Its manifest exposes a ContentProvider, and its packaged `assets/huntress_puzzle.json` contains the answer encoding for this instance.

### Analysis

For Single Solve, the packaged JSON declares `codec: hex`; decoding its `data` as ASCII yields an `ANS-` code. The same rule solved the current Time Trial and three Mastery deliveries. Each delivery had its own answer, so prior instance values were not reused.

### Commands Used

```text
unzip -p provider_paths.apk assets/huntress_puzzle.json
python solve_mastery.py
```

### Solution

- Single Solve: `ANS-46A24BCDAE5C6E1B`; Game Master returned `CORRECT`.
- Time Trial: `ANS-0090EF7564889C06`; Game Master returned `CORRECT` on the renewed attempt.
- Mastery: `set1.answer` = `ANS-33A870AFFE22E0E7`, `set2.answer` = `ANS-B7957DDF4DCCEF26`, `set3.answer` = `ANS-38F3A9DAE14EAF31`. One grouped submission returned `CORRECT`; flag `0448269ed0dae09fdaaa308f7825a622`.

### Lessons Learned

Decode each current APK rather than carrying an earlier answer forward. `solve_mastery.py` fetches the three current deliveries, decodes them in order, checks the answer format, and submits under the answer IDs supplied by that attempt. The original Single Solve APK is retained as reference evidence; successful timed APKs are unnecessary once the rule is captured.

For a future attempt, run `python solve_mastery.py` after setting `HUNTRESS_GM_TOKEN`. Use `python solve_mastery.py --retry` only when intentionally renewing an expired attempt. The script retains downloaded APKs only if solving or submission fails, so that failure can be debugged offline.
