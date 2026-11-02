# Exported Trust

Day 1 · Mobile / Android · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `mobile-android-day-01-exported-trust`

## Earlier local account

**Release:** Day 01 Challenges

| Author | Category |
|---|---|
| [John Hammond](https://youtube.com/@_JohnHammond), and [Just Hacking Training](https://justhacking.com) | 📱 Mobile |

Identify an exported deep-link Activity that attaches an embedded client credential, invoke it with the correct case reference, and return the backend evidence code.

You can download the **single-solve file** for this challenge here:

**Challenge file:** exported_trust.apk

or ask the Game Master for your single-solve file in the **AI Homebase** virtual machine.

**System:** Start/connect through CourseStack or the challenge instructions.

**Scored task:** Single Solve: Submit the flag for 1 static task. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 2

Use the Game Master to get fresh targets for Time Trial and Mastery Mode.

**Scored task:** Time Trial: Submit the flag for 1 new dynamic task in under 2 seconds. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 3

**Scored task:** Mastery Mode: Submit the flag after completing 3 new dynamic tasks in under 2 seconds. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 5

---

!alt text (source reference: `image.png`; not linked in this draft)

## Later Homebase account

### Day 01 — Exported Trust

### Challenge

- **ID:** `mobile-android-day-01-exported-trust`
- **Lane:** Mobile Android
- **Prompt:** “Identify an exported deep-link Activity that attaches an embedded client credential, invoke it with the correct case reference, and return the backend evidence code.”
- **Historical status:** Single Solve, Time Trial, and Mastery are all recorded as `CORRECT`. This review did not treat those historical completions as new training attempts.

The Time Trial ID is `mobile-android-day-01-exported-trust/time_trial`; the
Mastery ID is `mobile-android-day-01-exported-trust/mastery`.

### Questions and answer formats

The API requires the exact backend answer code, with the format
`ANS-` followed by exactly 16 uppercase hexadecimal characters. Normalization
is exact: submit no spaces or explanation. Every question uses this wording,
with the case and package below substituted:

> For case `<case>` in package `<package>`: Identify an exported deep-link
> Activity that attaches an embedded client credential, invoke it with the
> correct case reference, and return the backend evidence code. Submit only
> the exact backend answer code returned for this case.

| Attempt | Exact answer ID | Case | Package |
| --- | --- | --- | --- |
| Single Solve | `answer` | `MOB-01-073E9A824E` | `com.huntress.mobile.d01.v073e9a824e9e` |
| Historical Time Trial | `answer` | `MOB-01-4D5BCD5AD9` | `com.huntress.mobile.d01.v4d5bcd5ad9c0` |
| Historical Mastery 1 | `set1.answer` | `MOB-01-0DAC1DD945` | `com.huntress.mobile.d01.v0dac1dd9457a` |
| Historical Mastery 2 | `set2.answer` | `MOB-01-D28E90FE08` | `com.huntress.mobile.d01.vd28e90fe0809` |
| Historical Mastery 3 | `set3.answer` | `MOB-01-F1EC220721` | `com.huntress.mobile.d01.vf1ec220721f6` |
| Ranked Time Trial | `answer` | `MOB-01-327559DEFB` | `com.huntress.mobile.d01.v327559defb2f` |
| Additional ranked Time Trial | `answer` | `MOB-01-F05F302A5D` | `com.huntress.mobile.d01.vf05f302a5d4f` |
| Latest ranked Time Trial | `answer` | `MOB-01-68D8E9B679` | `com.huntress.mobile.d01.v68d8e9b6798c` |
| Ranked Mastery 1 | `set1.answer` | `MOB-01-B7A5BCD748` | `com.huntress.mobile.d01.vb7a5bcd748c8` |
| Ranked Mastery 2 | `set2.answer` | `MOB-01-D7FA0F5483` | `com.huntress.mobile.d01.vd7fa0f54839d` |
| Ranked Mastery 3 | `set3.answer` | `MOB-01-FF091C3723` | `com.huntress.mobile.d01.vff091c37239d` |
| Latest ranked Mastery 1 | `set1.answer` | `MOB-01-6DB67922EE` | `com.huntress.mobile.d01.v6db67922eec5` |
| Latest ranked Mastery 2 | `set2.answer` | `MOB-01-9C40FB7A3C` | `com.huntress.mobile.d01.v9c40fb7a3c8c` |
| Latest ranked Mastery 3 | `set3.answer` | `MOB-01-7FFA16DBBA` | `com.huntress.mobile.d01.v7ffa16dbba60` |

### How to submit

Single Solve and Time Trial are complete when `answer` is accepted. Mastery is
complete when `set1.answer`, `set2.answer`, and `set3.answer` are all accepted.
The Game Master reports `CORRECT` for a completed attempt.

### Assigned artifacts

The API assigned one APK to each Single Solve and Time Trial attempt and three
APK deliveries to Mastery. Each contains the app package for its case.

| Attempt | File | API download | SHA-256 |
| --- | --- | --- | --- |
| Single Solve | `exported_trust.apk` | Download APK (private download link removed) | `64169ad2f314746e4d82cd048cd3c436dffafdedc187e01f44cabe6c0068509f` |
| Time Trial | `exported_trust_time_trial.apk` | Download APK (private download link removed) | `9a418563eb785bfec3b34a1a6706961c4065bd6e38f7a5f16072054a8d997049` |
| Mastery 1 | `exported_trust_mastery_01.apk` | Download APK (private download link removed) | `24071b106048b8d47bc3d8247626cc0983be9b7f40f571e40fbaf3c00dd6f611` |
| Mastery 2 | `exported_trust_mastery_02.apk` | Download APK (private download link removed) | `2a4b3b7ec261381f7af0ebfd19d980608cf514169156f6bbf07792f78d884ed8` |
| Mastery 3 | `exported_trust_mastery_03.apk` | Download APK (private download link removed) | `39cbacadae49960a34db1ffaf0691d2763a8c4e695647f5108c1fe48212fe53f` |
| Ranked Time Trial | `exported_trust_time_trial.apk` | Download APK (private download link removed) | `27519bb703abc85ba5753c0a1f4f1bd3b53f4ea4fc058a02f5ad02d8337a7f5b` |
| Additional ranked Time Trial | `exported_trust_time_trial.apk` | Download APK (private download link removed) | `e3c10f4c4a8c0126e53fa47699e67dc37aa0897d52837709f16f0871e2076e5a` |
| Latest ranked Time Trial | `exported_trust_time_trial.apk` | Download APK (private download link removed) | `e16076a273e64026dd6b8a43b2792fe9881fcb4c24490dc1bfd587d375c9e4b2` |
| Ranked Mastery 1 | `exported_trust_mastery_01.apk` | Download APK (private download link removed) | `48329f43943e9c4f630dda479732419ab80145ff9258ad26ddc5d8af59be7e5c` |
| Ranked Mastery 2 | `exported_trust_mastery_02.apk` | Download APK (private download link removed) | `91c3c7bf701a924f208fd2fc4a0331c7bd22917d68ebecd366068c8aa623a2b0` |
| Ranked Mastery 3 | `exported_trust_mastery_03.apk` | Download APK (private download link removed) | `9e7f80f153b3a76a2670376911e6060a93f8a53ac01d55f09e749c73f0d180b7` |
| Latest ranked Mastery 1 | `exported_trust_mastery_01.apk` | Download APK (private download link removed) | `bc9d531cf86435c9365e95ea1054115bb00954a9e29e3749d8918dec93d12e9b` |
| Latest ranked Mastery 2 | `exported_trust_mastery_02.apk` | Download APK (private download link removed) | `c8b6594242b8bd17cbad3b2d4c58d36ab16feff00aaa9f56d67ba5bf2dadbc26` |
| Latest ranked Mastery 3 | `exported_trust_mastery_03.apk` | Download APK (private download link removed) | `bfa7d6cba5c6e10ddd14b5204de6b82c1b6c838d665ad5971ceafdf074c54e74` |

The saved copies and sanitized response manifests used for offline regression
are under
`work/day-01/mobile-android/exported-trust-review-20261028/`.

### Solver review

The shared Android decoder already supports APK JSON assets and honors each
asset's declared codec. All five saved APKs use a plain-text puzzle asset. The
mode runner extracts a candidate from decoded asset bytes, checks it against
the live API answer format, and associates each Mastery question with its
numbered delivery. It rejects missing or ambiguous candidates and verifies
that the generated answer IDs match the response.

Static manifest inspection found an exported `ChallengeActivity` with a
`VIEW`/`BROWSABLE` intent filter for the `huntress01://exported-trust/unlock`
route. DEX strings also contain the local evidence endpoint and client
credential handling. APK code was inspected as data; it was not installed or
executed during offline regression.

### Training and execution

The previous Single Solve attempt ID was
`981d1fe8-3cee-4eb7-bf4b-121f2631555f`; it has no deadline and its answer is
accepted. The historical Time Trial attempt ID was
`575ed415-561a-4c52-a6ae-6a911eb602a7`; its deadline passed, all answers are
accepted, and its historical `hall_of_fame_eligible` value is false. The
historical Mastery attempt ID was
`367833dc-2cd4-4559-9b3f-0c780c7878fd`; its deadline passed, all three answers
are accepted, and its historical eligibility value is false.

Current Game Master metadata identifies these as legacy timed-by-default
routes (`run_for_time_supported:false`). Time Trial has no regular variants
and lists 16 ranked artifacts, one ranked set, and a 50-second ranked deadline.
Mastery has no regular variants and lists eight ranked bundles, three ranked
sets, and a 110-second ranked deadline. Before the latest four-run batch,
status showed seven Time Trial and three Mastery unique attempts remaining.
Two retries in each mode left five Time Trial and one Mastery attempt.
The final authorized Mastery retry used that last attempt, leaving five Time
Trial attempts and none in Mastery. Completed historical status alone does not
establish the eligibility of a future attempt.

No timed operation was used for training. The legacy `practice` continuation
was inspected but not used until the ranked Mastery pool was exhausted. After
the final ranked attempt, one untimed practice continuation reused the last
Mastery bundle; the Game Master returned no attempt ID or deadline.

### Ranked runs this session

| Mode | Attempt ID | Server deadline | Result | Hall of Fame | Tasks | Client end-to-end | Local solver | Attempts remaining |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| Time Trial, first | `986bb300-e94d-46c9-9696-e73aca99c1b8` | `2026-10-28T20:42:05.715Z` (50 seconds) | `CORRECT`; answer accepted | Eligible | 1/1 | 6.35 s | 2.14 ms | 11 |
| Mastery | `1c906037-d3bc-4b4f-ad60-19535f8ffe8c` | `2026-10-28T20:43:37.677Z` (110 seconds) | `CORRECT`; all answers accepted | Eligible | 3/3 | 7.15 s | 2.92 ms | 6 |
| Time Trial, additional | `1145ce0f-c61a-4e19-99bc-7a4cafecb133` | `2026-10-28T20:53:05.739Z` (50 seconds) | `CORRECT`; answer accepted | Eligible | 1/1 | 6.96 s | 2.39 ms | 10 |
| Time Trial, latest | `b75cf4dd-c882-46f2-9080-ded0528af396` | `2026-10-28T20:59:37.999Z` (50 seconds) | `CORRECT`; answer accepted | Eligible | 1/1 | 4.41 s | 2.24 ms | 9 |
| Mastery, latest | `faf4c5c7-c918-41e8-9fca-78b3758b8ff1` | `2026-10-28T21:01:23.381Z` (110 seconds) | `CORRECT`; all answers accepted | Eligible | 3/3 | 6.30 s | 3.05 ms | 5 |
| Time Trial, speed check 1 | `7506630c-3ca0-44ff-ac08-8dde0063f563` | `2026-10-28T21:06:18.849Z` (50 seconds) | `CORRECT`; answer accepted | Eligible | 1/1 | 4.91 s | 2.23 ms | 8 |
| Time Trial, speed check 2 | `2e6a825d-3eb9-4cdd-a9c3-57f2f2478242` | `2026-10-28T21:06:32.298Z` (50 seconds) | `CORRECT`; answer accepted | Eligible | 1/1 | 4.90 s | 2.28 ms | 7 |
| Mastery, speed check 1 | `ca4c7472-526a-4e16-b4fd-a7d431c4023a` | `2026-10-28T21:07:44.898Z` (110 seconds) | `CORRECT`; all answers accepted | Eligible | 3/3 | 5.57 s | 3.21 ms | 4 |
| Mastery, speed check 2 | `54af5a15-ab51-47cf-97bc-4eb91f825fe4` | `2026-10-28T21:07:56.915Z` (110 seconds) | `CORRECT`; all answers accepted | Eligible | 3/3 | 6.14 s | 3.13 ms | 3 |
| Time Trial, fast run 1 | `73a01176-89f2-4f6c-8dea-aedc7c9413fd` | `2026-10-28T21:15:55.040Z` (50 seconds) | `CORRECT`; answer accepted | Eligible | 1/1 | 4.44 s | 2.35 ms | 6 |
| Time Trial, fast run 2 | `43287b05-fc80-4876-81e9-eb2563d504ea` | `2026-10-28T21:16:09.357Z` (50 seconds) | `CORRECT`; answer accepted | Eligible | 1/1 | 6.98 s | 2.20 ms | 5 |
| Mastery, fast run 1 | `74f1d6c4-9ad1-4460-830b-86117e3299b7` | `2026-10-28T21:17:24.563Z` (110 seconds) | `CORRECT`; all answers accepted | Eligible | 3/3 | 5.07 s | 3.03 ms | 2 |
| Mastery, fast run 2 | `dc4bf6ad-1f8b-4cec-90e3-a0737807830d` | `2026-10-28T21:17:38.537Z` (110 seconds) | `CORRECT`; all answers accepted | Eligible | 3/3 | 7.92 s | 3.08 ms | 1 |
| Mastery, final fast run | `839de394-c7b2-4066-bd36-eb20acfbdb14` | `2026-10-28T21:21:46.630Z` (110 seconds) | `CORRECT`; all answers accepted | Eligible | 3/3 | 7.64 s | 3.12 ms | 0 |

The Game Master returned `hall_of_fame_eligible:true` for every ranked attempt
in the table. Final Time Trial and Mastery status responses returned `CORRECT`
with the expected IDs accepted; the latest list reports both modes as solved.
Neither response reported pending scoring. All clocks have ended; no timed
attempt is active.

For Time Trial, the client measured about 2.32 seconds for the retry response,
1.69 seconds for artifact transfer, 1.41 seconds for submission, and 0.92
seconds for the final status request. Mastery measured about 2.23 seconds,
1.87 seconds, 1.54 seconds, and 1.50 seconds for those same steps. The three
Mastery downloads ran concurrently.

The additional Time Trial measured 2.87 seconds for the retry response, 2.25
seconds for artifact transfer, and 1.83 seconds for submission. The updated
runner did not issue a status request before reporting `CORRECT`; a separate
read-only status check afterward confirmed the result. This client run was
slower overall because its service requests took longer. The Game Master API
does not expose the leaderboard's official solve time or place, so the
CourseStack entry is needed to compare ranked times.

The latest Time Trial took 1.81 seconds for start/retry, 1.37 seconds for the
APK download, and 1.22 seconds for submission. The two speed-check Time Trials
took 1.98–2.10 seconds to start, 1.65–1.67 seconds to download, and 1.15–1.26
seconds to submit. Solver time stayed near 2.2 ms.

The latest Mastery took 2.51 seconds for start/retry, 1.75 seconds for all
three concurrent downloads, and 2.04 seconds for submission. The two
speed-check Mastery runs took 1.96–2.25 seconds to start, 2.17–2.53 seconds
for the concurrent downloads, and 1.14–1.64 seconds to submit. Solver time
stayed near 3.2 ms. A separate read-only status request confirmed each run and
its Hall of Fame eligibility. The latest Mastery answers were also reproduced
offline from the saved response and APKs.

The four fast runs used the capability download route and `--fast`. Time Trial
1 took 1.77 seconds to start, 1.41 seconds to download, and 1.26 seconds to
submit. Time Trial 2 took 3.08, 1.86, and 2.04 seconds for those stages.
Mastery 1 took 1.94 seconds to start, 1.72 seconds for the concurrent
downloads, and 1.40 seconds to submit. Mastery 2 took 3.27, 2.25, and 2.39
seconds. The final Mastery retry took 2.52 seconds to start, 2.71 seconds for
the downloads, and 2.40 seconds to submit. Solver time stayed near 3 ms, and
offline fast-mode answers matched all five live outputs.

### Untimed practice after Mastery pool exhaustion

One `op=practice` continuation was run after Mastery's ranked-attempt counter
reached zero. The response marked `practice:true`, `hall_of_fame_eligible:false`,
and had no deadline or attempt ID. It returned all three question IDs but no
artifact manifest or `answer_ids`; the runner now derives the three delivery
indices and answer IDs from the question records. The three downloaded APKs
matched the last ranked Mastery bundle, so this was a replay, not a fresh
randomized variant.

The solver processed and submitted all three practice answers. The submit
response was `already_solved`; the follow-up status still showed the previous
ranked attempt as `CORRECT` with its three accepted IDs. This verifies the
practice artifact workflow but does not establish a newly accepted replay or
award another timed score. Client end-to-end time was 6.31 seconds: practice
response 1.05 seconds, three downloads 2.34 seconds, submission 1.58 seconds,
status check 1.34 seconds, and solver 3.01 ms.

Offline commands:

```sh
python3 mobile-android-tools/run_modes.py \
  --offline-response work/day-01/mobile-android/exported-trust-review-20261028/responses/single_solve.json \
  --offline-artifact work/day-01/mobile-android/exported-trust-review-20261028/single_solve/exported_trust.apk

python3 mobile-android-tools/run_modes.py \
  --offline-response work/day-01/mobile-android/exported-trust-review-20261028/responses/time_trial.json \
  --offline-artifact work/day-01/mobile-android/exported-trust-review-20261028/time_trial/exported_trust_time_trial.apk

python3 mobile-android-tools/run_modes.py \
  --offline-response work/day-01/mobile-android/exported-trust-review-20261028/responses/mastery.json \
  --offline-artifact work/day-01/mobile-android/exported-trust-review-20261028/mastery/exported_trust_mastery_01.apk \
  --offline-artifact work/day-01/mobile-android/exported-trust-review-20261028/mastery/exported_trust_mastery_02.apk \
  --offline-artifact work/day-01/mobile-android/exported-trust-review-20261028/mastery/exported_trust_mastery_03.apk
```

After a fresh preflight, the prepared legacy ranked commands are:

```sh
python3 mobile-android-tools/run_modes.py \
  mobile-android-day-01-exported-trust/time_trial \
  --ranked --legacy-timed-default --retry

python3 mobile-android-tools/run_modes.py \
  mobile-android-day-01-exported-trust/mastery \
  --ranked --legacy-timed-default --retry
```

Each command starts or advances one attempt, downloads its assigned APKs,
extracts answers, and submits outstanding answer IDs. A `CORRECT` submission
avoids a redundant status request; other results still trigger a status check.
Do not run either command during preparation. The runner now requires explicit
route selection for Time Trial and Mastery: use `--regular-untimed` only after
metadata confirms that regular play is untimed, or use the ranked flags shown
above. It does not hash files on the speed-critical path unless
`--verify-sha256` is requested.

### Offline regression results and limitations

The solver processed the one previously assigned Single Solve APK, one
previously assigned Time Trial APK, and all three previously assigned Mastery
APKs. It produced one answer for each single-question mode and three answers
for Mastery. Local decode time was approximately 3–4 ms for one APK and 7 ms
for three APKs in the earlier run. The final warm regression measured about
2.5–3.0 ms for one APK and 2.9 ms for all three Mastery APKs.

These are five previously assigned artifacts, not fresh variants from this
training session. Twenty-eight fresh randomized APKs were assigned across the
ranked attempts: seven Time Trial APKs and seven three-task Mastery bundles.
The solver extracted all twenty-eight and their submissions were accepted.
Together, the saved and fresh assignments produced thirty-three successful
answer extractions. The five latest fast runs were rerun offline; both Time
Trial answers and all nine Mastery answers matched their live outputs.

The currently published regular pools are empty, so no regular-pool untimed
submission could be made for Time Trial or Mastery. The one legacy Mastery
practice continuation reused the final ranked artifact set and did not create
a new accepted replay. No fresh untimed practice variants were available.
`inspect_dex.py` is unavailable on this host because Androguard is not
installed; `aapt` and the existing static DEX string reader were available.

### Follow-up speed tuning

The decoder module is loaded before the start/retry request. A successful
`CORRECT` submission is accepted as completion directly,
so the runner skips its post-submit status request; incomplete or pending
results still use `op=status`. The earlier runs spent 0.9–1.5 seconds on that
extra request, though removing it may shorten client completion time without
changing the server's recorded solve time.

The runner also has a `--fast` option that skips embedded DEX SHA-1 and
Adler-32 checks. APK SHA-256 verification is already off unless
`--verify-sha256` is requested. The Exported Trust artifacts inspected here
use the `plain` codec, so they do not invoke the DEX integrity checks and
`--fast` is not expected to improve this challenge's measured solve time.

A read-only keep-alive check against the completed Time Trial status endpoint
did not show a repeatable win: urllib took 1.33 and 0.93 seconds; a reused HTTP
connection took 1.21 and 0.96 seconds. A read-only comparison of the two
documented artifact routes on the same three saved APKs measured 2.20–2.43
seconds via capability-based `op=download`, versus 2.79–2.99 seconds via
`op=artifact`; every response was 12,704 bytes and matched the API SHA-256.
The comparison requests ran concurrently, so the roughly 0.6-second difference
is indicative rather than a controlled benchmark. The runner now uses
`op=download` when a start response provides a valid capability, and retains
`op=artifact` as a fallback.

Even with the faster artifact route, the observed timed path has three
sequential service stages: start/retry, downloads, and submit. Recent Mastery
runs spent about 2.0–2.3 seconds starting, 2.2–2.5 seconds downloading, and
1.1–1.6 seconds submitting, while decoding took about 3 ms. Thus, local solver
work is already negligible, and these request timings still put full
client-observed completion above two seconds. The ten saved artifacts from the
earlier regression passed after the code changes. The latest Time Trial APK
was solved in its live run, and all four additional Time Trial/Mastery
speed-check attempts passed offline regression.

## Retained sources

- [early/01-Exported_Trust/readme.md](../../source-notes/early/01-Exported_Trust/readme.md)
- [later/writeups/day-01/mobile-android-exported-trust.md](../../source-notes/later/writeups/day-01/mobile-android-exported-trust.md)
