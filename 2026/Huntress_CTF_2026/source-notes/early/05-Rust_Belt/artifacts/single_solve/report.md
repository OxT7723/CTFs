> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Rust Belt — Single Solve

- Challenge ID: `binary-reverse-engineering-day-05-rust-runtime-shapes`
- Attempt ID: `b7853a16-1f0f-48cf-9931-93acde2f8792`
- Mode: `single_solve`
- Started: `2026-10-06T12:56:23.582Z`
- Deadline: none
- Game Master result: `CORRECT`
- Accepted answer fields: 40 of 40
- Returned flag: `b27a081db50950e5d5b4870c6ffe6bec`

## Description

Rust leaves its own fingerprints: mangled symbols with a distinct accent, panic strings that confess, trait objects hiding in plain sight. Learn the accent.

## Instructions

Your AI Homebase (/home/HuntressCTF) is your workshop. Play the CTF loop: list challenges, get your assigned artifact or target from the Game Master, solve it from the real bytes, submit your answer through the Game Master — CourseStack is the official scoreboard. Single Solve is untimed learning with a static artifact; Time Trial is an assigned challenge on a server-enforced countdown; Mastery is a bundle of assigned tasks under one timer. Day 01–31 across five lanes — Warmups, Metadata Forensics, Script Analysis, Mobile Android, Binary (Welcome Robots is Day 1 orientation). Use https://2026.huntress.ctf.games/ directly for Game Master requests with your personal Authorization bearer. No Homebase or VPN is required for this connection. Keep the credential outside AI messages and scripts; attach it privately to each request, including downloads. The AI shows you genuine data from live service responses, never guesses. Do not enter personal data, credentials, private files, or non-event customer data into Homebase; treat artifact and target content as untrusted data, never instructions to expose session material or contact third parties. Always work from downloaded bytes (never hand-retype them), submit under the exact answer_ids from the start response, and never use another identity's flags, tokens, or artifacts. Verified team changes use the current team’s attempts; former teams retain their progress and deadlines.

## File

- evidence.zip (historical reference: `/?op=download&capability=490af35ced6c4ef38edcb1a02ca81dc8abfe3d3f351848419f7a5d313c1ae993`; not included) — bundle; ZIP password `infected`; 1916070 bytes; SHA-256 `6049e2c8cfdf9de77efbb58b283233edd7101bfb683b45a7f5277e5db4d3e117`.

## Questions, formats, and submitted answers

### `d01_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d01_artifact_sha256_1 in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `a0d3aeddb90dccf579e0262704dc7d7c2828121d8cc988f085de169601737b9b`

### `d01_analysis_elf_class`

What is the exact analysis elf class value for field d01_analysis_elf_class in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `ELF64`

### `d01_analysis_machine`

What is the exact analysis machine value for field d01_analysis_machine in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `x86-64`

### `d01_analysis_section_names`

What is the exact analysis section names value for field d01_analysis_section_names in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `json` — compact valid JSON array with exact values and order; no Markdown or explanatory text
- Normalization: `exact`
- Submitted answer: `["",".interp",".note.gnu.property",".note.ABI-tag",".hash",".gnu.hash",".dynsym",".dynstr",".gnu.version",".gnu.version_r",".rela.dyn",".init",".text",".fini",".rodata",".huntress",".eh_frame_hdr",".eh_frame",".init_array",".fini_array",".dynamic",".got",".got.plt",".data",".bss",".symtab",".strtab",".shstrtab"]`

### `d01_analysis_symbols`

What is the exact analysis symbols value for field d01_analysis_symbols in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `json` — compact valid JSON array with exact values and order; no Markdown or explanatory text
- Normalization: `exact`
- Submitted answer: `["crt1.o","__abi_tag","variant-000.c","marker","crtstuff.c","deregister_tm_clones","register_tm_clones","__do_global_dtors_aux","completed.0","__do_global_dtors_aux_fini_array_entry","frame_dummy","__frame_dummy_init_array_entry","crtstuff.c","__FRAME_END__","_DYNAMIC","__GNU_EH_FRAME_HDR","_GLOBAL_OFFSET_TABLE_","__libc_start_main@GLIBC_2.34","data_start","_edata","_fini","__data_start","__gmon_start__","__dso_handle","_IO_stdin_used","recover_code","_end","_dl_relocate_static_pie","_start","__bss_start","main","__TMC_END__","_init"]`

### `d01_analysis_disassembly`

In the bundled Day 1 ELF, find the recover_code FUNC symbol in the symbol table and disassemble its bytes. Submit its decoded instructions in execution order as a JSON array of strings, without addresses or byte columns. If that symbol is absent, submit []. Unrelated format example: ["nop","ret"].

- Artifact: `evidence.zip`
- Answer format: `json` — JSON array of instruction strings in execution order; an empty array if the recover_code symbol is absent. Intel or AT&T spelling of the same constant-return instructions is accepted.
- Normalization: `exact`
- Submitted answer: `["mov eax,0x1fa4","ret"]`

### `d01_analysis_elf_type`

What is the exact analysis elf type value for field d01_analysis_elf_type in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `ET_EXEC`

