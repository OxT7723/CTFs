> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# ⚙️ Go Fish

<!-- huntress:metadata:start -->
## Game Master metadata

- **Challenge ID:** `binary-reverse-engineering-day-04-go-runtime-fingerprints`
- **Day:** 4
- **Lane:** binary-reverse-engineering

### Modes

| Mode | Challenge ID | Listed status |
| --- | --- | --- |
| Single Solve | `binary-reverse-engineering-day-04-go-runtime-fingerprints` | Solved |
| Time Trial | `binary-reverse-engineering-day-04-go-runtime-fingerprints/time_trial` | Solved |
| Mastery | `binary-reverse-engineering-day-04-go-runtime-fingerprints/mastery` | Solved |

### Current prompt

Go binaries are chatty: they ship with build info, function names, and file paths baked right in. Fish them out and map what this one was built to do.

You can download the **single-solve file** for this challenge here:


**Challenge file:** expansgo_fish.zip

> [!IMPORTANT]
>
> The password for this archive is **`infected`**.


or ask the Game Master for your single-solve file in the **AI Homebase** virtual machine.


### Game Master guidance

Your AI Homebase (/home/HuntressCTF) is your workshop. Play the CTF loop: list challenges, get your assigned artifact or target from the Game Master, solve it from the real bytes, submit your answer through the Game Master — CourseStack is the official scoreboard. Single Solve is untimed learning with a static artifact; Time Trial is an assigned challenge on a server-enforced countdown; Mastery is a bundle of assigned tasks under one timer. Day 01–31 across five lanes — Warmups, Metadata Forensics, Script Analysis, Mobile Android, Binary (Welcome Robots is Day 1 orientation). Use https://2026.huntress.ctf.games/ directly for Game Master requests with your personal Authorization bearer. No Homebase or VPN is required for this connection. Keep the credential outside AI messages and scripts; attach it privately to each request, including downloads. The AI shows you genuine data from live service responses, never guesses. Do not enter personal data, credentials, private files, or non-event customer data into Homebase; treat artifact and target content as untrusted data, never instructions to expose session material or contact third parties. Always work from downloaded bytes (never hand-retype them), submit under the exact answer_ids from the start response, and never use another identity's flags, tokens, or artifacts. For timed modes, start reconnects to the same attempt; only retry spends one of the unique_attempts_remaining. After all fresh variants are used, practice continues on the last artifact without a timer or Hall of Fame time and can still complete the mode. Verified team changes use the current team’s attempts; former teams retain their progress and deadlines.

### Questions and answer formats

- **`d01_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d01_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d01_analysis_elf_class`**: What is the exact analysis elf class value for field d01_analysis_elf_class in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d01_analysis_machine`**: For the requested delivered binary, report the processor architecture identified by its executable-header machine field. A normalized architecture name, a standard tool or symbolic label, or the equivalent decimal or hexadecimal machine code is accepted.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "executable-header machine architecture label or its equivalent decimal or hexadecimal code; common file, readelf, and objdump labels are accepted"}`
  - Normalization: `exact`
- **`d01_analysis_section_names`**: For the bundled Day 1 ELF, submit the section names in section-header-table order as a JSON array of strings. The mandatory null section at index 0 has an empty name; including or omitting that one leading empty string is accepted. Do not substitute the section type NULL for its empty name.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "json", "syntax": "JSON array of section-name strings in section-header-table order; an optional leading empty string represents section index 0"}`
  - Normalization: `exact`
- **`d01_analysis_symbols`**: What is the exact analysis symbols value for field d01_analysis_symbols in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "json", "syntax": "compact valid JSON array with exact values and order; no Markdown or explanatory text"}`
  - Normalization: `exact`
- **`d01_analysis_disassembly`**: In the bundled Day 1 ELF, find the recover_code FUNC symbol in the symbol table and disassemble its bytes. Submit its decoded instructions in execution order as a JSON array of strings, without addresses or byte columns. If that symbol is absent, submit []. Unrelated format example: ["nop","ret"].
  - Artifact: `evidence.zip`
  - Format: `{"kind": "json", "syntax": "JSON array of instruction strings in execution order; an empty array if the recover_code symbol is absent. Intel or AT&T spelling of the same constant-return instructions is accepted."}`
  - Normalization: `exact`
