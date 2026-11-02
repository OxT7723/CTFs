# Resourceful

Day 20 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 20 Binary Reverse Engineering — Resourceful

### Results

All modes used the regular, untimed route. No Hall of Fame timed run was
requested.

| Mode | Attempt | Accepted | Game Master result | Deadline |
| --- | --- | ---: | --- | --- |
| Single Solve | `00dcc845-06a2-468a-a5dc-7974c35129b9` | 240 / 240 | `CORRECT` | None |
| Time Trial | `7b6c787f-f506-46c7-b7e9-ce7f38121ee0` | 240 / 240 | `CORRECT` | None |
| Mastery | `96f33a69-f3a8-4bf9-9dfd-25cafa9b6aef` | 1,200 / 1,200 | `CORRECT` | None |

Fresh Game Master status checks returned `CORRECT` for all three attempts, and
the Day 20 list marks all three as solved. The returned status fields do not
include a CourseStack points total or a pending-scoring field, so points were
not independently confirmed.

### Challenge and records

Challenge ID: `binary-reverse-engineering-day-20-resources-and-overlays`.
**Resourceful** asks players to map resources, overlays, and bytes beyond
binary section boundaries. Each attempt's complete player-facing fields,
question text, answer formats, answer IDs, and artifact metadata are preserved
in its start response:

- Single Solve response (source reference: `../../work/day-20/binary/00dcc845-06a2-468a-a5dc-7974c35129b9/start-response.json`; not linked in this draft)
- Time Trial response (source reference: `../../work/day-20/binary/7b6c787f-f506-46c7-b7e9-ce7f38121ee0/start-response.json`; not linked in this draft)
- Mastery response (source reference: `../../work/day-20/binary/96f33a69-f3a8-4bf9-9dfd-25cafa9b6aef/start-response.json`; not linked in this draft)

Every archive download was SHA-256 checked against its assigned start
response.

| Mode / set | Artifact | SHA-256 |
| --- | --- | --- |
| Single Solve | evidence.zip (private download link removed) | `cfc4f3e2213afdd913e403ecdc9cded5610474b7aa24367a017344acb4ab7da5` |
| Time Trial | evidence.zip (private download link removed) | `64d8a1a760a31a210e8cecdcbe869857ec87fde3a9130dc403558d2c73e0cfcd` |
| Mastery set 1 | evidence.zip (private download link removed) | `6ce5699d1149229f4eb70816a7b5a1af83eec7717124a170fbe415d021e6422c` |
| Mastery set 2 | evidence.zip (private download link removed) | `02e89473365cd0d9722befb38c1b690f7e7a20e7bca256621f03f8c3672d0365` |
| Mastery set 3 | evidence.zip (private download link removed) | `a4c07ac8ad87d7436106bd8cdd8ce2b28322e1ac847c38d0f93e6706160214b9` |
| Mastery set 4 | evidence.zip (private download link removed) | `9466d574990ed3fa5cb44a7d18bc15e7adc9ade3e56c13f9d83c22a80da7f78e` |
| Mastery set 5 | evidence.zip (private download link removed) | `6e1396f3ac4b24b3161f2f3237967d6dc5762460dba7443a7f4c20949aaf7f56` |

### Solver update

The reusable analyzer now handles the Day 20 `RS20` resource overlay: it
checks the declared HCFG resource and scratch lengths against the exact member
end, verifies the scratch SHA-256, and reads the HCFG record from the resource
start. The `d20_analysis_hcfg_resource_size` field is read from the overlay's
little-endian resource-length field. Existing PK19 overlay handling remains
available.

Attempt archives, extracted files, candidates, submissions, and status
responses are under `work/day-20/binary/<attempt-id>/`. The reusable solver is
[analyze_evidence.py](../../tools/later/binary-reverse-engineering-tools/analyze_evidence.py).

## Retained sources

- [later/writeups/day-20/binary-resourceful.md](../../source-notes/later/writeups/day-20/binary-resourceful.md)
