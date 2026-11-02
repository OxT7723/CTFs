> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 20 Mobile: Loaded Later

- Challenge ID: `mobile-android-day-20-loaded-later`
- Prompt: Analyze a challenge-signed secondary DEX and recover the module contract.
- All three routes returned `CORRECT`; final Day 20 Mobile listing marks each solved.
- Time Trial and Mastery used regular untimed variants (`run_for_time` omitted); all deadlines were `null`.
- Every question requested the exact backend code in `ANS-` plus 16 uppercase hexadecimal characters.
- Full live questions, guidance, answer IDs, and attempt metadata are retained in the per-attempt `start-response.json` (historical reference: `</home/HuntressCTF/work/day-20/mobile-android/d5879539-e975-43e2-9712-57a6751a8306/start-response.json>`; not included) (Time Trial (historical reference: `</home/HuntressCTF/work/day-20/mobile-android/c71ed20a-f269-4bc9-a046-3c5bf7e2cda4/start-response.json>`; not included), Mastery (historical reference: `</home/HuntressCTF/work/day-20/mobile-android/da10db2e-769a-4545-8ae3-5348c47d68c1/start-response.json>`; not included)).

## Results

| Mode | Attempt | Answer IDs accepted | Result |
| --- | --- | --- | --- |
| Single Solve | `d5879539-e975-43e2-9712-57a6751a8306` (historical reference: `</home/HuntressCTF/work/day-20/mobile-android/d5879539-e975-43e2-9712-57a6751a8306/start-response.json>`; not included) | `answer` | `CORRECT` |
| Time Trial | `c71ed20a-f269-4bc9-a046-3c5bf7e2cda4` (historical reference: `</home/HuntressCTF/work/day-20/mobile-android/c71ed20a-f269-4bc9-a046-3c5bf7e2cda4/start-response.json>`; not included) | `answer` | `CORRECT` |
| Mastery | `da10db2e-769a-4545-8ae3-5348c47d68c1` (historical reference: `</home/HuntressCTF/work/day-20/mobile-android/da10db2e-769a-4545-8ae3-5348c47d68c1/start-response.json>`; not included) | `set1.answer`–`set5.answer` | `CORRECT` (5/5) |

## Questions, answer fields, and timer

All routes asked: “Analyze a challenge-signed secondary DEX and recover the
module contract. Submit only the exact backend answer code returned for this
case.” The required format was `ANS-` followed by exactly 16 uppercase
hexadecimal characters, with no spaces or explanation.

| Route | Case | Answer ID |
| --- | --- | --- |
| Single Solve | `MOB-20-6AE5A9BC36` | `answer` |
| Time Trial | `MOB-20-5A5C3DF811` | `answer` |
| Mastery, set 1 | `MOB-02-73B7FB5863` | `set1.answer` |
| Mastery, set 2 | `MOB-09-179FF2394D` | `set2.answer` |
| Mastery, set 3 | `MOB-11-185AB1D929` | `set3.answer` |
| Mastery, set 4 | `MOB-18-53E29E0546` | `set4.answer` |
| Mastery, set 5 | `MOB-20-2E98251E6E` | `set5.answer` |

Single Solve was untimed. Time Trial and Mastery ran regular, untimed variants
with no server deadline. “Done” meant one accepted answer for each single-case
route and all five accepted answer IDs for Mastery.

The Game Master status and final filtered listing confirm completion. The
Game Master responses expose no CourseStack points or pending-scoring field,
so the point total itself could not be independently confirmed here.

## Solve method and tooling

The APK's `assets/huntress_puzzle.json` declares `codec: dynamic` and references
`assets/payload.dex`. The Mobile decoder reads the referenced DEX string table,
checks the DEX SHA-1 and Adler-32 header values, and lets the existing mode
runner match the live answer format. It does not execute the bytecode or
hardcode any answer, hash, filename, or URL.

Updated reusable files:

- [decode_puzzle_assets.py](../../../../tools/later/mobile-android-tools/decode_puzzle_assets.py)
- [Mobile tools README](../../../../tools/later/mobile-android-tools/README.md)

## Assigned artifacts

Each APK is the assigned evidence for its case: one Single Solve APK, one
Time Trial APK, and five Mastery APKs corresponding to sets 1–5. Each contains
the puzzle asset pointing to its own secondary DEX.

- Single Solve — loaded_later.apk (retired artifact link; see artifact inventory) — SHA-256 `e870c4e7a7a438df46a56216a0ca04fca21042637f2347e4b98b226859a622ea`
- Time Trial — loaded_later_time_trial.apk (retired artifact link; see artifact inventory) — SHA-256 `fd177fa5e571ab85215f69fc789b364d7e9ced139254905737be1a53613d79a0`
- Mastery delivery 1 — loaded_later_mastery_01.apk (retired artifact link; see artifact inventory) — SHA-256 `6c1f2351a1f69ec2831321f44f9f6cae59a4a0c81384980abc048010c796a0c0`
- Mastery delivery 2 — loaded_later_mastery_02.apk (retired artifact link; see artifact inventory) — SHA-256 `a164696848652d7ac9a526ad70cc46e96a6953755d8649279a0703cbeb76c94a`
- Mastery delivery 3 — loaded_later_mastery_03.apk (retired artifact link; see artifact inventory) — SHA-256 `0bf7af8a7d15f03491dacc2d8c4630033795b25769ffd19635a485f6347ead03`
- Mastery delivery 4 — loaded_later_mastery_04.apk (retired artifact link; see artifact inventory) — SHA-256 `b22607b245e65a4b03120d38af60edad0bc8d895648551b48657bdf32e880410`
- Mastery delivery 5 — loaded_later_mastery_05.apk (retired artifact link; see artifact inventory) — SHA-256 `2286d3b9ab4f94e2149c130e93226ab92410fe19236edb0084f6f5cf652679fe`
