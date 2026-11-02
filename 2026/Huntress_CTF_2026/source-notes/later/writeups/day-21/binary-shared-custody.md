> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 21 Binary Reverse Engineering — Shared Custody

## Results

All modes used the regular untimed route; no Hall of Fame run was requested.

| Mode | Attempt | Accepted | Game Master result | Deadline |
| --- | --- | ---: | --- | --- |
| Single Solve | `b613ee54-a696-4dca-a6f2-3c8c40826075` | 252 / 252 | `CORRECT` | None |
| Time Trial | `cafbd76a-d04a-42cf-9864-3cd7543c54f5` | 252 / 252 | `CORRECT` | None |
| Mastery | `b99d9cdb-73a3-4f98-80c9-9d1bd2e63b8e` | 1,260 / 1,260 | `CORRECT` | None |

Fresh status checks returned `CORRECT`; the Day 21 challenge list marks all
three modes solved. The proxy returned no CourseStack points total or pending
scoring field, so points were not independently confirmed.

## Challenge and records

Challenge ID: `binary-reverse-engineering-day-21-shared-library-boundaries`.
The challenge examines the loader and shared plugin, including ELF machine
values and HCFG configuration. Full live questions and answer formats are in
each attempt's start response:

- Single Solve response (historical reference: `../../work/day-21/binary/b613ee54-a696-4dca-a6f2-3c8c40826075/start-response.json`; not included)
- Time Trial response (historical reference: `../../work/day-21/binary/cafbd76a-d04a-42cf-9864-3cd7543c54f5/start-response.json`; not included)
- Mastery response (historical reference: `../../work/day-21/binary/b99d9cdb-73a3-4f98-80c9-9d1bd2e63b8e/start-response.json`; not included)

| Mode / set | Artifact | SHA-256 |
| --- | --- | --- |
| Single Solve | evidence.zip (retired artifact link; see artifact inventory) | `2ecbedd8939df63f3dad1a97d8945e5f8b4fac41f4de7d59e6d6cb46b0f3102b` |
| Time Trial | evidence.zip (retired artifact link; see artifact inventory) | `62fd698cffb78cbcfddb3a15e5dff3bbded1a628d55039b10c340bc091535729` |
| Mastery set 1 | evidence.zip (retired artifact link; see artifact inventory) | `d71bbd7bc9ad0239224c3e221fb40789b5841103fb58583d298830ecc58bc58f` |
| Mastery set 2 | evidence.zip (retired artifact link; see artifact inventory) | `a1004d44333bdac4bad04cf96f87ebf8f1161169c82551047b2554bb226dbd86` |
| Mastery set 3 | evidence.zip (retired artifact link; see artifact inventory) | `d390185a2af29ca98c0a11cc9e460a696bb4c045f6e4816db79340cd8fb037c9` |
| Mastery set 4 | evidence.zip (retired artifact link; see artifact inventory) | `a6d10b09959bfbf0437aec316b77ec8372f20c79a8278db0fe8d163ba8197483` |
| Mastery set 5 | evidence.zip (retired artifact link; see artifact inventory) | `65e7d3b907d7263c671641392c02cd7811acec4f47225c62e365e8e80e9b6643` |

## Solver update

The reusable analyzer now selects role-named loader and plugin specimens,
includes `.cmxs` shared objects, reads numeric ELF machine values when the
answer format requests an integer, and searches multi-binary artifacts for
the HCFG-bearing member. Each downloaded archive was SHA-256 checked against
its live start response.

Attempt archives, extracted files, candidates, submissions, and status
responses are under `work/day-21/binary/<attempt-id>/`. The reusable solver is
[analyze_evidence.py](../../../../tools/later/binary-reverse-engineering-tools/analyze_evidence.py).
