# Rust Belt

Day 5 · Binary reverse engineering · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `binary-reverse-engineering-day-05-rust-runtime-shapes`

## Earlier local account

---

Despite the Rust title, each delivery compounds the binary skills from Days 1–5. One password-protected `evidence.zip` contains a Day 1 C ELF, a Day 2 C++ executable, a Day 3 .NET DLL and runtime configuration file, a Day 4 Go executable, and a Day 5 Rust executable. Single Solve and Time Trial each ask 40 questions about one delivery. Mastery asks the same 40 questions for each of two independently assigned deliveries, under one timer. The ZIP password is `infected`.

The values below belong to this player's assigned files. Fetch and analyze the current delivery for a new attempt; variant numbers, hashes, configuration strings, and even ELF versus PE containers can change.

Use `readelf -h -S -s` on `d01--variant-*.elf`. The Single Solve specimen is an `ELF64`, little-endian `ET_EXEC` for `x86-64`. The section-name answer is the section table in order **including its initial empty name**. The symbol answer is the `.symtab` in order **excluding entries with empty names**; it still includes compiler and linker entries such as `crt1.o`. In the Single Solve file, that yields 28 section names and 33 symbol names.

The `recover_code` symbol is a six-byte `FUNC`. Disassembling only its bytes gives the exact instruction array `["mov eax,0x1fa4","ret"]` for Single Solve. The constant comes from the assigned bytes and must be extracted again for later attempts. `pyelftools` locates the symbol and its section; Capstone decodes the instruction bytes in execution order.

Identify the container from its bytes: `\x7fELF` maps to the answer `elf`, while `MZ` maps to `pe`. Do not infer the container from the challenge day or programming language. The Day 3 managed DLL is specifically `PE_CLI`; its PE machine field is `i386`, and the CLI metadata version in the Single Solve file is `v4.0.30319`. The Day 4 and Day 5 architecture answers for the successful attempts were `x86-64`.

Each later binary contains an `HCFG` block. The first 12 bytes are a four-byte magic, one-byte version, one-byte XOR key, a little-endian 16-bit payload length, and a little-endian CRC32. XOR the next `length` bytes with the key, verify the decoded bytes against that CRC32, and parse the resulting JSON. This recovers the campaign, domain, mutex, and URL fields without executing the specimens. The Day 3 questions use campaign, domain, and mutex; the other days also request the URL and CRC32. Day 2 additionally requests its XOR key. The Single Solve Day 2 key is `0x31`, and the decoded campaign is `BR02-000`.

Hash each **extracted file** for its `artifact_sha256` answer, rather than hashing the outer ZIP. Day 3 has two file-hash fields: one for the DLL and one for its `.runtimeconfig.json`. The outer ZIP hash verifies that the download matches the Game Master assignment.

The accepted labels are exact. `elf` is lowercase, `x86-64` uses a hyphen, `PE_CLI` is the compound managed-format token, and JSON arrays are compact strings with the original order preserved. The full question, format, and submitted-answer lists are in the per-mode reports below.

From the repository root, these commands inspect the saved Single Solve evidence:

```bash
sha256sum 05-Rust_Belt/evidence.zip
7z l -pinfected 05-Rust_Belt/evidence.zip
readelf -h -S -s 05-Rust_Belt/artifacts/single_solve/d01--variant-000.elf
objdump -d --disassemble=recover_code -Mintel 05-Rust_Belt/artifacts/single_solve/d01--variant-000.elf
```

`solve_time_trial.py` and `solve_mastery.py` implement the byte extraction and authenticated Game Master submission. They read `HUNTRESS_GM_TOKEN` from the environment; neither script prints or stores the token. Running either script starts a live timed attempt, and `solve_mastery.py --retry` renews an expired one.

| Mode | Verified Game Master result | Assigned ZIP SHA-256 | Returned flag | Full answer report |
| --- | --- | --- | --- | --- |
| Single Solve | `CORRECT`, 40/40 accepted | `6049e2c8cfdf9de77efbb58b283233edd7101bfb683b45a7f5277e5db4d3e117` | `b27a081db50950e5d5b4870c6ffe6bec` | Single Solve report (source reference: `artifacts/single_solve/report.md`; not linked in this draft) |
| Time Trial | `CORRECT`, 40/40 accepted | `bd4d4acc247c8b50a2f64ef899594809be85990962a27dfdc240666cdb3e9020` | `f302a9e80d10e1593f4628ef236b18be` | Time Trial report (source reference: `artifacts/time_trial/attempt-fb3d857c-67b4-454b-b928-f28c95bb5d9c/report.md`; not linked in this draft) |
| Mastery, delivery 1 | `CORRECT`, 80/80 accepted across both deliveries | `b596b79455848788997f36f390aec4710d511dc0b1f93038c5513351cd65ba98` | `620327ef66ac9a08382b60d9b8c45b3f` | Mastery report (source reference: `artifacts/mastery/attempt-9bf7f790-4620-421e-978a-bfa017ce7cd4/report.md`; not linked in this draft) |
| Mastery, delivery 2 | Same accepted Mastery attempt | `9046889d2654f5e1ebd1e72fe9832812a0181b82d66989b9d8996de7c2afa19c` | Same flag | Mastery report (source reference: `artifacts/mastery/attempt-9bf7f790-4620-421e-978a-bfa017ce7cd4/report.md`; not linked in this draft) |

The Time Trial attempt was `fb3d857c-67b4-454b-b928-f28c95bb5d9c`; its seven-second deadline was met. The successful Mastery attempt was `9bf7f790-4620-421e-978a-bfa017ce7cd4`, also under a seven-second deadline. The Game Master returned `CORRECT` in each mode; CourseStack points were not separately checked.

- Derive every answer from the currently assigned ZIP. Mastery delivers two ZIPs, and each `set1.` or `set2.` answer must come from its corresponding delivery.
- Preserve all section names, including the empty first entry, and preserve all nonempty symbol names in symbol-table order. Filtering to only interesting symbols fails the exact array check.
- Validate each decoded `HCFG` payload with its stored CRC32 before trusting the JSON or submitting its fields.
- A Mastery attempt expired before submission when its second delivery included PE variants for Days 2 and 4. The solver was extended to handle both PE and ELF containers; the retry returned new assigned material, which was downloaded and solved afresh. An expired timer is not evidence that a later retry will reuse the same bytes.
- Submit all fields using the exact `answer_ids` returned for that attempt. The successful timed attempts used one submission per bundle, and status checks confirmed 40/40 and 80/80 accepted fields respectively.

## Retained sources

- [early/05-Rust_Belt/readme.md](../../source-notes/early/05-Rust_Belt/readme.md)
