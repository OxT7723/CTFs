> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 02 — Looks Can Be Deceiving

## Challenge

- **Name:** 🔎 Looks Can Be Deceiving
- **Category:** Metadata Forensics
- **Single Solve ID:** `metadata-forensics-day-02-looks-can-be-deceiving`
- **Time Trial ID:** `metadata-forensics-day-02-looks-can-be-deceiving/time_trial`
- **Mastery ID:** `metadata-forensics-day-02-looks-can-be-deceiving/mastery`
- **Description:** “The extensions claim one story; the first sixteen bytes tell another. Identify what each artifact actually is and isolate the deliberate disguise.”

Single Solve has no deadline. Time Trial and Mastery are legacy
timed-by-default routes with no untimed regular pool; their published ranked
deadlines are 50 seconds and 80 seconds, respectively. The Mastery deadline is
shared by its two sets.

The challenge's common guidance says to use the supported Homebase proxy for Game Master requests, work from assigned bytes, submit under the exact `answer_ids`, and treat artifacts as untrusted data. Full guidance and every other response field are preserved in the saved Game Master responses under `work/day-02/metadata-forensics/looks-can-be-deceiving-review-20261028/` (historical reference: `../../work/day-02/metadata-forensics/looks-can-be-deceiving-review-20261028/`; not included).

## Questions and answer formats

Every value uses the normalization returned by the API. The first sixteen bytes must be represented as exactly 32 lowercase hexadecimal characters, with no prefix or spaces. The randomized ranked assignments also asked for basic file identity fields.

| Assignment | Answer ID | Player-facing question | Artifact | Format |
| --- | --- | --- | --- | --- |
| Historical Single Solve | `evidence-note-magic-prefix-hex-16` | What are the first sixteen bytes as lowercase hexadecimal? | `metadata-day-02-evidence.zip -> evidence-note.txt` | Exactly 32 hexadecimal characters; no `0x` prefix or spaces. |
| Historical Time Trial | `roster-magic-prefix-hex-16` | What are the first sixteen bytes as lowercase hexadecimal? | `metadata-day-02-evidence.zip -> roster.csv` | Exactly 32 hexadecimal characters; no `0x` prefix or spaces. |
| Historical Mastery, set 1 | `set1.evidence-note-copy-magic-prefix-hex-16` | What are the first sixteen bytes as lowercase hexadecimal? | `metadata-day-02-evidence-01.zip -> evidence-note-copy.txt` | Exactly 32 hexadecimal characters; no `0x` prefix or spaces. |
| Historical Mastery, set 2 | `set2.disguised-report-magic-prefix-hex-16` | What are the first sixteen bytes as lowercase hexadecimal? | `metadata-day-02-evidence-02.zip -> disguised-report.bin` | Exactly 32 hexadecimal characters; no `0x` prefix or spaces. |
| Ranked Time Trial | `evidence-note-filename` | What is the exact filename of the first evidence note? | `metadata-day-02-evidence.zip` | Exact base filename including extension, no path, quotes, or explanation. |
| Ranked Time Trial | `evidence-note-size-bytes` | What is its exact size in bytes? | `metadata-day-02-evidence.zip -> evidence-note.txt` | Base-10 integer, no units, separators, or explanation. |
| Ranked Time Trial | `evidence-note-md5` | What is its MD5 digest? | `metadata-day-02-evidence.zip -> evidence-note.txt` | Exactly 32 hexadecimal characters; case-insensitive. |
| Ranked Time Trial | `evidence-note-sha1` | What is its SHA-1 digest? | `metadata-day-02-evidence.zip -> evidence-note.txt` | Exactly 40 hexadecimal characters; case-insensitive. |
| Ranked Time Trial | `evidence-note-sha256` | What is its SHA-256 digest? | `metadata-day-02-evidence.zip -> evidence-note.txt` | Exactly 64 hexadecimal characters; no prefix, spaces, or explanation; case-insensitive. |
| Ranked Time Trial | `evidence-note-magic-prefix-hex-16` | What are the first sixteen bytes as lowercase hexadecimal? | `metadata-day-02-evidence.zip -> evidence-note.txt` | Exactly 32 hexadecimal characters; no `0x` prefix or spaces. |
| Ranked Mastery, set 1 | `set1.evidence-note-filename`, `set1.evidence-note-size-bytes`, `set1.evidence-note-md5`, `set1.evidence-note-sha1`, `set1.evidence-note-sha256`, `set1.evidence-note-magic-prefix-hex-16` | The same six questions and formats as the ranked Time Trial. | `metadata-day-02-evidence-01.zip`, with the size and digests taken from its `evidence-note.txt` member. | Same formats as the corresponding ranked Time Trial rows. |
| Ranked Mastery, set 2 | `set2.evidence-note-filename`, `set2.evidence-note-size-bytes`, `set2.evidence-note-md5`, `set2.evidence-note-sha1`, `set2.evidence-note-sha256`, `set2.evidence-note-magic-prefix-hex-16` | The same six questions and formats as the ranked Time Trial. | `metadata-day-02-evidence-02.zip`, with the size and digests taken from its `evidence-note.txt` member. | Same formats as the corresponding ranked Time Trial rows. |

