# Bind Over Matter

Day 10 · Script analysis · **Evidence summary**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `script-analysis-day-10-wmi-persistence-reconstruction`.

## Challenge

A MOF file declares classes, namespaces, filters, and consumers, but only some bindings actually tie them together. Reconstruct the persistence intent, separate the operational relationships from the decoys, and name the subscription that would really survive a reboot.

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

The later Day 10 shared notes explicitly skipped Bind Over Matter. Its recorded completion here comes from the earlier state snapshot, not that later session.

## Evidence retained

- [Original challenge notes](../../source-notes/early/10-Bind_Over_Matter/readme.md)
- [Saved challenge state](../../source-notes/early/10-Bind_Over_Matter/challenge_state.json)
- [Reusable tooling guide](../../tools/later/script-analysis-tools/README.md)

This short record preserves what the available material supports. The original AI transcript and a complete per-attempt command/output trail are not included here; no challenge was rerun to fill those gaps.

## Retained sources

- [early/10-Bind_Over_Matter/readme.md](../../source-notes/early/10-Bind_Over_Matter/readme.md)
- [later/writeups/day-10/solve-notes.md](../../source-notes/later/writeups/day-10/solve-notes.md)
