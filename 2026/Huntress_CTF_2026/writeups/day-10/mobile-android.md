# Network Config Split

Day 10 · Mobile / Android · **Evidence summary**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `mobile-android-day-10-network-config-split`.

## Challenge

Diff manifest and Network Security Config variants to locate the true transport exception.

The saved assignment asks, for example:

- For case MOB-10-A4B83C4513 in package com.huntress.mobile.d10.va4b83c45132b: Diff manifest and Network Security Config variants to locate the true transport exception. Submit only the exact backend answer code returned for this case.

## Retained solver approach

The retained mobile tooling reads APK assets and declared codecs, reconstructs answer data, and matches it to the assignment’s answer format. It also includes manifest and DEX inspection helpers. These capabilities explain the available automation, but do not establish which path the AI used for this particular APK.

## Recorded result

The historical challenge-state snapshot records:

| Mode | Listed solved | Status result |
| --- | --- | --- |
| single_solve | True | CORRECT |
| time_trial | True | CORRECT |
| mastery | True | CORRECT |

These are retained service-state values, not a fresh check. They do not by themselves establish a ranked timed completion or a CourseStack points total.

## Evidence retained

- [Original challenge notes](../../source-notes/early/10-Network_Config_Split/readme.md)
- [Saved challenge state](../../source-notes/early/10-Network_Config_Split/challenge_state.json)
- [Reusable tooling guide](../../tools/later/mobile-android-tools/README.md)

This short record preserves what the available material supports. The original AI transcript and a complete per-attempt command/output trail are not included here; no challenge was rerun to fill those gaps.

## Retained sources

- [early/10-Network_Config_Split/readme.md](../../source-notes/early/10-Network_Config_Split/readme.md)
- [later/writeups/day-10/solve-notes.md](../../source-notes/later/writeups/day-10/solve-notes.md)
