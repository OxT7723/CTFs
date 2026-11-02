> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 02 Script Analysis — Host With the Most

## Challenge

- **Single Solve ID:** `script-analysis-day-02-encoded-intent`
- **Time Trial ID:** `script-analysis-day-02-encoded-intent/time_trial`
- **Mastery ID:** `script-analysis-day-02-encoded-intent/mastery`
- **Lane:** Script Analysis
- **Prompt:** Windows Script Host has JScript plans for execution, download,
  upload, and impact. Carry your PowerShell findings forward, tell a function
  call from an invocation or a property access, and work out which script hands
  off to which.

The reusable solver maps each live question ID to the matching artifact,
recovers PowerShell and JScript descriptors from inert source text, classifies
the behavior graph, extracts exact synthetic indicators, and validates the
complete candidate map against the API question IDs and enum formats. Each
assignment contains 87 answers; Mastery has two deliveries and 174 answers.

## Attempts and results

| Mode | Attempt | Answers accepted | Game Master result | Hall of Fame | Standings |
| --- | --- | ---: | --- | --- | --- |
| Single Solve, historical | `be8c2eb9-64f1-49fc-bd92-cfdb75699ff6` | 87 / 87 | `CORRECT` | Not applicable | — |
| Time Trial, historical | `2aeb1c7e-df8f-42d7-b7ac-9dcea0c5372d` | 87 / 87 | `CORRECT` | Ineligible | — |
| Mastery, historical | `a1891827-0362-4141-a93f-45965f905084` | 174 / 174 | `CORRECT` | Ineligible | — |
| Time Trial, ranked | `33baf158-5536-45b4-9e42-d6e2ad81c99d` | 87 / 87 | `CORRECT` | Eligible | 2.646 s, place 101 |
| Time Trial, ranked repeat | `fc24b24d-7a34-42d2-adef-a58df407b9f7` | 87 / 87 | `CORRECT` | Eligible | Not returned by the proxy |
| Time Trial, ranked repeat 2 | `e49181bd-b43f-43d2-8050-b8ca957c3fc8` | 87 / 87 | `CORRECT` | Eligible | 0.681 s, place 39 |
| Mastery, ranked | `179ed688-4972-46e8-b4d7-bde376143ebd` | 174 / 174 | `CORRECT` | Eligible | 3.513 s, place 94 |
| Mastery, ranked repeat | `20437104-cc1d-4ad4-a164-669e967b7244` | 174 / 174 | `CORRECT` | Eligible | 1.073 s, place 35 |

Ranked times and places in the final column were supplied by the user from
CourseStack; the Game Master responses do not return standings. Before this
batch, the latest user-reported standings were Time Trial 0.681 s/place 39
(from 2.646 s/place 101) and Mastery 1.073 s/place 35 (from 3.513 s/place 94).
After the batch, the user reported Time Trial holding at 0.681 s/place 39 and
Mastery improving to 0.943 s/place 29. The additional runs were explicitly
authorized after the original one-attempt limits.

### Additional authorized batch: 10 Time Trial and 10 Mastery attempts

Each attempt below returned `CORRECT`, accepted every answer, and reported
`hall_of_fame_eligible: true`. The client wall times include Game Master
requests and are not the official CourseStack leaderboard times.