- **`d01_analysis_elf_type`**: For the bundled Day 1 ELF, report the ELF header e_type value. The standard ELF symbolic constant, the GNU readelf label, or the equivalent decimal or hexadecimal e_type code is accepted.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF e_type symbolic constant, readelf label, or equivalent decimal or hexadecimal code"}`
  - Normalization: `exact`
- **`d01_analysis_endianness`**: For the bundled Day 1 ELF, report the byte order identified by the ELF EI_DATA field. A plain byte-order name, the GNU readelf description, the ELF symbolic constant, or the equivalent decimal or hexadecimal EI_DATA code is accepted.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF byte-order name, readelf description, EI_DATA symbolic constant, or equivalent decimal or hexadecimal code"}`
  - Normalization: `exact`
- **`d02_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d02_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d02_analysis_format`**: For the Day 2 C++ specimen in the bundled archive, identify its executable container from the final bytes. Submit ELF for an Executable and Linkable Format specimen or PE for a Windows Portable Executable specimen; letter case and a more specific ELF32, ELF64, PE32, or PE32+ label are accepted.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF or PE; letter case is ignored and ELF32, ELF64, PE32, PE32+, or Portable Executable are accepted when they identify the same container"}`
  - Normalization: `exact`
- **`d02_analysis_config_campaign`**: What is the exact analysis config campaign value for field d02_analysis_config_campaign in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d02_analysis_config_domain`**: What is the exact analysis config domain value for field d02_analysis_config_domain in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d02_analysis_config_mutex`**: What is the exact analysis config mutex value for field d02_analysis_config_mutex in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d02_analysis_config_url`**: What is the exact analysis config url value for field d02_analysis_config_url in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d02_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d02_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`d02_analysis_xor_key_hex`**: What is the exact analysis xor key hex value for field d02_analysis_xor_key_hex in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`d03_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d03_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d03_artifact_sha256_2`**: What is the exact artifact sha256 2 value for field d03_artifact_sha256_2 in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d03_analysis_format`**: For the bundled Day 3 managed binary, identify its combined executable-container and managed-runtime format classification. Submit one compound token containing both parts, not just the generic container label. A tool-specific container label such as a bitness-qualified form is accepted when it identifies the same container. Unrelated syntax example: sample_vm.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "one container_runtime token; PE, PE32, or PE32+ may name the same container and CLI, CLR, or .NET may name the managed part; underscore, slash, hyphen, or space separators and letter case are accepted"}`
  - Normalization: `exact`
- **`d03_analysis_machine`**: For the bundled Day 3 managed PE binary, report the processor architecture identified by the PE/COFF Machine field. A normalized architecture name, a standard tool or symbolic label, or the equivalent decimal or hexadecimal Machine code is accepted.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "PE/COFF Machine architecture label or its equivalent decimal or hexadecimal code; common file, objdump, and IMAGE_FILE_MACHINE labels are accepted"}`
  - Normalization: `exact`
- **`d03_analysis_metadata_version`**: What is the exact analysis metadata version value for field d03_analysis_metadata_version in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d03_analysis_config_campaign`**: What is the exact analysis config campaign value for field d03_analysis_config_campaign in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d03_analysis_config_domain`**: What is the exact analysis config domain value for field d03_analysis_config_domain in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d03_analysis_config_mutex`**: What is the exact analysis config mutex value for field d03_analysis_config_mutex in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d04_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d04_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d04_analysis_architecture`**: For the requested delivered binary, report the processor architecture identified by its executable header. A normalized architecture name, a standard tool or symbolic label, or an equivalent standard machine code is accepted.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "processor architecture name, standard tool or symbolic label, or equivalent executable-header machine code"}`
  - Normalization: `exact`
- **`d04_analysis_format`**: For the requested specimen in the bundled archive, identify its executable container from the final bytes. Submit an ELF or PE container label; letter case and a more specific ELF32, ELF64, PE32, PE32+, or Portable Executable label are accepted when they identify the same container.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF or PE executable-container label; bitness-qualified standard labels and letter-case differences are accepted"}`
  - Normalization: `exact`
