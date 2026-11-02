> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 16 Metadata Forensics — Return to Sender

## Results

All three modes returned `CORRECT`; every answer ID was accepted:

| Mode | Attempt | Accepted |
| --- | --- | --- |
| Single Solve | `9136f3a1-2705-4812-8b29-746cbad92e6b` | 1 / 1 |
| Time Trial | `cd7e40b0-74e5-487e-91e5-74b5114e9816` | 21 / 21 |
| Mastery | `4e28c7c1-0428-40f4-a646-ca56cca84660` | 105 / 105 |

Time Trial and Mastery used regular attempts (`run_for_time: false`); neither
had a deadline. The Day 16 Metadata Forensics list marks all three modes
`solved: true`. No Game Master response reported pending scoring.

## Assigned artifacts

- Single Solve: Download metadata-day-16-evidence.zip (retired artifact link; see artifact inventory) —
  SHA-256 `69a297ddfef262c09d3f5c212630e187ba45037dc5e2f5af8fb0a454d54776bf`.
- Time Trial: Download evidence.zip (retired artifact link; see artifact inventory) —
  SHA-256 `e200bc5970169055842b7c4c4398d2f0945e3009ee73a43b764cf1e01a2e7f6d`.
- Mastery: Download mastery bundle (retired artifact link; see artifact inventory) —
  SHA-256 `9d387e8883ba4003db98f86a6ff7451e7298dbd145465a218d093ce576d52332`.
  The bundle contains `evidence-01.zip` through `evidence-05.zip`.

## Solver update

Added email `Message-ID` extraction from downloaded `.eml` bytes to
`metadata-forensics-tools/run_challenge.py`. The existing runner handled all
other fields across the five mastery bundles. Installed the declared
`pefile` and `pyzipper` dependencies needed by the existing tooling.
