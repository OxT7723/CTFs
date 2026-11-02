# Dependency Surface

Day 27 · Mobile / Android · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 27 Mobile: Dependency Surface

- Challenge: `mobile-android-day-27-dependency-surface`
- Prompt: Prove which generated dependency flaw is reachable from an exported mobile surface.
- All three regular modes returned `CORRECT`; the final Day 27 Mobile listing marks each mode solved.
- Time Trial and Mastery used the regular untimed pool. No `run_for_time:true` was sent. All deadlines were null.
- The Game Master returned no pending scoring state. Its status response does not report a CourseStack point total.

### Method

The existing `mobile-android-tools/run_modes.py` decoded the assigned APK puzzle assets, verified their SHA-256 hashes, matched the live answer formats and IDs, and submitted the answers. The tool handled all three modes without code changes; Mastery had eleven deliveries and answer IDs `set1.answer` through `set11.answer`.

For the Single Solve package, the manifest declares an exported `ChallengeActivity` with a browsable `VIEW` filter for `huntress27://dependency-surface/unlock`. Static DEX inspection showed it reads `answer` and `case_id` from the intent or URI and forwards them to the local challenge endpoint. The APK also declares the challenge-owned `DependencySurface` class. The solver used the exact answer code decoded from each current attempt's puzzle asset.

### Results and artifacts

| Mode | Attempt | Result | Artifact |
| --- | --- | --- | --- |
| Single Solve | `d103d06a-38bd-4629-a5af-14f8996d464e` | `CORRECT`, `answer` accepted | dependency_surface.apk (private download link removed) — SHA-256 `b366fd1d3bc0a53ff20b57aea54b37c0eb2cbfa646ffa69d3c1a76548213d6df` |
| Time Trial | `a450add9-394d-4e42-951d-13e0ea19ede0` | `CORRECT`, `answer` accepted | dependency_surface_time_trial.apk (private download link removed) — SHA-256 `92b405e3fb9527c0614ebfdd341a2c2a6ddb79de0e56e44d60e786c852376925` |
| Mastery | `0c0f0c48-1ec1-4e7c-9b46-515f32ac26f8` | `CORRECT`, 11/11 accepted | Eleven assigned APK/APKS deliveries listed below |

### Questions and answer fields

Every question asks: “Prove which generated dependency flaw is reachable from an exported mobile surface. Submit only the exact backend answer code returned for this case.” The answer format is `ANS-` followed by exactly 16 uppercase hexadecimal characters, with no spaces or explanation; normalization is exact.

| Mode / answer ID | Case | Package |
| --- | --- | --- |
| Single Solve `answer` | `MOB-27-7540D4374B` | `com.huntress.mobile.d27.v7540d4374bc6` |
| Time Trial `answer` | `MOB-27-83B6D98B4F` | `com.huntress.mobile.d27.v83b6d98b4f8d` |
| Mastery `set1.answer` | `MOB-01-7626D74BD7` | `com.huntress.mobile.d01.v7626d74bd727` |
| Mastery `set2.answer` | `MOB-04-198662851B` | `com.huntress.mobile.d04.v198662851b3a` |
| Mastery `set3.answer` | `MOB-07-E26E4DA4FA` | `com.huntress.mobile.d07.ve26e4da4faec` |
| Mastery `set4.answer` | `MOB-10-B618DEDB20` | `com.huntress.mobile.d10.vb618dedb20fb` |
| Mastery `set5.answer` | `MOB-11-596AC19493` | `com.huntress.mobile.d11.v596ac19493db` |
| Mastery `set6.answer` | `MOB-14-7D6CED40BC` | `com.huntress.mobile.d14.v7d6ced40bc8f` |
| Mastery `set7.answer` | `MOB-18-CAE86F766A` | `com.huntress.mobile.d18.vcae86f766aa0` |
| Mastery `set8.answer` | `MOB-20-1FB7CDEFCD` | `com.huntress.mobile.d20.v1fb7cdefcddf` |
| Mastery `set9.answer` | `MOB-21-A44372BA94` | `com.huntress.mobile.d21.va44372ba94e6` |
| Mastery `set10.answer` | `MOB-26-866E4DD39E` | `com.huntress.mobile.d26.v866e4dd39e97` |
| Mastery `set11.answer` | `MOB-27-43991656AC` | `com.huntress.mobile.d27.v43991656ac7f` |

The start responses also included standard Game Master guidance about using assigned bytes, exact answer IDs, and regular versus timed play. These full responses are preserved in the attempt records.

Mastery artifacts:

- Delivery 1 — dependency_surface_mastery_01.apk (private download link removed) — SHA-256 `da0fb840e7b20f8db0ebda3788d5605f9584c01a06b89f488bcf8b7226225800`
- Delivery 2 — dependency_surface_mastery_02.apk (private download link removed) — SHA-256 `a942a7a4949b802b9f6632e4af05c632beba80d9f00d6e67653f1e38048ec7ba`
- Delivery 3 — dependency_surface_mastery_03.apk (private download link removed) — SHA-256 `9403d247cb87077f8b4dfce292ae12b329c80fa9527127bb4fbbdeccb705cda2`
- Delivery 4 — dependency_surface_mastery_04.apk (private download link removed) — SHA-256 `4bea4013953fc7ca50765596e3bbad079b96e702b34d57a99a130daabdd9a546`
- Delivery 5 — dependency_surface_mastery_05.apk (private download link removed) — SHA-256 `7d842b44bee2171692c954637b7423a1f478d9d0368a64fe2f9ee77468c19b3e`
- Delivery 6 — dependency_surface_mastery_06.apk (private download link removed) — SHA-256 `8f39cdaa4981b3596b74336db16abe1adfe898c2fea03284c20959579a7c9a55`
- Delivery 7 — dependency_surface_mastery_07.apk (private download link removed) — SHA-256 `6e5f2a8008eb9efaa4854a3b71a883eebbcd2aba1d23b64163f253c7f4557c29`
- Delivery 8 — dependency_surface_mastery_08.apk (private download link removed) — SHA-256 `ed2fd953f3b0317d0223fffd09df3be30a604457ab293f6e99fb757d361c53e5`
- Delivery 9 — dependency_surface_mastery_09.apk (private download link removed) — SHA-256 `a47ee77e9c5c9544a6ac45259e513eb794193b6e05b821669f34e68ac9f3ad67`
- Delivery 10 — dependency_surface_mastery_10.apks (private download link removed) — SHA-256 `014e99e98d1eb558634bd7ff5df0a4c08a44395a383b3a77733911c6d84850f7`
- Delivery 11 — dependency_surface_mastery_11.apk (private download link removed) — SHA-256 `056cdca7cf6323848548b08774a9c030dd7bcd95cb1cdfe1bea166e4d496043d`

### Local records and tools

Attempt responses, downloaded bytes, candidate answers, submissions, and status responses are saved under `work/day-27/mobile-android/`. The Android tooling requirements were installed in `mobile-android-tools/.venv/` so the existing decoder and static DEX inspector are ready for later Mobile challenges.

## Retained sources

- [later/writeups/day-27/mobile-dependency-surface.md](../../source-notes/later/writeups/day-27/mobile-dependency-surface.md)
