# Zip Code

Day 13 · Script analysis · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 13 Script Analysis: Zip Code

- Challenge ID: `script-analysis-day-13-archive-delivery-chain`
- Lane: Script Analysis
- Day 13 filtered list: one challenge in three modes
- Analysis: used the existing `script-analysis-tools/run_modes.py` runner and
  `script_analysis_solver.py`; specimens were statically decoded without being
  executed. No solver changes were needed.

| Mode | Questions accepted | Result | Assigned archive |
| --- | ---: | --- | --- |
| Single Solve | 913/913 | `CORRECT` | evidence.zip (private download link removed) |
| Time Trial | 913/913 | `CORRECT`, 50-second deadline | evidence.zip (private download link removed) |
| Mastery | 1826/1826 across two sets | `CORRECT`, 80-second deadline | evidence.zip (private download link removed) |

SHA-256 by mode:

- Single Solve: `08092cc83956b363d385540b735de4538e9e0d230cade07e8a53f9e4598d7ba2`
- Time Trial: `0120487f1b8a0aaabeee0063e28c0c9663fd238144c6108bc7ac83a0dfd6d352`
- Mastery: `46fb0fb9dfa1275fca309f8c6c2d3293d9199d1707a0e8be360c2f8eaf289c80`

All three final Game Master status responses report `CORRECT` with every answer
ID accepted. They contain no pending-scoring state; the proxy status response
does not expose a numeric CourseStack points total.

To reuse the runner for a fresh assignment:

```sh
work/day-08/venv/bin/python script-analysis-tools/run_modes.py <challenge-id>
```

The runner saves each attempt, artifact, candidate answers, submission
outcomes, and final status under `work/day-13/script-analysis/<attempt-id>/`.

## Retained sources

- [later/writeups/day-13/script-analysis-zip-code.md](../../source-notes/later/writeups/day-13/script-analysis-zip-code.md)
