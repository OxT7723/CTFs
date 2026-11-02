> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# ⚙️ Pool Party

<!-- huntress:metadata:start -->
## Game Master metadata

- **Challenge ID:** `binary-reverse-engineering-day-06-java-bytecode-loader`
- **Day:** 6
- **Lane:** binary-reverse-engineering

### Modes

| Mode | Challenge ID | Listed status |
| --- | --- | --- |
| Single Solve | `binary-reverse-engineering-day-06-java-bytecode-loader` | Solved |
| Time Trial | `binary-reverse-engineering-day-06-java-bytecode-loader/time_trial` | Solved |
| Mastery | `binary-reverse-engineering-day-06-java-bytecode-loader/mastery` | Solved |

### Current prompt

Every Java class file carries its own phone book: the constant pool. Names, methods, invocations — it's all in there. Dive in and take attendance.

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
- **`d05_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d05_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d05_analysis_architecture`**: For the requested delivered binary, report the processor architecture identified by its executable header. A normalized architecture name, a standard tool or symbolic label, or an equivalent standard machine code is accepted.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "processor architecture name, standard tool or symbolic label, or equivalent executable-header machine code"}`
  - Normalization: `exact`
- **`d05_analysis_format`**: For the requested specimen in the bundled archive, identify its executable container from the final bytes. Submit an ELF or PE container label; letter case and a more specific ELF32, ELF64, PE32, PE32+, or Portable Executable label are accepted when they identify the same container.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF or PE executable-container label; bitness-qualified standard labels and letter-case differences are accepted"}`
  - Normalization: `exact`
- **`d05_analysis_config_campaign`**: What is the exact analysis config campaign value for field d05_analysis_config_campaign in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d05_analysis_config_domain`**: What is the exact analysis config domain value for field d05_analysis_config_domain in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d05_analysis_config_mutex`**: What is the exact analysis config mutex value for field d05_analysis_config_mutex in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d05_analysis_config_url`**: What is the exact analysis config url value for field d05_analysis_config_url in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d05_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d05_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`d06_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d06_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d06_analysis_format`**: For the requested Java specimen in the bundled archive, identify its archive container from the final bytes. Standard JAR, Java archive, and Java-archive MIME labels are accepted.
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "JAR, Java archive, Java Archive (JAR), or application/java-archive"}`
  - Normalization: `exact`
- **`d06_analysis_config_campaign`**: What is the exact analysis config campaign value for field d06_analysis_config_campaign in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d06_analysis_config_domain`**: What is the exact analysis config domain value for field d06_analysis_config_domain in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d06_analysis_config_mutex`**: What is the exact analysis config mutex value for field d06_analysis_config_mutex in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d06_analysis_config_url`**: What is the exact analysis config url value for field d06_analysis_config_url in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`d06_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d06_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`d06_analysis_hcfg_version`**: What is the exact analysis hcfg version value for field d06_analysis_hcfg_version in the delivered evidence set?
  - Artifact: `evidence.zip`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
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
- **`set1.d05_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d05_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d05_analysis_architecture`**: For the requested delivered binary, report the processor architecture identified by its executable header. A normalized architecture name, a standard tool or symbolic label, or an equivalent standard machine code is accepted.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "processor architecture name, standard tool or symbolic label, or equivalent executable-header machine code"}`
  - Normalization: `exact`
- **`set1.d05_analysis_format`**: For the requested specimen in the bundled archive, identify its executable container from the final bytes. Submit an ELF or PE container label; letter case and a more specific ELF32, ELF64, PE32, PE32+, or Portable Executable label are accepted when they identify the same container.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF or PE executable-container label; bitness-qualified standard labels and letter-case differences are accepted"}`
  - Normalization: `exact`
