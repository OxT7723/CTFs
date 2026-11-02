> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 20 — The Butler Did It

## Result

All three regular modes completed with `CORRECT`; the Game Master status
reported every answer ID accepted. No timed Hall of Fame attempt was requested.

| Mode | Attempt | Accepted | Artifact SHA-256 |
| --- | --- | ---: | --- |
| Single Solve | `f18e3586-e0c2-401e-9252-62bb02a82483` | 1,329 / 1,329 | `b43ad00571c6597bd3266d38feea1416c80a41da9f39eb16123024e3c1690f3a` |
| Time Trial | `2d38ebc8-86cc-42d5-900a-f059cf2ee6d4` | 1,329 / 1,329 | `f54e673ed0ed90bdfdfb8ffcbc51e7a0b295ff0674f9377c565a9dacd50c5569` |
| Mastery | `89c6a5aa-73ef-4e57-959b-511a8ec5f5e6` | 6,645 / 6,645 | `7fb1678b0f105b00448ab802d01174b1c5fce47fddf8baacbd3fae4dcc095bea` |

The Game Master returned `CORRECT` for each attempt, with no scoring-pending
status. Its status response did not include CourseStack point totals.

## Method

Used the existing deterministic Script Analysis parser and mode runner. The
runner downloaded each assigned archive, checked its SHA-256, extracted the
evidence, built answers from the live question IDs, submitted them, and saved
the final Game Master status.

The shared parser already handled this Jenkins/Groovy pipeline set and its
mode variants, so no solver changes were needed.

To run a future assigned variant:

```sh
python3 script-analysis-tools/run_modes.py \
  'script-analysis-day-20-jenkins-pipeline-intrusion'
```

Add `/time_trial` or `/mastery` to the challenge ID for those modes. The
runner uses the regular assignment by default.

Attempt records, extracted evidence, candidate answers, and status responses
are under `work/day-20/script-analysis/<attempt-id>/`.
