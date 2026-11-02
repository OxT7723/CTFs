> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 17 — Fetch Quest

## Results

All three regular modes completed with `CORRECT`; every answer was accepted.

| Mode | Accepted answers | Assigned artifact SHA-256 |
| --- | ---: | --- |
| Single Solve | 1,139 / 1,139 | `fe5c28a3276922d02e6db9106ade56b0037dbdcccdec2ceab2793eb0b6e50867` |
| Time Trial | 1,139 / 1,139 | `786aafcacd2fc3e5e5ed964c9f38c27a15477c52e08241c5be8409696c55b664` |
| Mastery | 5,695 / 5,695 | `817baeafa940f8df4e41b8fa731cce03c06736991e684e5d386c10bf90f613b1` |

The final Day 17 Script Analysis list marks all three modes solved. Game
Master status returned `CORRECT` for each. The status responses provide no
CourseStack scoring fields, so points could not be independently confirmed.

## Method

The existing `script-analysis-tools/run_modes.py` workflow downloaded each
assigned archive through the supported proxy, validated its SHA-256, built
answers with the canonical `script_analysis_solver.py`, and submitted them
under the answer IDs from each live attempt. Attempt evidence and summaries
are saved under `work/day-17/script-analysis/`.
