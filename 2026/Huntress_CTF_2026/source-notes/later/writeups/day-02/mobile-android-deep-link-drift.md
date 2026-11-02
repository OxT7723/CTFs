> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 02 — Deep Link Drift

## Challenge

- **ID:** `mobile-android-day-02-deep-link-drift`
- **Lane:** Mobile Android
- **Prompt:** “Day 1 taught you the roads. Now learn which ones are actually guarded — tell verified routing apart from a scheme and host that wave everybody through.”
- **Historical status:** Single Solve, Time Trial, and Mastery are all recorded as `CORRECT`.
- **Answer format:** Each question requires `ANS-` followed by exactly 16 uppercase hexadecimal characters, with no spaces or explanation. Normalization is exact.

The Time Trial ID is `mobile-android-day-02-deep-link-drift/time_trial`; the
Mastery ID is `mobile-android-day-02-deep-link-drift/mastery`.

## Historical questions

| Mode | Answer ID | Case | Package |
| --- | --- | --- | --- |
| Single Solve | `answer` | `MOB-02-15B6E1B835` | `com.huntress.mobile.d02.v15b6e1b8356f` |
| Historical Time Trial | `answer` | `MOB-02-7961FE2922` | `com.huntress.mobile.d02.v7961fe2922d9` |
| Historical Mastery 1 | `set1.answer` | `MOB-02-1601E4CE90` | `com.huntress.mobile.d02.v1601e4ce905c` |
| Historical Mastery 2 | `set2.answer` | `MOB-02-93CF95A29C` | `com.huntress.mobile.d02.v93cf95a29c03` |
| Historical Mastery 3 | `set3.answer` | `MOB-02-BA5E39EC95` | `com.huntress.mobile.d02.vba5e39ec951d` |

Each question asks for the exact backend answer code returned for its case.
Single Solve and Time Trial require `answer`; Mastery requires all three
`setN.answer` fields.

## Historical artifacts

All files were downloaded through `op=artifact` from the supported Game Master
proxy and matched the API-provided SHA-256.

| Mode | File | API download | SHA-256 |
| --- | --- | --- | --- |
| Single Solve | `deep_link_drift.apk` | Download APK (retired artifact link; see artifact inventory) | `9211e52f1844b86ef8f75622dc36df52e6e7e9935b48cf1d24ded475148cac07` |
| Time Trial | `deep_link_drift_time_trial.apk` | Download APK (retired artifact link; see artifact inventory) | `cb6af40479cce787a74b3c4394469678383935ec1b99e1deeb5ca6e7a42d91de` |
| Mastery 1 | `deep_link_drift_mastery_01.apk` | Download APK (retired artifact link; see artifact inventory) | `f07ee1d515eae77fb86a1f2026aa72f63452901a46bf3e0e738441c9c2fbddef` |
| Mastery 2 | `deep_link_drift_mastery_02.apk` | Download APK (retired artifact link; see artifact inventory) | `28a747a0672c05304520faeda3eb018cbe2878401e866f930ef0d0a225666407` |
| Mastery 3 | `deep_link_drift_mastery_03.apk` | Download APK (retired artifact link; see artifact inventory) | `22be4efbf0cf6d2a91e5a5c22f0bfdfe3a7330fd7d860ac5f04ab23bb56bea10` |

## Solver review

The shared `decode_puzzle_assets.py` already supports the `reverse` codec
declared by `assets/huntress_puzzle.json`. The mode runner matches decoded
candidates against each live question's answer format and exact answer ID.
No challenge-specific solver change was needed.

Manifest inspection found an exported `ChallengeActivity` with a
`VIEW`/`BROWSABLE` filter for `huntress02://deep-link-drift/unlock`. The APK
was read statically and was not installed or executed.

Offline regression produced the required answers for all five historical
APKs:

| Mode | Questions | Solver time |
| --- | ---: | ---: |
| Single Solve | 1 | 1.98 ms |
| Time Trial | 1 | 2.04 ms |
| Mastery | 3 | 2.84 ms |

The Time Trial and Mastery artifacts are expired historical assignments.
Their answers were already accepted on those attempts. No fresh regular
variants were available, and no answers were resubmitted to those completed
attempts.

## Ranked runs

The Game Master lists the Time Trial as a legacy timed-by-default route with a
50-second ranked deadline, ranked pool size 16, and no regular pool. Mastery
has a 110-second ranked deadline, ranked pool size 8, and no regular pool.
The first preflight showed 15 Time Trial and six Mastery attempts remaining.
Historical `hall_of_fame_eligible:false` values did not determine eligibility
for new attempts; each new response was checked directly.

Two new ranked runs were made per timed mode after the offline review. All four
were accepted and the Game Master returned `hall_of_fame_eligible:true`.

| Mode | Attempt ID | Deadline | Result | HOF | Tasks | Client end-to-end | Solver | Attempts remaining |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| Time Trial 1 | `b27f27de-1176-41d8-b108-b3d4789126cc` | `2026-10-28T21:38:25.476Z` (50 s) | `CORRECT` | Eligible | 1/1 | 4.58 s | 2.23 ms | 14 |
| Time Trial 2 | `766082ef-6049-4fba-8df3-81cac5159542` | `2026-10-28T21:38:39.830Z` (50 s) | `CORRECT` | Eligible | 1/1 | 6.08 s | 2.26 ms | 13 |
| Mastery 1 | `ae507a39-f741-48a3-b607-fdf5d829aa13` | `2026-10-28T21:39:54.361Z` (110 s) | `CORRECT` | Eligible | 3/3 | 5.92 s | 2.97 ms | 5 |
| Mastery 2 | `0af49972-77be-444b-a773-8bd09919cafc` | `2026-10-28T21:40:07.979Z` (110 s) | `CORRECT` | Eligible | 3/3 | 4.94 s | 3.25 ms | 4 |

