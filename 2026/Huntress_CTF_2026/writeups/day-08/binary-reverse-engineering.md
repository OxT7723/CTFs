# Swift Justice

Day 8 · Binary reverse engineering · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `binary-reverse-engineering-day-08-swift-network-configuration`

## Earlier local account

---

The report describes an 80-field Single Solve evidence inventory across eight binaries and archives in an AES ZIP, using `infected`. It says 74 fields were accepted and six format fields remained after five failed submissions each. HCFG records were reportedly decoded and checked by CRC; .NET and two JAR files were inspected statically. The live status confirms an active untimed Single Solve attempt but does not expose accepted-field counts. Review the current attempt's specific unresolved IDs and prior failures before any further submission. This was the historical status when the note was recorded; all three modes were completed on 2026-10-09.

The assignment is an evidence inventory across eight binaries and archives. The goal is to recover the requested hashes, binary metadata, and the embedded network configuration. The Game Master offered Single Solve, Time Trial, and Mastery; all three returned `CORRECT` and are confirmed complete by live status. CourseStack remains the official score ledger.

| Mode | Attempt | Submitted fields | Result |
| --- | --- | ---: | --- |
| Single Solve | `f141de28-14b2-44fe-8178-bd9ea133a411` | 80 | `CORRECT` |
| Time Trial | `6ba5d48c-e267-42c4-aef3-c1eb85d2f250` | 80 | `CORRECT` |
| Mastery | `903820af-5f75-4791-ad56-dd0dfad68d59` | 400, across five deliveries | `CORRECT` |

The assigned `evidence.zip` uses the archive password `infected`. I downloaded its original bytes through the authenticated public Game Master and verified the archive SHA-256 against the current assignment before extraction with `7z`. The nine extracted files cover eight numbered tasks; Day 3 has both a DLL and a runtime configuration JSON file. The solver hashes those files individually, never the extracted directory or the containing ZIP.

| Task | Evidence and derivation |
| --- | --- |
| Day 1 | Read the ELF header, ordered section names, and nonempty symbol names using `pyelftools`. Locate the `recover_code` function in `.symtab` and disassemble only its symbol bytes with Capstone. In the Single Solve sample it is `mov eax, 8100; ret`. |
| Day 2 | Detect the ELF format and C++ metadata, then locate and decode its HCFG record. |
| Day 3 | Recognize the i386 PE with CLR metadata and `v4.0.30319`, hash both the DLL and runtime configuration, then decode HCFG in the DLL. |
| Days 4–5 | Read the ELF architecture and HCFG version/key. Day 5 uses the last HCFG marker in the binary. |
| Days 6–7 | Inspect JAR ZIP entries and compression methods, find the base64 encoded HCFG inside a class file, and decode it. The observed methods are `[0,8]`. |
| Day 8 | Read the Swift ELF class/machine and find its base64 encoded HCFG record. Decode its JSON to obtain `campaign`, `domain`, `mutex`, and `url`. |

An HCFG record starts with `HCFG`; its version is byte 4, XOR key byte 5, and little endian CRC32 bytes 8–11. XOR each byte after the 12 byte header with the key, isolate the JSON object, and require its CRC32 to match the header. For the Single Solve sample, the Day 8 record yields `https://node-000.day08.example.invalid/api/BR08-000` and CRC32 `0x6a033bfd`. This `.invalid` address is challenge data, not a service to contact.

The original game AI recap reported 74 accepted fields and six unresolved format fields. That count was not independently available from the live status. Recomputing the supplied 80 answers from the current Single Solve archive produced an exact match; submitting them returned `CORRECT`. No guessed replacements were needed.

Use the current Game Master assignment and answer IDs for each run. With the archive already downloaded, the static extraction and answer generation steps are:

```sh
7z x -pinfected -o08-Swift_Justice/single_extracted 08-Swift_Justice/evidence.zip
python 08-Swift_Justice/solve_evidence.py 08-Swift_Justice/single_extracted
```

`solve_evidence.py` requires `pyelftools` and `capstone` and outputs a JSON answer map. It does not submit. The retained `single_answers.json` contains the complete verified Single Solve values. `run_mode.py time_trial` and `run_mode.py mastery` start the respective live mode, authenticate with `HUNTRESS_GM_TOKEN` from the environment, download and hash-check each current delivery, extract with `7z`, run the parser, check the current answer ID set, and submit. It never stores the bearer token. Each timed attempt generated its own archive and answer file; Mastery required `set1.` through `set5.` prefixes, totaling 400 fields. The five Mastery Day 8 URLs differ by current variant, so old answer values must not be reused.

- Essential: `solve_evidence.py`, `run_mode.py`, `single_answers.json`, this write-up, and `challenge_state.json`.
- Reference evidence: the original Single Solve `evidence.zip` and its extracted files, plus `timed_runs/` archives, extracted samples, answer maps, and result summaries. These preserve the exact successful variants for verification.
- Potentially disposable after any separate retention decision: duplicate extracted timed files and archives once the verified samples have been backed up. Nothing was deleted.

## Retained sources

- [early/08-Swift_Justice/readme.md](../../source-notes/early/08-Swift_Justice/readme.md)
- [later/writeups/day-08/progress-notes.md](../../source-notes/later/writeups/day-08/progress-notes.md)
