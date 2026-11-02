> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

> **SHA1-Hulud chronology:** The original Game AI investigation predates the successful account in `source-notes/user-updates/sha1-hulud-web-pro-writeup.md`. Earlier claims that the flag check was an irreversible input KDF are superseded. A recorded local verification and a Game Master completion claim are distinct evidence. The complete successful emulator and its companion files are not present in these uploads.

# SHA1-Hulud attempted answers

Challenge: `binary-reverse-engineering-day-30-sha1-hulud`
Attempt: `353f3c79-6a5e-42b3-b061-0b531ec2e59e`
Last updated: 2026-10-31

This log separates Game Master submissions from local emulator probes. A local
comparison failure is not the same as a server submission. Do not submit an
answer already marked **rejected**.

## Completion record

The Game Master status check on 2026-10-31 returned `CORRECT` for this attempt
and listed answer ID `flag` as accepted. The successful answer text was not
preserved in the local submission records.

## Earlier Game Master submissions

| Exact answer | Result | Record |
| --- | --- | --- |
| `Wonderwall` | Rejected | `submission-plaintext-name.json` |
| `d1165c99aa46170bdf824f7109e106e8d25aa6e9` | Rejected | `submission-self-code-sha1.json` |

These saved submissions were rejected, but their JSON files no longer contain
the submitted answer text. Keep them marked as tried; do not recreate their
answers from their filenames:

| Submission record | Result | Exact answer |
| --- | --- | --- |
| `submission-mapped-image-sha1.json` | Rejected | Not preserved |
| `submission-name-correction.json` | Rejected | Not preserved |
| `submission-sha1-archive.json` | Rejected | Not preserved |
| `submission-sha1.json` | Rejected | Not preserved |
| `submission-title-literal.json` | Rejected | Not preserved; earlier notes describe it as the title-literal attempt |

## Local emulator flag candidates

| Exact input | Result | Evidence |
| --- | --- | --- |
| `Wonder Wall!` | Rejected by local comparison | `/tmp/sha1-hulud-fixedprobe.log`; comparison completed with the success state still zero |
| `infected` | Rejected by local comparison | `/tmp/sha1-hulud-narrow-infected.log`; `al=0` |
| `Shai-Hulud` | Rejected by local comparison | `/tmp/sha1-hulud-narrow-shai.log`; `al=0` |
| `flag{wonderwall}` | Rejected by local comparison | `/tmp/sha1-hulud-narrow-flag-wonderwall.log`; `al=0` |
| `Wonder Wall` | Rejected by the local comparison; final success gate at `0` | `notes/findings.md`; `/tmp/sha1-hulud-narrow-2026-10-31d.log` |
| `flag{wonder_wall}` | Rejected by the local comparison; all 18 mismatch accumulators were `0xff`, final success gate `0` | `notes/findings.md`; `/tmp/sha1-hulud-narrow-flag-wonder-underscore-2026-10-31.log` |
| `flag{Wonder Wall}` | Rejected by the local comparison; all 18 mismatch accumulators were `0xff`, final success gate `0` | `notes/findings.md`; `/tmp/sha1-hulud-narrow-flag-Wonder-Wall-2026-10-31.log` |
| `flag{anyway_heres_wonder_wall}` | Rejected by the local comparison; all 18 mismatch accumulators were `0xff`, final success gate `0` | `analysis/local-comparison-capture.json`; `/tmp/sha1-hulud-narrow-flag-anyway-heres-wonder-wall-2026-10-31.log` |

## Incomplete local replay

| Exact input | Status | Evidence |
| --- | --- | --- |
| `anyway_heres_wonder_wall` | Partial replay only: 400 of 816 comparison pairs and 9 of 18 group results were captured; the success gate was not reached. This is not a pass/fail result and was not submitted. | `analysis/partial-no-wrapper-capture.json` |

## Other emulator inputs already tried

These were run through the emulator while tracing or testing the validator.
They are recorded to avoid repeating probes; they are not known flag answers.

| Input | Saved result |
| --- | --- |
| `4655387b8898109bd3c42eee3a9b3a581698c13d` | Trace reached no recorded final comparison (`COMPARE_COUNT 0`); not submitted |
| `2269a01611eb34111181af2201b7f649cb38e67e` | Used in 40-character/hash probes; saved logs show no final validator comparison; not submitted |
| `flag{test}` | Diagnostic input used in multiple tracing runs |
| `flagtest` | Diagnostic input used in path tracing |
| `test_input` | Diagnostic input used in tracing |
| `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` | Length/control probe |
