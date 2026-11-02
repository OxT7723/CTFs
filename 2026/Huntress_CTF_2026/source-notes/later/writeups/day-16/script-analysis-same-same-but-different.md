> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 16 — Same Same, But Different

## Result

All three regular modes completed with `CORRECT`; every submitted answer ID was
accepted and no questions remain unresolved.

| Mode | Accepted answers | Assigned artifact | SHA-256 |
| --- | ---: | --- | --- |
| Single Solve | 1,095 / 1,095 | Assigned evidence archive (retired artifact link; see artifact inventory) | `be61ff1436f7c9ed9036ecf2623877472086c08cae4dc86faed91dab9ae31c76` |
| Time Trial | 1,095 / 1,095 | Assigned evidence archive (retired artifact link; see artifact inventory) | `c90f16768316cc6eb21d869206354119164dc757175cb08d744a5e80e2034b7d` |
| Mastery | 5,475 / 5,475 across five sets | Assigned evidence archive (retired artifact link; see artifact inventory) | `a89ae5811502bdcf41427938aa49bfe768b65bac256d9b65a07686ba140fa69a` |

The final Day 16 Script Analysis list marks all three modes `solved: true`.
Game Master status returned `CORRECT` for each. Neither the list nor status
responses contain CourseStack points or scoring state, and the Game Master
OpenAPI describes no scoring operation, so points could not be independently
confirmed.

## Method

Downloaded each assigned archive through the supported proxy and verified its
SHA-256. The existing canonical `script_analysis_solver.py` and
`run_modes.py` handled the randomized artifacts without changes. The runner
saved extracted evidence, candidate answers, submissions, and final status
under `work/day-16/script-analysis/<attempt-id>/`.
