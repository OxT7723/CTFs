# Routine Check

Day 7 · Binary reverse engineering · **Evidence summary**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `binary-reverse-engineering-day-07-kotlin-staging-logic`.

## Challenge

Kotlin coroutines don't run — they suspend, resume, and hop between states. Reconstruct the state machine from the metadata and figure out what this one was staging.

The saved assignment asks, for example:

- What is the exact artifact sha256 1 value for field d01_artifact_sha256_1 in the delivered evidence set?
- What is the exact analysis elf class value for field d01_analysis_elf_class in the delivered evidence set?
- For the requested delivered binary, report the processor architecture identified by its executable-header machine field. A normalized architecture name, a standard tool or symbolic label, or the equivalent decimal or hexadecimal machine code is accepted.

## Retained solver approach

The retained analyzer reads binary headers, sections, symbols and disassembly, and extracts and validates embedded configuration records. Its runner maps the extracted values to the assignment’s answer IDs. This is a description of the retained tooling, not a replay of the original analysis.

## Recorded result

The historical challenge-state snapshot records:

| Mode | Listed solved | Status result |
| --- | --- | --- |
| single_solve | True | CORRECT |
| time_trial | True | CORRECT |
| mastery | True | CORRECT |

These are retained service-state values, not a fresh check. They do not by themselves establish a ranked timed completion or a CourseStack points total.

## Evidence retained

- [Original challenge notes](../../source-notes/early/07-Routine_Check/readme.md)
- [Saved challenge state](../../source-notes/early/07-Routine_Check/challenge_state.json)
- [Reusable tooling guide](../../tools/later/binary-reverse-engineering-tools/README.md)

This short record preserves what the available material supports. The original AI transcript and a complete per-attempt command/output trail are not included here; no challenge was rerun to fill those gaps.

## Retained sources

- [early/07-Routine_Check/readme.md](../../source-notes/early/07-Routine_Check/readme.md)
