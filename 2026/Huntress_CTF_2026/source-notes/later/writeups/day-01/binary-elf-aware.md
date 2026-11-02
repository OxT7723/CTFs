> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 01: ELF Aware

## Challenge

- **Single Solve:** `binary-reverse-engineering-day-01-c-elf-orientation`
- **Time Trial:** `binary-reverse-engineering-day-01-c-elf-orientation/time_trial`
- **Mastery:** `binary-reverse-engineering-day-01-c-elf-orientation/mastery`
- **Lane:** Binary Reverse Engineering
- **Description:** “Before you can reverse anything, you have to learn to read. These plain C binaries are your primer: headers, section tables, symbol tables. Start with `readelf -h -S` and work your way down.”

Every specimen asks for its ELF class, byte order, machine architecture,
object type, `.huntress` marker, whether `.symtab` remains, designated exported
symbol, `recover_code` return constant, and entry point. The exact answer IDs
come from the current Game Master response. Single Solve uses the unprefixed
IDs; Time Trial repeats the nine fields for `slot0` through `slot3`; Mastery
uses those slots in each of `set1` and `set2`.

Formats are exact text for the header, marker, and symbol fields; `true` or
`false` for `.symtab`; a base-10 integer for `recover_code`; and lowercase
hexadecimal with a `0x` prefix for the entry point. The Game Master asks for
`none` when a requested field is absent.

## Solver

The existing reusable implementation is
`binary-reverse-engineering-tools/analyze_evidence.py`. It extracts the
encrypted evidence ZIP, maps slot and set IDs to their specimens, reads ELF
headers and sections with `readelf`, and recovers function constants from
`objdump` disassembly. The existing `run_modes.py` runner obtains artifacts,
builds answers, skips previously accepted IDs on a resumed attempt, submits
the answer set, and records the result. Its optional `--keep-alive` mode reuses
the Game Master HTTP connection for start, submission, and status JSON calls;
artifact downloads continue through the supported proxy as their own request.

The mode runner checks its required `pyzipper` dependency before contacting
the Game Master. `readelf` and `objdump` are also required. For an authorized
fresh attempt, the general command is:

```sh
binary-reverse-engineering-tools/.venv/bin/python \
  binary-reverse-engineering-tools/run_modes.py "$CHALLENGE_ID" \
  --download-workers 1 --keep-alive
```

On this challenge, Time Trial and Mastery are legacy timed-by-default routes:
the Game Master reports `run_for_time_supported:false`, and retrying them
starts a clock. Do not use the command above for those modes during untimed
training. A `--retry` on either route is a new timed attempt. For a prepared
Time Trial, omitting `--batch-size` sends all answers in one request; use
`--skip-initial-status` only on a fresh attempt when no answers can already be
accepted. The runner checks final status after submission by default;
`--skip-final-status` omits that post-submission request and relies on the
submission response, which can be verified separately afterward.
`--skip-artifact-hash` omits local SHA-256 calculation and verification; use it
only when integrity verification is not needed during the run.

## Findings and fix

The solver handled the historical artifacts, but the ranked Time Trial
artifact included a stripped `slot-3.elf` with no `.symtab` and no defined
global function symbols. The exported-symbol question expects `none` when that
field is absent. `designated_exported_symbol` previously raised an error when
it found no defined function candidates, aborting the whole answer build.

The analyzer now returns `none` when there are no defined global function
symbols or no designated analysis-symbol candidate. It still raises on
multiple plausible candidates instead of guessing. The ranked artifact now
produces all 36 answer IDs offline in about 0.04 seconds.

The Game Master then identified a second solver bug. ELF type answers must use
the ELF enum (`ET_EXEC`), not `readelf`'s display token (`EXEC`) or full display
text (`EXEC (Executable file)`). A one-answer test rejected the old value and
accepted `ET_EXEC`. The analyzer now maps standard `readelf` type tokens to
their ELF enum names.

The mode runner now reports concise Game Master HTTP errors and records start,
download, extraction, solver, status, submission, and total wall time, along
with Hall of Fame eligibility and remaining unique attempts. It stops
automatic answer bisection after an incorrect timed batch and records HTTP 429
cooldowns, leaving the assigned artifact for offline review.

## Session results

- Single Solve was already complete: 9/9 answer IDs accepted historically.
- The completed Time Trial had 36/36 accepted historically. Its regular pool
  is empty. The documented practice operation was rejected because fresh
  timed variants remain.
- The completed Mastery had 72/72 accepted historically and zero unique
  attempts remaining. Practice returned the completed result without a new
  attempt or artifacts.
- No fresh untimed variants were available. The historical Single Solve,
  Time Trial, and both Mastery deliveries were downloaded and checked against
  their API SHA-256 values for offline regression.
