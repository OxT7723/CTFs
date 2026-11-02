> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 03 — Intent Injection

## Challenge

- **ID:** `mobile-android-day-03-intent-injection`
- **Lane:** Mobile Android
- **Prompt:** “Trace attacker-controlled extras through an internal navigation boundary.”
- **Historical status:** Single Solve, Time Trial, and Mastery are recorded as `CORRECT`.
- **Answer format:** Submit only `ANS-` followed by exactly 16 uppercase hexadecimal characters. Normalization is exact.

The Time Trial ID is `mobile-android-day-03-intent-injection/time_trial`;
the Mastery ID is `mobile-android-day-03-intent-injection/mastery`.

## Questions and answer IDs

Each API question reads: “For case {case} in package {package}: Trace
attacker-controlled extras through an internal navigation boundary. Submit only
the exact backend answer code returned for this case.” The table gives the
exact case and package for each question. The API format kind is `pattern`,
with the syntax shown above, and normalization is `exact`.

| Mode | Answer ID | Case | Package | Artifact |
| --- | --- | --- | --- | --- |
| Single Solve | `answer` | `MOB-03-8006859B52` | `com.huntress.mobile.d03.v8006859b5257` | `intent_injection.apk` |
| Historical Time Trial | `answer` | `MOB-03-18693A2A78` | `com.huntress.mobile.d03.v18693a2a7801` | `intent_injection_time_trial.apk` |
| Ranked Time Trial | `answer` | `MOB-03-1758793940` | `com.huntress.mobile.d03.v1758793940bb` | `intent_injection_time_trial.apk` |
| Follow-up Time Trial 1 | `answer` | `MOB-03-C14D761426` | `com.huntress.mobile.d03.vc14d76142656` | `intent_injection_time_trial.apk` |
| Follow-up Time Trial 2 | `answer` | `MOB-03-557E920DFC` | `com.huntress.mobile.d03.v557e920dfcde` | `intent_injection_time_trial.apk` |
| Historical Mastery 1 | `set1.answer` | `MOB-03-A44356F818` | `com.huntress.mobile.d03.va44356f818bf` | delivery 1 |
| Historical Mastery 2 | `set2.answer` | `MOB-03-89D5BF7514` | `com.huntress.mobile.d03.v89d5bf751448` | delivery 2 |
| Historical Mastery 3 | `set3.answer` | `MOB-03-8C27168DD9` | `com.huntress.mobile.d03.v8c27168dd926` | delivery 3 |
| Ranked Mastery 1 | `set1.answer` | `MOB-03-C32E8315B5` | `com.huntress.mobile.d03.vc32e8315b5f2` | delivery 1 |
| Ranked Mastery 2 | `set2.answer` | `MOB-03-5708D83922` | `com.huntress.mobile.d03.v5708d83922ce` | delivery 2 |
| Ranked Mastery 3 | `set3.answer` | `MOB-03-AC652C71F6` | `com.huntress.mobile.d03.vac652c71f6e6` | delivery 3 |
| Follow-up Mastery 1, delivery 1 | `set1.answer` | `MOB-03-7313F536F9` | `com.huntress.mobile.d03.v7313f536f985` | APK 1 |
| Follow-up Mastery 1, delivery 2 | `set2.answer` | `MOB-03-1096B199AC` | `com.huntress.mobile.d03.v1096b199ac69` | APK 2 |
| Follow-up Mastery 1, delivery 3 | `set3.answer` | `MOB-03-0BF5CA4BFB` | `com.huntress.mobile.d03.v0bf5ca4bfb77` | APK 3 |
| Follow-up Mastery 2, delivery 1 | `set1.answer` | `MOB-03-F422AFCB31` | `com.huntress.mobile.d03.vf422afcb31dd` | APK 1 |
| Follow-up Mastery 2, delivery 2 | `set2.answer` | `MOB-03-B7551DB30F` | `com.huntress.mobile.d03.vb7551db30ff3` | APK 2 |
| Follow-up Mastery 2, delivery 3 | `set3.answer` | `MOB-03-EFEFF1A4A5` | `com.huntress.mobile.d03.vefeff1a4a5b6` | APK 3 |