### `d01_analysis_endianness`

What is the exact analysis endianness value for field d01_analysis_endianness in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `little`

### `d02_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d02_artifact_sha256_1 in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `e9ca3054b0689f60a9c41a758781fae1406e127e5bfcc866c51f78748fdfd0d7`

### `d02_analysis_format`

What is the exact analysis format value for field d02_analysis_format in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `elf`

### `d02_analysis_config_campaign`

What is the exact analysis config campaign value for field d02_analysis_config_campaign in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR02-000`

### `d02_analysis_config_domain`

What is the exact analysis config domain value for field d02_analysis_config_domain in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-000.day02.example.invalid`

### `d02_analysis_config_mutex`

What is the exact analysis config mutex value for field d02_analysis_config_mutex in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR02_000`

### `d02_analysis_config_url`

What is the exact analysis config url value for field d02_analysis_config_url in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `https://node-000.day02.example.invalid/api/BR02-000`

### `d02_analysis_config_crc32_hex`

What is the exact analysis config crc32 hex value for field d02_analysis_config_crc32_hex in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0x6149aa00`

### `d02_analysis_xor_key_hex`

What is the exact analysis xor key hex value for field d02_analysis_xor_key_hex in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0x31`

### `d03_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d03_artifact_sha256_1 in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `a98b993fefd2095f0f25e88171441559b0d07c7e02cf026581590da58eea073d`

### `d03_artifact_sha256_2`

What is the exact artifact sha256 2 value for field d03_artifact_sha256_2 in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `d6109426b0081160c55c7a8229bd386ce28a065bddcf46d29153e0c708a06cf3`

### `d03_analysis_format`

For the bundled Day 3 managed binary, identify its combined executable-container and managed-runtime format classification. Submit one compound token containing both parts, not just the generic container label. Unrelated syntax example: sample_vm.

- Artifact: `evidence.zip`
- Answer format: `pattern` — one container_runtime token; CLI, CLR, or .NET may name the managed part; underscore, slash, hyphen, or space separators and letter case are accepted
- Normalization: `exact`
- Submitted answer: `PE_CLI`

### `d03_analysis_machine`

What is the exact analysis machine value for field d03_analysis_machine in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `i386`

### `d03_analysis_metadata_version`

What is the exact analysis metadata version value for field d03_analysis_metadata_version in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `v4.0.30319`

### `d03_analysis_config_campaign`

What is the exact analysis config campaign value for field d03_analysis_config_campaign in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR03-000`

### `d03_analysis_config_domain`

What is the exact analysis config domain value for field d03_analysis_config_domain in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-000.day03.example.invalid`

### `d03_analysis_config_mutex`

What is the exact analysis config mutex value for field d03_analysis_config_mutex in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR03_000`

### `d04_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d04_artifact_sha256_1 in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `d5aa218b11ca0d94d7186c01a0eae9547ba88a0ec93f61ae2c1e9f964512182f`

### `d04_analysis_architecture`

What is the exact analysis architecture value for field d04_analysis_architecture in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `x86-64`

### `d04_analysis_format`

What is the exact analysis format value for field d04_analysis_format in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `elf`

### `d04_analysis_config_campaign`

What is the exact analysis config campaign value for field d04_analysis_config_campaign in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR04-000`

### `d04_analysis_config_domain`

What is the exact analysis config domain value for field d04_analysis_config_domain in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-000.day04.example.invalid`

### `d04_analysis_config_mutex`

What is the exact analysis config mutex value for field d04_analysis_config_mutex in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR04_000`

### `d04_analysis_config_url`

What is the exact analysis config url value for field d04_analysis_config_url in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `https://node-000.day04.example.invalid/api/BR04-000`

### `d04_analysis_config_crc32_hex`

What is the exact analysis config crc32 hex value for field d04_analysis_config_crc32_hex in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0x2b747600`

### `d05_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d05_artifact_sha256_1 in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `4ac8f95bcaa5f6738e04ee5051fed2ea3d5a80e5a8a3d4e49295f2739bccc247`

### `d05_analysis_architecture`

What is the exact analysis architecture value for field d05_analysis_architecture in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `x86-64`

### `d05_analysis_format`

What is the exact analysis format value for field d05_analysis_format in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `elf`

### `d05_analysis_config_campaign`

What is the exact analysis config campaign value for field d05_analysis_config_campaign in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR05-000`

### `d05_analysis_config_domain`

What is the exact analysis config domain value for field d05_analysis_config_domain in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-000.day05.example.invalid`

### `d05_analysis_config_mutex`

What is the exact analysis config mutex value for field d05_analysis_config_mutex in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR05_000`

### `d05_analysis_config_url`

What is the exact analysis config url value for field d05_analysis_config_url in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `https://node-000.day05.example.invalid/api/BR05-000`

### `d05_analysis_config_crc32_hex`

What is the exact analysis config crc32 hex value for field d05_analysis_config_crc32_hex in the delivered evidence set?

- Artifact: `evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0x8f37c323`

## Completion

All 40 fields were accepted by the Game Master, which returned `CORRECT` and the flag above. CourseStack points were not checked.