- Five ranked Time Trial attempts were performed after explicit
  authorizations. Each was Hall of Fame eligible at start with a 50-second
  deadline. The first stopped during answer generation on a stripped specimen.
  The second and third answer batches were rejected; per-answer batching on
  the fourth isolated the type mismatch and confirmed `ET_EXEC`. That attempt
  expired before its remaining fields were accepted.
- A five-answer submission was mistakenly sent after the fourth attempt's
  deadline; the Game Master rejected it as expired. No answer was accepted
  from that late submission.
- The fifth attempt completed successfully: the Game Master returned
  `CORRECT`, accepted all 36 fields, and reported Hall of Fame eligible.
  Total runner time was 45.54 seconds, including 38.03 seconds submitting
  36 single-answer requests. Final status reports 247 unique attempts
  remaining.
- The sixth attempt also completed successfully. It submitted all 36 answers
  in one batch, skipped the runner's pre-submission status request, and still
  verified final status. The Game Master returned `CORRECT` and
  `hall_of_fame_eligible:true`; runner wall time was 9.54 seconds
  (start 4.16s, download 2.68s, solver 0.042s, submission 1.59s, final status
  1.05s). Final status reports 246 unique attempts remaining.
- The seventh attempt completed successfully with the same one-batch workflow:
  `CORRECT`, all 36 accepted, and Hall of Fame eligible. Runner wall time was
  7.27 seconds (start 1.89s, download 2.36s, solver 0.043s, submission 2.05s,
  final status 0.90s). Final status reports 245 unique attempts remaining.
- The eighth attempt was a control run with the final status request enabled.
  It returned `CORRECT`, accepted all 36 fields, and was Hall of Fame eligible.
  Runner wall time was 6.22 seconds, including 0.96 seconds for final status.
