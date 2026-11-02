# Predictable Crypto

Day 14 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 14 Mobile: Predictable Crypto

Challenge: `mobile-android-day-14-predictable-crypto`

Single Solve, Time Trial, and Mastery all returned `CORRECT`; status confirms
every answer ID was accepted. The timed attempts were the default non-Hall-of-
Fame starts and both were completed before their 30-second deadlines. The
status responses contain no pending-scoring marker or CourseStack point total.

### Reusable method

The APK's `assets/huntress_puzzle.json` declares a Caesar codec and its key.
Reverse the declared character shift, then use the existing runner to match
the decoded text against the live answer format and submit with the current
answer IDs. The DEX confirms the app passes the answer and case ID to its
evidence route as the proof and case identifier.

`mobile-android-tools/decode_puzzle_assets.py` and its README now support the
declared Caesar codec. `mobile-android-tools/run_modes.py` required no
challenge-specific changes; it downloaded and SHA-256-verified every assigned
APK, submitted each mode, and saved the response records under
`work/day-14/mobile-android/<attempt-id>/`.

### Results

| Mode | Attempt | Deadline | Result |
| --- | --- | --- | --- |
| Single Solve | `682c3e5c-12d8-4742-9dea-7d2b1c558c73` | None | `CORRECT` |
| Time Trial | `6da54214-4489-41fb-86f5-8d0d9116335e` | 2026-10-14 13:02:54 UTC | `CORRECT` |
| Mastery | `9b1eabb8-931d-4260-b7eb-3eb879982475` | 2026-10-14 13:02:58 UTC | `CORRECT` (3/3) |

### Assigned artifacts

- Single Solve — predictable_crypto.apk (private download link removed) — SHA-256 `b6d3fff1c44485eab54e3b8fb89ad5d0a30e509bdc2b60dd35fbcca0b7400fee`
- Time Trial — predictable_crypto_time_trial.apk (private download link removed) — SHA-256 `ef619068a4795a4a7414de05e21c99ba3c8f1523e0c0eddb180e769b68e49e66`
- Mastery delivery 1 — predictable_crypto_mastery_01.apk (private download link removed) — SHA-256 `a684fcd3da1214e127569673454e4ffdc545b545fc981afb17e344bf327e52d5`
- Mastery delivery 2 — predictable_crypto_mastery_02.apk (private download link removed) — SHA-256 `1ef24b5759bc5ade85cfce0e2bde889d408f5f4cfc3ec3185ae9c51f3ebbb137`
- Mastery delivery 3 — predictable_crypto_mastery_03.apk (private download link removed) — SHA-256 `0a50cf28cd77204fe268454a9c55613dafbf05d8a7274a7c14ec8eed29b7929a`

## Retained sources

- [later/writeups/day-14/mobile-predictable-crypto.md](../../source-notes/later/writeups/day-14/mobile-predictable-crypto.md)
