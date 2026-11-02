# Debug Me If You Can

Day 21 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 21 Mobile: Debug Me If You Can

- Challenge ID: `mobile-android-day-21-debug-me-if-you-can`
- Prompt: Neutralize a clean-room anti-debug state machine while retaining the intended app flow.
- All three modes returned `CORRECT`; the final Day 21 Mobile listing marks all three solved.
- Time Trial and Mastery used regular untimed variants (`run_for_time` omitted); all deadlines were `null`.
- Each question requested the exact backend answer code for its case, formatted as `ANS-` followed by exactly 16 uppercase hexadecimal characters.
- Full live questions, answer IDs, and attempt data are retained in each linked `start-response.json`.

### Results

| Mode | Attempt | Answer IDs accepted | Result |
| --- | --- | --- | --- |
| Single Solve | 77c9bbed-72c6-4ba2-8929-7c08477d9604 (source reference: `/home/HuntressCTF/work/day-21/mobile-android/77c9bbed-72c6-4ba2-8929-7c08477d9604/start-response.json`; not linked in this draft) | `answer` | `CORRECT` |
| Time Trial | 158b78bb-4dcc-4071-a9c6-1fb4358db02c (source reference: `/home/HuntressCTF/work/day-21/mobile-android/158b78bb-4dcc-4071-a9c6-1fb4358db02c/start-response.json`; not linked in this draft) | `answer` | `CORRECT` |
| Mastery | 428abba8-f027-4ba2-9691-26899f764208 (source reference: `/home/HuntressCTF/work/day-21/mobile-android/428abba8-f027-4ba2-9691-26899f764208/start-response.json`; not linked in this draft) | `set1.answer`–`set5.answer` | `CORRECT` (5/5) |

### Questions and answer fields

Every case asked: “Neutralize a clean-room anti-debug state machine while retaining the intended app flow. Submit only the exact backend answer code returned for this case.”

| Route | Case | Answer ID |
| --- | --- | --- |
| Single Solve | `MOB-21-2943307F87` | `answer` |
| Time Trial | `MOB-21-A6745E56D3` | `answer` |
| Mastery, set 1 | `MOB-03-1455921705` | `set1.answer` |
| Mastery, set 2 | `MOB-10-5D349FC723` | `set2.answer` |
| Mastery, set 3 | `MOB-13-29C92231F6` | `set3.answer` |
| Mastery, set 4 | `MOB-19-86D24A43E7` | `set4.answer` |
| Mastery, set 5 | `MOB-21-99B7C751EF` | `set5.answer` |

### Assigned APKs

- Single Solve — debug_me_if_you_can.apk (private download link removed) — SHA-256 `ef187c93e27df27525db3b23e6d8201160c0495d345424cb243d4390cb194d1d`
- Time Trial — debug_me_if_you_can_time_trial.apk (private download link removed) — SHA-256 `577dd2da101500696852e44e2dbd477ce57073d36c91d129eb8c445544f57278`
- Mastery delivery 1 — debug_me_if_you_can_mastery_01.apk (private download link removed) — SHA-256 `ed5242d03125db3b23e6d8201160c0495d345424cb243d4390cb194d1d`
- Mastery delivery 2 — debug_me_if_you_can_mastery_02.apk (private download link removed) — SHA-256 `c068132c6efd4ab06bd318b825befd5d96da7790e45d0b373e2684a31d7fd620`
- Mastery delivery 3 — debug_me_if_you_can_mastery_03.apk (private download link removed) — SHA-256 `9b40f9f09f9c3ac0b4036d41d5b4b07f18d94d6f43662b3a0eea969b15f209b0`
- Mastery delivery 4 — debug_me_if_you_can_mastery_04.apk (private download link removed) — SHA-256 `30c534d4c3c185160366bc60c90e88f98d6ec04a1c2d7853ad455bb974293504`
- Mastery delivery 5 — debug_me_if_you_can_mastery_05.apk (private download link removed) — SHA-256 `acd2b3092ed87abe0d972cdd49e0a7be85f8e611c1f9712bbf707f47db476fc8`

### Solve method and verification

The existing `mobile-android-tools/run_modes.py` downloaded each current attempt's APKs, checked their SHA-256 hashes, and used `decode_puzzle_assets.py` to extract format-matching candidates from the APK assets. It then submitted under the live answer IDs and recorded each submission and status. No tool changes were needed.

Game Master status returned `CORRECT` for each mode and the final filtered listing confirmed all solved. The responses did not include a separate CourseStack point total or scoring-pending field, so the point ledger could not be independently verified through the documented Game Master API.

## Retained sources

- [later/writeups/day-21/mobile-debug-me-if-you-can.md](../../source-notes/later/writeups/day-21/mobile-debug-me-if-you-can.md)
