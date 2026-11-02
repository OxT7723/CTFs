> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 28 Mobile: Protocol Reconstruction

- Challenge: `mobile-android-day-28-protocol-reconstruction`
- Prompt: Reconstruct the app-to-backend protocol and preserve nonce and ordering semantics.
- All three regular modes returned `CORRECT`; the live Day 28 Mobile listing marks each solved.
- Time Trial and Mastery used regular untimed play (`run_for_time:false`); all deadlines were null.
- Status returned no pending scoring state. Game Master status does not report a CourseStack point total.

## Method

The existing `mobile-android-tools/run_modes.py` downloaded each assigned APK/APKS, verified its SHA-256, decoded the answer in byte order, matched the live answer format and IDs, and submitted it.

The new `packet` codec in `decode_puzzle_assets.py` parses the `HA` framing marker and one-byte payload length, then returns only the declared payload. Trailing protocol fields remain outside the answer payload. The APK's exported browsable `huntress28://protocol-reconstruction/unlock` handler reads the `answer` and `case_id` values and passes them to its evidence endpoint in a fixed query order.

## Results

| Mode | Attempt | Accepted |
| --- | --- | --- |
| Single Solve | `591fdc30-4fab-47b2-bb8d-e4d487657a06` | `answer` |
| Time Trial | `ff07b81b-feca-4550-ad3f-d23c0ff6d9c0` | `answer` |
| Mastery | `fde106df-db09-413a-8e04-b14f159267fd` | `set1.answer`–`set12.answer` (12/12) |

Mastery cases were `MOB-01-00CE6B14FF`, `MOB-04-4A0BA83D13`, `MOB-07-E547E800F9`, `MOB-08-39CD84B6EB`, `MOB-11-0F0D612428`, `MOB-14-DA060B60CD`, `MOB-17-738435CF8C`, `MOB-18-2620282A8B`, `MOB-22-16411FCFD5`, `MOB-24-D4167863FA`, `MOB-26-FE7D979F2C`, and `MOB-28-89A40AD781`.

## Assigned artifacts

- Single Solve — protocol_reconstruction.apk (retired artifact link; see artifact inventory) — SHA-256 `1146daecc34e9b3cd727c7a83f135091dc10b01c4081e430d7b4f6bb4a4efbd5`
- Time Trial — protocol_reconstruction_time_trial.apk (retired artifact link; see artifact inventory) — SHA-256 `2ea21adcdc4a615bccf0164ebeaf76ccc74b082822fb443d59954f6db4c512f6`
- Mastery 1 — protocol_reconstruction_mastery_01.apk (retired artifact link; see artifact inventory) — SHA-256 `5d571fbcd9b3f10d9039648304d45a00aa5fa968b65652f32c40b13b6acab2fa`
- Mastery 2 — protocol_reconstruction_mastery_02.apk (retired artifact link; see artifact inventory) — SHA-256 `f537cbd9fa8dba27e6dbe07dfee2b83c846352686b2950b3f2bfb0180c431abf`
- Mastery 3 — protocol_reconstruction_mastery_03.apk (retired artifact link; see artifact inventory) — SHA-256 `1dbb8026ca928b8146ba2e1335550d8591ce5c1cb557d0b343b9862561083807`
- Mastery 4 — protocol_reconstruction_mastery_04.apk (retired artifact link; see artifact inventory) — SHA-256 `b0e5526a3c6f7d51b7cb5fbbf324cd9a31221868a8f1c82cb6552c107a8ad308`
- Mastery 5 — protocol_reconstruction_mastery_05.apk (retired artifact link; see artifact inventory) — SHA-256 `eebcd37bdad002657690039d4aed07b6887870de4b95cbc141f2a68d2263cbb1`
- Mastery 6 — protocol_reconstruction_mastery_06.apk (retired artifact link; see artifact inventory) — SHA-256 `a31345e63fffc1eaf162825aa3aa06c65bda731e7ffa1744aa26cb1da9839299`
- Mastery 7 — protocol_reconstruction_mastery_07.apk (retired artifact link; see artifact inventory) — SHA-256 `dd293ed1adf6f95a05bb8d756c6682fa1332b563d617dabb7f84ff8bb1414974`
- Mastery 8 — protocol_reconstruction_mastery_08.apk (retired artifact link; see artifact inventory) — SHA-256 `69e66aef8ee0b5e280d51f2e1e3dc9fd362a4d18e53167d8b47dfffe56a24be1`
- Mastery 9 — protocol_reconstruction_mastery_09.apk (retired artifact link; see artifact inventory) — SHA-256 `77e784e0de9533d522518e7852e677dddc74e51d8c35cb63028ac194777f1ff1`
- Mastery 10 — protocol_reconstruction_mastery_10.apk (retired artifact link; see artifact inventory) — SHA-256 `b54a4527586b09e009b64d3bddee81a6504b6a06bd7e49abdf9a60f8d37150e8`
- Mastery 11 — protocol_reconstruction_mastery_11.apks (retired artifact link; see artifact inventory) — SHA-256 `0cf2dc29302f2a80e23c760fafc962e9c77df197b9268f746986418b991ebba1`
- Mastery 12 — protocol_reconstruction_mastery_12.apk (retired artifact link; see artifact inventory) — SHA-256 `5e4417e673844fc669af7cd429c278df6af53304d3cca370cc94029e4cc05601`

Attempt responses, assigned bytes, candidates, submissions, and status responses are saved under `work/day-28/mobile-android/`.
