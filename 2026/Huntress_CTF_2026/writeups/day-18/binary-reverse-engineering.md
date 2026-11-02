# Flow State

Day 18 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 18 Binary: Flow State

Challenge: `binary-reverse-engineering-day-18-control-flow-reconstruction`

The prompt is: “Follow the calls and the program tells you its story.
Reconstruct the call graph, read the API intent at each edge, and prove no
injection hides in the flow.”

The existing `binary-reverse-engineering-tools/run_modes.py` and
`analyze_evidence.py` handled the live answer contract without changes.
Single Solve and Time Trial each had 216 answer fields; Mastery had 864 fields
across four assigned evidence bundles. The solver downloaded each assignment,
checked the API-provided SHA-256, generated answers from the extracted bytes,
and submitted them using the live answer IDs.

### Results

| Mode | Result | Accepted | Deadline |
| --- | --- | ---: | --- |
| Single Solve | CORRECT | 216 / 216 | Untimed |
| Time Trial | CORRECT | 216 / 216 | 2026-10-18 14:25:53 UTC |
| Mastery | CORRECT | 864 / 864 | 2026-10-18 14:29:08 UTC |

No Hall-of-Fame timed run was requested. The Game Master list reports all
three modes solved. Its status responses expose no CourseStack score or award
state; the CourseStack host root returned the Apache default page, so point
posting remains unconfirmed.

### Assigned evidence

Each artifact is the delivered evidence bundle for its mode/set.

#### Single Solve

Download evidence.zip (private download link removed)
SHA-256: `2e8dcfbe27cb788688817c9a43f5cd41d072f22e38dbcf0756fcc76e0c6a9dad`

#### Time Trial

Download evidence.zip (private download link removed)
SHA-256: `172f7881b1f7c8a24964f1011710609762fc824027d6693ed4f8a675ff722606`

#### Mastery sets

1. Download evidence.zip (private download link removed)
   SHA-256: `b558b946b756f96b9efe19dc2db78c4b9570b98c0478925db5da8c3f59202f5d`
2. Download evidence.zip (private download link removed)
   SHA-256: `53505136edeed726dafd591b017e4b882dd2cf25fb1a31d55e33c7a8c862194d`
3. Download evidence.zip (private download link removed)
   SHA-256: `16bb5b501bfa36a4fff3465a9bfef03854c171d71af39b5c17cdcb98c6ffba58`
4. Download evidence.zip (private download link removed)
   SHA-256: `35ff20aacb4d211a58bd690bb3d343b8b68afb548f39ba46c09dcd0d77a2aa06`

Attempt records and candidate answers are under `work/day-18/binary/` in this
workspace. No answers remained unresolved, and no solver changes were needed.

## Retained sources

- [later/writeups/day-18/binary-flow-state.md](../../source-notes/later/writeups/day-18/binary-flow-state.md)