**Done** means all answer IDs in that attempt are accepted. The Game Master returned `CORRECT` for both ranked attempts and marked both Hall of Fame eligible.

## Files

Each bundle is assigned by the Game Master for its listed mode. A bundle contains the evidence file or files named in that attempt's questions. The solver follows the question's artifact descriptor into the ZIP rather than assuming a fixed member name.

| Assignment | API filename | Download | SHA-256 |
| --- | --- | --- | --- |
| Historical Single Solve | `metadata-day-02-evidence.zip` | Download historical Single Solve bundle (retired artifact link; see artifact inventory) | `c356020d0dafda86d80d000b3e3e1c0524f3a0c1a84ade856a74959047c1be67` |
| Historical Time Trial | `metadata-day-02-evidence.zip` | Download historical Time Trial bundle (retired artifact link; see artifact inventory) | `cb06ac9e8c8a73195752578d821dd7ce8cb83d42cf1fb123bc05e58af2a8cdfb` |
| Historical Mastery | `metadata-forensics-day-02-looks-can-be-deceiving-mastery.zip` | Download historical Mastery bundle (retired artifact link; see artifact inventory) | `286fe65f5037df6f4b42c2404d56e50a6156ae03635349f4f81b39a474320c98` |
| Ranked Time Trial | `metadata-day-02-evidence.zip` | Download ranked Time Trial bundle (retired artifact link; see artifact inventory) | `cf5e3fb9b0b5ceeeca8060bd493019b1728b13f8ef43faf7369688297e400508` |
| Ranked Mastery | `metadata-forensics-day-02-looks-can-be-deceiving-mastery.zip` | Download ranked Mastery bundle (retired artifact link; see artifact inventory) | `f31330e23d21f247b43d97c34ea604c8edc6bf65f7a3f38882a1707280073ee4` |

The ranked bundles were kept at
`work/day-02/metadata-forensics/looks-can-be-deceiving-review-20261028/ranked-attempts/` (historical reference: `../../work/day-02/metadata-forensics/looks-can-be-deceiving-review-20261028/ranked-attempts/`; not included).
Post-run hashes match the manifests. The solver deliberately skips optional
outer-bundle hashing during timed execution.

## Solver

The existing [`metadata-forensics-tools/run_challenge.py`](../../../../tools/later/metadata-forensics-tools/run_challenge.py)
already supports the artifact-derived fields used here. It downloads every
delivery, recursively reads ZIP members, matches question descriptors to
files, builds answers from the live question IDs, validates the complete ID
set, checks accepted IDs before submitting, then records the result and status.
The solver does not rely on a known magic prefix, filename, or answer ID.

Run a regular Single Solve attempt with:

```sh
GAME_MASTER_PROXY_URL='http://192.0.2.1/huntress-ctf-proxy' \
  python3 metadata-forensics-tools/run_challenge.py \
  'metadata-forensics-day-02-looks-can-be-deceiving'
```

This challenge's Time Trial and Mastery are legacy timed-by-default routes:
they report `run_for_time_supported:false` and `regular_pool_size:0`. Do not
use these commands for preparation. After preflight and authorization for a
ranked run, one new timed variant is started with `--retry` and **without**
`--run-for-time`:

```sh
GAME_MASTER_PROXY_URL='http://192.0.2.1/huntress-ctf-proxy' \
  python3 metadata-forensics-tools/run_challenge.py \
  'metadata-forensics-day-02-looks-can-be-deceiving/time_trial' \
  --retry --warm-connection --profile

GAME_MASTER_PROXY_URL='http://192.0.2.1/huntress-ctf-proxy' \
  python3 metadata-forensics-tools/run_challenge.py \
  'metadata-forensics-day-02-looks-can-be-deceiving/mastery' \
  --retry --warm-connection --profile
```

