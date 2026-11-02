# Chunk Norris

Day 5 · Metadata forensics · **Evidence summary**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `metadata-forensics-day-05-chunk-norris`.

## Challenge

The PNGs render, but rendering is not proof. Walk their chunks, verify their declared geometry, and locate the image with an unexpected structural passenger.

The saved assignment asks, for example:

- Determine png.ihdr_dimensions_pixels for panel-001.png.

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

- [Original challenge notes](../../source-notes/early/05-Chunk_Norris/readme.md)
- [Saved challenge state](../../source-notes/early/05-Chunk_Norris/challenge_state.json)
- [Reusable tooling guide](../../tools/later/metadata-forensics-tools/README.md)

This short record preserves what the available material supports. The original AI transcript and a complete per-attempt command/output trail are not included here; no challenge was rerun to fill those gaps.

## Retained sources

- [early/05-Chunk_Norris/readme.md](../../source-notes/early/05-Chunk_Norris/readme.md)