| Mode | Attempt ID | Client total | Solver processing | Attempts remaining after run |
| --- | --- | ---: | ---: | ---: |
| Time Trial 1 | `753825a8-65e8-46d1-9aff-d74b3559ab6f` | 2.596 s | 41 ms | 9 |
| Time Trial 2 | `b3e0a9e2-d309-49d3-b7d9-3840fd5e93ca` | 5.284 s | 41 ms | 8 |
| Time Trial 3 | `5f0181d7-be78-4270-8032-68ea9ac97de3` | 4.364 s | 45 ms | 7 |
| Time Trial 4 | `c7537d73-1fae-4bcb-bb0e-4687daedc4b5` | 2.180 s | 41 ms | 6 |
| Time Trial 5 | `174cdbef-bded-4541-92c6-e478a297e32f` | 2.133 s | 41 ms | 5 |
| Time Trial 6 | `88ed95eb-c29c-49e1-97a5-2d59a67dc5c5` | 2.233 s | 48 ms | 4 |
| Time Trial 7 | `7ed05bfe-28d3-459a-b720-a5e74b31fad2` | 2.441 s | 97 ms | 3 |
| Time Trial 8 | `c5051074-550c-4c57-bb9b-204069de34f5` | 1.911 s | 43 ms | 2 |
| Time Trial 9 | `4292a56f-ef43-4d92-9202-0a8404c8a9b5` | 4.353 s | 42 ms | 1 |
| Time Trial 10 | `4c73ea97-ec8d-451d-81ab-8673f7827fa4` | 4.867 s | 42 ms | 0 |
| Mastery 1 | `47c94eea-c543-41bb-bf9a-cd71f1a7787f` | 5.362 s | 101 ms | 24 |
| Mastery 2 | `3432e373-c365-403a-bcc2-06539c257bf9` | 5.179 s | 99 ms | 23 |
| Mastery 3 | `c426026a-d165-4206-8a19-27bb7a712e93` | 4.428 s | 102 ms | 22 |
| Mastery 4 | `ea316bf8-3761-47e9-a9a5-94a892f9480d` | 3.118 s | 81 ms | 21 |
| Mastery 5 | `6bbf4a89-7d62-498d-a3ca-4ff9bf0b38d3` | 3.588 s | 81 ms | 20 |
| Mastery 6 | `5308d145-d416-4e1e-b6d0-04bb426ebfcd` | 2.351 s | 78 ms | 19 |
| Mastery 7 | `5bb49cbe-e016-4f5f-8157-d8514b9c2c6e` | 4.656 s | 78 ms | 18 |
| Mastery 8 | `89f0276c-4e2d-41cd-83b1-bd9cf8b8f905` | 5.200 s | 77 ms | 17 |
| Mastery 9 | `018a101a-a085-4f4e-b007-18848a602a14` | 4.707 s | 78 ms | 16 |
| Mastery 10 | `fda171ba-9556-4f8d-8a4b-16c50740e58d` | 4.892 s | 78 ms | 15 |

Time Trial client totals averaged 3.236 s (median 2.518 s, range 1.911–5.284 s);
Mastery totals averaged 4.348 s (median 4.681 s, range 2.351–5.362 s). Solver
processing stayed between 41 and 97 ms for Time Trial and 77 and 102 ms for
Mastery. Most variation came from artifact, submission, and status request
latency. The CourseStack standings after this batch were not available through
the Game Master proxy.

The first three Mastery attempts used an experimental parallel extraction
change. Its offline regression produced the same 174-answer map, but processing
times stayed around 99–102 ms and did not improve. The change was reverted
before Mastery attempt 4. The committed runner continues to download the two
Mastery deliveries concurrently and submit the answer map as one batch.

The historical solve attribution is unavailable. Before the ranked runs, both
old timed attempts had ended and all their answer IDs were accepted. The three
ranked Time Trial deadlines were 2026-10-28 22:41:38, 22:56:08, and 22:59:15
UTC (50 seconds each). The two Mastery deadlines were 22:42:32 and 22:59:58 UTC
(80 seconds each). No API response reported a pending scoring state. The proxy
does not expose numeric CourseStack points.

The ranked runner's measured client wall times were **7.05**, **5.59**, and
**3.17 seconds** for Time Trial, and **7.60** and **2.75 seconds** for Mastery.
These totals include Game Master requests; exact server-side completion
timestamps were not returned. The live listing's solve budgets were 30 seconds
and 60 seconds, respectively.

## Training limits

Both timed routes are legacy timed-by-default routes:

- `run_for_time_supported` is `false`.
- `regular_pool_size` is `0`.
- The Time Trial ranked pool has 32 variants. Ten additional attempts were
  used in this batch; the latest response reported 0 attempts remaining.
- The Mastery ranked pool has 32 variants; 27 attempts remained before the
  first ranked run, 26 after it, 25 before this batch, and 15 after it.
- `op=practice` is documented as a legacy continuation after fresh variants
  are used. It was not invoked while ranked attempts remained.

No untimed Time Trial or Mastery attempt was available because both routes
have `regular_pool_size: 0`. All 20 attempts in the additional batch were
timed ranked attempts, explicitly authorized by the user. There were no fresh,
non-ranked artifacts available for training.

## Artifact records

Every artifact below is an API-assigned `evidence.zip` bundle. It contains
PowerShell scenario samples and JScript specimens. Mastery deliveries are
separate bundles and map to their corresponding `set1.*` or `set2.*` question
IDs. SHA-256 values were checked after each run, outside the timed path.

### Single Solve

- Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `7743a1af7c51d0950e7620561cf392791a9537e044a8ca11d344b11540ade516`

### Historical Time Trial

- Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `190a2f8861d0aeaf55e571c16ef4d2c3f7caddf01d23374653ccda22b9b0350f`

### Historical Mastery

- Download delivery 1 evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `6d446dae77bd1038557396ef8b673de86fd6a2691329b76671f7088882420943`
- Download delivery 2 evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `7c6712f011a58e43d9ddb6fa5d230061f4060aa18e5aae77847aed9ff904fd75`

### Ranked Time Trial

- Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `ac05667135d67ba77d85ded9412d864637b1f40a2bc556393ee602f2e89909f8`
- Download repeat evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `8ed05ae03561c83c15af16ec03038e7dd7238fd23f4ab402a36c7fd5eaf4870e`
- Download repeat 2 evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `cd4ceff83fce78cf3fd08bec8b9a787570777f5b7a4b8e32a5d39c8596d6cff8`

### Ranked Mastery

- Download delivery 1 evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `5ad1287e44d0dcb7812e072e2b61414da1046ae62d072cc2c360cc7b8f453b32`
- Download delivery 2 evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `1409271054c8c39735a56dbd68218cb3f3e56359eca2d2b2e7b3e5f746589ef5`
- Download repeat delivery 1 evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `71810765c3fb3e521832a0f121f99e4a9ab41891d3bffabe549672b07f27b039`
- Download repeat delivery 2 evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `ec1c38ae9608ba694bdc5293f30f96c5480f67474396f7f1cd9351e3e162d8da`

### Additional authorized batch artifacts

These fresh bundles were assigned to the 10 Time Trial and 10 Mastery attempts
listed above. Each local SHA-256 matched the API-provided value.

#### Time Trial

- Run 1: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `3e5d41cf21da4360a20fdad95ebb467a72fbcd4295cb93a854c12513a24d255e`
- Run 2: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `262e540edef0f06e083a9dffeb3a40c59cd8921f03daf454d1b52347ff63d7a6`
- Run 3: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `2cc8db3d374c86eacba78a5daaa52ee0eb1109254f3370d1302d8ec6a57e0723`
- Run 4: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `f62773fe1d72d8a86cb3f033a30ec26c988a5c79824b5c6ef517f81cf6bb90ee`
- Run 5: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `eba18dde962f7be09edea85414f1fc50a2b3af8ef99e32265f2b46e42ea40d58`
- Run 6: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `1a958d1e06f82515dd9250db354ea32a8d7b063a48ddade2067e352aff66ce7e`
- Run 7: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `d0a49e81512fb2e00932df4afbfa8180a0933859df44f21bf6adb58d19ef0af1`
- Run 8: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `4b26a587d316532d2d20bddc12a39719013cc30ce8ba4c9ed457abe8424f99e3`
- Run 9: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `a8443935d8f1ba073a028128acc81aa442e11c3e911d73c24cd950b4af9d2ca4`
- Run 10: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `1a425f9c8808915a7297ca77cdd12dcf429ee4b0586839f2f4bdf837a1b0a058`

#### Mastery

- Run 1, delivery 1: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `6fbd035528745ecb299bc49a93571dabb002d8a81590622e46d8826a39f6724b`
- Run 1, delivery 2: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `574fc8845c397048f94ff7f158dac48e2b39a14a5f0ab0635fd42172804bf712`
- Run 2, delivery 1: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `bda5c1dbbdbc9b95329916677bc72f4eea5e675be5e9e49df4b66528fc9c13c1`
- Run 2, delivery 2: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `d45739822e8756a5fdb518e4a1bf66b7c1af1ae6611a42dbb0a998271a430154`
- Run 3, delivery 1: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `b68beac3d4c165bc6ca10440baa9ad87f39e74c8964c29604fb6dc3afb03b566`
- Run 3, delivery 2: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `056fa40d8fa664b234ef2a84f0bf2c998945b7eeaa778cdcfd188fe96db31329`
- Run 4, delivery 1: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `f888b8c2f22b25ca3113d93624fd60d4a87df0b6d0f8cf8c2454b4890478f708`
- Run 4, delivery 2: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `dde3311c85e7d6e97646be9f482f095c46059781dd5526e2a01487f4b9b0a96f`
- Run 5, delivery 1: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `29b124ca2b51cc022fb201f4bfe2dd361125796621823ad397594b56212d467b`
- Run 5, delivery 2: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `9749adb09f8cd2343065308c886defdd6d817a98dc43ad91e9930366eec8909c`
- Run 6, delivery 1: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `68399c3525fadc41f0603bdeb382eedad067938d7f6c4175581b60554417de79`
- Run 6, delivery 2: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `ec412e8971434afb41cdda4549e419316c92c5eaa8f7817fb09b135ae49703a2`
- Run 7, delivery 1: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `449761b9a4250387b0fb25934f50aaf3f6cbac4e0497c1b2185aa5f441c2722f`
- Run 7, delivery 2: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `8c1bab445b9743add681c87a7f1964a7d46de69ed3300eec91e31e118dfb2626`
- Run 8, delivery 1: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `0800fdb496f3bba7cf3f25df107c13ba12d00c093b95757fd0edd5fab40dbb27`
- Run 8, delivery 2: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `19f4279da8ebfd42fa9c6a9ebb8aa71e67e96e28326497c34b15be0414f83d31`
- Run 9, delivery 1: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `2fcfea1765095083ad3b08c6e293959222088860fe4e0e50c2b833908458cf4b`
- Run 9, delivery 2: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `fb284c685864969b10415a8734470622fd9d62aadd7d4f8baec1586580836a13`
- Run 10, delivery 1: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `cba5420b040a04809369a4f73155a856c6f3b54822c7937881a6f3fa1717094e`
- Run 10, delivery 2: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256: `6f456fd35aa519637bf1193fa0830ae35d6b7d3ef7dbb80b32e5512dfda6112c`