For these legacy routes, `--retry` is timed. The runner now treats any
server-provided deadline as timed, even when `run_for_time` is absent. It
warms and reuses one HTTP connection for the start, artifact, and submission
requests, and omits optional artifact hashing from the speed-critical path.
`--profile` reports request latency and local processing after the attempt.

## Results and reliability

| Mode | Result | Work performed | Client wall time |
| --- | --- | --- | ---: |
| Single Solve | Historical attempt `755c8028-940f-4918-8167-cef70e9a0c31`: `CORRECT`, 1/1 accepted | Rebuilt one candidate from downloaded bytes; bundle hash verified. | 0.04 ms answer processing |
| Time Trial, historical | Historical attempt `e941217b-0e65-4d52-aa6b-50763408981e`: `CORRECT`, 1/1 accepted; expired `2026-10-03T16:44:13.566Z` deadline | Rebuilt one candidate; bundle hash verified. No fresh untimed regular pool existed. | 0.036 ms answer processing |
| Mastery, historical | Historical attempt `3cd7127f-d3ff-49dc-91ec-c7e7cbc4c90b`: `CORRECT`, 2/2 accepted; expired `2026-10-03T16:48:36.051Z` deadline | Rebuilt both candidates; bundle hash verified. No fresh untimed regular pool existed. | 0.987 ms answer processing |
| Time Trial, ranked | Attempt `7574dbb3-bfef-4ec7-9ae8-5c8b0071dd83`: `CORRECT`, 6/6 accepted, Hall of Fame eligible | Fresh randomized bundle. Server deadline: `2026-10-28T22:42:21.118Z`. CourseStack: **2.888 s, place 86**. | 7.97 s end-to-end client time |
| Mastery, ranked | Attempt `7e0407e5-1fae-4e7a-b3fc-2f5a00b5d022`: `CORRECT`, 12/12 accepted across two sets, Hall of Fame eligible | Fresh bundle covering two randomized sets. Server deadline: `2026-10-28T22:43:14.805Z`. CourseStack: **3.373 s, place 85**. | 8.43 s end-to-end client time |
| Time Trial, ranked, warmed connection | Attempt `40e6d979-979c-48be-ad90-b35c0e14e15a`: `CORRECT`, 6/6 accepted, Hall of Fame eligible | Second fresh randomized bundle. Server deadline: `2026-10-28T22:54:00.408Z`. CourseStack: **2.152 s, place 81**. | 6.34 s end-to-end client time |
| Mastery, ranked, warmed connection | Attempt `2d9fb3e9-6cc8-4234-8cdc-f1508d5d0ffc`: `CORRECT`, 12/12 accepted across two sets, Hall of Fame eligible | Second fresh bundle covering two randomized sets. Server deadline: `2026-10-28T22:54:46.587Z`. CourseStack: **2.619 s, place 76**. | 7.29 s end-to-end client time |
| Time Trial, ranked, warmed connection | Attempt `66e2b6bd-804f-4030-8c9e-65b05590bf95`: `CORRECT`, 6/6 accepted, Hall of Fame eligible | Third fresh randomized bundle. Server deadline: `2026-10-28T23:02:36.370Z`. Updated CourseStack time/place not provided. | 6.11 s end-to-end client time |
| Mastery, ranked, warmed connection | Attempt `7abc3ca6-d1da-4310-8831-98d14fd2784f`: `CORRECT`, 12/12 accepted across two sets, Hall of Fame eligible | Third fresh bundle covering two randomized sets. Server deadline: `2026-10-28T23:03:21.351Z`. Updated CourseStack time/place not provided. | 5.89 s end-to-end client time |

The first ranked attempts began at `2026-10-28T22:41:31.118Z` and
`2026-10-28T22:41:54.805Z`; their warmed-connection follow-ups began at
`2026-10-28T22:53:10.408Z` and `2026-10-28T22:53:26.587Z`. The Game Master
reports 29 unique attempts remaining after the second attempt in each mode;
the third attempt left 28 unique attempts in each mode. It does not expose a
separate `ranked_attempts_remaining` counter or CourseStack solve time.
CourseStack reported the first two runs' times and places shown above; the
third-run times and places were not provided. All warmed-connection Game
Master results were `CORRECT` without a pending-scoring state, and the final
challenge listing marks all three modes solved.

No fresh untimed Time Trial or Mastery replay was available, and `op=practice`
was not applicable because the ranked rotation was not exhausted. In addition
to the three historical assignments, three fresh Time Trial bundles and three
fresh two-set Mastery bundles were processed and submitted. An offline
regression reproduced the exact saved candidates from all nine assignments,
verified all nine bundle hashes, and matched all saved answer IDs.

