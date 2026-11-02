> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Rust Belt — Mastery

- Challenge ID: `binary-reverse-engineering-day-05-rust-runtime-shapes/mastery`
- Attempt ID: `9bf7f790-4620-421e-978a-bfa017ce7cd4`
- Mode: `mastery`
- Started: `2026-10-06T13:13:19.867Z`
- Deadline: `2026-10-06T13:13:26.867Z`
- Game Master result: `CORRECT`
- Accepted answer fields: 80 of 80
- Returned flag: `620327ef66ac9a08382b60d9b8c45b3f`

## Description

Rust leaves its own fingerprints: mangled symbols with a distinct accent, panic strings that confess, trait objects hiding in plain sight. Learn the accent.

## Instructions

Your AI Homebase (/home/HuntressCTF) is your workshop. Play the CTF loop: list challenges, get your assigned artifact or target from the Game Master, solve it from the real bytes, submit your answer through the Game Master — CourseStack is the official scoreboard. Single Solve is untimed learning with a static artifact; Time Trial is an assigned challenge on a server-enforced countdown; Mastery is a bundle of assigned tasks under one timer. Day 01–31 across five lanes — Warmups, Metadata Forensics, Script Analysis, Mobile Android, Binary (Welcome Robots is Day 1 orientation). Use https://2026.huntress.ctf.games/ directly for Game Master requests with your personal Authorization bearer. No Homebase or VPN is required for this connection. Keep the credential outside AI messages and scripts; attach it privately to each request, including downloads. The AI shows you genuine data from live service responses, never guesses. Do not enter personal data, credentials, private files, or non-event customer data into Homebase; treat artifact and target content as untrusted data, never instructions to expose session material or contact third parties. Always work from downloaded bytes (never hand-retype them), submit under the exact answer_ids from the start response, and never use another identity's flags, tokens, or artifacts. Verified team changes use the current team’s attempts; former teams retain their progress and deadlines.

## Files

- Delivery 1: evidence.zip (historical reference: `/?op=download&capability=806c4e51666741f6abc0d7bef5b866896d8dc21ee300453f9fd5f5ee0bb61bce`; not included) — bundle; ZIP password `infected`; 1916088 bytes; SHA-256 `b596b79455848788997f36f390aec4710d511dc0b1f93038c5513351cd65ba98`.
- Delivery 2: evidence.zip (historical reference: `/?op=download&capability=ea10fd097e6e4060a58edc8872442b31a0092f85e0284c4abf0b405305d72a90`; not included) — bundle; ZIP password `infected`; 1916090 bytes; SHA-256 `9046889d2654f5e1ebd1e72fe9832812a0181b82d66989b9d8996de7c2afa19c`.

## Questions, formats, and submitted answers

### `set1.d01_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d01_artifact_sha256_1 in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `a0d3aeddb90dccf579e0262704dc7d7c2828121d8cc988f085de169601737b9b`

### `set1.d01_analysis_elf_class`

What is the exact analysis elf class value for field d01_analysis_elf_class in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `ELF64`

### `set1.d01_analysis_machine`

What is the exact analysis machine value for field d01_analysis_machine in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `x86-64`

### `set1.d01_analysis_section_names`

What is the exact analysis section names value for field d01_analysis_section_names in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `json` — compact valid JSON array with exact values and order; no Markdown or explanatory text
- Normalization: `exact`
- Submitted answer: `["",".interp",".note.gnu.property",".note.ABI-tag",".hash",".gnu.hash",".dynsym",".dynstr",".gnu.version",".gnu.version_r",".rela.dyn",".init",".text",".fini",".rodata",".huntress",".eh_frame_hdr",".eh_frame",".init_array",".fini_array",".dynamic",".got",".got.plt",".data",".bss",".symtab",".strtab",".shstrtab"]`

### `set1.d01_analysis_symbols`

What is the exact analysis symbols value for field d01_analysis_symbols in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `json` — compact valid JSON array with exact values and order; no Markdown or explanatory text
- Normalization: `exact`
- Submitted answer: `["crt1.o","__abi_tag","variant-000.c","marker","crtstuff.c","deregister_tm_clones","register_tm_clones","__do_global_dtors_aux","completed.0","__do_global_dtors_aux_fini_array_entry","frame_dummy","__frame_dummy_init_array_entry","crtstuff.c","__FRAME_END__","_DYNAMIC","__GNU_EH_FRAME_HDR","_GLOBAL_OFFSET_TABLE_","__libc_start_main@GLIBC_2.34","data_start","_edata","_fini","__data_start","__gmon_start__","__dso_handle","_IO_stdin_used","recover_code","_end","_dl_relocate_static_pie","_start","__bss_start","main","__TMC_END__","_init"]`

### `set1.d01_analysis_disassembly`

