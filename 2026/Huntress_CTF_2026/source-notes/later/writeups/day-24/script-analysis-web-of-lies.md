> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 24 Script Analysis — Web of Lies

## Results

Completed the regular Single Solve, Time Trial, and Mastery routes. No
Hall-of-Fame timing was requested.

| Mode | Attempt | Answers accepted | Assigned artifact (SHA-256) | Game Master |
| --- | --- | ---: | --- | --- |
| Single Solve | `aa71af55-7e7b-407d-86ad-f3d5673eca3e` | 1,516 / 1,516 | Download evidence.zip (retired artifact link; see artifact inventory) · `6239594b109301fa09b96af0ff3665ae13f262447f08b0d5129178aacd3c712f` | `CORRECT` |
| Time Trial | `ae689601-d9bb-412c-bec4-da7cd70bb41a` | 1,560 / 1,560 | Download evidence.zip (retired artifact link; see artifact inventory) · `673acd424c394a4dc12ba57ec11efe2d53a0a41f0d17e59a6d1adae6f800acac` | `CORRECT` |
| Mastery | `763d4dd5-52fb-4fce-8e3e-5e850f00cc09` | 12,480 / 12,480 | Download script-analysis-day-24-jsp-webshell-source-mastery.zip (retired artifact link; see artifact inventory) · `461e3b71baf0b2855e1d941716b0c8a6c3d9fe645f211488064dfba6655b89e1` | `CORRECT` |

The Game Master status responses confirm all answers accepted and no unresolved
IDs. The supported proxy does not expose CourseStack point totals or a separate
scoring-status field.

## Method

Downloaded each attempt's assigned archive through the Game Master and checked
its SHA-256. The existing `script_analysis_solver.py` built candidates for all
question IDs, including the JSP host and polyglot fixtures. Its generic
descriptor decoding handled this variant without a code change. Specimens
were treated as inert data and were not executed.
