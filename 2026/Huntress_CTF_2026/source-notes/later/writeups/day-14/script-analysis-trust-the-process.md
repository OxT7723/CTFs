> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 14 — Trust the Process

## Result

All three Script Analysis modes completed with `CORRECT`:

| Mode | Accepted answers | Assigned archive SHA-256 |
| --- | ---: | --- |
| Single Solve | 971 / 971 | `98b763891adf3fabc82a97dbec0cb2db4e24c44c68f15df09607997af0e07c6d` |
| Time Trial | 971 / 971 | `dc55fb5913bbbab93eaf755efd87b0f1250725f27c8332a9833ed7f48dabafd0` |
| Mastery | 1942 / 1942 | `e3cc1eed2245cc69097c7ecbc6d3f629acd34083a875dfd923cef32a562eeffd` |

The final filtered Game Master list marks each mode `solved: true`. Its
responses contain no separate CourseStack points or pending-scoring field.

## Method

Downloaded and hash-checked each assigned AES ZIP, then extracted it with the
event password `infected`. Generated answers from the extracted files with
`script-analysis-tools/script_analysis_solver.py`; it reconstructed descriptor
values and mapped the live question IDs and formats without executing specimens.
The existing mode runner handled the randomized timed assignments and mastery
sets:

```sh
python3 script-analysis-tools/run_modes.py \
  'script-analysis-day-14-msbuild-trusted-project-abuse/time_trial'
```

The runner now finds the shared AES ZIP dependency itself, defaults to the
supported 500-answer batch size, and enforces the API's 500-answer and 512 KiB
request limits when forming submissions.
