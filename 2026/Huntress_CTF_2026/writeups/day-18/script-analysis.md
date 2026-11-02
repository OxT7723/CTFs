# Orphan Process

Day 18 · Script analysis · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 18 Script Analysis — Orphan Process

### Results

| Mode | Challenge ID | Attempt | Answers accepted | Result |
| --- | --- | --- | ---: | --- |
| Single Solve | `script-analysis-day-18-process-story` | `e92f5bae-ed84-4088-af57-87504b582350` | 1,194 / 1,194 | CORRECT |
| Time Trial | `script-analysis-day-18-process-story/time_trial` | `bf6c3add-0446-404d-b1b8-99c537e34381` | 1,194 / 1,194 | CORRECT |
| Mastery | `script-analysis-day-18-process-story/mastery` | `8db6bae6-5183-4a5a-bfaa-c76b5e5779a5` | 5,970 / 5,970 | CORRECT |

Time Trial and Mastery used the regular untimed routes. No Hall of Fame timer
was requested. The final Day 18 Script Analysis list reported `solved: true`
for all three modes. The proxy did not expose point totals or a separate
CourseStack scoring field; none of the final responses reported a pending
scoring status.

### Artifacts and solver notes

Evidence ZIP SHA-256 values:

- Single Solve: `b75763de750f6378553db861950aacb11b1f7d2832c6a8183b351e35f3ade48d`
- Time Trial: `b942a179c0f9bc23c5560b8486a290fd713d5b57968b9e4a14b44e8db83bdc40`
- Mastery: `dd2665e03aaea2f25bf699724a45b35318ab0b78e627bed11aa097d48da7f7c0`

The assigned archives and answer maps are preserved in the corresponding
`work/day-18/script-analysis/<attempt-id>/` directories.

The reusable parser in `script-analysis-tools/script_analysis_solver.py` now
recovers Google Apps Script descriptors assembled from fragmented hex,
hex/Base64, and Base64 payloads without executing the specimens. Some decoded
descriptors had `attack` values that disagreed with their `steps`; graph-only
answers were rejected for those fields. Use the reconstructed descriptor's
`attack` field when present, and derive from the graph rubric when it is
absent. This matched the Game Master's accepted answers across all three
assigned modes.

## Retained sources

- [later/writeups/day-18/script-analysis-orphan-process.md](../../source-notes/later/writeups/day-18/script-analysis-orphan-process.md)
