# Ashes to Assets

Day 25 · Script analysis · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 25 Script Analysis — Ashes to Assets

Completed all three regular modes in progression order. Time Trial and Mastery
used the default untimed route; no Hall of Fame timing was requested.

| Mode | Attempt | Accepted | Artifact SHA-256 | Game Master |
| --- | --- | ---: | --- | --- |
| Single Solve | `f1a2831e-3586-45b9-bf0c-897aaf55b114` | 1,571 / 1,571 | `16a0930e89b42ac708a641e48a27754158f937a7a6ae3336ab518eb0617020dc` | `CORRECT` |
| Time Trial | `c5d19888-0f1e-4e82-b3f5-a37c305438e1` | 1,625 / 1,625 | `c3a524b48257e1106fda803d9c561db1564847a24ca790e8a45aa65e9b3eaed3` | `CORRECT` |
| Mastery | `bf7ed1eb-6be5-4039-8050-3f4eba339444` | 14,625 / 14,625 | `1b04001ef11753bcd8440e6c9e7c3adc25e9c5ac9fc1cbfc66a7c7023fdc1900` | `CORRECT` |

The existing `script-analysis-tools/run_modes.py` and
`script_analysis_solver.py` handled the assigned artifacts without changes.
The runner downloaded each attempt's own archive, verified its SHA-256, built
answers from the live question IDs, submitted them, and confirmed zero
unresolved IDs in the final summaries.

Fresh Game Master status requests confirmed `CORRECT` for all modes. The
supported status and submission responses did not include a CourseStack
scoring field or point total, so ledger posting could not be independently
verified through this proxy.

## Retained sources

- [later/writeups/day-25/script-analysis-ashes-to-assets.md](../../source-notes/later/writeups/day-25/script-analysis-ashes-to-assets.md)
