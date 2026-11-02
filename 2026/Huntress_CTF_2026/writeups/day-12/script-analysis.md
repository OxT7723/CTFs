# AutoIt Takes Two

Day 12 · Script analysis · **Evidence summary**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `script-analysis-day-12-autoit-workflow-pair`.

## Challenge

Two inert AutoIt workflows arrived as a matched set, and each one carries half the story. Correlate them with everything you've proven so far, and decide which pairing is genuine and which is just going through the motions.

The saved assignment asks, for example:

- What scenario best describes resource-sample.ps1?
- What is its primary MITRE ATT&CK technique ID?
- What exact URL is embedded in the resource sample?

## Recorded AI approach

The shared day notes retain the following challenge-specific account:

reused the static script-analysis solver on the
  encrypted evidence archive (password `infected`); specimens were analyzed as
  data and not executed. The contract contained 855 questions in Single Solve
  and Time Trial, and 1,710 in Mastery. The solver now maps an `If True Then`
  wrapper to the accepted `direct` control-flow value. All three modes returned
  `CORRECT`; attempt records and answer maps are under
  `work/day-12/script-analysis/`.

## Recorded result

The historical challenge-state snapshot records:

| Mode | Listed solved | Status result |
| --- | --- | --- |
| single_solve | True | CORRECT |
| time_trial | True | CORRECT |
| mastery | True | CORRECT |

These are retained service-state values, not a fresh check. They do not by themselves establish a ranked timed completion or a CourseStack points total.

## Evidence retained

- [Original challenge notes](../../source-notes/early/12-AutoIt_Takes_Two/readme.md)
- [Saved challenge state](../../source-notes/early/12-AutoIt_Takes_Two/challenge_state.json)
- [Reusable tooling guide](../../tools/later/script-analysis-tools/README.md)
- [Shared day notes](../../source-notes/later/writeups/day-12/progress-notes.md)

This short record preserves what the available material supports. The original AI transcript and a complete per-attempt command/output trail are not included here; no challenge was rerun to fill those gaps.

## Retained sources

- [early/12-AutoIt_Takes_Two/readme.md](../../source-notes/early/12-AutoIt_Takes_Two/readme.md)
- [later/writeups/day-12/progress-notes.md](../../source-notes/later/writeups/day-12/progress-notes.md)
