> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 28 Script Analysis: Out of Order

The maintained `script-analysis-tools/run_modes.py` runner and
`script_analysis_solver.py` completed all three regular modes. The runner
downloaded each assigned archive, verified its SHA-256, extracted the evidence
as data, generated candidates from the live question IDs, and submitted them.

| Mode | Questions accepted | Attempt record |
| --- | ---: | --- |
| Single Solve | 1,703 / 1,703 | `work/day-28/script-analysis/cae59790-4b28-406c-9933-71a6652747a3/` |
| Time Trial | 1,781 / 1,781 | `work/day-28/script-analysis/70cdb1d0-6990-4f50-9822-694e040508f2/` |
| Mastery | 21,372 / 21,372 | `work/day-28/script-analysis/9cb45c71-5573-4876-8cce-9b0cc213749c/` |

Each submission returned `CORRECT`, and a final filtered list showed all three
modes solved. The modes used regular play; `run_for_time` was not requested.
Game Master responses did not include a CourseStack scoring status or point
total. No solver changes were needed.