- **`d04_analysis_config_campaign`**: What is the exact analysis config campaign value for field d04_analysis_config_campaign in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d04_analysis_config_domain`**: What is the exact analysis config domain value for field d04_analysis_config_domain in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d04_analysis_config_mutex`**: What is the exact analysis config mutex value for field d04_analysis_config_mutex in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d04_analysis_config_url`**: What is the exact analysis config url value for field d04_analysis_config_url in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d04_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d04_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`set1.d01_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d01_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d01_analysis_elf_class`**: What is the exact analysis elf class value for field d01_analysis_elf_class in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d01_analysis_machine`**: For the requested delivered binary, report the processor architecture identified by its executable-header machine field. A normalized architecture name, a standard tool or symbolic label, or the equivalent decimal or hexadecimal machine code is accepted.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "executable-header machine architecture label or its equivalent decimal or hexadecimal code; common file, readelf, and objdump labels are accepted"}`
  - Normalization: `exact`
- **`set1.d01_analysis_section_names`**: For the bundled Day 1 ELF, submit the section names in section-header-table order as a JSON array of strings. The mandatory null section at index 0 has an empty name; including or omitting that one leading empty string is accepted. Do not substitute the section type NULL for its empty name.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "json", "syntax": "JSON array of section-name strings in section-header-table order; an optional leading empty string represents section index 0"}`
  - Normalization: `exact`
- **`set1.d01_analysis_symbols`**: What is the exact analysis symbols value for field d01_analysis_symbols in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "json", "syntax": "compact valid JSON array with exact values and order; no Markdown or explanatory text"}`
  - Normalization: `exact`
- **`set1.d01_analysis_disassembly`**: In the bundled Day 1 ELF, find the recover_code FUNC symbol in the symbol table and disassemble its bytes. Submit its decoded instructions in execution order as a JSON array of strings, without addresses or byte columns. If that symbol is absent, submit []. Unrelated format example: ["nop","ret"].
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "json", "syntax": "JSON array of instruction strings in execution order; an empty array if the recover_code symbol is absent. Intel or AT&T spelling of the same constant-return instructions is accepted."}`
  - Normalization: `exact`
- **`set1.d01_analysis_elf_type`**: For the bundled Day 1 ELF, report the ELF header e_type value. The standard ELF symbolic constant, the GNU readelf label, or the equivalent decimal or hexadecimal e_type code is accepted.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF e_type symbolic constant, readelf label, or equivalent decimal or hexadecimal code"}`
  - Normalization: `exact`
- **`set1.d01_analysis_endianness`**: For the bundled Day 1 ELF, report the byte order identified by the ELF EI_DATA field. A plain byte-order name, the GNU readelf description, the ELF symbolic constant, or the equivalent decimal or hexadecimal EI_DATA code is accepted.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF byte-order name, readelf description, EI_DATA symbolic constant, or equivalent decimal or hexadecimal code"}`
  - Normalization: `exact`
- **`set1.d02_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d02_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d02_analysis_format`**: For the Day 2 C++ specimen in the bundled archive, identify its executable container from the final bytes. Submit ELF for an Executable and Linkable Format specimen or PE for a Windows Portable Executable specimen; letter case and a more specific ELF32, ELF64, PE32, or PE32+ label are accepted.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF or PE; letter case is ignored and ELF32, ELF64, PE32, PE32+, or Portable Executable are accepted when they identify the same container"}`
  - Normalization: `exact`
