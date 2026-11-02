> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 19 Script Analysis — Sharp Practice

## Results

| Mode | Attempt | Accepted | Game Master result | Deadline |
| --- | --- | ---: | --- | --- |
| Single Solve | `1fba457b-c7aa-4797-a65d-f2f88a1ae724` | 1,249 / 1,249 | `CORRECT` | None |
| Time Trial, regular untimed route | `34c3e37d-8f19-44fd-b011-1e89ab74e1af` | 1,249 / 1,249 | `CORRECT` | None |
| Mastery, regular untimed route | `d102ae6a-d645-47f3-9640-1c6147993032` | 6,245 / 6,245 | `CORRECT` | None |

The filtered Day 19 Script Analysis list reports `solved: true` for all three
modes. The Game Master status and list responses expose no numeric CourseStack
points or separate scoring status, so point totals could not be independently
verified here.

## Challenge and response records

**Sharp Practice** (`script-analysis-day-19-managed-assembly-bridge`) asks the
player to recover layered configuration in a Roslyn C# script and inline ASPX
host, resolve static handoffs, and identify the bridge destination. The full
player-facing prompt, guidance, questions, answer formats, and exact answer IDs
for each attempt are preserved in its start response:

- Single Solve response (historical reference: `../../work/day-19/script-analysis/1fba457b-c7aa-4797-a65d-f2f88a1ae724/start-response.json`; not included)
- Time Trial response (historical reference: `../../work/day-19/script-analysis/34c3e37d-8f19-44fd-b011-1e89ab74e1af/start-response.json`; not included)
- Mastery response (historical reference: `../../work/day-19/script-analysis/d102ae6a-d645-47f3-9640-1c6147993032/start-response.json`; not included)

Each attempt assigned an `evidence.zip` bundle. The bundle contains the
player-facing script specimens referenced by the questions, including PowerShell
samples, shell and Windows script samples, JScript and other hosted-language
bridges, plus recovered Python samples. The ASPX inline C# and `.csx` host
specimens are part of the host/bridge analysis. Mastery bundles five sets in
one archive. All assigned bytes were downloaded and SHA-256 checked by the
reusable runner before analysis.

| Mode | Assigned artifact | SHA-256 |
| --- | --- | --- |
| Single Solve | evidence.zip (retired artifact link; see artifact inventory) | `e1d310a9c5b739906fb0a4ad347b5cdcfc5ae1721689f0667aad7eedbace0471` |
| Time Trial | evidence.zip (retired artifact link; see artifact inventory) | `81add7aa73a80a3a7e1f1ed56451db514597120f5e66b2c076b33b1aff751537` |
| Mastery, five sets | evidence.zip (retired artifact link; see artifact inventory) | `d08235ccba398360d0e8614552a880be0a69c8683b8ef01f898d3c9a71067854` |

## Solver and evidence

The existing deterministic parser and `script-analysis-tools/run_modes.py`
handled all three randomized assignments without code changes or failed
submissions. Per-attempt archives, extracted specimens, candidate answers,
submission outcomes, and post-submit statuses are under
`work/day-19/script-analysis/<attempt-id>/`. No unresolved answer IDs remain.
