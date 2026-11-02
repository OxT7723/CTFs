# WebView Bridge

Day 7 · Mobile / Android · **Evidence summary**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `mobile-android-day-07-webview-bridge`.

## Challenge

Cross a challenge-owned WebView bridge through an untrusted origin.

The saved assignment asks, for example:

- For case MOB-07-9F5C796C19 in package com.huntress.mobile.d07.v9f5c796c198b: Cross a challenge-owned WebView bridge through an untrusted origin. Submit only the exact backend answer code returned for this case.

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

- [Original challenge notes](../../source-notes/early/07-WebView_Bridge/readme.md)
- [Saved challenge state](../../source-notes/early/07-WebView_Bridge/challenge_state.json)
- [Reusable tooling guide](../../tools/later/mobile-android-tools/README.md)

This short record preserves what the available material supports. The original AI transcript and a complete per-attempt command/output trail are not included here; no challenge was rerun to fill those gaps.

## Retained sources

- [early/07-WebView_Bridge/readme.md](../../source-notes/early/07-WebView_Bridge/readme.md)
