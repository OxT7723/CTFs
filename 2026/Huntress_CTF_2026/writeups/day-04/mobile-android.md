# Pending Intent Relay

Day 4 · Mobile / Android · **Evidence summary**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `mobile-android-day-04-pending-intent-relay`.

## Challenge

Recover and redirect a mutable PendingIntent while preserving every earlier component check.

The saved assignment asks, for example:

- For case MOB-04-0C53CC9C9F in package com.huntress.mobile.d04.v0c53cc9c9f40: Recover and redirect a mutable PendingIntent while preserving every earlier component check. Submit only the exact backend answer code returned for this case.

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

- [Original challenge notes](../../source-notes/early/04-Pending_Intent_Relay/readme.md)
- [Saved challenge state](../../source-notes/early/04-Pending_Intent_Relay/challenge_state.json)
- [Reusable tooling guide](../../tools/later/mobile-android-tools/README.md)

This short record preserves what the available material supports. The original AI transcript and a complete per-attempt command/output trail are not included here; no challenge was rerun to fill those gaps.

## Retained sources

- [early/04-Pending_Intent_Relay/readme.md](../../source-notes/early/04-Pending_Intent_Relay/readme.md)