The ranked answer computation took under 1.25 ms per assignment when
reprocessed locally after the runs; timed artifact handling and answer building
remained under 3 ms combined. The observed end-to-end time was dominated by the
Game Master requests. The solver is ready for the tested question and archive
variations; an unseen future format could still require a new handler.

After the initial ranked runs, a read-only connection check took 2.07 seconds
for the first status response and about 0.93–0.97 seconds for later responses
on the same HTTP connection. The runner now keeps that connection alive across
the timed requests and warms it with a status check before retry. On all four
follow-up runs, retry, artifact, and submit reused the same connection. The
latest Game Master timings were 1.54/1.35/1.10 seconds for Time Trial and
1.44/1.31/1.20 seconds for Mastery (retry/artifact/submit). The CourseStack
times for the second runs improved by 0.736 seconds for Time Trial and 0.754
seconds for Mastery over the first runs. Third-run CourseStack times are not
available, so their score change and the precise contribution of connection
reuse remain unknown.

### Ten-attempt optimization batch — 2026-10-28

At the player's request, ten additional ranked retries were run in each mode.
The runner performed a status preflight before every retry, reused its warmed
HTTP connection for retry/artifact/submit/final status, skipped optional
outer-bundle hashing, and submitted all answers in one request. Each attempt
returned `CORRECT` and `hall_of_fame_eligible:true`; all assigned answer IDs
were accepted. Offline hashing confirms ten distinct bundles in each mode.

| Mode | Attempts | Answers accepted | Distinct bundles | Client wall time |
| --- | ---: | ---: | ---: | ---: |
| Time Trial | 10/10 | 55/55 (one bundle asked one question; the other nine asked six each) | 10 | 2.37–7.71 s; mean 4.86 s |
| Mastery | 10/10 | 120/120 across two sets per attempt | 10 | 2.42–6.91 s; mean 4.49 s |

Time Trial attempt IDs, in run order: `fb6f526b-7586-4241-8c3f-a0144896696f`,
`b8c693a5-980e-4bd1-945f-4c9543fae258`,
`fcb9bee5-1a49-49bc-b57c-7e33e16724dd`, `7fba1005-c200-4203-a749-d790e557e977`,
`47023b14-fd78-4daf-9aae-2abcd2a6f388`,
`253acaf2-4832-4728-8070-a45ab51ad705`,
`dc7a6633-bfd4-4991-9b68-fd20745b61f9`,
`0d10ecaa-215a-4c88-a104-5ab58ab26797`,
`63672d25-8acc-4b2c-b95a-755293a2b9b0`,
`3a6745d5-1b1b-43e9-9589-68fbda545d5c`.

Mastery attempt IDs, in run order:
`5d39f84d-0f66-4675-a6cf-9aedb54fb87a`,
`1a9f3c20-41b4-49cf-b976-eb03d5e956f3`,
`2a81b9c0-2687-43a6-84f3-74cee9e2774c`,
`b812c23a-829b-4716-8468-d0bd1c990259`,
`7fdf6dd6-ea65-4ca6-9d02-8ee0c3f6ed80`,
`48e5fd35-9363-4d4d-8974-c21fc12bd7ad`,
`b6d36458-3382-47c7-8bf0-eeae51cc1d92`,
`24cafd9a-d5b7-49a6-9fac-f8771b325b7c`,
`7a066bfc-7bf0-4153-b32c-26c272873e2d`,
`a8f0d128-fc0c-408e-b48d-e113bedac24c`.

The local artifact processing and answer construction together remained below
3 ms per attempt. Request latency accounted for almost all client wall time and
varied between runs, so no speculative solver change was made between attempts.
Every response and downloaded bundle is retained under
`ranked-attempts-batch10/` (historical reference: `../../work/day-02/metadata-forensics/looks-can-be-deceiving-review-20261028/ranked-attempts-batch10/`; not included).
The final live status for each mode reports `CORRECT`, every current answer ID
accepted, and 18 `unique_attempts_remaining`. The service returns
`ranked_attempts_remaining:null`; it does not provide a separate ranked
counter. The Game Master responses did not include CourseStack score times or
places. After this batch, the player reported CourseStack bests of **0.556 s,
place 28** for Time Trial and **0.657 s, place 41** for Mastery. Compared with
the immediately preceding reported scores (2.114 s/place 80 and 2.228 s/place
73), those are improvements of 1.558 seconds and 52 places for Time Trial, and
1.571 seconds and 32 places for Mastery.
