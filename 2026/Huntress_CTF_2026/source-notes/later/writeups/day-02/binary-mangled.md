> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 02 Binary Reverse Engineering — Mangled

## Challenge

- **Name:** ⚙️ Mangled
- **Single Solve ID:** `binary-reverse-engineering-day-02-cpp-and-pe-orientation`
- **Time Trial ID:** `binary-reverse-engineering-day-02-cpp-and-pe-orientation/time_trial`
- **Mastery ID:** `binary-reverse-engineering-day-02-cpp-and-pe-orientation/mastery`
- **Lane:** Binary Reverse Engineering
- **Description:** “C++ on Windows. The symbols are mangled, the classes hide behind vtables, and RTTI is your Rosetta Stone. Demangle it all with `c++filt`, reconstruct the classes, and don't forget the PE imports.”

Every task uses an `evidence.zip` bundle. The single and Time Trial bundles each contain C and C++ specimens. Mastery has two deliveries, one per set. The questions ask for hashes and binary metadata, decoded configuration values, and C++ vtable/typeinfo/symbol evidence.

## Questions and answer formats

Single Solve and Time Trial use these 17 answer IDs. Mastery asks the same questions for both deliveries, prefixing each ID with `set1.` or `set2.`.

| Answer ID | Player-facing question | Required format |
| --- | --- | --- |
| `c_sha256` | What is the exact c sha256 value for field c_sha256 in the delivered evidence set? | Exact 64-character hexadecimal SHA-256; no prefix or spaces. |
| `c_marker` | What is the exact c marker value for field c_marker in the delivered evidence set? | Exact artifact text; use `none` only if absent. |
| `c_has_symtab` | What is the exact c has symtab value for field c_has_symtab in the delivered evidence set? | `true` or `false`. |
| `c_recover_code` | What is the exact c recover code value for field c_recover_code in the delivered evidence set? | Base-10 integer. |
| `c_machine` | What is the exact c machine value for field c_machine in the delivered evidence set? | Exact artifact text; use `none` only if absent. |
| `cpp_sha256` | What is the exact cpp sha256 value for field cpp_sha256 in the delivered evidence set? | Exact 64-character hexadecimal SHA-256; no prefix or spaces. |
| `cpp_format` | For the Day 2 C++ specimen in the bundled archive, identify its executable container from the final bytes. Submit ELF for an Executable and Linkable Format specimen or PE for a Windows Portable Executable specimen; letter case and a more specific ELF32, ELF64, PE32, or PE32+ label are accepted. | `ELF` or `PE`; case is ignored and the listed specific labels are accepted. |
| `cpp_xor_key` | What is the exact cpp xor key value for field cpp_xor_key in the delivered evidence set? | Lowercase hexadecimal with a `0x` prefix. |
| `cpp_config_crc32` | What is the exact cpp config crc32 value for field cpp_config_crc32 in the delivered evidence set? | Lowercase hexadecimal with a `0x` prefix. |
| `campaign` | What is the exact campaign value for field campaign in the delivered evidence set? | Exact artifact text; use `none` only if absent. |
| `domain` | What is the exact domain value for field domain in the delivered evidence set? | Exact artifact text; use `none` only if absent. |
| `url` | What is the exact url value for field url in the delivered evidence set? | Exact artifact text; use `none` only if absent. |
| `mutex` | What is the exact mutex value for field mutex in the delivered evidence set? | Exact artifact text; use `none` only if absent. |
| `has_cpp_vtable` | What is the exact has cpp vtable value for field has_cpp_vtable in the delivered evidence set? | `true` or `false`. |
| `has_cpp_typeinfo` | What is the exact has cpp typeinfo value for field has_cpp_typeinfo in the delivered evidence set? | `true` or `false`. |
| `mangled_score_symbol` | What is the exact mangled score symbol value for field mangled_score_symbol in the delivered evidence set? | Exact artifact text; use `none` only if absent. |
| `vtable_symbol` | What is the exact vtable symbol value for field vtable_symbol in the delivered evidence set? | Exact artifact text; use `none` only if absent. |

The stored Game Master responses retain the full current question text and answer formats:
Single Solve (historical reference: `../../work/day-02/binary/mangled-review-20261028/responses/single_solve.json`; not included),
Time Trial preflight (historical reference: `../../work/day-02/binary/mangled-review-20261028/responses/preflight-time-trial.json`; not included),
Mastery preflight (historical reference: `../../work/day-02/binary/mangled-review-20261028/responses/preflight-mastery.json`; not included).

## Solver and execution

The existing reusable implementation is
[analyze_evidence.py](../../../../tools/later/binary-reverse-engineering-tools/analyze_evidence.py),
with the Game Master workflow in
[run_modes.py](../../../../tools/later/binary-reverse-engineering-tools/run_modes.py).
It discovers specimens from the delivered archive, analyzes the bytes, maps
answers to the API-provided question IDs, and processes numbered Mastery sets.
It contains no Mangled-specific answers or fixed specimen hashes.

Required components are Python, the package in
`binary-reverse-engineering-tools/requirements.txt`, and GNU `readelf`,
`objdump`, and `nm`. `c++filt` is optional for manual symbol inspection; the
solver does not call it. The AES ZIP password is `infected`.

For a prepared future ranked Time Trial on this legacy timed-by-default route,
the runner's `--retry` sends `op=retry` without `run_for_time:true`:

