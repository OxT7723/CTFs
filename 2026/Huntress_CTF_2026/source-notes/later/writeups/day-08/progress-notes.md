> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 8 progress

## Completed

- **Entity Relations** — Single Solve, Time Trial, and Mastery accepted.
- **What’s in the Box?** — Single Solve, Time Trial, and Mastery accepted.

## Completed

- **Lost in Translation** (`script-analysis-day-08-cross-language-iocs`) — Single Solve accepted, flag `7fdae1588f468a70c72cf2c3507e6718`. Attempt `b648c265-ada1-4b20-837e-0d049ee816e7`; 615/615 fields accepted.
  - Password-protected `evidence.zip` opened with `infected`; SHA-256 `82856ed6ca80c3db2e2528c4dbee30874b9643c8d6f5652b7761e7439f8548fe`.
  - The artifact contains cross-language inert script fixtures. Decode each descriptor from its declared codec, then map behavior graphs, indicators, and syntax fields. A Day 9 helper script supplied useful role, ATT&CK, Batch expansion, and control-flow classification rules.
  - Start response: `lost-in-translation-start.json`; accepted answers/state: `lost-in-translation-progress.json`; extracted files: `lost-in-translation/`; decoder/candidate builder: `decode_lost_artifacts.py`, `build_lost_candidates.py`.
  - Time Trial — untimed regular attempt `1f413c9f-62b3-457d-8d10-8b669d91b0b6`, 615/615 accepted, flag `3351a350a5b7101e7991ab4bea8c6b71`. Passworded ZIP SHA-256 `537201df52e7dc32f6926efa3e3fdc1cf69ea2431e5b0fd3f31caf137504475c`; extracted under `lost-time-trial-regular/`. Full candidate answers, submission history, and per-question troubleshooting: `lost-time-trial-progress.json`, `lost-time-trial-submission-history.json`, `lost-time-trial-unresolved.json`.
- **Swift Justice** (`binary-reverse-engineering-day-08-swift-network-configuration`), Single Solve, attempt `f141de28-14b2-44fe-8178-bd9ea133a411`.
  - Password-protected `evidence.zip` opened with `infected`; SHA-256 `2f6bce1ccadc28c17e60783ad22c4e5c3029aef5a2c462803358e8ef5e94f31b`.
  - The earlier local progress snapshot had 74/80 fields accepted, with six `analysis_format` questions parked after five failed submissions each: d02, d04, d05, d06, d07, d08.
  - Start response: `swift-justice-start.json`; full accepted/failed state: `swift-justice-progress.json`; five guesses per parked field: `swift-justice-backup.json`; candidate values: `swift-justice-single-candidates.json`; extracted files: `swift-justice/`.
  - A read-only Game Master status check on 2026-10-31 returned `CORRECT` with all 80/80 answer IDs accepted for the same attempt. The saved progress files remain a historical snapshot; the later completion response was not saved locally.
- **Cleartext Session** (`mobile-android-day-08-cleartext-session`), Single Solve, attempt `e03a95a3-4996-44f3-ae11-ef2848c9b033` — accepted.
  - APK SHA-256: `60fb542da7a218f5ea4ccd7a9c6015b6349753b46aae9093729ca8be0020bad8`.
  - `assets/huntress_puzzle.json` uses the `reverse` codec; reversing its data yields the accepted answer `ANS-93ED6CB8E42D7666`.
  - APK DEX confirms it passes `case_id` and this value as `proof` over cleartext HTTP to the case backend. Full artifact and submission state: `cleartext-session-progress.json`.
  - Time Trial attempt `9f1a15ec-b8e2-4bb3-ae4e-42b1f57bb78c` — accepted with `ANS-8CC39DFF2A9E0892`; artifact SHA-256 `1030a792d62579a6ddd1c6cf919ff5f1c57641aa36f0869685e59842b8a1e21f`.
  - Mastery ranked attempt expired before submission. Regular Mastery retry `3a4d8559-228b-4271-9339-89a54f3c880e` — all five answers accepted. Start details, downloaded artifacts, hashes, and codes: `cleartext-session-mastery-retry.json` and `cleartext-session-mastery-submit.json`.
