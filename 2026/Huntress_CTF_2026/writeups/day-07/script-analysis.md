# Node by Node

Day 7 · Script analysis · **Evidence summary**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `script-analysis-day-07-node-operation-graphs`.

## Challenge

Eight Node.js operation graphs that will never execute. Spot the indirect expansions and token fragmentation, then sort each graph into its role — benign, staging, dropping, downloading, uploading, launching, scheduled, or multi-stage — from the final bytes alone.

The saved assignment asks, for example:

- What scenario best describes resource-sample.ps1?
- What is its primary MITRE ATT&CK technique ID?
- What exact URL is embedded in the resource sample?

## Retained solver approach

The retained script-analysis solver treats specimens as data, parses encoded descriptors, builds candidate answers, and checks their IDs and allowed formats against the saved question contract. Its mode runner handles the assignment and submission workflow. This describes the available automation; the exact original sequence is not retained in the challenge narrative.

## Recorded result

The historical challenge-state snapshot records:

| Mode | Listed solved | Status result |
| --- | --- | --- |
| single_solve | True | CORRECT |
| time_trial | True | CORRECT |
| mastery | True | CORRECT |

These are retained service-state values, not a fresh check. They do not by themselves establish a ranked timed completion or a CourseStack points total.

## Evidence retained

- [Original challenge notes](../../source-notes/early/07-Node_by_Node/readme.md)
- [Saved challenge state](../../source-notes/early/07-Node_by_Node/challenge_state.json)
- [Reusable tooling guide](../../tools/later/script-analysis-tools/README.md)

This short record preserves what the available material supports. The original AI transcript and a complete per-attempt command/output trail are not included here; no challenge was rerun to fill those gaps.

## Retained sources

- [early/07-Node_by_Node/readme.md](../../source-notes/early/07-Node_by_Node/readme.md)