Final status confirmed both modes solved, with 13 Time Trial and four Mastery
ranked attempts remaining. No regular untimed variants were available. No
practice continuation was used because neither ranked rotation is exhausted.

Request timing varied more than solver timing. Time Trial 1 took 1.83 seconds
to start, 1.56 seconds to download, and 1.18 seconds to submit; Time Trial 2
took 2.42, 1.49, and 2.16 seconds. Mastery 1 took 2.43 seconds to start, 2.03
seconds for three concurrent downloads, and 1.45 seconds to submit. Mastery 2
took 1.96, 1.74, and 1.24 seconds. Solver execution remained about 2–3 ms.

## Fresh ranked cases

| Attempt | Answer ID | Case | Package |
| --- | --- | --- | --- |
| Time Trial 1 | `answer` | `MOB-02-6BA6C4DF69` | `com.huntress.mobile.d02.v6ba6c4df6981` |
| Time Trial 2 | `answer` | `MOB-02-70C8AE307B` | `com.huntress.mobile.d02.v70c8ae307be4` |
| Mastery 1 | `set1.answer` | `MOB-02-4A1200AF32` | `com.huntress.mobile.d02.v4a1200af3236` |
| Mastery 1 | `set2.answer` | `MOB-02-55556139E9` | `com.huntress.mobile.d02.v55556139e9ac` |
| Mastery 1 | `set3.answer` | `MOB-02-0F67445B89` | `com.huntress.mobile.d02.v0f67445b890b` |
| Mastery 2 | `set1.answer` | `MOB-02-79E9598DB9` | `com.huntress.mobile.d02.v79e9598db95c` |
| Mastery 2 | `set2.answer` | `MOB-02-638EBC3CB7` | `com.huntress.mobile.d02.v638ebc3cb710` |
| Mastery 2 | `set3.answer` | `MOB-02-D253EF1A57` | `com.huntress.mobile.d02.vd253ef1a577a` |

Each fresh question uses the same prompt and answer format described above,
with the listed case and package substituted.

## Fresh ranked artifacts

Post-run SHA-256 checks matched all API-provided hashes.

| Attempt | File | API download | SHA-256 |
| --- | --- | --- | --- |
| Time Trial 1 | `deep_link_drift_time_trial.apk` | Download APK (retired artifact link; see artifact inventory) | `7f1aaea600a9635df0b16c034ae641211d00e65f172559e87654f3296233c04d` |
| Time Trial 2 | `deep_link_drift_time_trial.apk` | Download APK (retired artifact link; see artifact inventory) | `d813cd29e488f47631b01529089ed0fa66dcb6cec15a747a436b717e39762730` |
| Mastery 1 | `deep_link_drift_mastery_01.apk` | Download APK (retired artifact link; see artifact inventory) | `d4fc8be22d0197dafdb8d0980d5a8547e5fbeb661b8b88c4b4ec58a5d6173cbb` |
| Mastery 1 | `deep_link_drift_mastery_02.apk` | Download APK (retired artifact link; see artifact inventory) | `94464a726a4ad802a23333043c4941d73298378dcab70449879e790c551d8385` |
| Mastery 1 | `deep_link_drift_mastery_03.apk` | Download APK (retired artifact link; see artifact inventory) | `de970e5e8533d0e67c02573a973f74845d94cc071eed145b7059f958e24d9cb8` |
| Mastery 2 | `deep_link_drift_mastery_01.apk` | Download APK (retired artifact link; see artifact inventory) | `832ba04ec1f965d29f62eaf797259c8c228ffd8dea6d534f67a00d4403e1c00f` |
| Mastery 2 | `deep_link_drift_mastery_02.apk` | Download APK (retired artifact link; see artifact inventory) | `dbb6371a26dd30adf7248ba239db9ba456f27361c286385ba6d50616f6c1a7ba` |
| Mastery 2 | `deep_link_drift_mastery_03.apk` | Download APK (retired artifact link; see artifact inventory) | `61e5e02589fb50c19e8c5b2090ef83af01860f5edbe0b608335c66449111b495` |

All eight fresh APKs were reprocessed offline; the generated answers matched
the live run outputs. Including the five historical files, the solver has now
processed 13 assigned APKs. No challenge-specific solver code changes were
needed.

```sh
python3 mobile-android-tools/run_modes.py \
  mobile-android-day-02-deep-link-drift/time_trial \
  --ranked --legacy-timed-default --retry --fast

python3 mobile-android-tools/run_modes.py \
  mobile-android-day-02-deep-link-drift/mastery \
  --ranked --legacy-timed-default --retry --fast
```

`--fast` skips DEX integrity hashes; the current artifacts use the `reverse`
JSON asset codec and do not use DEX-backed assets. The runner uses the
capability download route when the API provides one, downloads Mastery
deliveries concurrently, submits outstanding answer IDs together, and avoids
a redundant status request after a successful submit. Future ranked commands
require a fresh status/list preflight and no more than the authorized retries.
