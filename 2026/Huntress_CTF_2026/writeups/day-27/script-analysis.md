# FROM Whence It Came

Day 27 · Script analysis · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 27 Script Analysis: FROM Whence It Came

The existing `script-analysis-tools/run_modes.py` runner and
`script_analysis_solver.py` solved the live Docker build attribution variants
without code changes. The runner downloaded each assigned archive, validated
its SHA-256, extracted the specimens as data, checked candidates against the
returned question IDs, submitted, and reconciled accepted IDs with status.

All three regular modes completed with Game Master result `CORRECT`:

| Mode | Questions | Accepted | Attempt record |
| --- | ---: | ---: | --- |
| Single Solve | 1,659 | 1,659 | `work/day-27/script-analysis/1c32f053-c011-4ec0-8647-1459a70652cb/` |
| Time Trial | 1,659 | 1,659 | `work/day-27/script-analysis/5a28cfb4-4c6c-4d65-8286-0905073d75b6/` |
| Mastery | 18,249 | 18,249 | `work/day-27/script-analysis/002ecc40-fc66-41c0-ae95-ac3596178b53/` |

These were regular, non-Hall-of-Fame attempts (`run_for_time` was not
requested). Each attempt record contains the downloaded archive, its hash,
start response, candidate answers, submission outcomes, final response, and
live status snapshot. A final filtered Day 27 list reported all three modes
as `solved: true`. The Game Master responses did not include a separate
CourseStack points total or pending status.

No reusable solver changes were needed.

## Retained sources

- [later/writeups/day-27/script-analysis-from-whence-it-came.md](../../source-notes/later/writeups/day-27/script-analysis-from-whence-it-came.md)