Single Solve and Time Trial each require `answer`. Mastery requires all three
`setN.answer` fields. The current Game Master response is authoritative for
answer IDs and case details.

## Artifacts

These assigned APKs were downloaded using their Game Master capability links.
Their SHA-256 values match the API responses.
Each APK is the input for its corresponding case; Mastery delivery numbers map
to the matching `setN.answer` fields.

| Mode | File | Download | SHA-256 |
| --- | --- | --- | --- |
| Single Solve | `intent_injection.apk` | Download APK (retired artifact link; see artifact inventory) | `3127e3a93000b594fe4555747aed236f6f77bd8daaf2be41cfe60849bf8708aa` |
| Time Trial | `intent_injection_time_trial.apk` | Download APK (retired artifact link; see artifact inventory) | `74834707253df5b0153a91c71d78ea881ed3ce28e6968fac35c6c6535d5d593a` |
| Mastery 1 | `intent_injection_mastery_01.apk` | Download APK (retired artifact link; see artifact inventory) | `67a71c88c38288582739bd39cd7b43dd1b3a5baac9171eef91061d800f7e93dc` |
| Mastery 2 | `intent_injection_mastery_02.apk` | Download APK (retired artifact link; see artifact inventory) | `a55f6dbc97cf93fc8258d1ee3d1ed5237917f9c563e381ddfaebc37a78ddc90a` |
| Mastery 3 | `intent_injection_mastery_03.apk` | Download APK (retired artifact link; see artifact inventory) | `651b8761d83ccd8d0d31594a5604255e0f2c21a53dbbb353b4c325b8faa38960` |
| Ranked Time Trial | `intent_injection_time_trial.apk` | Download APK (retired artifact link; see artifact inventory) | `db1acd0aa2d8aa92e583d8b87449e35e6524a8760b4b90725215ff38143bcfca` |
| Ranked Mastery 1 | `intent_injection_mastery_01.apk` | Download APK (retired artifact link; see artifact inventory) | `d6b31e6fa12450d78940586196f49c364c6dbd7b36100e3ec28b994a74412a8a` |
| Ranked Mastery 2 | `intent_injection_mastery_02.apk` | Download APK (retired artifact link; see artifact inventory) | `4200eeb7eaedb87cb7e95fc4d14eb9e4c861937aa3ce6e11e78a890164aebf82` |
| Ranked Mastery 3 | `intent_injection_mastery_03.apk` | Download APK (retired artifact link; see artifact inventory) | `e420b2acd1a606eca16c2be925df94b6ed4e2076688ab78822f25e47d0f5e384` |
| Follow-up Time Trial 1 | `intent_injection_time_trial.apk` | Download APK (retired artifact link; see artifact inventory) | `fc0641abfa59c4b36b254d5b772ead074d373577cf93298643ecbd012a95c179` |
| Follow-up Time Trial 2 | `intent_injection_time_trial.apk` | Download APK (retired artifact link; see artifact inventory) | `db40abe1d692f52bca3f37dbc27369d572db4113041ef6d511d8569a9fe0e376` |
| Follow-up Mastery 1, delivery 1 | `intent_injection_mastery_01.apk` | Download APK (retired artifact link; see artifact inventory) | `ac49841a5b372f3ee066b57901e075ae395cdfabc59f88d24de5ff7e082e02eb` |
| Follow-up Mastery 1, delivery 2 | `intent_injection_mastery_02.apk` | Download APK (retired artifact link; see artifact inventory) | `c9bbc0af1528b76bf781e64fddea798b001eae4ab06f90e2080994ab14286dd0` |
| Follow-up Mastery 1, delivery 3 | `intent_injection_mastery_03.apk` | Download APK (retired artifact link; see artifact inventory) | `123f6126d91dfccc3b85e77793e7ec6441b03583d9ed4d9b769b9b0db419f9f2` |
| Follow-up Mastery 2, delivery 1 | `intent_injection_mastery_01.apk` | Download APK (retired artifact link; see artifact inventory) | `5c4333c571b4e8abff4985c1346b5d0e8eb29997edce8596f2631434f299390c` |
| Follow-up Mastery 2, delivery 2 | `intent_injection_mastery_02.apk` | Download APK (retired artifact link; see artifact inventory) | `7d8909cc70e8bd7ff33ef2f63333e7264dc1f67ab41e3efc27524fe65da91bde` |
| Follow-up Mastery 2, delivery 3 | `intent_injection_mastery_03.apk` | Download APK (retired artifact link; see artifact inventory) | `8a914a58f64f3c0f7e7d728a2ce3a15dd3fb5e28d035e842de271b983d45e4a2` |

