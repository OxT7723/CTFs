> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 22 — Next, Next, Finish

## Result

All three regular modes completed with `CORRECT`; the Game Master status
reported every answer ID accepted. No Hall of Fame run was requested.

| Mode | Attempt | Accepted | Artifact SHA-256 |
| --- | --- | ---: | --- |
| Single Solve | `290aa6e1-040f-46e6-84a9-f190316589a2` | 1,417 / 1,417 | `e7361c83519bbc6e113f2c97ead65f4b18930d29b34b6d34672f3b1b67e14880` |
| Time Trial | `1b36a27c-4b85-4192-8c41-7727a58d3a84` | 1,417 / 1,417 | `8654becfb5f1b34b70a303b20209bbd7b98f9b579dcffc8438277552f0fe7305` |
| Mastery | `56ff5a9e-e674-452e-aa66-db55d622d5ed` | 8,502 / 8,502 | `cfc9b29e885533cd7b71fee8c959267f01fda1debcd4823a165188eef8c2813d` |

The Game Master returned `CORRECT` with a flag for each mode, and the final
status responses report `CORRECT` with every answer ID accepted. A follow-up
submission reported `already_solved` and said further submissions are not
scored. The proxy does not expose CourseStack point totals, so the ledger total
could not be independently read here.

## Method

Used the existing deterministic Script Analysis parser and mode runner. The
runner downloaded each assigned archive, checked its SHA-256, extracted the
evidence, built answers from the live question IDs, and submitted them. The
parser handled the NSIS installer chain and randomized mode variants without
challenge-specific solver changes.

The first Mastery submission encountered a transient proxy 502. Reconnected
to the same attempt, then completed it. The runner now retries transient
gateway and URL errors with bounded backoff and checkpoints each completed
submission batch.

Attempt records, extracted evidence, candidate answers, and status responses
are under `work/day-22/script-analysis/<attempt-id>/`.