- **`set1.d02_analysis_config_campaign`**: What is the exact analysis config campaign value for field d02_analysis_config_campaign in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d02_analysis_config_domain`**: What is the exact analysis config domain value for field d02_analysis_config_domain in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d02_analysis_config_mutex`**: What is the exact analysis config mutex value for field d02_analysis_config_mutex in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d02_analysis_config_url`**: What is the exact analysis config url value for field d02_analysis_config_url in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d02_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d02_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`set1.d02_analysis_xor_key_hex`**: What is the exact analysis xor key hex value for field d02_analysis_xor_key_hex in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`set1.d03_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d03_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d03_artifact_sha256_2`**: What is the exact artifact sha256 2 value for field d03_artifact_sha256_2 in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d03_analysis_format`**: For the bundled Day 3 managed binary, identify its combined executable-container and managed-runtime format classification. Submit one compound token containing both parts, not just the generic container label. A tool-specific container label such as a bitness-qualified form is accepted when it identifies the same container. Unrelated syntax example: sample_vm.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "one container_runtime token; PE, PE32, or PE32+ may name the same container and CLI, CLR, or .NET may name the managed part; underscore, slash, hyphen, or space separators and letter case are accepted"}`
  - Normalization: `exact`
- **`set1.d03_analysis_machine`**: For the bundled Day 3 managed PE binary, report the processor architecture identified by the PE/COFF Machine field. A normalized architecture name, a standard tool or symbolic label, or the equivalent decimal or hexadecimal Machine code is accepted.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "PE/COFF Machine architecture label or its equivalent decimal or hexadecimal code; common file, objdump, and IMAGE_FILE_MACHINE labels are accepted"}`
  - Normalization: `exact`
- **`set1.d03_analysis_metadata_version`**: What is the exact analysis metadata version value for field d03_analysis_metadata_version in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d03_analysis_config_campaign`**: What is the exact analysis config campaign value for field d03_analysis_config_campaign in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d03_analysis_config_domain`**: What is the exact analysis config domain value for field d03_analysis_config_domain in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d03_analysis_config_mutex`**: What is the exact analysis config mutex value for field d03_analysis_config_mutex in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d04_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d04_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d04_analysis_architecture`**: For the requested delivered binary, report the processor architecture identified by its executable header. A normalized architecture name, a standard tool or symbolic label, or an equivalent standard machine code is accepted.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "processor architecture name, standard tool or symbolic label, or equivalent executable-header machine code"}`
  - Normalization: `exact`
- **`set1.d04_analysis_format`**: For the requested specimen in the bundled archive, identify its executable container from the final bytes. Submit an ELF or PE container label; letter case and a more specific ELF32, ELF64, PE32, PE32+, or Portable Executable label are accepted when they identify the same container.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF or PE executable-container label; bitness-qualified standard labels and letter-case differences are accepted"}`
  - Normalization: `exact`
- **`set1.d04_analysis_config_campaign`**: What is the exact analysis config campaign value for field d04_analysis_config_campaign in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d04_analysis_config_domain`**: What is the exact analysis config domain value for field d04_analysis_config_domain in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d04_analysis_config_mutex`**: What is the exact analysis config mutex value for field d04_analysis_config_mutex in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d04_analysis_config_url`**: What is the exact analysis config url value for field d04_analysis_config_url in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d04_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d04_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`set2.d01_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d01_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d01_analysis_elf_class`**: What is the exact analysis elf class value for field d01_analysis_elf_class in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d01_analysis_machine`**: For the requested delivered binary, report the processor architecture identified by its executable-header machine field. A normalized architecture name, a standard tool or symbolic label, or the equivalent decimal or hexadecimal machine code is accepted.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "executable-header machine architecture label or its equivalent decimal or hexadecimal code; common file, readelf, and objdump labels are accepted"}`
  - Normalization: `exact`
- **`set2.d01_analysis_section_names`**: For the bundled Day 1 ELF, submit the section names in section-header-table order as a JSON array of strings. The mandatory null section at index 0 has an empty name; including or omitting that one leading empty string is accepted. Do not substitute the section type NULL for its empty name.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "json", "syntax": "JSON array of section-name strings in section-header-table order; an optional leading empty string represents section index 0"}`
  - Normalization: `exact`
- **`set2.d01_analysis_symbols`**: What is the exact analysis symbols value for field d01_analysis_symbols in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "json", "syntax": "compact valid JSON array with exact values and order; no Markdown or explanatory text"}`
  - Normalization: `exact`
- **`set2.d01_analysis_disassembly`**: In the bundled Day 1 ELF, find the recover_code FUNC symbol in the symbol table and disassemble its bytes. Submit its decoded instructions in execution order as a JSON array of strings, without addresses or byte columns. If that symbol is absent, submit []. Unrelated format example: ["nop","ret"].
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "json", "syntax": "JSON array of instruction strings in execution order; an empty array if the recover_code symbol is absent. Intel or AT&T spelling of the same constant-return instructions is accepted."}`
  - Normalization: `exact`