Local copies and the captured player-facing API responses are under
`work/day-03/mobile-android/intent-injection/review-2026-10-28/`.

## Solver review

Static manifest inspection found an exported `ChallengeActivity` with a
`VIEW`/`BROWSABLE` route at `huntress03://intent-injection/unlock`. DEX review
shows the activity reads attacker-controlled `answer` and `case_id` values
from the incoming intent and passes them across the internal navigation
boundary.

The existing `mobile-android-tools/run_modes.py` and
`decode_puzzle_assets.py` already cover this artifact format. The puzzle
asset declares Base64, which the generic decoder handles. The runner validates
each candidate against the live answer format, associates Mastery deliveries
with their question IDs, checks that the complete answer ID set is present,
and submits only outstanding IDs.

No challenge-specific solver change was needed. Offline processing of the
five historical APKs succeeded:

| Mode | Questions | Solver execution |
| --- | ---: | ---: |
| Single Solve | 1 | 6.95 ms |
| Time Trial | 1 | 2.70 ms |
| Mastery | 3 | 12.81 ms |

These timings cover local decode and answer mapping; they exclude download,
attempt setup, and submission requests. Historical answers were already
accepted, so they were not resubmitted.

## Training and replay availability

The Game Master lists Time Trial as a legacy timed-by-default route:
`run_for_time_supported:false`, a 50-second ranked deadline, ranked pool size
16, and regular pool size 0. Mastery is also legacy timed-by-default, with a
110-second ranked deadline, ranked pool size 8, and regular pool size 0.
Historical status reports 14 unique Time Trial attempts and six unique
Mastery attempts remaining. Both historical timed attempts are complete,
expired, and reported `hall_of_fame_eligible:false`.

No untimed Time Trial or Mastery training route is available. A retry on
either legacy route would be timed, and the legacy practice continuation is
documented for use only after the ranked rotation is exhausted. The rotations
are not exhausted, so no regular retry or practice operation was used. The
historical artifacts provide offline regression coverage but are not fresh
untimed variants.

## Ranked attempts

Three new attempts were initiated in each timed mode: the first prepared run
and two additional runs using the keep-alive transport. Each had its own
list/status preflight. Both routes are legacy timed-by-default, so the runner
used `op=retry` without `run_for_time`. Every new response reported
`hall_of_fame_eligible:true`.

| Mode | Attempt ID | Deadline | Result | HOF eligible | Accepted tasks | End-to-end | Solver | Ranked attempts remaining |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| Time Trial | `9817d126-566a-4a9f-9c59-030432a6c9e6` | `2026-10-28T23:27:16.814Z` (50 s) | `CORRECT` | Yes | 1/1 | 5.15 s | 2.33 ms | 13 |
| Mastery | `16f3e918-64ce-499e-8a24-91b60cd90086` | `2026-10-28T23:28:42.880Z` (110 s) | `CORRECT` | Yes | 3/3 | 3.84 s | 3.00 ms | 5 |
| Time Trial, keep-alive 1 | `0880966e-81e6-4a69-8871-b630bf92272e` | `2026-10-28T23:38:15.570Z` (50 s) | `CORRECT` | Yes | 1/1 | 4.61 s | 2.70 ms | 12 |
| Mastery, keep-alive 1 | `527a758a-1c7a-4f8a-b3a4-b5c864a3fb14` | `2026-10-28T23:39:34.661Z` (110 s) | `CORRECT` | Yes | 3/3 | 5.16 s | 3.13 ms | 4 |
| Time Trial, keep-alive 2 | `0f9cab58-e85b-43f2-8673-721decc21d0d` | `2026-10-28T23:38:49.110Z` (50 s) | `CORRECT` | Yes | 1/1 | 4.29 s | 2.20 ms | 11 |
| Mastery, keep-alive 2 | `929c761b-67c5-4d83-8932-4bcb2213e08e` | `2026-10-28T23:40:02.400Z` (110 s) | `CORRECT` | Yes | 3/3 | 4.01 s | 3.18 ms | 3 |

