# Go Fish

Day 4 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `binary-reverse-engineering-day-04-go-runtime-fingerprints`

## Earlier local account

---

The existing Single Solve attempt was resumed, and its assigned AES-encrypted `evidence.zip` was retrieved with the documented password `infected`. The archive SHA-256 is `7c99f149a6aeebecdee3f614cbbc24d9d762c819033a3a3b26a0b31a1fd19fdf`. Member hashes and rejected answer candidates are recorded in `challenge_state.json`.

Static inspection found three ELF artifacts, one managed PE artifact, and its .NET runtime configuration. `d01--variant-000.elf` is ELF64, little-endian x86-64, not stripped; `recover_code` at `0x401126` disassembles to `mov eax,0x1fa4` followed by `ret`. `d03--variant-000.dll` is a 32-bit PE/CLI assembly with metadata version `v4.0.30319`, and its runtime configuration targets `net8.0`.

Single Solve is complete. The final two fields were accepted together after the Game Master clarified their question text and formats. `d01_analysis_disassembly` is `["mov eax,0x1fa4","ret"]`, derived from the six-byte `recover_code` FUNC symbol. `d03_analysis_format` is `PE_CLI`, the combined executable-container and managed-runtime classification. Earlier rejected candidates remain recorded in `challenge_state.json`; the changed question wording justified retrying the instruction array.

Time Trial was solved on the first submission for attempt `6af3f5e9-eef7-434c-832a-860307a312ae`: the Game Master returned `CORRECT` and a follow-up status listed all 32 answer IDs as accepted. The runner `solve_time_trial.py` fetched the assigned ZIP, extracted it with `infected`, derived all current-instance fields, checked the exact current answer-ID set, and submitted in one process. The successful timed ZIP was not retained; the durable Single Solve ZIP and reusable runner remain.

Mastery was solved on the first submission for attempt `6d540443-6f37-4c20-9161-a60a238b5c38`. It provided two independent ZIP deliveries under one deadline. `solve_mastery.py` downloaded each current delivery, reused the same artifact parser, prefixed answers with `set1.` and `set2.`, verified the 64 current answer IDs, and submitted them together. The Game Master returned `CORRECT`; follow-up status confirmed all 64 IDs accepted. Neither successful timed ZIP had a unique diagnostic value, so the original Single Solve ZIP remains the retained reference.

```text
sha256sum artifacts/single_solve/evidence.zip
7z t -pinfected artifacts/single_solve/evidence.zip
7z x -y -pinfected -o/tmp/huntress-d4-gofish artifacts/single_solve/evidence.zip
sha256sum /tmp/huntress-d4-gofish/*
file /tmp/huntress-d4-gofish/*
readelf -h -S -s /tmp/huntress-d4-gofish/d01--variant-000.elf
objdump -d -M intel --no-show-raw-insn /tmp/huntress-d4-gofish/d01--variant-000.elf
strings -a /tmp/huntress-d4-gofish/d03--variant-000.dll
```

The Game Master returned `CORRECT` for Single Solve and Time Trial (32 accepted IDs each) and Mastery (64 accepted IDs). For future timed variants, derive the disassembly constant and managed format from the current assigned artifact rather than copying this instance's values.

Both timed runners are reusable. They import the tested ELF, PE/CLI, and configuration parsers from `../05-Rust_Belt/solve_time_trial.py`. Running a script normally reconnects to its current attempt. Use `--retry` only when deliberately requesting a new timed attempt for a faster result:

```text
python 04-Go_Fish/solve_time_trial.py --retry
python 04-Go_Fish/solve_mastery.py --retry
```

Each runner downloads the newly assigned artifact, derives answers, checks its live answer-ID set, and submits once. A failed or unsupported timed variant is retained for debugging; successful timed ZIPs are not archived. The Game Master's `retry` operation spends a fresh-variant attempt, while ordinary start reconnects.

## Retained sources

- [early/04-Go_Fish/readme.md](../../source-notes/early/04-Go_Fish/readme.md)