- **`set1.d05_analysis_config_campaign`**: What is the exact analysis config campaign value for field d05_analysis_config_campaign in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d05_analysis_config_domain`**: What is the exact analysis config domain value for field d05_analysis_config_domain in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d05_analysis_config_mutex`**: What is the exact analysis config mutex value for field d05_analysis_config_mutex in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d05_analysis_config_url`**: What is the exact analysis config url value for field d05_analysis_config_url in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d05_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d05_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`set1.d06_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d06_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d06_analysis_format`**: For the requested Java specimen in the bundled archive, identify its archive container from the final bytes. Standard JAR, Java archive, and Java-archive MIME labels are accepted.
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "JAR, Java archive, Java Archive (JAR), or application/java-archive"}`
  - Normalization: `exact`
- **`set1.d06_analysis_config_campaign`**: What is the exact analysis config campaign value for field d06_analysis_config_campaign in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d06_analysis_config_domain`**: What is the exact analysis config domain value for field d06_analysis_config_domain in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d06_analysis_config_mutex`**: What is the exact analysis config mutex value for field d06_analysis_config_mutex in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d06_analysis_config_url`**: What is the exact analysis config url value for field d06_analysis_config_url in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set1.d06_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d06_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`set1.d06_analysis_hcfg_version`**: What is the exact analysis hcfg version value for field d06_analysis_hcfg_version in the delivered evidence set?
  - Artifact: `delivery 1: evidence.zip`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
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
- **`set2.d05_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d05_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d05_analysis_architecture`**: For the requested delivered binary, report the processor architecture identified by its executable header. A normalized architecture name, a standard tool or symbolic label, or an equivalent standard machine code is accepted.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "processor architecture name, standard tool or symbolic label, or equivalent executable-header machine code"}`
  - Normalization: `exact`
- **`set2.d05_analysis_format`**: For the requested specimen in the bundled archive, identify its executable container from the final bytes. Submit an ELF or PE container label; letter case and a more specific ELF32, ELF64, PE32, PE32+, or Portable Executable label are accepted when they identify the same container.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "ELF or PE executable-container label; bitness-qualified standard labels and letter-case differences are accepted"}`
  - Normalization: `exact`
- **`set2.d05_analysis_config_campaign`**: What is the exact analysis config campaign value for field d05_analysis_config_campaign in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d05_analysis_config_domain`**: What is the exact analysis config domain value for field d05_analysis_config_domain in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d05_analysis_config_mutex`**: What is the exact analysis config mutex value for field d05_analysis_config_mutex in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d05_analysis_config_url`**: What is the exact analysis config url value for field d05_analysis_config_url in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d05_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d05_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`set2.d06_artifact_sha256_1`**: What is the exact artifact sha256 1 value for field d06_artifact_sha256_1 in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d06_analysis_format`**: For the requested Java specimen in the bundled archive, identify its archive container from the final bytes. Standard JAR, Java archive, and Java-archive MIME labels are accepted.
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "JAR, Java archive, Java Archive (JAR), or application/java-archive"}`
  - Normalization: `exact`