```sh
binary-reverse-engineering-tools/.venv/bin/python \
  binary-reverse-engineering-tools/run_modes.py \
  'binary-reverse-engineering-day-02-cpp-and-pe-orientation/time_trial' \
  --retry --keep-alive --skip-initial-status --skip-artifact-hash \
  --download-workers 1
```

This command starts a timed attempt on this route. Do not use it for untimed
training. The one ranked Time Trial authorized in this session has already
been used. `--skip-artifact-hash` omits only the archive hash calculation;
the solver still calculates the specimen SHA-256 values required by the
questions. The archive hash was checked offline after the run.

For offline replay, extract an assigned archive with the existing extractor,
then pass the matching saved API response to the analyzer:

```sh
binary-reverse-engineering-tools/.venv/bin/python \
  binary-reverse-engineering-tools/extract_zip.py evidence.zip extracted/
binary-reverse-engineering-tools/.venv/bin/python \
  binary-reverse-engineering-tools/analyze_evidence.py extracted/ \
  --answer-map start-response.json --output candidate-answers.json
```

The Day 02 Time Trial and Mastery routes have no regular untimed pool. Mastery
has no ranked attempts remaining either. Its `--practice` continuation is
untimed, but the server returned the already-solved result without an attempt
ID or artifact assignment.

## Results

| Mode | Attempt | Result | Variants tested this session | Solver time |
| --- | --- | --- | ---: | ---: |
| Single Solve | Historical `4ef237a8-c4e8-4e9d-9187-d60a1457e566` | Previously `CORRECT`, 17/17 accepted | 1 saved artifact | 20.6 ms |
| Time Trial, regular | Historical `9acedadc-d35c-46a6-8c0e-19dab2893268` | Previously `CORRECT`, 17/17 accepted; no untimed replay route | 1 saved artifact | 70.5 ms |
| Mastery, regular/practice | Historical `ce161191-bdac-4920-bf04-0928067c81b2` | Previously `CORRECT`, 34/34 accepted. `op=practice` returned `CORRECT` but no new attempt or files. | 2 saved deliveries | 49.3 ms |
| Time Trial, ranked | `13af1f71-62ee-4c45-95ca-b79bdffef55a` | `CORRECT`, Hall of Fame eligible, 17/17 accepted | 1 fresh randomized artifact | 18.8 ms |
| Mastery, ranked | — | Skipped: zero unique ranked attempts remained | 0 | — |

The ranked Time Trial began at `2026-10-28T21:43:25.587Z` with a server
deadline of `2026-10-28T21:44:15.587Z`. Client end-to-end time was 7.985 seconds.
The Game Master reported 235 unique attempts remaining afterward. It did not
report an official leaderboard solve time or a CourseStack point total; the
attempt status and Day 02 listing both report completion.

The ranked archive SHA-256 matched the API manifest. An offline rerun produced
the exact same 17 candidates as the submitted run. The four saved historical
archives also produced all expected answer IDs: 17 Single Solve, 17 Time
Trial, and 34 Mastery answers. No new untimed randomized artifacts were
available, so the historical artifacts do not establish unseen-variant
coverage. The new ranked Time Trial provides one additional fresh variant.

## Artifact records

Historical artifacts were downloaded from their assigned attempts and checked
against the Game Master SHA-256 values.

| Assignment | Download | SHA-256 |
| --- | --- | --- |
| Single Solve | evidence.zip (retired artifact link; see artifact inventory) | `a9a78ed2120a5677af25606492f9418468a53ff6173fbbf79675c2d475cca55c` |
| Historical Time Trial | evidence.zip (retired artifact link; see artifact inventory) | `f629fd72a491da0d39a2d67def03b3851093ead5c313bd37ac7bf0315f6089e1` |
| Historical Mastery, set 1 | evidence.zip (retired artifact link; see artifact inventory) | `6a35d7872fea9031c98e32cad6978b6fabd1fa87afe0c83c22e43baba530074d` |
| Historical Mastery, set 2 | evidence.zip (retired artifact link; see artifact inventory) | `3de6f061b6a64859e4b8bf78b1ec5151d1b3edb1723d74284d461548a51bd918` |
| Ranked Time Trial | evidence.zip (retired artifact link; see artifact inventory) | `2929bc9fe95fd2131ff9fb9b428d4b7a2cc12c57f70b956519e07d866617516f` |

Attempt responses, downloaded bytes, candidates, and run summaries are in
`work/day-02/binary/` (historical reference: `../../work/day-02/binary/`; not included). The offline review bundle
is in `mangled-review-20261028/` (historical reference: `../../work/day-02/binary/mangled-review-20261028/`; not included).

## Readiness and limitations

- **Correctness:** All 17 ranked Time Trial answers were accepted. Historical
  Single Solve and Time Trial artifacts and both Mastery deliveries mapped all
  their required IDs.
- **Automation:** The existing runner handles download, extraction, answer
  mapping, submission, accepted-ID tracking, and result recording.
- **Speed:** About 8 seconds end to end in the ranked run; local analysis took
  about 19 ms. Network time dominated.
- **Mastery:** Two deliveries and all 34 answer IDs were processed offline.
  The old practice route returned no new artifact, and no ranked Mastery
  attempt remained.
- **Remaining risk:** Only one fresh randomized ranked artifact was tested
  this session. Future unseen variants could expose a new specimen layout or
  parser edge case. No code change was needed after this run.
