# Native Library Secrets

Day 15 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 15 Mobile: Native Library Secrets

All three modes completed with `CORRECT`. Time Trial and Mastery used the
regular untimed routes; neither had a deadline. The Game Master status confirms
all answer IDs accepted. Its status response exposes no point total or scoring
pending field, so points cannot be independently confirmed here.

### Method and reusable tooling

The DEX builds an evidence URL with the supplied answer as `proof` and a
case-specific client secret. The native variant exposes its answer through a
secret getter in the APK's shared library. The other randomized deliveries use
the asset's declared codec: plain text, Caesar shift, or split pieces. For
split pieces, `order` maps each supplied piece to its original position.

`mobile-android-tools/decode_puzzle_assets.py` now handles plain and ordered
split assets and statically extracts printable strings from libraries that
export a secret or proof symbol. It does not load the shared library.
`run_modes.py` applies each live question's format to the values from that
question's assigned delivery.

### Results

| Mode | Attempt | Accepted IDs | Result |
| --- | --- | --- | --- |
| Single Solve | `302f5976-d0ac-4b34-b458-b672713cc456` | `answer` | `CORRECT` |
| Time Trial | `fe4a4c2b-e304-4fe2-8f71-cb90913e418e` | `answer` | `CORRECT` |
| Mastery | `59597e9c-5004-486c-85bf-0aa2763567e4` | `set1.answer`–`set5.answer` | `CORRECT` (5/5) |

### Assigned artifacts

- Single Solve — native_library_secrets.apk (private download link removed) — SHA-256 `0cf5bc290da521e7b1ae3412dbef7a176a44e2c17fb38cd9f3909adb126b5308`
- Time Trial — native_library_secrets_time_trial.apk (private download link removed) — SHA-256 `07154859df6ff342fa7630b9c8bfba8ba4bc65f65518a3d666ebe99b322e3d7a`
- Mastery delivery 1 — native_library_secrets_mastery_01.apk (private download link removed) — SHA-256 `5cc05902ca4b792e471fd4d467412ac129bcdceed116c239053483c44440fb87`
- Mastery delivery 2 — native_library_secrets_mastery_02.apk (private download link removed) — SHA-256 `cd0076bb52431ff908902b0ed5d851707e9730c476f7bc9cec73462f930b13df`
- Mastery delivery 3 — native_library_secrets_mastery_03.apk (private download link removed) — SHA-256 `38cb46361b79b42fc2cd0b00ec597189ffa66d156571c44d8cd3cb2a20b8ec26`
- Mastery delivery 4 — native_library_secrets_mastery_04.apk (private download link removed) — SHA-256 `a19f09e0f84b90059243783d7bcea2004290d412bf70b79a37bd61a6c0755836`
- Mastery delivery 5 — native_library_secrets_mastery_05.apk (private download link removed) — SHA-256 `084ec76b20c48ab987c3aaf1609014623f95cb22d3e0ba9588ac71725b99f71f`

## Retained sources

- [later/writeups/day-15/mobile-native-library-secrets.md](../../source-notes/later/writeups/day-15/mobile-native-library-secrets.md)