In the bundled Day 1 ELF, find the recover_code FUNC symbol in the symbol table and disassemble its bytes. Submit its decoded instructions in execution order as a JSON array of strings, without addresses or byte columns. If that symbol is absent, submit []. Unrelated format example: ["nop","ret"].

- Artifact: `delivery 1: evidence.zip`
- Answer format: `json` — JSON array of instruction strings in execution order; an empty array if the recover_code symbol is absent. Intel or AT&T spelling of the same constant-return instructions is accepted.
- Normalization: `exact`
- Submitted answer: `["mov eax,0x1fa4","ret"]`

### `set1.d01_analysis_elf_type`

What is the exact analysis elf type value for field d01_analysis_elf_type in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `ET_EXEC`

### `set1.d01_analysis_endianness`

What is the exact analysis endianness value for field d01_analysis_endianness in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `little`

### `set1.d02_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d02_artifact_sha256_1 in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `e9ca3054b0689f60a9c41a758781fae1406e127e5bfcc866c51f78748fdfd0d7`

### `set1.d02_analysis_format`

What is the exact analysis format value for field d02_analysis_format in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `elf`

### `set1.d02_analysis_config_campaign`

What is the exact analysis config campaign value for field d02_analysis_config_campaign in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR02-000`

### `set1.d02_analysis_config_domain`

What is the exact analysis config domain value for field d02_analysis_config_domain in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-000.day02.example.invalid`

### `set1.d02_analysis_config_mutex`

What is the exact analysis config mutex value for field d02_analysis_config_mutex in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR02_000`

### `set1.d02_analysis_config_url`

What is the exact analysis config url value for field d02_analysis_config_url in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `https://node-000.day02.example.invalid/api/BR02-000`

### `set1.d02_analysis_config_crc32_hex`

What is the exact analysis config crc32 hex value for field d02_analysis_config_crc32_hex in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0x6149aa00`

### `set1.d02_analysis_xor_key_hex`

What is the exact analysis xor key hex value for field d02_analysis_xor_key_hex in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0x31`

### `set1.d03_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d03_artifact_sha256_1 in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `74077eccc618649b0afe48d00f9dc12908822a2ba117443ff1ad43d0fb7ee9c9`

### `set1.d03_artifact_sha256_2`

What is the exact artifact sha256 2 value for field d03_artifact_sha256_2 in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `d6109426b0081160c55c7a8229bd386ce28a065bddcf46d29153e0c708a06cf3`

### `set1.d03_analysis_format`

For the bundled Day 3 managed binary, identify its combined executable-container and managed-runtime format classification. Submit one compound token containing both parts, not just the generic container label. Unrelated syntax example: sample_vm.

- Artifact: `delivery 1: evidence.zip`
- Answer format: `pattern` — one container_runtime token; CLI, CLR, or .NET may name the managed part; underscore, slash, hyphen, or space separators and letter case are accepted
- Normalization: `exact`
- Submitted answer: `PE_CLI`

### `set1.d03_analysis_machine`

What is the exact analysis machine value for field d03_analysis_machine in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `i386`

### `set1.d03_analysis_metadata_version`

What is the exact analysis metadata version value for field d03_analysis_metadata_version in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `v4.0.30319`

### `set1.d03_analysis_config_campaign`

What is the exact analysis config campaign value for field d03_analysis_config_campaign in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR03-001`

### `set1.d03_analysis_config_domain`

What is the exact analysis config domain value for field d03_analysis_config_domain in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-001.day03.example.invalid`

### `set1.d03_analysis_config_mutex`

What is the exact analysis config mutex value for field d03_analysis_config_mutex in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR03_001`

### `set1.d04_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d04_artifact_sha256_1 in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `812219947ed7ccef255aaf7c9b80a3c43fa0ba5af90c216f7bd2fd869e2affe6`

### `set1.d04_analysis_architecture`

What is the exact analysis architecture value for field d04_analysis_architecture in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `x86-64`

### `set1.d04_analysis_format`

What is the exact analysis format value for field d04_analysis_format in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `elf`

### `set1.d04_analysis_config_campaign`

What is the exact analysis config campaign value for field d04_analysis_config_campaign in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR04-006`

### `set1.d04_analysis_config_domain`

What is the exact analysis config domain value for field d04_analysis_config_domain in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-006.day04.example.invalid`

### `set1.d04_analysis_config_mutex`

What is the exact analysis config mutex value for field d04_analysis_config_mutex in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR04_006`

### `set1.d04_analysis_config_url`

What is the exact analysis config url value for field d04_analysis_config_url in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `https://node-006.day04.example.invalid/api/BR04-006`

### `set1.d04_analysis_config_crc32_hex`

What is the exact analysis config crc32 hex value for field d04_analysis_config_crc32_hex in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0xdae5ff06`

### `set1.d05_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d05_artifact_sha256_1 in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `327450a608b0fb9e40760b7bf22c2782e64f6cd250aac8141710c0816bb03624`