Final status confirmed all answer IDs accepted for the latest Time Trial and
Mastery attempts, with `hall_of_fame_eligible:true`. No response reported a
pending scoring state. The API did not provide `variant_fresh`; the new APKs
have distinct SHA-256 values and case/package identifiers from the historical
artifacts. Attempt data and downloaded files are preserved under
`work/day-03/mobile-android/<attempt-id>/`.

The Time Trial request took 1.81 s, its download 1.46 s, and submission
1.87 s. The Mastery request took 1.37 s, its three concurrent downloads
0.50 s, and submission 1.96 s. Local solver execution was under 3 ms for each
run. Network requests dominated the client duration.

## Keep-alive transport experiment

`run_modes.py` now reuses one standard-library HTTP/1.1 connection per
thread and endpoint. Mastery artifact downloads still run concurrently; the
main thread reuses its connection for the attempt request and submission.
Requests are not automatically retried, so a lost response cannot silently
start a duplicate attempt.

A read-only two-request status probe took 0.51 s and 0.40 s with separate
connections, then 0.28 s and 0.27 s on one reused connection. The two
follow-up Time Trials averaged 4.45 s end-to-end versus 5.15 s in the
pre-change run. Their submissions took 1.16 s and 1.51 s versus 1.87 s
before the change. Mastery did not show a total-time gain: the follow-up runs
took 5.16 s and 4.01 s versus 3.84 s before the change. Its artifact/start
latency varied more than the submission savings.

This is a small sample. It suggests connection reuse can save request
overhead, but it did not consistently reduce complete run time. The proxy and
Game Master response latency remain the main bottleneck.

## Commands

Offline regression, without contacting the Game Master or submitting answers:

```sh
mobile-android-tools/.venv/bin/python mobile-android-tools/run_modes.py \
  --offline-response work/day-03/mobile-android/intent-injection/review-2026-10-28/single-response.json \
  --offline-artifact work/day-03/mobile-android/intent-injection/review-2026-10-28/single/intent_injection.apk

mobile-android-tools/.venv/bin/python mobile-android-tools/run_modes.py \
  --offline-response work/day-03/mobile-android/intent-injection/review-2026-10-28/mastery-response.json \
  --offline-artifact work/day-03/mobile-android/intent-injection/review-2026-10-28/mastery/intent_injection_mastery_01.apk \
  --offline-artifact work/day-03/mobile-android/intent-injection/review-2026-10-28/mastery/intent_injection_mastery_02.apk \
  --offline-artifact work/day-03/mobile-android/intent-injection/review-2026-10-28/mastery/intent_injection_mastery_03.apk
```

The existing runner's legacy ranked command for a completed mode is:

```sh
mobile-android-tools/.venv/bin/python mobile-android-tools/run_modes.py \
  mobile-android-day-03-intent-injection/time_trial \
  --ranked --legacy-timed-default --retry --fast
```

Use it only after a fresh list/status preflight confirms the current attempt
is complete, no scoring state is pending, and another ranked attempt is
authorized. Three new Time Trial and three new Mastery attempts have been
used in this review; do not run these commands again in this session. The
Mastery command uses the same options with
`mobile-android-day-03-intent-injection/mastery`.

For Single Solve, the ordinary command downloads, solves, and submits
outstanding answer IDs:

```sh
mobile-android-tools/.venv/bin/python mobile-android-tools/run_modes.py \
  mobile-android-day-03-intent-injection
```

`--fast` skips embedded DEX integrity checks on the timed path. The runner
imports the decoder before the attempt request, downloads Mastery deliveries
concurrently, and avoids a redundant status request after an accepted
submission.

## Current validation limits

All 17 available APKs passed offline processing: five historical artifacts
and 12 newly assigned ranked artifacts (17/17 questions). The ranked
artifacts have distinct hashes and case/package identifiers from the
historical files. There were no fresh untimed randomized artifacts available
for training. The final Game Master status reports 11 Time Trial and three
Mastery unique ranked attempts remaining.
