# Package Deal

Day 21 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 21 Metadata Forensics — Package Deal

### Challenge

- **ID:** `metadata-forensics-day-21-package-deal`
- **Name:** 🔎 Package Deal
- **Description:** Mobile packages have been mirrored under friendly filenames. Recover Android package identities, distinguish rebuilds from clones, and expose the borrowed product name.
- Single Solve asks for `apk.package_name` in `mobile-001.apk`, as exact artifact-derived text with surrounding whitespace trimmed. Its answer ID is `d21-apk-001-apk-package-name`.
- The Time Trial and Mastery question lists and answer formats are preserved verbatim in each attempt's `start-response.json`.

### Results

All modes returned `CORRECT`; their status responses show every answer accepted. Time Trial and Mastery ran as regular untimed attempts (`run_for_time: false`, no deadlines). The final filtered Game Master listing marks all three modes solved by the current player. No scoring-pending status was returned.

| Mode | Attempt | Accepted |
| --- | --- | --- |
| Single Solve | `b055e19e-348b-49e9-83b3-fd4f6632996a` | 1 / 1 |
| Time Trial | `d544e6a0-dab3-400a-8972-bc3275ac989d` | 26 / 26 |
| Mastery | `858d1e96-7171-4cbe-b604-afb36a59c386` | 130 / 130 |

### Assigned artifacts

- Single Solve: Download metadata-day-21-evidence.zip (private download link removed) — SHA-256 `98c16652870620b94a0cdc96f69026848a527d500817c6c4503aea6431f5df87`.
- Time Trial: Download evidence.zip (private download link removed) — SHA-256 `22eabba5e80290120951354b127986de399f7c82093715b5623df6e8de8d322b`.
- Mastery: Download metadata-forensics-day-21-package-deal-mastery.zip (private download link removed) — SHA-256 `789eb34f9dce49b5566731723e4960d9111b794d7402f4ecd7269de242471a0c`.

### Solver update

Added APK package-name extraction to `metadata-forensics-tools/run_challenge.py`. It runs `aapt dump badging` on the assigned APK bytes and reads the manifest package name, supporting this field in future metadata variants.

Full start responses, downloaded bytes, hashes, candidate answers, submission results, and status responses are under `metadata-forensics-tools/attempt-records/metadata-forensics-day-21-package-deal/`.

## Retained sources

- [later/writeups/day-21/metadata-forensics-package-deal.md](../../source-notes/later/writeups/day-21/metadata-forensics-package-deal.md)
