> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 21 — Actions Speak Louder

## Result

All three regular modes completed. Game Master status and the filtered
challenge list reported each mode as `CORRECT` and solved; no status was
pending. No Hall of Fame timing was requested.

| Mode | Attempt | Accepted | Assigned archive SHA-256 |
| --- | --- | ---: | --- |
| Single Solve | `2d24dfa1-0d64-4cef-9764-e58edfc5412c` | 1,373 / 1,373 | `e005f70c2a553e72ce46d151f6aaa431f2b7b71719910072b7643c971c19d046` |
| Time Trial | `b6a49f44-63c4-43a1-af56-5c80bbea254c` | 1,373 / 1,373 | `7b0e9130cb2e682b808cc039e967a4f4b79925549c9bcdfab35e0c04c5049a7f` |
| Mastery | `07777a2f-9538-4695-95bd-6b7e7de8d109` | 6,865 / 6,865 | `258ffb307fda734c45060e99f3185626c2c2c2bffa0d2a76fc5f9b5642ce3afe` |

The Game Master status responses contained no point totals. The challenge
list marked all three modes solved, with no scoring-pending status.

## Assigned evidence archives

Each archive contains the script evidence referenced by the mode's questions.
Mastery contains five sets of evidence.

- Single Solve: Download assigned evidence archive (retired artifact link; see artifact inventory) — SHA-256: `e005f70c2a553e72ce46d151f6aaa431f2b7b71719910072b7643c971c19d046`
- Time Trial: Download assigned evidence archive (retired artifact link; see artifact inventory) — SHA-256: `7b0e9130cb2e682b808cc039e967a4f4b79925549c9bcdfab35e0c04c5049a7f`
- Mastery: Download assigned evidence archive (retired artifact link; see artifact inventory) — SHA-256: `258ffb307fda734c45060e99f3185626c2c2c2bffa0d2a76fc5f9b5642ce3afe`

## Method

Used `script-analysis-tools/run_modes.py` with each exact challenge ID. The
runner saved each live start response, downloaded and hash-checked its
assigned archive, extracted the evidence, generated answers from the current
question IDs, submitted them, and saved the final status.

Mastery assigned five evidence sets. Optimized the runner's answer batching
to calculate request sizes incrementally instead of serializing every growing
candidate batch. Attempt records are under
`work/day-21/script-analysis/<attempt-id>/`.
