> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 15 — Crumb Trail

## Result

All three regular, untimed modes completed with `CORRECT`:

| Mode | Accepted answers | Assigned archive SHA-256 |
| --- | ---: | --- |
| Single Solve | 1,026 / 1,026 | `3f603de468657d5f7cd2e6f89311f8456f0b0f78e785e3394b14c8055aa282a5` |
| Time Trial | 1,026 / 1,026 | `517d4745d6f5e466aa9811e2097c23a50ed0e1d0820348db438bda14494bcc4c` |
| Mastery | 5,130 / 5,130 | `362927f4466288a1a03750a47d3b37bfb5ec2e6b623a47c5a1976ca789e5b8b1` |

The filtered Game Master list marks all three modes `solved: true`. The Game
Master status responses do not contain CourseStack scoring fields, so point
totals could not be independently confirmed here.

## Method

Downloaded each attempt's assigned archive through the proxy and verified its
SHA-256. The canonical parser reconstructed descriptor values without running
the specimens. The Time Trial's first submission accepted 1,018 answers and
left eight Batch expansion IDs unresolved. Those files enabled delayed
expansion for other code, but their descriptor reconstruction assignments
used percent expansion or CALL double expansion.

Updated `batch_expansion()` in
`script-analysis-tools/script_analysis_solver.py` to classify the descriptor
reconstruction assignment itself. The corrected answers completed Time Trial;
the updated solver also completed all five Mastery sets.

The reusable runner stores each mode's response, downloaded archive, extracted
evidence, candidates, submissions, and status under
`work/day-15/script-analysis/<attempt-id>/`. The complete Single Solve
question/answer-format inventory is in
`work/day-15/script-analysis/attempt-records/4c5ea1eb-6e9a-4d65-97f2-f652ccf9c8b4/challenge-details.md`.