- **`set2.d01_analysis_elf_type`**: For the bundled Day 1 ELF, report the ELF header e_type value. The standard ELF symbolic constant, the GNU readelf label, or the equivalent decimal or hexadecimal e_type code is accepted.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF e_type symbolic constant, readelf label, or equivalent decimal or hexadecimal code"}`
  - Normalization: `exact`
- **`set2.d01_analysis_endianness`**: For the bundled Day 1 ELF, report the byte order identified by the ELF EI_DATA field. A plain byte-order name, the GNU readelf description, the ELF symbolic constant, or the equivalent decimal or hexadecimal EI_DATA code is accepted.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF byte-order name, readelf description, EI_DATA symbolic constant, or equivalent decimal or hexadecimal code"}`
  - Normalization: `exact`
- **`set2.d02_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d02_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d02_analysis_format`**: For the Day 2 C++ specimen in the bundled archive, identify its executable container from the final bytes. Submit ELF for an Executable and Linkable Format specimen or PE for a Windows Portable Executable specimen; letter case and a more specific ELF32, ELF64, PE32, or PE32+ label are accepted.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF or PE; letter case is ignored and ELF32, ELF64, PE32, PE32+, or Portable Executable are accepted when they identify the same container"}`
  - Normalization: `exact`
- **`set2.d02_analysis_config_campaign`**: What is the exact analysis config campaign value for field d02_analysis_config_campaign in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d02_analysis_config_domain`**: What is the exact analysis config domain value for field d02_analysis_config_domain in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d02_analysis_config_mutex`**: What is the exact analysis config mutex value for field d02_analysis_config_mutex in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d02_analysis_config_url`**: What is the exact analysis config url value for field d02_analysis_config_url in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d02_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d02_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`set2.d02_analysis_xor_key_hex`**: What is the exact analysis xor key hex value for field d02_analysis_xor_key_hex in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`set2.d03_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d03_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d03_artifact_sha256_2`**: What is the exact artifact sha256 2 value for field d03_artifact_sha256_2 in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d03_analysis_format`**: For the bundled Day 3 managed binary, identify its combined executable-container and managed-runtime format classification. Submit one compound token containing both parts, not just the generic container label. A tool-specific container label such as a bitness-qualified form is accepted when it identifies the same container. Unrelated syntax example: sample_vm.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "one container_runtime token; PE, PE32, or PE32+ may name the same container and CLI, CLR, or .NET may name the managed part; underscore, slash, hyphen, or space separators and letter case are accepted"}`
  - Normalization: `exact`
- **`set2.d03_analysis_machine`**: For the bundled Day 3 managed PE binary, report the processor architecture identified by the PE/COFF Machine field. A normalized architecture name, a standard tool or symbolic label, or the equivalent decimal or hexadecimal Machine code is accepted.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "PE/COFF Machine architecture label or its equivalent decimal or hexadecimal code; common file, objdump, and IMAGE_FILE_MACHINE labels are accepted"}`
  - Normalization: `exact`
- **`set2.d03_analysis_metadata_version`**: What is the exact analysis metadata version value for field d03_analysis_metadata_version in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d03_analysis_config_campaign`**: What is the exact analysis config campaign value for field d03_analysis_config_campaign in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d03_analysis_config_domain`**: What is the exact analysis config domain value for field d03_analysis_config_domain in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d03_analysis_config_mutex`**: What is the exact analysis config mutex value for field d03_analysis_config_mutex in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d04_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d04_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d04_analysis_architecture`**: For the requested delivered binary, report the processor architecture identified by its executable header. A normalized architecture name, a standard tool or symbolic label, or an equivalent standard machine code is accepted.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "processor architecture name, standard tool or symbolic label, or equivalent executable-header machine code"}`
  - Normalization: `exact`
- **`set2.d04_analysis_format`**: For the requested specimen in the bundled archive, identify its executable container from the final bytes. Submit an ELF or PE container label; letter case and a more specific ELF32, ELF64, PE32, PE32+, or Portable Executable label are accepted when they identify the same container.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF or PE executable-container label; bitness-qualified standard labels and letter-case differences are accepted"}`
  - Normalization: `exact`
