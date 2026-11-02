> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 14 Metadata Forensics — The Shortcut Home

**Challenge ID:** `metadata-forensics-day-14-shortcut-home`

## Results

All three modes returned `CORRECT`, with every submitted answer ID accepted:

| Mode | Answer ID(s) | Result |
| --- | --- | --- |
| Single Solve | `d14-lnk-001-lnk-target-path-windows` | `CORRECT` |
| Time Trial | `d14-lnk-002-lnk-target-path-windows` | `CORRECT`, within the 30-second deadline |
| Mastery | `set1.d14-lnk-003-lnk-target-path-windows`, `set2.d14-lnk-004-lnk-target-path-windows` | Both accepted; `CORRECT`, within the 30-second deadline |

Each assigned shortcut's `lnk.target_path_windows` was:

```text
C:\Windows\System32\cmd.exe
```

## Assigned artifacts

- Single Solve: metadata-day-14-evidence.zip (retired artifact link; see artifact inventory) — SHA-256 `cd5858414bfacebf40f6668b05456ff36d7626847737b5b7f0cd2d5e9745edec`; contains `shortcut-001.lnk`.
- Time Trial: metadata-day-14-evidence.zip (retired artifact link; see artifact inventory) — SHA-256 `6f8723bfc9078b8de591823f52d682ad7013fef6b6a98f439fd6a5d21cfd7bb5`; contains `shortcut-002.lnk`.
- Mastery: metadata-forensics-day-14-shortcut-home-mastery.zip (retired artifact link; see artifact inventory) — SHA-256 `f290c67a43c2a6e26578af61d1e0dc7066b596238fbeae9d14d4d9adf8ee4796`; contains the two assigned shortcut bundles for `shortcut-003.lnk` and `shortcut-004.lnk`.

## Method and scoring

The artifacts were downloaded for their active attempts and parsed as Windows
Shell Link files with `pylnk3`. The reusable runner now reads target paths from
the link metadata and works across randomized Time Trial and Mastery variants.
Install `pylnk3` with `metadata-forensics-tools/requirements.txt`.

The status endpoint returned `CORRECT` for all modes, and the Day 14 lane list
marks each mode solved. No response reported pending CourseStack scoring.
Attempt records, downloaded artifacts, candidates, submissions, and statuses
are under `attempt-records/metadata-forensics-day-14-shortcut-home/`.