- The ninth attempt skipped the runner's final status request. Its submission
  returned `CORRECT`; a separate status request afterward confirmed all 36
  accepted and Hall of Fame eligibility. Runner wall time was 6.54 seconds
  without the final status request. Run-to-run network variation outweighed
  the omitted request (the second run's start took 1.05 seconds longer); since
  status is checked after the accepted submission, it cannot improve the
  recorded solve time. Final status reports 243 unique attempts remaining.
- A read-only status benchmark confirmed that the proxy supports persistent
  HTTP connections. Fresh requests took 1.26–2.89 seconds; reused requests
  took 1.07–1.29 seconds in the runner validation. This suggests a modest
  transport improvement, though the sample is small and the calls are
  variable. No ranked attempt was used for this benchmark.
- Three further ranked Time Trial runs used `--keep-alive`, a single answer
  batch, and no status request in the submission path. Each returned
  `CORRECT`; separate post-run status checks confirmed all 36 answers and
  Hall of Fame eligibility. Runner times were 7.66, 5.42, and 7.58 seconds
  (mean 6.89 seconds); answer generation stayed near 0.04 seconds. These
  runs do not show a consistent end-to-end speedup over the previous runs:
  start, download, and submission latency varied, with the last submission
  taking 3.27 seconds. Final status reports 240 unique attempts remaining.
- Ten more ranked Time Trial runs used the same keep-alive and single-batch
  workflow. All ten returned `CORRECT`; separate status checks confirmed
  36/36 accepted and Hall of Fame eligibility on every attempt. Runner times
  ranged from 4.29 to 7.82 seconds (median 5.20, mean 5.48); answer
  generation averaged 0.043 seconds. This confirms solver reliability across
  these ten artifacts, while network latency still varies. Final status
  reports 230 unique attempts remaining.
- One ranked attempt tested `--skip-artifact-hash`. It returned `CORRECT`,
  accepted all 36 answers, and was Hall of Fame eligible. Runner time was
  7.53 seconds, including a 2.04-second download. After the timer, local
  SHA-256 verification matched the Game Master's expected hash and took
  0.327 ms for the 7,456-byte ZIP. The download was slower than the previous
  hashed-run average, so this test shows no measurable speed benefit from
  skipping the hash. Final status reports 229 unique attempts remaining.
- Ten more ranked Time Trial runs used `--skip-artifact-hash`. All ten
  returned `CORRECT`; status confirmed 36/36 accepted and HOF eligibility,
  and post-run SHA-256 checks matched all ten API-provided hashes. Runner
  times ranged from 4.77 to 7.91 seconds (median 5.57, mean 5.98); downloads
  averaged 1.77 seconds and answer generation averaged 0.042 seconds. The
  offline hash checks averaged 0.16 ms and did not affect the timed path.
  Comparing with the earlier hashed batch is not controlled, but this batch
  shows no speed gain from skipping the hash. Final status reports 219 unique
  attempts remaining.
- Three additional runs used keep-alive with normal SHA-256 verification.
  All returned `CORRECT`, accepted 36/36, and were Hall of Fame eligible.
  Runner times were 5.29, 4.75, and 6.32 seconds (mean 5.45); solver time
  stayed near 0.042 seconds. This small sample does not establish a timing
  difference from the no-hash runs. Final status reports 216 unique attempts
  remaining.
- Ranked Mastery had zero unique attempts remaining. An explicitly requested
  retry returned HTTP 409 `rotation_exhausted` (“You have used every timed
  attempt for this challenge.”). Follow-up status still showed the historical
  attempt `CORRECT` with 72/72 accepted, zero attempts remaining, and no active
  deadline; no new timer or attempt was created.

## Artifacts reviewed

- Single Solve `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `90bb41ce9d55b924436486cb123db1d0a79a885697599511c44da5c336fad9b4`.
- Historical Time Trial `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `48850ef76d65038de8f431ce86dffbb67524fb4894d5da4640050b17117b0ab7`.
- Historical Mastery set 1 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `962e8a1b7e3994827a465e2686cb220cebc69975fc9489edc30cb3be0f2da5ea`.
- Historical Mastery set 2 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `460a37c1d3fa7a5f0dd793dc824c09b773ff3981b3065efc0f84dda1cf4e4b71`.
- First ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `55658a4750542a208d859c55502e972d72357ae4adb1c1d5ccb6db04a7daa3e3`.
- Second ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `7010fd650e50fd0807125ac6e21c0485feed849c8eb20ae8080fd78e60b77f78`.
- Third ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `e1c3cba9806b5051bbef920b59be3c0c1942321179c96ca23c71ddabbeb09a6f`.
- Fourth ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `68e9a4d02330c18af16c98557779fac1a39425f2c6432d3accfdd52e27fb70b8`.
- Fifth ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `1465efcf866c091f6b5a9592036b48982656b6b03cc745a22c33f2e17f68f8cb`.
- Sixth ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `ec668e6c902d4a6f3db8be1d29e7769c8f1936c06761e9d97f8426943f5178c6`.
- Seventh ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `475c8b015cb3d5f5ffd634691e53878fa9b396c0f4be34a569466fcfe006a7cd`.
- Eighth ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `74998cd4bade09ecf6cb397206f4d2037a64637606a534c490621edf915323dd`.
- Ninth ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `0a17ed7b83d2f68bd811e90de01d984fb370d17d750e846c50a2441820484ab8`.
- Tenth ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `9a73c26949d1b2cbc74dcedd64de922127179f8672d4470bc8004aada1718cec`.
- Eleventh ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `e35bd4b002d44757745212ef4a3e0ef7b031f2c8ac2048c0311c1fd0b55902fd`.
- Twelfth ranked Time Trial artifact `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `6ede47a65c99c63a91af7174a7e00a2bd195858ed254f1865b8a0ca29452f3d0`.
- Timed keep-alive run 13 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `b1d897f3c402fd73a95dadc1a0f8ffc49d46d69b1df47d18cb6f5931c3e25953`.
- Timed keep-alive run 14 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `56378d3aa92267bcd0e9648af39ed2106a74a4c829f4cfbc19cff9aa9eb973d2`.
- Timed keep-alive run 15 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `194f7df7d0450d8c0953adfdff09808df147cac5fedeb330c6f436ae3cf2480e`.
- Timed keep-alive run 16 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `a8d7cb63cade953ff57247b725698e8f0954c493ed9c5f68b4f0c6793bf2e4a2`.
- Timed keep-alive run 17 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `e81b1efec9292a31599d1929e69cc90565a91179e55084c22454d0f054d1a917`.
- Timed keep-alive run 18 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `103c353aeda6465e99c06c2bc5c9c0d61598252d0896eab991aa59a6055f7705`.
- Timed keep-alive run 19 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `bb697f9f5a928ff4b0c21acbf24ade14acdd878c879c726b8c9fb9683977ade2`.
- Timed keep-alive run 20 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `f5bcf9fea6c2add2eb4dfdea136848ec5e89ed735693182cac5fb7126c92a458`.
- Timed keep-alive run 21 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `bdb78237463af5cbc4cb3964e5f7a314b5d790b54873d72a0cf485024444e4f5`.
- Timed keep-alive run 22 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `4ba96b13586d83db5e1dbe53732be37d7040a4ce17203354d90affd5e4296842`.
- No-hash timed run `evidence.zip`: download (retired artifact link; see artifact inventory), expected SHA-256 `6d97b6675f0153ed2e41e63eea60e7096c6d8b37cf653970cba71135776daa97` (matched by post-run offline verification).
- No-hash timed run 23 `evidence.zip`: download (retired artifact link; see artifact inventory), expected SHA-256 `b011ff938f258960047ce5cf0cb39365ccdeb053c92417885789257ef23ab372`.
- No-hash timed run 24 `evidence.zip`: download (retired artifact link; see artifact inventory), expected SHA-256 `6f50934f2528e8b465db6a62d68ff2599109d571439fd53d0538e9dfbe429fdd`.
- No-hash timed run 25 `evidence.zip`: download (retired artifact link; see artifact inventory), expected SHA-256 `8f327433bf06bcadfd1bd09270b355a19b731f9b75397485a33c47047d524fb6`.
- No-hash timed run 26 `evidence.zip`: download (retired artifact link; see artifact inventory), expected SHA-256 `eb471f951310c07f1c3c9ee60e55739014d9575a777fa65e312197a909aa7970`.
- No-hash timed run 27 `evidence.zip`: download (retired artifact link; see artifact inventory), expected SHA-256 `ccc7711a72baea67f770ac8e80ffc2afd78c714e0ca5a1e9a6cabc7a17b58ab5`.
- No-hash timed run 28 `evidence.zip`: download (retired artifact link; see artifact inventory), expected SHA-256 `7ab3e3f3203f1eca403476823b6f56e7f61a8829f80637444f6e4c222a108e7f`.
- No-hash timed run 29 `evidence.zip`: download (retired artifact link; see artifact inventory), expected SHA-256 `c1784e40d19c4ca724fbc88a249b5153bafc2300036a91cca39e966401844e40`.
- No-hash timed run 30 `evidence.zip`: download (retired artifact link; see artifact inventory), expected SHA-256 `3d5f0d990bc75efb5ac4c070c89a7a47d8b551020a1c3491635bcdca15561f3d`.
- No-hash timed run 31 `evidence.zip`: download (retired artifact link; see artifact inventory), expected SHA-256 `13c60ebad06da0fa213748f60f6e81c9cd6af99107b0b4b2b8d29ab163be47ad`.
- No-hash timed run 32 `evidence.zip`: download (retired artifact link; see artifact inventory), expected SHA-256 `dc1f7a293ecc1e8bcb78be84fc9fdfcc6e2bb5b33e393d1347c1b783a5f827d2`.
- Verified-hash Time Trial run 33 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `b65c7228db42263ee4b2b423ea0524a288e2661fcd358bbddd855b8067fed0c4`.
- Verified-hash Time Trial run 34 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `286cc54a46ee5c7489e3470cea68eae6f4befe2bfdeffaccf7f7f0479ba9688d`.
- Verified-hash Time Trial run 35 `evidence.zip`: download (retired artifact link; see artifact inventory), SHA-256 `27d89e57ac1273cd35d010d19156f1367bc043208c690b43c7cfa0217d3d75f2`.

Offline records and preserved artifacts are under
`work/day-01/binary/elf-aware-regression/` and
`work/day-01/binary/9bbae33d-b5d8-4dcb-8483-9a7cf9588178/` and
`work/day-01/binary/d59dc7e3-d1b4-40d2-8f8b-81f1f4dcd80c/` and
`work/day-01/binary/42874722-00ae-486a-8ea4-00404572b9b7/` and
`work/day-01/binary/12295177-dc66-4341-99a6-b0b25690c391/` and
`work/day-01/binary/8ae2b9da-1db0-4355-850f-d0307e40ccc6/` and
`work/day-01/binary/f8693f7d-fed7-4ed0-89ee-7eb3cd1cd3b7/` and
`work/day-01/binary/348005cd-ecea-4451-804a-4e2e54b93267/` and
`work/day-01/binary/88bdfead-b7bf-4c1a-8309-6c8eb0b62da3/` and
`work/day-01/binary/a07f037c-c4a2-4bb1-ada8-73b472090487/` and
`work/day-01/binary/761c4f3a-337d-45c0-8721-9950cde28688/` and
`work/day-01/binary/e9f2aef2-b98c-4d39-b59b-e62c39cfc19d/` and
`work/day-01/binary/16a84ae4-ed98-4e1f-8d91-18dc38c3a006/`,
`work/day-01/binary/keepalive-batch-10-20261028.json`, and the ten attempt
directories named by the attempt IDs in that summary, plus
`work/day-01/binary/7260f9e8-3f0f-4ab3-834e-db3800027b24/`,
`work/day-01/binary/nohash-batch-10-20261028.json`, and the ten attempt
directories named by the no-hash batch summary, plus
`work/day-01/binary/keepalive-verified-batch-3-20261028.json` and its three
attempt directories.