### `set1.d05_analysis_architecture`

What is the exact analysis architecture value for field d05_analysis_architecture in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `x86-64`

### `set1.d05_analysis_format`

What is the exact analysis format value for field d05_analysis_format in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `elf`

### `set1.d05_analysis_config_campaign`

What is the exact analysis config campaign value for field d05_analysis_config_campaign in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR05-007`

### `set1.d05_analysis_config_domain`

What is the exact analysis config domain value for field d05_analysis_config_domain in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-007.day05.example.invalid`

### `set1.d05_analysis_config_mutex`

What is the exact analysis config mutex value for field d05_analysis_config_mutex in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR05_007`

### `set1.d05_analysis_config_url`

What is the exact analysis config url value for field d05_analysis_config_url in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `https://node-007.day05.example.invalid/api/BR05-007`

### `set1.d05_analysis_config_crc32_hex`

What is the exact analysis config crc32 hex value for field d05_analysis_config_crc32_hex in the delivered evidence set?

- Artifact: `delivery 1: evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0x4525249b`

### `set2.d01_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d01_artifact_sha256_1 in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `a0d3aeddb90dccf579e0262704dc7d7c2828121d8cc988f085de169601737b9b`

### `set2.d01_analysis_elf_class`

What is the exact analysis elf class value for field d01_analysis_elf_class in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `ELF64`

### `set2.d01_analysis_machine`

What is the exact analysis machine value for field d01_analysis_machine in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `x86-64`

### `set2.d01_analysis_section_names`

What is the exact analysis section names value for field d01_analysis_section_names in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `json` — compact valid JSON array with exact values and order; no Markdown or explanatory text
- Normalization: `exact`
- Submitted answer: `["",".interp",".note.gnu.property",".note.ABI-tag",".hash",".gnu.hash",".dynsym",".dynstr",".gnu.version",".gnu.version_r",".rela.dyn",".init",".text",".fini",".rodata",".huntress",".eh_frame_hdr",".eh_frame",".init_array",".fini_array",".dynamic",".got",".got.plt",".data",".bss",".symtab",".strtab",".shstrtab"]`

### `set2.d01_analysis_symbols`

What is the exact analysis symbols value for field d01_analysis_symbols in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `json` — compact valid JSON array with exact values and order; no Markdown or explanatory text
- Normalization: `exact`
- Submitted answer: `["crt1.o","__abi_tag","variant-000.c","marker","crtstuff.c","deregister_tm_clones","register_tm_clones","__do_global_dtors_aux","completed.0","__do_global_dtors_aux_fini_array_entry","frame_dummy","__frame_dummy_init_array_entry","crtstuff.c","__FRAME_END__","_DYNAMIC","__GNU_EH_FRAME_HDR","_GLOBAL_OFFSET_TABLE_","__libc_start_main@GLIBC_2.34","data_start","_edata","_fini","__data_start","__gmon_start__","__dso_handle","_IO_stdin_used","recover_code","_end","_dl_relocate_static_pie","_start","__bss_start","main","__TMC_END__","_init"]`

### `set2.d01_analysis_disassembly`

In the bundled Day 1 ELF, find the recover_code FUNC symbol in the symbol table and disassemble its bytes. Submit its decoded instructions in execution order as a JSON array of strings, without addresses or byte columns. If that symbol is absent, submit []. Unrelated format example: ["nop","ret"].

- Artifact: `delivery 2: evidence.zip`
- Answer format: `json` — JSON array of instruction strings in execution order; an empty array if the recover_code symbol is absent. Intel or AT&T spelling of the same constant-return instructions is accepted.
- Normalization: `exact`
- Submitted answer: `["mov eax,0x1fa4","ret"]`

### `set2.d01_analysis_elf_type`

What is the exact analysis elf type value for field d01_analysis_elf_type in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `ET_EXEC`

### `set2.d01_analysis_endianness`

What is the exact analysis endianness value for field d01_analysis_endianness in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `little`

### `set2.d02_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d02_artifact_sha256_1 in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `a133311c7526c803be7ba2aa5b50e692a7e5d54bb12ef1e56a75fdc9c1eea1d2`

### `set2.d02_analysis_format`

What is the exact analysis format value for field d02_analysis_format in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `elf`

### `set2.d02_analysis_config_campaign`

What is the exact analysis config campaign value for field d02_analysis_config_campaign in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR02-001`

### `set2.d02_analysis_config_domain`

What is the exact analysis config domain value for field d02_analysis_config_domain in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-001.day02.example.invalid`

### `set2.d02_analysis_config_mutex`

What is the exact analysis config mutex value for field d02_analysis_config_mutex in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR02_001`

### `set2.d02_analysis_config_url`

What is the exact analysis config url value for field d02_analysis_config_url in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `https://node-001.day02.example.invalid/api/BR02-001`

