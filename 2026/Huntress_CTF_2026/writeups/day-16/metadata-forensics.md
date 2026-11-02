# Return to Sender

Day 16 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 16 Metadata Forensics — Return to Sender

### Results

All three modes returned `CORRECT`; every answer ID was accepted:

| Mode | Attempt | Accepted |
| --- | --- | --- |
| Single Solve | `9136f3a1-2705-4812-8b29-746cbad92e6b` | 1 / 1 |
| Time Trial | `cd7e40b0-74e5-487e-91e5-74b5114e9816` | 21 / 21 |
| Mastery | `4e28c7c1-0428-40f4-a646-ca56cca84660` | 105 / 105 |

Time Trial and Mastery used regular attempts (`run_for_time: false`); neither
had a deadline. The Day 16 Metadata Forensics list marks all three modes
`solved: true`. No Game Master response reported pending scoring.

### Assigned artifacts

- Single Solve: Download metadata-day-16-evidence.zip (private download link removed) —
  SHA-256 `69a297ddfef262c09d3f5c212630e187ba45037dc5e2f5af8fb0a454d54776bf`.
- Time Trial: Download evidence.zip (private download link removed) —
  SHA-256 `e200bc5970169055842b7c4c4398d2f0945e3009ee73a43b764cf1e01a2e7f6d`.
- Mastery: Download mastery bundle (private download link removed) —
  SHA-256 `9d387e8883ba4003db98f86a6ff7451e7298dbd145465a218d093ce576d52332`.
  The bundle contains `evidence-01.zip` through `evidence-05.zip`.

### Solver update

Added email `Message-ID` extraction from downloaded `.eml` bytes to
`metadata-forensics-tools/run_challenge.py`. The existing runner handled all
other fields across the five mastery bundles. Installed the declared
`pefile` and `pyzipper` dependencies needed by the existing tooling.

## Retained sources

- [later/writeups/day-16/metadata-forensics-return-to-sender.md](../../source-notes/later/writeups/day-16/metadata-forensics-return-to-sender.md)