- **`set2.d06_analysis_config_campaign`**: What is the exact analysis config campaign value for field d06_analysis_config_campaign in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d06_analysis_config_domain`**: What is the exact analysis config domain value for field d06_analysis_config_domain in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d06_analysis_config_mutex`**: What is the exact analysis config mutex value for field d06_analysis_config_mutex in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d06_analysis_config_url`**: What is the exact analysis config url value for field d06_analysis_config_url in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `exact`
- **`set2.d06_analysis_config_crc32_hex`**: What is the exact analysis config crc32 hex value for field d06_analysis_config_crc32_hex in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `exact`
- **`set2.d06_analysis_hcfg_version`**: What is the exact analysis hcfg version value for field d06_analysis_hcfg_version in the delivered evidence set?
  - Artifact: `delivery 2: evidence.zip`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `exact`
<!-- huntress:metadata:end -->


---

## My Notes

### Objective and evidence

Pool Party is a cumulative binary analysis exercise. Each encrypted `evidence.zip` contains Day 1 through Day 6 samples: an ELF, a native ELF or PE sample, a .NET assembly and runtime configuration, native Go and Rust samples, and a Java JAR. Single Solve had 48 answer IDs. Mastery had two independent deliveries and 96 `set1.` / `set2.` answer IDs. The answers depend on the assigned bytes, so each attempt was downloaded and parsed anew.

### Analysis and verified derivation

The ZIP password was the documented `infected`. The solver opens it with `pyzipper` and never executes the extracted programs. SHA-256 values are calculated over each extracted file in ZIP order.

For Day 1, `pyelftools` reads the ELF header, section names in section-header order, and **every nonempty name in `.symtab` order**. This complete symbol array was the remaining Single Solve answer and the Game Master accepted it. The `recover_code` FUNC symbol supplies the address and size for `capstone` disassembly; the six-byte function decodes to `mov eax, 0x1fa4; ret` in the retained Single Solve sample. The server accepted the equivalent AT&T spelling previously submitted. If `recover_code` is absent, the solver returns `[]`.

The native and .NET samples carry an `HCFG` record. Its header is the four-byte marker, one-byte version, one-byte XOR key, a little-endian 16-bit JSON length, and a little-endian 32-bit CRC32. XOR the following `length` bytes with the key, verify CRC32 over the decoded JSON, then read `campaign`, `domain`, `mutex`, and `url`. The solver searches for a record whose checksum and JSON parse both succeed, since an incidental `HCFG` byte sequence can also occur in code. The Day 3 managed sample has PE/CLI metadata; its runtime version comes from the CLI metadata root. Day 6 stores a Base64-encoded HCFG record in a Java class constant. The solver extracts the class from the JAR, decodes that constant, and applies the same HCFG parser. File format and architecture are determined from the current sample's container and headers.

### Reproduce

```bash
python 06-Pool_Party/solve.py 06-Pool_Party/evidence.zip
python 06-Pool_Party/solve.py 06-Pool_Party/time_trial_latest_evidence.zip
python 06-Pool_Party/solve.py 06-Pool_Party/mastery_set1_evidence.zip
python 06-Pool_Party/solve.py 06-Pool_Party/mastery_set2_evidence.zip
```

The first command produces the 48 unprefixed answer IDs. For Mastery, prefix each delivery's output with its current `setN.` namespace, using the current Game Master `answer_ids`. `run_mastery.py` records how the two deliveries were downloaded, checked against server SHA-256, parsed, mapped, and submitted. It is specific to this challenge and requires `HUNTRESS_GM_TOKEN` in the environment; it does not print that credential.

### Mode results and corrections

- **Single Solve:** `CORRECT` on 2026-10-08. The existing 47 accepted answers matched the retained current artifact. The complete `.symtab` name array supplied the 48th.
- **Time Trial:** `CORRECT` on 2026-10-08, with a server deadline three seconds after the accepted submission. An earlier seven-second attempt expired; another revealed PE variants for Days 2 and 4, which the solver was updated to handle. The successful attempt used the fresh ZIP and answer IDs.
- **Mastery:** `CORRECT` on 2026-10-08 through the Game Master's untimed practice continuation after the first timed attempt expired and `retry` returned `rotation_exhausted`. Both current deliveries were parsed independently. The server marked this completion as ineligible for Hall of Fame timing.

### Retention inventory

Keep `solve.py`, `run_mastery.py`, the original Single Solve `evidence.zip`, `challenge_state.json`, and this write-up for reproduction. The successful Time Trial ZIP and two Mastery ZIPs are useful variant samples. Earlier expired Time Trial downloads, extracted copies, and answer/result JSON files are potentially disposable duplicates; they were retained rather than deleted.

### Lessons Learned

Use the full symbol-table order for array questions, verify decoded HCFG data by CRC32, and prepare variant-aware parsing before starting a short timer. A mode's `CORRECT` status and Hall of Fame eligibility are separate facts.