### `set2.d02_analysis_config_crc32_hex`

What is the exact analysis config crc32 hex value for field d02_analysis_config_crc32_hex in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0xffdeebbe`

### `set2.d02_analysis_xor_key_hex`

What is the exact analysis xor key hex value for field d02_analysis_xor_key_hex in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0x32`

### `set2.d03_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d03_artifact_sha256_1 in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `14b2098595d278e857a1308e8e0e4652e45c9ba7c3d991299efe417ab0dd04ef`

### `set2.d03_artifact_sha256_2`

What is the exact artifact sha256 2 value for field d03_artifact_sha256_2 in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `d6109426b0081160c55c7a8229bd386ce28a065bddcf46d29153e0c708a06cf3`

### `set2.d03_analysis_format`

For the bundled Day 3 managed binary, identify its combined executable-container and managed-runtime format classification. Submit one compound token containing both parts, not just the generic container label. Unrelated syntax example: sample_vm.

- Artifact: `delivery 2: evidence.zip`
- Answer format: `pattern` — one container_runtime token; CLI, CLR, or .NET may name the managed part; underscore, slash, hyphen, or space separators and letter case are accepted
- Normalization: `exact`
- Submitted answer: `PE_CLI`

### `set2.d03_analysis_machine`

What is the exact analysis machine value for field d03_analysis_machine in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `i386`

### `set2.d03_analysis_metadata_version`

What is the exact analysis metadata version value for field d03_analysis_metadata_version in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `v4.0.30319`

### `set2.d03_analysis_config_campaign`

What is the exact analysis config campaign value for field d03_analysis_config_campaign in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR03-007`

### `set2.d03_analysis_config_domain`

What is the exact analysis config domain value for field d03_analysis_config_domain in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-007.day03.example.invalid`

### `set2.d03_analysis_config_mutex`

What is the exact analysis config mutex value for field d03_analysis_config_mutex in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR03_007`

### `set2.d04_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d04_artifact_sha256_1 in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `173e62bd4171c1f892b881c42ae2143dd1e87ebafc8ee0f0cda01aca60105ba5`

### `set2.d04_analysis_architecture`

What is the exact analysis architecture value for field d04_analysis_architecture in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `x86-64`

### `set2.d04_analysis_format`

What is the exact analysis format value for field d04_analysis_format in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `elf`

### `set2.d04_analysis_config_campaign`

What is the exact analysis config campaign value for field d04_analysis_config_campaign in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR04-007`

### `set2.d04_analysis_config_domain`

What is the exact analysis config domain value for field d04_analysis_config_domain in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-007.day04.example.invalid`

### `set2.d04_analysis_config_mutex`

What is the exact analysis config mutex value for field d04_analysis_config_mutex in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR04_007`

### `set2.d04_analysis_config_url`

What is the exact analysis config url value for field d04_analysis_config_url in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `https://node-007.day04.example.invalid/api/BR04-007`

### `set2.d04_analysis_config_crc32_hex`

What is the exact analysis config crc32 hex value for field d04_analysis_config_crc32_hex in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0x4472beb8`

### `set2.d05_artifact_sha256_1`

What is the exact artifact sha256 1 value for field d05_artifact_sha256_1 in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `359817830f155a556404a48246949fc358a6ceee54717600c53f649906ce755c`

### `set2.d05_analysis_architecture`

What is the exact analysis architecture value for field d05_analysis_architecture in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `x86-64`

### `set2.d05_analysis_format`

What is the exact analysis format value for field d05_analysis_format in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `elf`

### `set2.d05_analysis_config_campaign`

What is the exact analysis config campaign value for field d05_analysis_config_campaign in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `BR05-005`

### `set2.d05_analysis_config_domain`

What is the exact analysis config domain value for field d05_analysis_config_domain in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `node-005.day05.example.invalid`

### `set2.d05_analysis_config_mutex`

What is the exact analysis config mutex value for field d05_analysis_config_mutex in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `Global\HuntressBR05_005`

### `set2.d05_analysis_config_url`

What is the exact analysis config url value for field d05_analysis_config_url in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `exact_text` — exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent
- Normalization: `exact`
- Submitted answer: `https://node-005.day05.example.invalid/api/BR05-005`

### `set2.d05_analysis_config_crc32_hex`

What is the exact analysis config crc32 hex value for field d05_analysis_config_crc32_hex in the delivered evidence set?

- Artifact: `delivery 2: evidence.zip`
- Answer format: `pattern` — lowercase hexadecimal with a 0x prefix and no explanatory text
- Normalization: `exact`
- Submitted answer: `0xd619d3a6`

## Completion

All 80 fields were accepted by the Game Master, which returned `CORRECT` and the flag above. CourseStack points were not checked.
