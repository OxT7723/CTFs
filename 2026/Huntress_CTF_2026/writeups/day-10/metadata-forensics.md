# Where Do We Begin?

Day 10 · Metadata forensics · **Evidence summary**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `metadata-forensics-day-10-where-do-we-begin`.

## Challenge

Architecture tells you whether a binary can run; its entry point tells you where execution begins. Map the start addresses and catch the report that is lying.

The saved assignment asks, for example:

- Determine pe.address_of_entry_point_rva_hex for telemetry-agent-001.exe.

## Retained solver approach

The retained metadata runner reads the question contract, selects an artifact parser, and builds an answer from the assigned bytes. Its helpers cover binary headers and container metadata. The questions below identify the requested property; the saved metadata does not preserve a step-by-step account of the actual parsing session.

## Recorded result

The historical challenge-state snapshot records:

| Mode | Listed solved | Status result |
| --- | --- | --- |
| single_solve | True | CORRECT |
| time_trial | True | CORRECT |
| mastery | True | CORRECT |

These are retained service-state values, not a fresh check. They do not by themselves establish a ranked timed completion or a CourseStack points total.

## Evidence retained

- [Original challenge notes](../../source-notes/early/10-Where_Do_We_Begin/readme.md)
- [Saved challenge state](../../source-notes/early/10-Where_Do_We_Begin/challenge_state.json)
- [Reusable tooling guide](../../tools/later/metadata-forensics-tools/README.md)

This short record preserves what the available material supports. The original AI transcript and a complete per-attempt command/output trail are not included here; no challenge was rerun to fill those gaps.

## Retained sources

- [early/10-Where_Do_We_Begin/readme.md](../../source-notes/early/10-Where_Do_We_Begin/readme.md)
- [later/writeups/day-10/solve-notes.md](../../source-notes/later/writeups/day-10/solve-notes.md)
