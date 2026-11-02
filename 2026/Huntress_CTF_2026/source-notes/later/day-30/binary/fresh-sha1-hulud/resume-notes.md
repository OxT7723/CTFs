> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

> **SHA1-Hulud chronology:** The original Game AI investigation predates the successful account in `source-notes/user-updates/sha1-hulud-web-pro-writeup.md`. Earlier claims that the flag check was an irreversible input KDF are superseded. A recorded local verification and a Game Master completion claim are distinct evidence. The complete successful emulator and its companion files are not present in these uploads.

# SHA1-Hulud resume notes

## Completion update (2026-10-31)

The Game Master now returns `CORRECT` for this existing attempt and lists
answer ID `flag` as accepted. Completion was recorded at
`2026-10-31T15:32:26.832Z`. The successful submission text and response were
not saved locally. This note is now a historical reversing handoff; its
former unresolved status and resume plan are superseded.

The adjacent [attempted-flags.md](attempted-flags.md) remains useful for
distinguishing earlier rejected submissions and local emulator probes.

## Attempt and artifact

- Challenge: `binary-reverse-engineering-day-30-sha1-hulud`
- Attempt: `353f3c79-6a5e-42b3-b061-0b531ec2e59e`
- Mode: Single Solve, untimed; answer ID: `flag`
- Local executable: `extracted/sha1-hulud.exe`
- Assigned ZIP: `sha1_hulud.zip`
- Trace script: `analysis/solve_sha1_hulud_trace.py`
- Prompt clue: TeamPCP “dropped the ball with this payload name”; “here's Wonder Wall!”; ZIP password `infected`.
- The saved Game Master response records the ZIP SHA-256 as `9fc7b3bcb00c9b6ea174ac6cd17729912aa7588838722959e5cac9611aff8c38`. Per the player's instruction, do not redownload or rehash the artifact for this solve.

The Game Master status was checked read-only on 2026-10-30: at that time this
same attempt was active in `single_solve` with no deadline. OpenAPI lists
`openapi`, `list`, `status`, `artifact`, and `download` for GET, and
`start`, `submit`, `retry`, `practice`, and `reset` for POST; it documents no
hint operation. No Game Master submission was made during this turn.

## What the reversing established

- The program asks for a flag, then validates the entered text. On its success
  path it decrypts and prints `correct, the flag is ` followed by the entered
  text; it does not reveal a separate plaintext flag.
- The final comparison is around `0x140059cdc`. It processes 32 bytes, XORs
  three byte values, and accumulates mismatches at `[rbp+0xca8]`. The result at
  `0x140059cf3` is a single success bit, so the ordinary output provides no
  useful partial-match feedback.
- The deterministic narrow run produced target bytes
  `bca76889233d3ef978581f9e11f788daf6397ca3045c979b70867fdcd3fd5cbe`.
  The exact sequence was not found as raw bytes in the executable or the two
  already-extracted stage files; the target is assembled at runtime.
- The candidate side is input-dependent and uses a custom SHA-1-based,
  obfuscated transform. Anti-analysis and runtime clock/performance state made
  emulation slow and nondeterministic until the prior trace scripts added
  hooks. The user's theory that the real flag is entered and transformed
  before comparison matches the observations.
- Useful emulator reports and memory captures from the attempt are included in
  this folder (`speakeasy-report.json` and `speakeasy-memory.zip`). The
  narrower probe logs and scripts mentioned in the ledger were kept under
  `/tmp` on the original VM and are not part of this handoff.
- The user's pasted Google AI summary about “Wonderwall” as a threat tracking
  label and later events remains unverified. A quick search attempt yielded no
  usable independent result; don't treat that summary as evidence.

## Stopping point before completion

The last locally documented `Wonder Wall` run reached `0x14005a019` and failed its success gate
(`0`). It is recorded as a local rejection in `attempted-flags.md`; it was not
submitted. It produced 816 compare pairs and 18 mismatch results; its
temporary log is `/tmp/sha1-hulud-narrow-2026-10-31d.log`. The committed
`analysis/local-comparison-capture.json` contains the latest completed run,
`flag{anyway_heres_wonder_wall}`.

Both 45,000,000-round mixer loops (`0x14004194d` and `0x1400481db`) read the
executable image, not the candidate string. This corrects the earlier
interpretation that these loops were the input KDF. The full run made 59,359
SHA-1 compression calls and completed with module return value 0 after the
candidate check failed.

`analysis/solve_sha1_hulud_narrow.py` is the durable Speakeasy runner. It
captures comparison byte pairs, each mismatch accumulator, equality bits, and
the final success gate. The TEB and deliberate VEH fixes remain in place.

`flag{wonder_wall}` also completed the full local path and was rejected:
all 18 mismatch accumulators were `0xff`, and the final success gate was `0`.
It was not submitted. Its full log is
`/tmp/sha1-hulud-narrow-flag-wonder-underscore-2026-10-31.log`.

The prompt's exact text inside the standard wrapper, `flag{Wonder Wall}`, was
also rejected locally with all 18 mismatch accumulators at `0xff` and final
gate `0`. It was not submitted. Its full log is
`/tmp/sha1-hulud-narrow-flag-Wonder-Wall-2026-10-31.log`.

`flag{anyway_heres_wonder_wall}` was also rejected locally on 2026-10-31.
All 18 groups had mismatch `0xff` and the final gate was zero. The updated
capture includes all three XOR operands (`BL`, `SIL`, `DL`) at every compare
byte, plus iterator state. This candidate was not submitted; its full log is
`/tmp/sha1-hulud-narrow-flag-anyway-heres-wonder-wall-2026-10-31.log`.

The unwrapped input `anyway_heres_wonder_wall` was replayed but stopped before
the full comparison finished. Its partial capture has 400 of 816 byte pairs
across 9 of 18 groups and no success-gate observation, so it is not a
pass/fail result. The trace is preserved in
`analysis/partial-no-wrapper-capture.json`; it was not submitted.

`analysis/solve_sha1_hulud_trace.py` remains the user-modified trace script
copied from the original attempt folder. The original remains at
`work/day-30/binary/353f3c79-6a5e-42b3-b061-0b531ec2e59e/analysis/solve_sha1_hulud_trace.py`.
The executable and ZIP were copied as-is; they were not changed, redownloaded,
or rehashed. This handoff gathers the files from both SHA1-Hulud work folders:
the original attempt directory and `work/day-30/binary/fresh-sha1-hulud/`.
It also includes the earlier reversing notes and scripts in
[`notes/HANDOFF.md`](notes/HANDOFF.md), [`notes/findings.md`](notes/findings.md),
and `analysis/`. Duplicate artifact copies are kept in their original relative
locations.

## Historical resume plan (superseded)

This plan predates the accepted Game Master result. No further solve work is
needed based on this handoff.
