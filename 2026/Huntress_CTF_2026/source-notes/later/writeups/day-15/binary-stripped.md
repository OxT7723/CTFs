> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 15 Binary: Stripped

Challenge ID: `binary-reverse-engineering-day-15-assembly-and-symbol-loss`.
The regular Single Solve, Time Trial, and Mastery modes are complete.

| Mode | Attempt | Accepted | Deadline | Result |
| --- | --- | ---: | --- | --- |
| Single Solve | `543a0050-6929-441b-a3e0-394ebda0808e` | 150/150 | None | `CORRECT` |
| Time Trial | `9beb8deb-0bad-40cd-a39c-4bda11a5d03c` | 150/150 | None | `CORRECT` |
| Mastery | `0e7c86f5-1809-4807-b195-3167440a5d62` | 750/750 | None | `CORRECT` |

No Hall of Fame run was requested. The timed-mode status responses report
`run_for_time: false` and `hall_of_fame_eligible: false`. Game Master status
confirms all three solves and returned no pending-scoring state. Its supported
API exposes no CourseStack point totals, so points were not independently
verified.

The evidence bundles contain both stripped and symbolized ELF specimens. The
analyzer selects each by its role in the delivered filename and reads ELF
machine codes directly from the header. Artifact hash ordinals follow the
archive member order; the runner now records that order during extraction,
skips previously accepted IDs when resuming, and continues isolating answers
after an individual rejection.

Attempt records, assigned bytes, candidate answers, submissions, and final
status responses are under `work/day-15/binary/`.
