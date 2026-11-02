# Pool Party

Day 6 · Binary reverse engineering · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `binary-reverse-engineering-day-06-java-bytecode-loader`

## Earlier local account

---

Pool Party is a cumulative binary analysis exercise. Each encrypted `evidence.zip` contains Day 1 through Day 6 samples: an ELF, a native ELF or PE sample, a .NET assembly and runtime configuration, native Go and Rust samples, and a Java JAR. Single Solve had 48 answer IDs. Mastery had two independent deliveries and 96 `set1.` / `set2.` answer IDs. The answers depend on the assigned bytes, so each attempt was downloaded and parsed anew.

The ZIP password was the documented `infected`. The solver opens it with `pyzipper` and never executes the extracted programs. SHA-256 values are calculated over each extracted file in ZIP order.

For Day 1, `pyelftools` reads the ELF header, section names in section-header order, and **every nonempty name in `.symtab` order**. This complete symbol array was the remaining Single Solve answer and the Game Master accepted it. The `recover_code` FUNC symbol supplies the address and size for `capstone` disassembly; the six-byte function decodes to `mov eax, 0x1fa4; ret` in the retained Single Solve sample. The server accepted the equivalent AT&T spelling previously submitted. If `recover_code` is absent, the solver returns `[]`.

The native and .NET samples carry an `HCFG` record. Its header is the four-byte marker, one-byte version, one-byte XOR key, a little-endian 16-bit JSON length, and a little-endian 32-bit CRC32. XOR the following `length` bytes with the key, verify CRC32 over the decoded JSON, then read `campaign`, `domain`, `mutex`, and `url`. The solver searches for a record whose checksum and JSON parse both succeed, since an incidental `HCFG` byte sequence can also occur in code. The Day 3 managed sample has PE/CLI metadata; its runtime version comes from the CLI metadata root. Day 6 stores a Base64-encoded HCFG record in a Java class constant. The solver extracts the class from the JAR, decodes that constant, and applies the same HCFG parser. File format and architecture are determined from the current sample's container and headers.

```bash
python 06-Pool_Party/solve.py 06-Pool_Party/evidence.zip
python 06-Pool_Party/solve.py 06-Pool_Party/time_trial_latest_evidence.zip
python 06-Pool_Party/solve.py 06-Pool_Party/mastery_set1_evidence.zip
python 06-Pool_Party/solve.py 06-Pool_Party/mastery_set2_evidence.zip
```

The first command produces the 48 unprefixed answer IDs. For Mastery, prefix each delivery's output with its current `setN.` namespace, using the current Game Master `answer_ids`. `run_mastery.py` records how the two deliveries were downloaded, checked against server SHA-256, parsed, mapped, and submitted. It is specific to this challenge and requires `HUNTRESS_GM_TOKEN` in the environment; it does not print that credential.

- **Single Solve:** `CORRECT` on 2026-10-08. The existing 47 accepted answers matched the retained current artifact. The complete `.symtab` name array supplied the 48th.
- **Time Trial:** `CORRECT` on 2026-10-08, with a server deadline three seconds after the accepted submission. An earlier seven-second attempt expired; another revealed PE variants for Days 2 and 4, which the solver was updated to handle. The successful attempt used the fresh ZIP and answer IDs.
- **Mastery:** `CORRECT` on 2026-10-08 through the Game Master's untimed practice continuation after the first timed attempt expired and `retry` returned `rotation_exhausted`. Both current deliveries were parsed independently. The server marked this completion as ineligible for Hall of Fame timing.

Keep `solve.py`, `run_mastery.py`, the original Single Solve `evidence.zip`, `challenge_state.json`, and this write-up for reproduction. The successful Time Trial ZIP and two Mastery ZIPs are useful variant samples. Earlier expired Time Trial downloads, extracted copies, and answer/result JSON files are potentially disposable duplicates; they were retained rather than deleted.

Use the full symbol-table order for array questions, verify decoded HCFG data by CRC32, and prepare variant-aware parsing before starting a short timer. A mode's `CORRECT` status and Hall of Fame eligibility are separate facts.

## Retained sources

- [early/06-Pool_Party/readme.md](../../source-notes/early/06-Pool_Party/readme.md)
- [later/writeups/day-06/decode-summary.txt](../../source-notes/later/writeups/day-06/decode-summary.txt)