## Solver and execution

The maintained implementation is `script-analysis-tools/script_analysis_solver.py`.
It does not execute challenge specimens. The mode runner downloads each
delivery, extracts it with the event ZIP password `infected`, builds answers
from the live questions, submits them, and records accepted IDs and status.
Mastery deliveries are downloaded concurrently and mapped to their numbered
sets. The first delivery reuses the warm connection from the start request;
other concurrent deliveries use independent sessions.

Dependencies are listed in `script-analysis-tools/requirements.txt`:

```sh
python3 -m pip install -r script-analysis-tools/requirements.txt
```

For an already downloaded and extracted assignment, generate and validate the
candidate map offline:

```sh
python3 script-analysis-tools/script_analysis_solver.py extracted-artifacts \
  --answer-map start-or-status.json \
  --output candidate-answers.json
```

For a deliberate ranked run on these legacy routes, `--retry` begins a timed
attempt. Review the live list and status first; do not use this command for
untimed training.

```sh
python3 script-analysis-tools/run_modes.py \
  'script-analysis-day-02-encoded-intent/time_trial' --retry --fast

python3 script-analysis-tools/run_modes.py \
  'script-analysis-day-02-encoded-intent/mastery' --retry --fast
```

The new `--fast` option skips optional artifact hashing and a second file read
for the timed summary. The runner still saves the artifacts and candidate
answers. It prints the new attempt ID, deadline, answer count, remaining
attempts, and the actual `hall_of_fame_eligible` value immediately after start.
Hashes can be checked from the saved artifacts after the deadline.

## Regression and performance

Forty-one artifact bundles were processed: one Single Solve, one historical
Time Trial, two historical Mastery deliveries, 13 ranked Time Trials, and 24
ranked Mastery deliveries. On every bundle, the solver produced a complete
candidate map with no empty answers and matching API question IDs. All 41
local hashes matched their API-provided values.

The three historical assignments were tested offline only; their already
accepted answers were not resubmitted. All 25 new ranked assignments (13 Time
Trial and 12 Mastery attempts) were submitted end to end and accepted every
answer. The first five new assignments used the following client times:

| Run | Artifacts downloaded | Solver processing | Submission requests | Client total | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Ranked Time Trial, first | 1.68 s | 41 ms | 2.22 s | 7.05 s | 87 / 87 accepted |
| Ranked Time Trial, repeat | 1.88 s | 42 ms | 1.33 s | 5.59 s | 87 / 87 accepted |
| Ranked Time Trial, repeat 2 | 0.35 s | 41 ms | 0.67 s | 3.17 s | 87 / 87 accepted |
| Ranked Mastery, first | 2.25 s | 82 ms | 1.79 s | 7.60 s | 174 / 174 accepted |
| Ranked Mastery, repeat | 0.68 s | 78 ms | 0.72 s | 2.75 s | 174 / 174 accepted |

Answer generation alone took about 10–14 ms for 87-answer sets and 20 ms for
the 174-answer Mastery set during offline timing. Download and Game Master
request latency dominate local processing time. For the additional 10+10
batch timings, see the attempt table above. No new untimed variants were
available. The parallel extraction experiment was reverted; the final runner
keeps concurrent artifact downloads and avoids optional timed-path hashing
with `--fast`.

## Files changed and remaining risks

- `script-analysis-tools/run_modes.py` now reports the attempt's eligibility
  immediately and offers `--fast` to skip optional timed-path hashing.
- The Mastery downloader reuses the start request's warm connection for its
  first artifact while downloading remaining deliveries concurrently.
- `writeups/day-02/script-analysis-host-with-the-most.md` records the workflow,
  attempts, artifacts, and results.
- Attempt responses, archives, candidate maps, post-run statuses, and hashes
  are preserved under `work/day-02/script-analysis/`.

All available saved artifacts and all 25 new randomized ranked assignments
processed successfully. There were no fresh non-ranked variants to test. The
Game Master proxy did not provide updated CourseStack places after the latest
batch. Future randomized changes to the JScript encoding scheme or question
wording could still exceed the parser's current supported patterns; a new
answer ID or empty candidate is rejected before submission.