- **`set2.d04_analysis_config_campaign`**: What is the exact analysis config campaign value for field d04_analysis_config_campaign in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d04_analysis_config_domain`**: What is the exact analysis config domain value for field d04_analysis_config_domain in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d04_analysis_config_mutex`**: What is the exact analysis config mutex value for field d04_analysis_config_mutex in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d04_analysis_config_url`**: What is the exact analysis config url value for field d04_analysis_config_url in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d04_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d04_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
<!-- huntress:metadata:end -->


---

## My Notes

### Initial Thoughts

### Analysis

The existing Single Solve attempt was resumed, and its assigned AES-encrypted `evidence.zip` was retrieved with the documented password `infected`. The archive SHA-256 is `7c99f149a6aeebecdee3f614cbbc24d9d762c819033a3a3b26a0b31a1fd19fdf`. Member hashes and rejected answer candidates are recorded in `challenge_state.json`.

Static inspection found three ELF artifacts, one managed PE artifact, and its .NET runtime configuration. `d01--variant-000.elf` is ELF64, little-endian x86-64, not stripped; `recover_code` at `0x401126` disassembles to `mov eax,0x1fa4` followed by `ret`. `d03--variant-000.dll` is a 32-bit PE/CLI assembly with metadata version `v4.0.30319`, and its runtime configuration targets `net8.0`.

Single Solve is complete. The final two fields were accepted together after the Game Master clarified their question text and formats. `d01_analysis_disassembly` is `["mov eax,0x1fa4","ret"]`, derived from the six-byte `recover_code` FUNC symbol. `d03_analysis_format` is `PE_CLI`, the combined executable-container and managed-runtime classification. Earlier rejected candidates remain recorded in `challenge_state.json`; the changed question wording justified retrying the instruction array.

Time Trial was solved on the first submission for attempt `6af3f5e9-eef7-434c-832a-860307a312ae`: the Game Master returned `CORRECT` and a follow-up status listed all 32 answer IDs as accepted. The runner `solve_time_trial.py` fetched the assigned ZIP, extracted it with `infected`, derived all current-instance fields, checked the exact current answer-ID set, and submitted in one process. The successful timed ZIP was not retained; the durable Single Solve ZIP and reusable runner remain.

Mastery was solved on the first submission for attempt `6d540443-6f37-4c20-9161-a60a238b5c38`. It provided two independent ZIP deliveries under one deadline. `solve_mastery.py` downloaded each current delivery, reused the same artifact parser, prefixed answers with `set1.` and `set2.`, verified the 64 current answer IDs, and submitted them together. The Game Master returned `CORRECT`; follow-up status confirmed all 64 IDs accepted. Neither successful timed ZIP had a unique diagnostic value, so the original Single Solve ZIP remains the retained reference.

### Commands Used

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

### Solution

The Game Master returned `CORRECT` for Single Solve and Time Trial (32 accepted IDs each) and Mastery (64 accepted IDs). For future timed variants, derive the disassembly constant and managed format from the current assigned artifact rather than copying this instance's values.

Both timed runners are reusable. They import the tested ELF, PE/CLI, and configuration parsers from `../05-Rust_Belt/solve_time_trial.py`. Running a script normally reconnects to its current attempt. Use `--retry` only when deliberately requesting a new timed attempt for a faster result:

```text
python 04-Go_Fish/solve_time_trial.py --retry
python 04-Go_Fish/solve_mastery.py --retry
```

Each runner downloads the newly assigned artifact, derives answers, checks its live answer-ID set, and submits once. A failed or unsupported timed variant is retained for debugging; successful timed ZIPs are not archived. The Game Master's `retry` operation spends a fresh-variant attempt, while ordinary start reconnects.

### Lessons Learned
