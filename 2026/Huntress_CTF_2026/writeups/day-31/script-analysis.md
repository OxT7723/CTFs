# The Full Transform

Day 31 · Script analysis · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 31 Script Analysis: The Full Transform

All three standard modes completed with Game Master result `CORRECT`. The
maintained `script-analysis-tools/run_modes.py` downloaded the assigned
artifacts, built answers from their contents, submitted them, and confirmed
zero unresolved answer IDs.

| Mode | Attempt ID | Accepted | Artifact SHA-256 |
| --- | --- | ---: | --- |
| Single Solve | `7a4741f8-28b5-4788-9a49-39ebe375eda0` | 1,846/1,846 | `29520800185a93bc334a58a7a50e4178129c48058d87a8fc80cd500ec807b475` |
| Time Trial (regular) | `86e6d5c1-d68b-423d-aba1-1c54297795c8` | 1,950/1,950 | `b9f85d292f4cd5af1e92c5cdc8b4b2feca3a4e59f4d5d934cf2fc68770c146d5` |
| Mastery (regular) | `8d5ca366-3790-4890-aa57-78e210a4f983` | 29,250/29,250 | `e8a6a8c66aad39f7db3dbce25faf18fc048311f0f039b054e6ec9e52a3115a8d` |

The final filtered Day 31 listing marks all three modes solved. The Game
Master responses did not include a CourseStack points total or a separate
scoring-status field, and none reported `pending`.

### Ranked timed runs

Five fresh ranked Time Trial variants and five fresh ranked Mastery variants
also completed with `CORRECT`. Every answer was accepted in every run. The
runner's fast path skipped archive hashing during the timed attempt; afterward,
all ten saved archive hashes were verified against their live start responses.
No solver changes were needed.

The client end-to-end times below include the retry/start request, artifact
download, answer processing and submission, and final status/evidence
recording. They are local measurements, not official Game Master leaderboard
times.

| Mode | Attempt ID | Accepted | Client end-to-end | Artifact SHA-256 |
| --- | --- | ---: | ---: | --- |
| Time Trial | `c0345c6c-af8d-4252-b752-7e1bdab7dc91` | 1,950/1,950 | 5.391 s | `bb1169b56d5f07e491bb6e03e3445643cb0312fd63565a71fe1b0a00f2c6fcde` |
| Time Trial | `e04feade-ec9f-4cf9-bdd8-a7d64439dc58` | 1,950/1,950 | 4.513 s | `1af123ccf0cce6a9e415c56de9fa59fb48fc76cc2f35b645479857a91f3c8b9f` |
| Time Trial | `adb0349d-2f90-4932-b66f-4a4dc3a77852` | 1,950/1,950 | 3.054 s | `0c495399cb90a0b28f86f45454764cd2741a4e573e4bf78d36c8ab54ae2571ec` |
| Time Trial | `54e7be37-9a65-4565-b8d4-b8a0c475c3b4` | 1,950/1,950 | 3.329 s | `a50768c72a65728f72ff3db66bff7a626c80dd3accb88685e83f1720dbeb5b63` |
| Time Trial | `b8beaafa-5621-4035-bd29-81a3ba2f3e62` | 1,950/1,950 | 3.421 s | `b2d8f1b18d88463322b9d85fab892437dbc9a5dca7424a6f8fd296c20026a884` |
| Mastery | `cb5ad508-46a9-46f8-90e7-8995c1d9b97a` | 29,250/29,250 | 21.891 s | `15b3627217a1fb46165f33e14bd7c9d268625241099440c2a1ecb5ce2af26088` |
| Mastery | `b2e84f0f-0816-4d6e-9cc2-d6726d70cbd0` | 29,250/29,250 | 19.003 s | `6e8dcc5f42570775f5582b40ce4885ef7751cd2a73b39653f9fbf1c7a6799c63` |
| Mastery | `d1cb4a99-7eae-4bbd-847d-ccf67686ef03` | 29,250/29,250 | 20.058 s | `12e3e084560a510e0e0b48d3e6388ad1f563e6eca1321842d88b5d8b2387daf1` |
| Mastery | `69412da8-f456-4b4e-a8f6-553d803b8a59` | 29,250/29,250 | 18.297 s | `7f399567b23526b3d0cf2b9b0c08ae3f080b7b24db888ce6a0f283439204a894` |
| Mastery | `1304b134-c35c-4b6a-a5af-e666524e7adb` | 29,250/29,250 | 19.891 s | `1583ff0efbee710bfd8f7dfc82de1623c3eb60a59c0b679c6224762cd265d29a` |

The fastest client end-to-end runs were 3.054 seconds for Time Trial and
18.297 seconds for Mastery. The ignored local attempt records, including full
Game Master start responses, candidates, submissions, and status responses,
are under `work/day-31/script-analysis/<attempt-id>/`.

## Retained sources

- [later/writeups/day-31/script-analysis-the-full-transform.md](../../source-notes/later/writeups/day-31/script-analysis-the-full-transform.md)
