# Trust the Process

Day 14 · Script analysis · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 14 — Trust the Process

### Result

All three Script Analysis modes completed with `CORRECT`:

| Mode | Accepted answers | Assigned archive SHA-256 |
| --- | ---: | --- |
| Single Solve | 971 / 971 | `98b763891adf3fabc82a97dbec0cb2db4e24c44c68f15df09607997af0e07c6d` |
| Time Trial | 971 / 971 | `dc55fb5913bbbab93eaf755efd87b0f1250725f27c8332a9833ed7f48dabafd0` |
| Mastery | 1942 / 1942 | `e3cc1eed2245cc69097c7ecbc6d3f629acd34083a875dfd923cef32a562eeffd` |

The final filtered Game Master list marks each mode `solved: true`. Its
responses contain no separate CourseStack points or pending-scoring field.

### Method

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

## Retained sources

- [later/writeups/day-14/script-analysis-trust-the-process.md](../../source-notes/later/writeups/day-14/script-analysis-trust-the-process.md)
