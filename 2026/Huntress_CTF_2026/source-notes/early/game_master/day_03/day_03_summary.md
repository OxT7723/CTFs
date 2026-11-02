> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Huntress CTF 2026 - Day 3

Generated from the Game Master through the Homebase SSH connection.

## Challenges

| Lane | Challenge | ID | Questions | Detail file |
|---|---|---|---:|---|
| binary-reverse-engineering | ⚙️ Table Manners | `binary-reverse-engineering-day-03-managed-configuration` | 24 | binary-reverse-engineering-day-03-managed-configuration.json (historical reference: `details/binary-reverse-engineering-day-03-managed-configuration.json`; not included) |
| binary-reverse-engineering | ⚙️ Table Manners | `binary-reverse-engineering-day-03-managed-configuration` | 24 | binary-reverse-engineering-day-03-managed-configuration.json (historical reference: `details/binary-reverse-engineering-day-03-managed-configuration.json`; not included) |
| binary-reverse-engineering | ⚙️ Table Manners | `binary-reverse-engineering-day-03-managed-configuration` | 24 | binary-reverse-engineering-day-03-managed-configuration.json (historical reference: `details/binary-reverse-engineering-day-03-managed-configuration.json`; not included) |
| metadata-forensics | 🔎 BOM Voyage | `metadata-forensics-day-03-bom-voyage` | 1 | metadata-forensics-day-03-bom-voyage.json (historical reference: `details/metadata-forensics-day-03-bom-voyage.json`; not included) |
| metadata-forensics | 🔎 BOM Voyage | `metadata-forensics-day-03-bom-voyage` | 1 | metadata-forensics-day-03-bom-voyage.json (historical reference: `details/metadata-forensics-day-03-bom-voyage.json`; not included) |
| metadata-forensics | 🔎 BOM Voyage | `metadata-forensics-day-03-bom-voyage` | 1 | metadata-forensics-day-03-bom-voyage.json (historical reference: `details/metadata-forensics-day-03-bom-voyage.json`; not included) |
| mobile-android | 📱 Intent Injection | `mobile-android-day-03-intent-injection` | 1 | mobile-android-day-03-intent-injection.json (historical reference: `details/mobile-android-day-03-intent-injection.json`; not included) |
| mobile-android | 📱 Intent Injection | `mobile-android-day-03-intent-injection` | 1 | mobile-android-day-03-intent-injection.json (historical reference: `details/mobile-android-day-03-intent-injection.json`; not included) |
| mobile-android | 📱 Intent Injection | `mobile-android-day-03-intent-injection` | 1 | mobile-android-day-03-intent-injection.json (historical reference: `details/mobile-android-day-03-intent-injection.json`; not included) |
| script-analysis | 📜 Expansion Pack | `script-analysis-day-03-batch-expansion` | 159 | script-analysis-day-03-batch-expansion.json (historical reference: `details/script-analysis-day-03-batch-expansion.json`; not included) |
| script-analysis | 📜 Expansion Pack | `script-analysis-day-03-batch-expansion` | 159 | script-analysis-day-03-batch-expansion.json (historical reference: `details/script-analysis-day-03-batch-expansion.json`; not included) |
| script-analysis | 📜 Expansion Pack | `script-analysis-day-03-batch-expansion` | 159 | script-analysis-day-03-batch-expansion.json (historical reference: `details/script-analysis-day-03-batch-expansion.json`; not included) |
| warmups | 👶 Hex Appeal | `warmups-day-03` | 1 | warmups-day-03.json (historical reference: `details/warmups-day-03.json`; not included) |
| warmups | 👶 Hex Appeal | `warmups-day-03` | 1 | warmups-day-03.json (historical reference: `details/warmups-day-03.json`; not included) |
| warmups | 👶 Hex Appeal | `warmups-day-03` | 1 | warmups-day-03.json (historical reference: `details/warmups-day-03.json`; not included) |

## ⚙️ Table Manners

- **ID:** `binary-reverse-engineering-day-03-managed-configuration`
- **Lane:** `binary-reverse-engineering`

### Prompt

A .NET binary is a database wearing a trench coat. Read the CLI metadata tables — methods, strings, signatures — and find where the configuration is stashed. `ilspycmd` and `strings` are your friends.

### Artifact

- **SHA-256:** `9d7a0aee73c18b68c60bb8b8785ec1a6407ca54f9ae7c2df0d0890adcc37d777`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`d01_artifact_sha256_1`** - What is the exact artifact sha256 1 value for field d01_artifact_sha256_1 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
2. **`d01_analysis_elf_class`** - What is the exact analysis elf class value for field d01_analysis_elf_class in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
3. **`d01_analysis_machine`** - What is the exact analysis machine value for field d01_analysis_machine in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
4. **`d01_analysis_section_names`** - What is the exact analysis section names value for field d01_analysis_section_names in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `json`
5. **`d01_analysis_symbols`** - What is the exact analysis symbols value for field d01_analysis_symbols in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `json`
6. **`d01_analysis_disassembly`** - What is the exact analysis disassembly value for field d01_analysis_disassembly in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `json`
7. **`d01_analysis_elf_type`** - What is the exact analysis elf type value for field d01_analysis_elf_type in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
8. **`d01_analysis_endianness`** - What is the exact analysis endianness value for field d01_analysis_endianness in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
9. **`d02_artifact_sha256_1`** - What is the exact artifact sha256 1 value for field d02_artifact_sha256_1 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
10. **`d02_analysis_format`** - What is the exact analysis format value for field d02_analysis_format in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
11. **`d02_analysis_config_campaign`** - What is the exact analysis config campaign value for field d02_analysis_config_campaign in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
12. **`d02_analysis_config_domain`** - What is the exact analysis config domain value for field d02_analysis_config_domain in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
13. **`d02_analysis_config_mutex`** - What is the exact analysis config mutex value for field d02_analysis_config_mutex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
14. **`d02_analysis_config_url`** - What is the exact analysis config url value for field d02_analysis_config_url in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
15. **`d02_analysis_config_crc32_hex`** - What is the exact analysis config crc32 hex value for field d02_analysis_config_crc32_hex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `pattern`
16. **`d02_analysis_xor_key_hex`** - What is the exact analysis xor key hex value for field d02_analysis_xor_key_hex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `pattern`
17. **`d03_artifact_sha256_1`** - What is the exact artifact sha256 1 value for field d03_artifact_sha256_1 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
18. **`d03_artifact_sha256_2`** - What is the exact artifact sha256 2 value for field d03_artifact_sha256_2 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
19. **`d03_analysis_format`** - What is the exact analysis format value for field d03_analysis_format in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
20. **`d03_analysis_machine`** - What is the exact analysis machine value for field d03_analysis_machine in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
21. **`d03_analysis_metadata_version`** - What is the exact analysis metadata version value for field d03_analysis_metadata_version in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
22. **`d03_analysis_config_campaign`** - What is the exact analysis config campaign value for field d03_analysis_config_campaign in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
23. **`d03_analysis_config_domain`** - What is the exact analysis config domain value for field d03_analysis_config_domain in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
24. **`d03_analysis_config_mutex`** - What is the exact analysis config mutex value for field d03_analysis_config_mutex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`

### Answer IDs

```text
d01_artifact_sha256_1
d01_analysis_elf_class
d01_analysis_machine
d01_analysis_section_names
d01_analysis_symbols
d01_analysis_disassembly
d01_analysis_elf_type
d01_analysis_endianness
d02_artifact_sha256_1
d02_analysis_format
d02_analysis_config_campaign
d02_analysis_config_domain
d02_analysis_config_mutex
d02_analysis_config_url
d02_analysis_config_crc32_hex
d02_analysis_xor_key_hex
d03_artifact_sha256_1
d03_artifact_sha256_2
d03_analysis_format
d03_analysis_machine
d03_analysis_metadata_version
d03_analysis_config_campaign
d03_analysis_config_domain
d03_analysis_config_mutex
```

## ⚙️ Table Manners

- **ID:** `binary-reverse-engineering-day-03-managed-configuration`
- **Lane:** `binary-reverse-engineering`

### Prompt

A .NET binary is a database wearing a trench coat. Read the CLI metadata tables — methods, strings, signatures — and find where the configuration is stashed. `ilspycmd` and `strings` are your friends.

### Artifact

- **SHA-256:** `9d7a0aee73c18b68c60bb8b8785ec1a6407ca54f9ae7c2df0d0890adcc37d777`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`d01_artifact_sha256_1`** - What is the exact artifact sha256 1 value for field d01_artifact_sha256_1 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
2. **`d01_analysis_elf_class`** - What is the exact analysis elf class value for field d01_analysis_elf_class in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
3. **`d01_analysis_machine`** - What is the exact analysis machine value for field d01_analysis_machine in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
4. **`d01_analysis_section_names`** - What is the exact analysis section names value for field d01_analysis_section_names in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `json`
5. **`d01_analysis_symbols`** - What is the exact analysis symbols value for field d01_analysis_symbols in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `json`
6. **`d01_analysis_disassembly`** - What is the exact analysis disassembly value for field d01_analysis_disassembly in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `json`
7. **`d01_analysis_elf_type`** - What is the exact analysis elf type value for field d01_analysis_elf_type in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
8. **`d01_analysis_endianness`** - What is the exact analysis endianness value for field d01_analysis_endianness in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
9. **`d02_artifact_sha256_1`** - What is the exact artifact sha256 1 value for field d02_artifact_sha256_1 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
10. **`d02_analysis_format`** - What is the exact analysis format value for field d02_analysis_format in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
11. **`d02_analysis_config_campaign`** - What is the exact analysis config campaign value for field d02_analysis_config_campaign in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
12. **`d02_analysis_config_domain`** - What is the exact analysis config domain value for field d02_analysis_config_domain in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
13. **`d02_analysis_config_mutex`** - What is the exact analysis config mutex value for field d02_analysis_config_mutex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
14. **`d02_analysis_config_url`** - What is the exact analysis config url value for field d02_analysis_config_url in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
15. **`d02_analysis_config_crc32_hex`** - What is the exact analysis config crc32 hex value for field d02_analysis_config_crc32_hex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `pattern`
16. **`d02_analysis_xor_key_hex`** - What is the exact analysis xor key hex value for field d02_analysis_xor_key_hex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `pattern`
17. **`d03_artifact_sha256_1`** - What is the exact artifact sha256 1 value for field d03_artifact_sha256_1 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
18. **`d03_artifact_sha256_2`** - What is the exact artifact sha256 2 value for field d03_artifact_sha256_2 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
19. **`d03_analysis_format`** - What is the exact analysis format value for field d03_analysis_format in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
20. **`d03_analysis_machine`** - What is the exact analysis machine value for field d03_analysis_machine in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
21. **`d03_analysis_metadata_version`** - What is the exact analysis metadata version value for field d03_analysis_metadata_version in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
22. **`d03_analysis_config_campaign`** - What is the exact analysis config campaign value for field d03_analysis_config_campaign in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
23. **`d03_analysis_config_domain`** - What is the exact analysis config domain value for field d03_analysis_config_domain in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
24. **`d03_analysis_config_mutex`** - What is the exact analysis config mutex value for field d03_analysis_config_mutex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`

### Answer IDs

```text
d01_artifact_sha256_1
d01_analysis_elf_class
d01_analysis_machine
d01_analysis_section_names
d01_analysis_symbols
d01_analysis_disassembly
d01_analysis_elf_type
d01_analysis_endianness
d02_artifact_sha256_1
d02_analysis_format
d02_analysis_config_campaign
d02_analysis_config_domain
d02_analysis_config_mutex
d02_analysis_config_url
d02_analysis_config_crc32_hex
d02_analysis_xor_key_hex
d03_artifact_sha256_1
d03_artifact_sha256_2
d03_analysis_format
d03_analysis_machine
d03_analysis_metadata_version
d03_analysis_config_campaign
d03_analysis_config_domain
d03_analysis_config_mutex
```

## ⚙️ Table Manners

- **ID:** `binary-reverse-engineering-day-03-managed-configuration`
- **Lane:** `binary-reverse-engineering`

### Prompt

A .NET binary is a database wearing a trench coat. Read the CLI metadata tables — methods, strings, signatures — and find where the configuration is stashed. `ilspycmd` and `strings` are your friends.

### Artifact

- **SHA-256:** `9d7a0aee73c18b68c60bb8b8785ec1a6407ca54f9ae7c2df0d0890adcc37d777`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`d01_artifact_sha256_1`** - What is the exact artifact sha256 1 value for field d01_artifact_sha256_1 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
2. **`d01_analysis_elf_class`** - What is the exact analysis elf class value for field d01_analysis_elf_class in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
3. **`d01_analysis_machine`** - What is the exact analysis machine value for field d01_analysis_machine in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
4. **`d01_analysis_section_names`** - What is the exact analysis section names value for field d01_analysis_section_names in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `json`
5. **`d01_analysis_symbols`** - What is the exact analysis symbols value for field d01_analysis_symbols in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `json`
6. **`d01_analysis_disassembly`** - What is the exact analysis disassembly value for field d01_analysis_disassembly in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `json`
7. **`d01_analysis_elf_type`** - What is the exact analysis elf type value for field d01_analysis_elf_type in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
8. **`d01_analysis_endianness`** - What is the exact analysis endianness value for field d01_analysis_endianness in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
9. **`d02_artifact_sha256_1`** - What is the exact artifact sha256 1 value for field d02_artifact_sha256_1 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
10. **`d02_analysis_format`** - What is the exact analysis format value for field d02_analysis_format in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
11. **`d02_analysis_config_campaign`** - What is the exact analysis config campaign value for field d02_analysis_config_campaign in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
12. **`d02_analysis_config_domain`** - What is the exact analysis config domain value for field d02_analysis_config_domain in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
13. **`d02_analysis_config_mutex`** - What is the exact analysis config mutex value for field d02_analysis_config_mutex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
14. **`d02_analysis_config_url`** - What is the exact analysis config url value for field d02_analysis_config_url in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
15. **`d02_analysis_config_crc32_hex`** - What is the exact analysis config crc32 hex value for field d02_analysis_config_crc32_hex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `pattern`
16. **`d02_analysis_xor_key_hex`** - What is the exact analysis xor key hex value for field d02_analysis_xor_key_hex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `pattern`
17. **`d03_artifact_sha256_1`** - What is the exact artifact sha256 1 value for field d03_artifact_sha256_1 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
18. **`d03_artifact_sha256_2`** - What is the exact artifact sha256 2 value for field d03_artifact_sha256_2 in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
19. **`d03_analysis_format`** - What is the exact analysis format value for field d03_analysis_format in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
20. **`d03_analysis_machine`** - What is the exact analysis machine value for field d03_analysis_machine in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
21. **`d03_analysis_metadata_version`** - What is the exact analysis metadata version value for field d03_analysis_metadata_version in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
22. **`d03_analysis_config_campaign`** - What is the exact analysis config campaign value for field d03_analysis_config_campaign in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
23. **`d03_analysis_config_domain`** - What is the exact analysis config domain value for field d03_analysis_config_domain in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`
24. **`d03_analysis_config_mutex`** - What is the exact analysis config mutex value for field d03_analysis_config_mutex in the delivered evidence set?
   - Artifact: `evidence.zip`
   - Format: `exact_text`

### Answer IDs

```text
d01_artifact_sha256_1
d01_analysis_elf_class
d01_analysis_machine
d01_analysis_section_names
d01_analysis_symbols
d01_analysis_disassembly
d01_analysis_elf_type
d01_analysis_endianness
d02_artifact_sha256_1
d02_analysis_format
d02_analysis_config_campaign
d02_analysis_config_domain
d02_analysis_config_mutex
d02_analysis_config_url
d02_analysis_config_crc32_hex
d02_analysis_xor_key_hex
d03_artifact_sha256_1
d03_artifact_sha256_2
d03_analysis_format
d03_analysis_machine
d03_analysis_metadata_version
d03_analysis_config_campaign
d03_analysis_config_domain
d03_analysis_config_mutex
```

## 🔎 BOM Voyage

- **ID:** `metadata-forensics-day-03-bom-voyage`
- **Lane:** `metadata-forensics`

### Prompt

A text export pipeline produced files that look identical in an editor but behave differently in scripts. Find the encoding landmines before they break the investigation.

### Artifact

- **SHA-256:** `207c74a175c574a31325c983afa860b59477238a9d1d9e075de7cfabadf0a285`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`evidence-note-text-utf8-bom-present`** - Determine text.utf8_bom_present for evidence-note.txt.
   - Artifact: `metadata-day-03-evidence.zip -> evidence-note.txt`
   - Format: `enum`
   - Accepted values: `true`, `false`

### Answer IDs

```text
evidence-note-text-utf8-bom-present
```

## 🔎 BOM Voyage

- **ID:** `metadata-forensics-day-03-bom-voyage`
- **Lane:** `metadata-forensics`

### Prompt

A text export pipeline produced files that look identical in an editor but behave differently in scripts. Find the encoding landmines before they break the investigation.

### Artifact

- **SHA-256:** `207c74a175c574a31325c983afa860b59477238a9d1d9e075de7cfabadf0a285`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`evidence-note-text-utf8-bom-present`** - Determine text.utf8_bom_present for evidence-note.txt.
   - Artifact: `metadata-day-03-evidence.zip -> evidence-note.txt`
   - Format: `enum`
   - Accepted values: `true`, `false`

### Answer IDs

```text
evidence-note-text-utf8-bom-present
```

## 🔎 BOM Voyage

- **ID:** `metadata-forensics-day-03-bom-voyage`
- **Lane:** `metadata-forensics`

### Prompt

A text export pipeline produced files that look identical in an editor but behave differently in scripts. Find the encoding landmines before they break the investigation.

### Artifact

- **SHA-256:** `207c74a175c574a31325c983afa860b59477238a9d1d9e075de7cfabadf0a285`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`evidence-note-text-utf8-bom-present`** - Determine text.utf8_bom_present for evidence-note.txt.
   - Artifact: `metadata-day-03-evidence.zip -> evidence-note.txt`
   - Format: `enum`
   - Accepted values: `true`, `false`

### Answer IDs

```text
evidence-note-text-utf8-bom-present
```

## 📱 Intent Injection

- **ID:** `mobile-android-day-03-intent-injection`
- **Lane:** `mobile-android`

### Prompt

Trace attacker-controlled extras through an internal navigation boundary.

### Artifact

- **SHA-256:** `3127e3a93000b594fe4555747aed236f6f77bd8daaf2be41cfe60849bf8708aa`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`answer`** - For case MOB-03-8006859B52 in package com.huntress.mobile.d03.v8006859b5257: Trace attacker-controlled extras through an internal navigation boundary. Submit only the exact backend answer code returned for this case.
   - Artifact: `intent_injection.apk`
   - Format: `pattern`

### Answer IDs

```text
answer
```

## 📱 Intent Injection

- **ID:** `mobile-android-day-03-intent-injection`
- **Lane:** `mobile-android`

### Prompt

Trace attacker-controlled extras through an internal navigation boundary.

### Artifact

- **SHA-256:** `3127e3a93000b594fe4555747aed236f6f77bd8daaf2be41cfe60849bf8708aa`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`answer`** - For case MOB-03-8006859B52 in package com.huntress.mobile.d03.v8006859b5257: Trace attacker-controlled extras through an internal navigation boundary. Submit only the exact backend answer code returned for this case.
   - Artifact: `intent_injection.apk`
   - Format: `pattern`

### Answer IDs

```text
answer
```

## 📱 Intent Injection

- **ID:** `mobile-android-day-03-intent-injection`
- **Lane:** `mobile-android`

### Prompt

Trace attacker-controlled extras through an internal navigation boundary.

### Artifact

- **SHA-256:** `3127e3a93000b594fe4555747aed236f6f77bd8daaf2be41cfe60849bf8708aa`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`answer`** - For case MOB-03-8006859B52 in package com.huntress.mobile.d03.v8006859b5257: Trace attacker-controlled extras through an internal navigation boundary. Submit only the exact backend answer code returned for this case.
   - Artifact: `intent_injection.apk`
   - Format: `pattern`

### Answer IDs

```text
answer
```

## 📜 Expansion Pack

- **ID:** `script-analysis-day-03-batch-expansion`
- **Lane:** `script-analysis`

### Prompt

cmd.exe expands percents, delays expansion, CALLs twice, and bends FOR loops into indirection. Reconstruct every variable exactly as the interpreter would see it — without executing a single line — then follow the staged chain to its final handoff.

### Artifact

- **SHA-256:** `ce1a3fb0a5425cfa0794fc7b7f09ec93b86b74544ad93283a55ebe0ee3fcc23e`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`resource-scenario`** - What scenario best describes resource-sample.ps1?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `enum`
   - Accepted values: `resource_hijacking`, `synthetic_collection`, `synthetic_impact`
2. **`resource-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `mitre_attack_id`
3. **`resource-url`** - What exact URL is embedded in the resource sample?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `exact_text`
4. **`resource-wallet`** - What exact wallet indicator is embedded in the resource sample?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `exact_text`
5. **`resource-mutex`** - What exact mutex indicator is embedded in the resource sample?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `exact_text`
6. **`collection-scenario`** - What scenario best describes collection-sample.ps1?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `enum`
   - Accepted values: `resource_hijacking`, `synthetic_collection`, `synthetic_impact`
7. **`collection-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `mitre_attack_id`
8. **`collection-url`** - What exact URL is embedded in the collection sample?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `exact_text`
9. **`collection-file`** - What is the first exact filename indicator in the collection sample?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `exact_text`
10. **`collection-user-agent`** - What exact user-agent indicator is embedded in the collection sample?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `exact_text`
11. **`impact-scenario`** - What scenario best describes impact-sample.ps1?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `enum`
   - Accepted values: `resource_hijacking`, `synthetic_collection`, `synthetic_impact`
12. **`impact-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `mitre_attack_id`
13. **`impact-extension`** - What exact extension indicator is embedded in the impact sample?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `exact_text`
14. **`impact-note`** - What exact recovery-note filename is embedded in the impact sample?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `exact_text`
15. **`impact-url`** - What exact URL is embedded in the impact sample?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `exact_text`
16. **`jscript-benign-role`** - Classify host-context.js as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
17. **`jscript-benign-attack`** - What is its primary ATT&CK technique ID, or none?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `mitre_attack_id`
18. **`jscript-benign-adapter`** - What exact Windows adapter name does the reconstructed plan reference?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
19. **`jscript-benign-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
20. **`jscript-benign-host`** - What exact synthetic host identifier is reconstructed?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
21. **`jscript-stager-role`** - Classify memory-stage.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
22. **`jscript-stager-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `mitre_attack_id`
23. **`jscript-stager-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
24. **`jscript-stager-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
25. **`jscript-stager-url`** - What exact reserved-domain URL is reconstructed?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
26. **`jscript-dropper-role`** - Classify embedded-write.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
27. **`jscript-dropper-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `mitre_attack_id`
28. **`jscript-dropper-adapter`** - What exact file adapter is reconstructed?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
29. **`jscript-dropper-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
30. **`jscript-dropper-path`** - What exact synthetic output path is reconstructed?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
31. **`jscript-downloader-role`** - Classify remote-write.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
32. **`jscript-downloader-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `mitre_attack_id`
33. **`jscript-downloader-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
34. **`jscript-downloader-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
35. **`jscript-downloader-url`** - What exact reserved-domain URL is reconstructed?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
36. **`jscript-launcher-role`** - Classify local-dispatch.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
37. **`jscript-launcher-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `mitre_attack_id`
38. **`jscript-launcher-adapter`** - What exact process adapter is reconstructed?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
39. **`jscript-launcher-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
40. **`jscript-launcher-path`** - What exact local path is reconstructed?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
41. **`jscript-chain-role`** - Classify staged-handoff.js by its complete ordered behavior graph.
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
42. **`jscript-chain-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `mitre_attack_id`
43. **`jscript-chain-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
44. **`jscript-chain-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
45. **`jscript-chain-next-stage`** - What exact PowerShell next-stage filename is reconstructed?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
46. **`jscript-benign-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
47. **`jscript-benign-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
48. **`jscript-benign-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
49. **`jscript-stager-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
50. **`jscript-stager-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
51. **`jscript-stager-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
52. **`jscript-dropper-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
53. **`jscript-dropper-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
54. **`jscript-dropper-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
55. **`jscript-downloader-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
56. **`jscript-downloader-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
57. **`jscript-downloader-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
58. **`jscript-launcher-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
59. **`jscript-launcher-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
60. **`jscript-launcher-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
61. **`jscript-chain-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
62. **`jscript-chain-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
63. **`jscript-chain-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
64. **`jscript-uploader-role`** - Classify outbound-transfer.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
65. **`jscript-uploader-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `mitre_attack_id`
66. **`jscript-uploader-adapter`** - What exact outbound-transfer adapter or LOLBin is reconstructed?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
67. **`jscript-uploader-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
68. **`jscript-uploader-url`** - What exact reserved-domain upload destination is reconstructed?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
69. **`jscript-uploader-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
70. **`jscript-uploader-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
71. **`jscript-uploader-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
72. **`jscript-impact-role`** - Classify impact-plan.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
73. **`jscript-impact-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `mitre_attack_id`
74. **`jscript-impact-adapter`** - What exact content-transformation adapter is reconstructed?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
75. **`jscript-impact-extension`** - What exact synthetic transformed-file extension is reconstructed?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
76. **`jscript-impact-note`** - What exact synthetic recovery-note name is reconstructed?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
77. **`jscript-impact-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
78. **`jscript-impact-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
79. **`jscript-impact-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
80. **`jscript-relay-role`** - Classify relay-handoff.js by its complete ordered behavior graph.
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
81. **`jscript-relay-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `mitre_attack_id`
82. **`jscript-relay-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
83. **`jscript-relay-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
84. **`jscript-relay-next-stage`** - What exact JScript next-stage filename is reconstructed?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
85. **`jscript-relay-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
86. **`jscript-relay-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
87. **`jscript-relay-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
88. **`batch-benign-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
89. **`batch-benign-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `mitre_attack_id`
90. **`batch-benign-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
91. **`batch-benign-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
92. **`batch-benign-host-id`** - Recover the exact host_id indicator.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
93. **`batch-benign-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
94. **`batch-benign-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
95. **`batch-benign-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
96. **`batch-stager-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
97. **`batch-stager-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `mitre_attack_id`
98. **`batch-stager-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
99. **`batch-stager-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
100. **`batch-stager-url`** - Recover the exact url indicator.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
101. **`batch-stager-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
102. **`batch-stager-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
103. **`batch-stager-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
104. **`batch-dropper-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
105. **`batch-dropper-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `mitre_attack_id`
106. **`batch-dropper-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
107. **`batch-dropper-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
108. **`batch-dropper-file-path`** - Recover the exact file_path indicator.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
109. **`batch-dropper-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
110. **`batch-dropper-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
111. **`batch-dropper-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
112. **`batch-downloader-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
113. **`batch-downloader-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `mitre_attack_id`
114. **`batch-downloader-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
115. **`batch-downloader-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
116. **`batch-downloader-url`** - Recover the exact url indicator.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
117. **`batch-downloader-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
118. **`batch-downloader-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
119. **`batch-downloader-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
120. **`batch-uploader-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
121. **`batch-uploader-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `mitre_attack_id`
122. **`batch-uploader-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
123. **`batch-uploader-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
124. **`batch-uploader-upload-url`** - Recover the exact upload_url indicator.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
125. **`batch-uploader-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
126. **`batch-uploader-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
127. **`batch-uploader-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
128. **`batch-launcher-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
129. **`batch-launcher-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `mitre_attack_id`
130. **`batch-launcher-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
131. **`batch-launcher-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
132. **`batch-launcher-file-path`** - Recover the exact file_path indicator.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
133. **`batch-launcher-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
134. **`batch-launcher-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
135. **`batch-launcher-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
136. **`batch-impact-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
137. **`batch-impact-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `mitre_attack_id`
138. **`batch-impact-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
139. **`batch-impact-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
140. **`batch-impact-note-name`** - Recover the exact note_name indicator.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
141. **`batch-impact-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
142. **`batch-impact-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
143. **`batch-impact-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
144. **`batch-chain-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
145. **`batch-chain-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `mitre_attack_id`
146. **`batch-chain-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
147. **`batch-chain-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
148. **`batch-chain-next-stage`** - Recover the exact next_stage indicator.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
149. **`batch-chain-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
150. **`batch-chain-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
151. **`batch-chain-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
152. **`batch-relay-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
153. **`batch-relay-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `mitre_attack_id`
154. **`batch-relay-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
155. **`batch-relay-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
156. **`batch-relay-next-stage`** - Recover the exact next_stage indicator.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
157. **`batch-relay-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
158. **`batch-relay-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
159. **`batch-relay-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`

### Answer IDs

```text
resource-scenario
resource-attack
resource-url
resource-wallet
resource-mutex
collection-scenario
collection-attack
collection-url
collection-file
collection-user-agent
impact-scenario
impact-attack
impact-extension
impact-note
impact-url
jscript-benign-role
jscript-benign-attack
jscript-benign-adapter
jscript-benign-campaign
jscript-benign-host
jscript-stager-role
jscript-stager-attack
jscript-stager-adapter
jscript-stager-campaign
jscript-stager-url
jscript-dropper-role
jscript-dropper-attack
jscript-dropper-adapter
jscript-dropper-campaign
jscript-dropper-path
jscript-downloader-role
jscript-downloader-attack
jscript-downloader-adapter
jscript-downloader-campaign
jscript-downloader-url
jscript-launcher-role
jscript-launcher-attack
jscript-launcher-adapter
jscript-launcher-campaign
jscript-launcher-path
jscript-chain-role
jscript-chain-attack
jscript-chain-adapter
jscript-chain-campaign
jscript-chain-next-stage
jscript-benign-function-style
jscript-benign-invocation-style
jscript-benign-property-style
jscript-stager-function-style
jscript-stager-invocation-style
jscript-stager-property-style
jscript-dropper-function-style
jscript-dropper-invocation-style
jscript-dropper-property-style
jscript-downloader-function-style
jscript-downloader-invocation-style
jscript-downloader-property-style
jscript-launcher-function-style
jscript-launcher-invocation-style
jscript-launcher-property-style
jscript-chain-function-style
jscript-chain-invocation-style
jscript-chain-property-style
jscript-uploader-role
jscript-uploader-attack
jscript-uploader-adapter
jscript-uploader-campaign
jscript-uploader-url
jscript-uploader-function-style
jscript-uploader-invocation-style
jscript-uploader-property-style
jscript-impact-role
jscript-impact-attack
jscript-impact-adapter
jscript-impact-extension
jscript-impact-note
jscript-impact-function-style
jscript-impact-invocation-style
jscript-impact-property-style
jscript-relay-role
jscript-relay-attack
jscript-relay-adapter
jscript-relay-campaign
jscript-relay-next-stage
jscript-relay-function-style
jscript-relay-invocation-style
jscript-relay-property-style
batch-benign-role
batch-benign-attack
batch-benign-adapter
batch-benign-campaign
batch-benign-host-id
batch-benign-expansion
batch-benign-control
batch-benign-graph
batch-stager-role
batch-stager-attack
batch-stager-adapter
batch-stager-campaign
batch-stager-url
batch-stager-expansion
batch-stager-control
batch-stager-graph
batch-dropper-role
batch-dropper-attack
batch-dropper-adapter
batch-dropper-campaign
batch-dropper-file-path
batch-dropper-expansion
batch-dropper-control
batch-dropper-graph
batch-downloader-role
batch-downloader-attack
batch-downloader-adapter
batch-downloader-campaign
batch-downloader-url
batch-downloader-expansion
batch-downloader-control
batch-downloader-graph
batch-uploader-role
batch-uploader-attack
batch-uploader-adapter
batch-uploader-campaign
batch-uploader-upload-url
batch-uploader-expansion
batch-uploader-control
batch-uploader-graph
batch-launcher-role
batch-launcher-attack
batch-launcher-adapter
batch-launcher-campaign
batch-launcher-file-path
batch-launcher-expansion
batch-launcher-control
batch-launcher-graph
batch-impact-role
batch-impact-attack
batch-impact-adapter
batch-impact-campaign
batch-impact-note-name
batch-impact-expansion
batch-impact-control
batch-impact-graph
batch-chain-role
batch-chain-attack
batch-chain-adapter
batch-chain-campaign
batch-chain-next-stage
batch-chain-expansion
batch-chain-control
batch-chain-graph
batch-relay-role
batch-relay-attack
batch-relay-adapter
batch-relay-campaign
batch-relay-next-stage
batch-relay-expansion
batch-relay-control
batch-relay-graph
```

## 📜 Expansion Pack

- **ID:** `script-analysis-day-03-batch-expansion`
- **Lane:** `script-analysis`

### Prompt

cmd.exe expands percents, delays expansion, CALLs twice, and bends FOR loops into indirection. Reconstruct every variable exactly as the interpreter would see it — without executing a single line — then follow the staged chain to its final handoff.

### Artifact

- **SHA-256:** `ce1a3fb0a5425cfa0794fc7b7f09ec93b86b74544ad93283a55ebe0ee3fcc23e`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`resource-scenario`** - What scenario best describes resource-sample.ps1?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `enum`
   - Accepted values: `resource_hijacking`, `synthetic_collection`, `synthetic_impact`
2. **`resource-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `mitre_attack_id`
3. **`resource-url`** - What exact URL is embedded in the resource sample?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `exact_text`
4. **`resource-wallet`** - What exact wallet indicator is embedded in the resource sample?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `exact_text`
5. **`resource-mutex`** - What exact mutex indicator is embedded in the resource sample?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `exact_text`
6. **`collection-scenario`** - What scenario best describes collection-sample.ps1?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `enum`
   - Accepted values: `resource_hijacking`, `synthetic_collection`, `synthetic_impact`
7. **`collection-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `mitre_attack_id`
8. **`collection-url`** - What exact URL is embedded in the collection sample?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `exact_text`
9. **`collection-file`** - What is the first exact filename indicator in the collection sample?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `exact_text`
10. **`collection-user-agent`** - What exact user-agent indicator is embedded in the collection sample?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `exact_text`
11. **`impact-scenario`** - What scenario best describes impact-sample.ps1?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `enum`
   - Accepted values: `resource_hijacking`, `synthetic_collection`, `synthetic_impact`
12. **`impact-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `mitre_attack_id`
13. **`impact-extension`** - What exact extension indicator is embedded in the impact sample?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `exact_text`
14. **`impact-note`** - What exact recovery-note filename is embedded in the impact sample?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `exact_text`
15. **`impact-url`** - What exact URL is embedded in the impact sample?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `exact_text`
16. **`jscript-benign-role`** - Classify host-context.js as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
17. **`jscript-benign-attack`** - What is its primary ATT&CK technique ID, or none?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `mitre_attack_id`
18. **`jscript-benign-adapter`** - What exact Windows adapter name does the reconstructed plan reference?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
19. **`jscript-benign-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
20. **`jscript-benign-host`** - What exact synthetic host identifier is reconstructed?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
21. **`jscript-stager-role`** - Classify memory-stage.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
22. **`jscript-stager-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `mitre_attack_id`
23. **`jscript-stager-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
24. **`jscript-stager-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
25. **`jscript-stager-url`** - What exact reserved-domain URL is reconstructed?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
26. **`jscript-dropper-role`** - Classify embedded-write.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
27. **`jscript-dropper-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `mitre_attack_id`
28. **`jscript-dropper-adapter`** - What exact file adapter is reconstructed?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
29. **`jscript-dropper-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
30. **`jscript-dropper-path`** - What exact synthetic output path is reconstructed?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
31. **`jscript-downloader-role`** - Classify remote-write.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
32. **`jscript-downloader-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `mitre_attack_id`
33. **`jscript-downloader-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
34. **`jscript-downloader-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
35. **`jscript-downloader-url`** - What exact reserved-domain URL is reconstructed?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
36. **`jscript-launcher-role`** - Classify local-dispatch.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
37. **`jscript-launcher-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `mitre_attack_id`
38. **`jscript-launcher-adapter`** - What exact process adapter is reconstructed?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
39. **`jscript-launcher-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
40. **`jscript-launcher-path`** - What exact local path is reconstructed?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
41. **`jscript-chain-role`** - Classify staged-handoff.js by its complete ordered behavior graph.
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
42. **`jscript-chain-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `mitre_attack_id`
43. **`jscript-chain-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
44. **`jscript-chain-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
45. **`jscript-chain-next-stage`** - What exact PowerShell next-stage filename is reconstructed?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
46. **`jscript-benign-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
47. **`jscript-benign-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
48. **`jscript-benign-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
49. **`jscript-stager-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
50. **`jscript-stager-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
51. **`jscript-stager-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
52. **`jscript-dropper-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
53. **`jscript-dropper-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
54. **`jscript-dropper-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
55. **`jscript-downloader-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
56. **`jscript-downloader-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
57. **`jscript-downloader-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
58. **`jscript-launcher-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
59. **`jscript-launcher-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
60. **`jscript-launcher-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
61. **`jscript-chain-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
62. **`jscript-chain-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
63. **`jscript-chain-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
64. **`jscript-uploader-role`** - Classify outbound-transfer.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
65. **`jscript-uploader-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `mitre_attack_id`
66. **`jscript-uploader-adapter`** - What exact outbound-transfer adapter or LOLBin is reconstructed?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
67. **`jscript-uploader-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
68. **`jscript-uploader-url`** - What exact reserved-domain upload destination is reconstructed?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
69. **`jscript-uploader-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
70. **`jscript-uploader-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
71. **`jscript-uploader-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
72. **`jscript-impact-role`** - Classify impact-plan.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
73. **`jscript-impact-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `mitre_attack_id`
74. **`jscript-impact-adapter`** - What exact content-transformation adapter is reconstructed?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
75. **`jscript-impact-extension`** - What exact synthetic transformed-file extension is reconstructed?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
76. **`jscript-impact-note`** - What exact synthetic recovery-note name is reconstructed?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
77. **`jscript-impact-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
78. **`jscript-impact-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
79. **`jscript-impact-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
80. **`jscript-relay-role`** - Classify relay-handoff.js by its complete ordered behavior graph.
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
81. **`jscript-relay-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `mitre_attack_id`
82. **`jscript-relay-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
83. **`jscript-relay-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
84. **`jscript-relay-next-stage`** - What exact JScript next-stage filename is reconstructed?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
85. **`jscript-relay-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
86. **`jscript-relay-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
87. **`jscript-relay-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
88. **`batch-benign-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
89. **`batch-benign-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `mitre_attack_id`
90. **`batch-benign-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
91. **`batch-benign-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
92. **`batch-benign-host-id`** - Recover the exact host_id indicator.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
93. **`batch-benign-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
94. **`batch-benign-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
95. **`batch-benign-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
96. **`batch-stager-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
97. **`batch-stager-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `mitre_attack_id`
98. **`batch-stager-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
99. **`batch-stager-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
100. **`batch-stager-url`** - Recover the exact url indicator.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
101. **`batch-stager-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
102. **`batch-stager-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
103. **`batch-stager-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
104. **`batch-dropper-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
105. **`batch-dropper-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `mitre_attack_id`
106. **`batch-dropper-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
107. **`batch-dropper-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
108. **`batch-dropper-file-path`** - Recover the exact file_path indicator.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
109. **`batch-dropper-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
110. **`batch-dropper-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
111. **`batch-dropper-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
112. **`batch-downloader-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
113. **`batch-downloader-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `mitre_attack_id`
114. **`batch-downloader-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
115. **`batch-downloader-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
116. **`batch-downloader-url`** - Recover the exact url indicator.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
117. **`batch-downloader-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
118. **`batch-downloader-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
119. **`batch-downloader-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
120. **`batch-uploader-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
121. **`batch-uploader-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `mitre_attack_id`
122. **`batch-uploader-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
123. **`batch-uploader-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
124. **`batch-uploader-upload-url`** - Recover the exact upload_url indicator.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
125. **`batch-uploader-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
126. **`batch-uploader-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
127. **`batch-uploader-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
128. **`batch-launcher-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
129. **`batch-launcher-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `mitre_attack_id`
130. **`batch-launcher-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
131. **`batch-launcher-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
132. **`batch-launcher-file-path`** - Recover the exact file_path indicator.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
133. **`batch-launcher-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
134. **`batch-launcher-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
135. **`batch-launcher-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
136. **`batch-impact-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
137. **`batch-impact-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `mitre_attack_id`
138. **`batch-impact-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
139. **`batch-impact-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
140. **`batch-impact-note-name`** - Recover the exact note_name indicator.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
141. **`batch-impact-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
142. **`batch-impact-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
143. **`batch-impact-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
144. **`batch-chain-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
145. **`batch-chain-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `mitre_attack_id`
146. **`batch-chain-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
147. **`batch-chain-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
148. **`batch-chain-next-stage`** - Recover the exact next_stage indicator.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
149. **`batch-chain-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
150. **`batch-chain-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
151. **`batch-chain-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
152. **`batch-relay-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
153. **`batch-relay-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `mitre_attack_id`
154. **`batch-relay-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
155. **`batch-relay-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
156. **`batch-relay-next-stage`** - Recover the exact next_stage indicator.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
157. **`batch-relay-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
158. **`batch-relay-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
159. **`batch-relay-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`

### Answer IDs

```text
resource-scenario
resource-attack
resource-url
resource-wallet
resource-mutex
collection-scenario
collection-attack
collection-url
collection-file
collection-user-agent
impact-scenario
impact-attack
impact-extension
impact-note
impact-url
jscript-benign-role
jscript-benign-attack
jscript-benign-adapter
jscript-benign-campaign
jscript-benign-host
jscript-stager-role
jscript-stager-attack
jscript-stager-adapter
jscript-stager-campaign
jscript-stager-url
jscript-dropper-role
jscript-dropper-attack
jscript-dropper-adapter
jscript-dropper-campaign
jscript-dropper-path
jscript-downloader-role
jscript-downloader-attack
jscript-downloader-adapter
jscript-downloader-campaign
jscript-downloader-url
jscript-launcher-role
jscript-launcher-attack
jscript-launcher-adapter
jscript-launcher-campaign
jscript-launcher-path
jscript-chain-role
jscript-chain-attack
jscript-chain-adapter
jscript-chain-campaign
jscript-chain-next-stage
jscript-benign-function-style
jscript-benign-invocation-style
jscript-benign-property-style
jscript-stager-function-style
jscript-stager-invocation-style
jscript-stager-property-style
jscript-dropper-function-style
jscript-dropper-invocation-style
jscript-dropper-property-style
jscript-downloader-function-style
jscript-downloader-invocation-style
jscript-downloader-property-style
jscript-launcher-function-style
jscript-launcher-invocation-style
jscript-launcher-property-style
jscript-chain-function-style
jscript-chain-invocation-style
jscript-chain-property-style
jscript-uploader-role
jscript-uploader-attack
jscript-uploader-adapter
jscript-uploader-campaign
jscript-uploader-url
jscript-uploader-function-style
jscript-uploader-invocation-style
jscript-uploader-property-style
jscript-impact-role
jscript-impact-attack
jscript-impact-adapter
jscript-impact-extension
jscript-impact-note
jscript-impact-function-style
jscript-impact-invocation-style
jscript-impact-property-style
jscript-relay-role
jscript-relay-attack
jscript-relay-adapter
jscript-relay-campaign
jscript-relay-next-stage
jscript-relay-function-style
jscript-relay-invocation-style
jscript-relay-property-style
batch-benign-role
batch-benign-attack
batch-benign-adapter
batch-benign-campaign
batch-benign-host-id
batch-benign-expansion
batch-benign-control
batch-benign-graph
batch-stager-role
batch-stager-attack
batch-stager-adapter
batch-stager-campaign
batch-stager-url
batch-stager-expansion
batch-stager-control
batch-stager-graph
batch-dropper-role
batch-dropper-attack
batch-dropper-adapter
batch-dropper-campaign
batch-dropper-file-path
batch-dropper-expansion
batch-dropper-control
batch-dropper-graph
batch-downloader-role
batch-downloader-attack
batch-downloader-adapter
batch-downloader-campaign
batch-downloader-url
batch-downloader-expansion
batch-downloader-control
batch-downloader-graph
batch-uploader-role
batch-uploader-attack
batch-uploader-adapter
batch-uploader-campaign
batch-uploader-upload-url
batch-uploader-expansion
batch-uploader-control
batch-uploader-graph
batch-launcher-role
batch-launcher-attack
batch-launcher-adapter
batch-launcher-campaign
batch-launcher-file-path
batch-launcher-expansion
batch-launcher-control
batch-launcher-graph
batch-impact-role
batch-impact-attack
batch-impact-adapter
batch-impact-campaign
batch-impact-note-name
batch-impact-expansion
batch-impact-control
batch-impact-graph
batch-chain-role
batch-chain-attack
batch-chain-adapter
batch-chain-campaign
batch-chain-next-stage
batch-chain-expansion
batch-chain-control
batch-chain-graph
batch-relay-role
batch-relay-attack
batch-relay-adapter
batch-relay-campaign
batch-relay-next-stage
batch-relay-expansion
batch-relay-control
batch-relay-graph
```

## 📜 Expansion Pack

- **ID:** `script-analysis-day-03-batch-expansion`
- **Lane:** `script-analysis`

### Prompt

cmd.exe expands percents, delays expansion, CALLs twice, and bends FOR loops into indirection. Reconstruct every variable exactly as the interpreter would see it — without executing a single line — then follow the staged chain to its final handoff.

### Artifact

- **SHA-256:** `ce1a3fb0a5425cfa0794fc7b7f09ec93b86b74544ad93283a55ebe0ee3fcc23e`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`resource-scenario`** - What scenario best describes resource-sample.ps1?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `enum`
   - Accepted values: `resource_hijacking`, `synthetic_collection`, `synthetic_impact`
2. **`resource-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `mitre_attack_id`
3. **`resource-url`** - What exact URL is embedded in the resource sample?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `exact_text`
4. **`resource-wallet`** - What exact wallet indicator is embedded in the resource sample?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `exact_text`
5. **`resource-mutex`** - What exact mutex indicator is embedded in the resource sample?
   - Artifact: `evidence.zip -> resource-sample.ps1`
   - Format: `exact_text`
6. **`collection-scenario`** - What scenario best describes collection-sample.ps1?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `enum`
   - Accepted values: `resource_hijacking`, `synthetic_collection`, `synthetic_impact`
7. **`collection-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `mitre_attack_id`
8. **`collection-url`** - What exact URL is embedded in the collection sample?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `exact_text`
9. **`collection-file`** - What is the first exact filename indicator in the collection sample?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `exact_text`
10. **`collection-user-agent`** - What exact user-agent indicator is embedded in the collection sample?
   - Artifact: `evidence.zip -> collection-sample.ps1`
   - Format: `exact_text`
11. **`impact-scenario`** - What scenario best describes impact-sample.ps1?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `enum`
   - Accepted values: `resource_hijacking`, `synthetic_collection`, `synthetic_impact`
12. **`impact-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `mitre_attack_id`
13. **`impact-extension`** - What exact extension indicator is embedded in the impact sample?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `exact_text`
14. **`impact-note`** - What exact recovery-note filename is embedded in the impact sample?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `exact_text`
15. **`impact-url`** - What exact URL is embedded in the impact sample?
   - Artifact: `evidence.zip -> impact-sample.ps1`
   - Format: `exact_text`
16. **`jscript-benign-role`** - Classify host-context.js as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
17. **`jscript-benign-attack`** - What is its primary ATT&CK technique ID, or none?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `mitre_attack_id`
18. **`jscript-benign-adapter`** - What exact Windows adapter name does the reconstructed plan reference?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
19. **`jscript-benign-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
20. **`jscript-benign-host`** - What exact synthetic host identifier is reconstructed?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
21. **`jscript-stager-role`** - Classify memory-stage.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
22. **`jscript-stager-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `mitre_attack_id`
23. **`jscript-stager-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
24. **`jscript-stager-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
25. **`jscript-stager-url`** - What exact reserved-domain URL is reconstructed?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
26. **`jscript-dropper-role`** - Classify embedded-write.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
27. **`jscript-dropper-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `mitre_attack_id`
28. **`jscript-dropper-adapter`** - What exact file adapter is reconstructed?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
29. **`jscript-dropper-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
30. **`jscript-dropper-path`** - What exact synthetic output path is reconstructed?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
31. **`jscript-downloader-role`** - Classify remote-write.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
32. **`jscript-downloader-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `mitre_attack_id`
33. **`jscript-downloader-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
34. **`jscript-downloader-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
35. **`jscript-downloader-url`** - What exact reserved-domain URL is reconstructed?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
36. **`jscript-launcher-role`** - Classify local-dispatch.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
37. **`jscript-launcher-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `mitre_attack_id`
38. **`jscript-launcher-adapter`** - What exact process adapter is reconstructed?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
39. **`jscript-launcher-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
40. **`jscript-launcher-path`** - What exact local path is reconstructed?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
41. **`jscript-chain-role`** - Classify staged-handoff.js by its complete ordered behavior graph.
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
42. **`jscript-chain-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `mitre_attack_id`
43. **`jscript-chain-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
44. **`jscript-chain-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
45. **`jscript-chain-next-stage`** - What exact PowerShell next-stage filename is reconstructed?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
46. **`jscript-benign-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
47. **`jscript-benign-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
48. **`jscript-benign-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> host-context.js`
   - Format: `exact_text`
49. **`jscript-stager-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
50. **`jscript-stager-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
51. **`jscript-stager-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> memory-stage.js`
   - Format: `exact_text`
52. **`jscript-dropper-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
53. **`jscript-dropper-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
54. **`jscript-dropper-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> embedded-write.js`
   - Format: `exact_text`
55. **`jscript-downloader-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
56. **`jscript-downloader-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
57. **`jscript-downloader-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> remote-write.js`
   - Format: `exact_text`
58. **`jscript-launcher-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
59. **`jscript-launcher-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
60. **`jscript-launcher-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> local-dispatch.js`
   - Format: `exact_text`
61. **`jscript-chain-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
62. **`jscript-chain-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
63. **`jscript-chain-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> staged-handoff.js`
   - Format: `exact_text`
64. **`jscript-uploader-role`** - Classify outbound-transfer.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
65. **`jscript-uploader-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `mitre_attack_id`
66. **`jscript-uploader-adapter`** - What exact outbound-transfer adapter or LOLBin is reconstructed?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
67. **`jscript-uploader-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
68. **`jscript-uploader-url`** - What exact reserved-domain upload destination is reconstructed?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
69. **`jscript-uploader-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
70. **`jscript-uploader-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
71. **`jscript-uploader-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> outbound-transfer.js`
   - Format: `exact_text`
72. **`jscript-impact-role`** - Classify impact-plan.js by its ordered behavior graph.
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
73. **`jscript-impact-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `mitre_attack_id`
74. **`jscript-impact-adapter`** - What exact content-transformation adapter is reconstructed?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
75. **`jscript-impact-extension`** - What exact synthetic transformed-file extension is reconstructed?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
76. **`jscript-impact-note`** - What exact synthetic recovery-note name is reconstructed?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
77. **`jscript-impact-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
78. **`jscript-impact-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
79. **`jscript-impact-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> impact-plan.js`
   - Format: `exact_text`
80. **`jscript-relay-role`** - Classify relay-handoff.js by its complete ordered behavior graph.
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
81. **`jscript-relay-attack`** - What is its primary MITRE ATT&CK technique ID?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `mitre_attack_id`
82. **`jscript-relay-adapter`** - What exact acquisition adapter is reconstructed?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
83. **`jscript-relay-campaign`** - What exact synthetic campaign identifier is reconstructed?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
84. **`jscript-relay-next-stage`** - What exact JScript next-stage filename is reconstructed?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
85. **`jscript-relay-function-style`** - Is the inspect function emitted as declaration, anonymous_expression, or named_expression?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
86. **`jscript-relay-invocation-style`** - Is descriptor recovery invoked with direct, call, or apply syntax?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
87. **`jscript-relay-property-style`** - Are descriptor properties accessed with dot, bracket_literal, or mixed syntax?
   - Artifact: `evidence.zip -> relay-handoff.js`
   - Format: `exact_text`
88. **`batch-benign-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
89. **`batch-benign-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `mitre_attack_id`
90. **`batch-benign-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
91. **`batch-benign-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
92. **`batch-benign-host-id`** - Recover the exact host_id indicator.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
93. **`batch-benign-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
94. **`batch-benign-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
95. **`batch-benign-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> host-context.cmd`
   - Format: `exact_text`
96. **`batch-stager-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
97. **`batch-stager-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `mitre_attack_id`
98. **`batch-stager-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
99. **`batch-stager-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
100. **`batch-stager-url`** - Recover the exact url indicator.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
101. **`batch-stager-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
102. **`batch-stager-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
103. **`batch-stager-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> memory-stage.bat`
   - Format: `exact_text`
104. **`batch-dropper-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
105. **`batch-dropper-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `mitre_attack_id`
106. **`batch-dropper-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
107. **`batch-dropper-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
108. **`batch-dropper-file-path`** - Recover the exact file_path indicator.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
109. **`batch-dropper-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
110. **`batch-dropper-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
111. **`batch-dropper-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> embedded-write.cmd`
   - Format: `exact_text`
112. **`batch-downloader-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
113. **`batch-downloader-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `mitre_attack_id`
114. **`batch-downloader-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
115. **`batch-downloader-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
116. **`batch-downloader-url`** - Recover the exact url indicator.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
117. **`batch-downloader-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
118. **`batch-downloader-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
119. **`batch-downloader-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> remote-write.bat`
   - Format: `exact_text`
120. **`batch-uploader-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
121. **`batch-uploader-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `mitre_attack_id`
122. **`batch-uploader-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
123. **`batch-uploader-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
124. **`batch-uploader-upload-url`** - Recover the exact upload_url indicator.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
125. **`batch-uploader-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
126. **`batch-uploader-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
127. **`batch-uploader-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> outbound-transfer.cmd`
   - Format: `exact_text`
128. **`batch-launcher-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
129. **`batch-launcher-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `mitre_attack_id`
130. **`batch-launcher-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
131. **`batch-launcher-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
132. **`batch-launcher-file-path`** - Recover the exact file_path indicator.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
133. **`batch-launcher-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
134. **`batch-launcher-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
135. **`batch-launcher-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> local-dispatch.bat`
   - Format: `exact_text`
136. **`batch-impact-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
137. **`batch-impact-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `mitre_attack_id`
138. **`batch-impact-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
139. **`batch-impact-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
140. **`batch-impact-note-name`** - Recover the exact note_name indicator.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
141. **`batch-impact-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
142. **`batch-impact-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
143. **`batch-impact-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> impact-plan.cmd`
   - Format: `exact_text`
144. **`batch-chain-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
145. **`batch-chain-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `mitre_attack_id`
146. **`batch-chain-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
147. **`batch-chain-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
148. **`batch-chain-next-stage`** - Recover the exact next_stage indicator.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
149. **`batch-chain-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
150. **`batch-chain-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
151. **`batch-chain-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> staged-handoff.bat`
   - Format: `exact_text`
152. **`batch-relay-role`** - Classify the Batch specimen as benign_utility, stager, dropper, downloader, uploader, launcher, impact, or staged_chain.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `enum`
   - Accepted values: `benign_utility`, `downloader`, `dropper`, `impact`, `launcher`, `persistence_descriptor`, `relay`, `staged_chain`, `stager`, `uploader`, `advanced_syntax`
153. **`batch-relay-attack`** - Recover the primary MITRE ATT&CK technique ID, or none.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `mitre_attack_id`
154. **`batch-relay-adapter`** - Recover the exact native adapter named by the reconstructed plan.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
155. **`batch-relay-campaign`** - Recover the exact synthetic campaign identifier.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
156. **`batch-relay-next-stage`** - Recover the exact next_stage indicator.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
157. **`batch-relay-expansion`** - Identify the percent, delayed, CALL-double, or FOR-indirect expansion form.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
158. **`batch-relay-control`** - Identify the exact Batch control-flow form.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`
159. **`batch-relay-graph`** - Identify the exact stage-graph topology.
   - Artifact: `evidence.zip -> relay-handoff.cmd`
   - Format: `exact_text`

### Answer IDs

```text
resource-scenario
resource-attack
resource-url
resource-wallet
resource-mutex
collection-scenario
collection-attack
collection-url
collection-file
collection-user-agent
impact-scenario
impact-attack
impact-extension
impact-note
impact-url
jscript-benign-role
jscript-benign-attack
jscript-benign-adapter
jscript-benign-campaign
jscript-benign-host
jscript-stager-role
jscript-stager-attack
jscript-stager-adapter
jscript-stager-campaign
jscript-stager-url
jscript-dropper-role
jscript-dropper-attack
jscript-dropper-adapter
jscript-dropper-campaign
jscript-dropper-path
jscript-downloader-role
jscript-downloader-attack
jscript-downloader-adapter
jscript-downloader-campaign
jscript-downloader-url
jscript-launcher-role
jscript-launcher-attack
jscript-launcher-adapter
jscript-launcher-campaign
jscript-launcher-path
jscript-chain-role
jscript-chain-attack
jscript-chain-adapter
jscript-chain-campaign
jscript-chain-next-stage
jscript-benign-function-style
jscript-benign-invocation-style
jscript-benign-property-style
jscript-stager-function-style
jscript-stager-invocation-style
jscript-stager-property-style
jscript-dropper-function-style
jscript-dropper-invocation-style
jscript-dropper-property-style
jscript-downloader-function-style
jscript-downloader-invocation-style
jscript-downloader-property-style
jscript-launcher-function-style
jscript-launcher-invocation-style
jscript-launcher-property-style
jscript-chain-function-style
jscript-chain-invocation-style
jscript-chain-property-style
jscript-uploader-role
jscript-uploader-attack
jscript-uploader-adapter
jscript-uploader-campaign
jscript-uploader-url
jscript-uploader-function-style
jscript-uploader-invocation-style
jscript-uploader-property-style
jscript-impact-role
jscript-impact-attack
jscript-impact-adapter
jscript-impact-extension
jscript-impact-note
jscript-impact-function-style
jscript-impact-invocation-style
jscript-impact-property-style
jscript-relay-role
jscript-relay-attack
jscript-relay-adapter
jscript-relay-campaign
jscript-relay-next-stage
jscript-relay-function-style
jscript-relay-invocation-style
jscript-relay-property-style
batch-benign-role
batch-benign-attack
batch-benign-adapter
batch-benign-campaign
batch-benign-host-id
batch-benign-expansion
batch-benign-control
batch-benign-graph
batch-stager-role
batch-stager-attack
batch-stager-adapter
batch-stager-campaign
batch-stager-url
batch-stager-expansion
batch-stager-control
batch-stager-graph
batch-dropper-role
batch-dropper-attack
batch-dropper-adapter
batch-dropper-campaign
batch-dropper-file-path
batch-dropper-expansion
batch-dropper-control
batch-dropper-graph
batch-downloader-role
batch-downloader-attack
batch-downloader-adapter
batch-downloader-campaign
batch-downloader-url
batch-downloader-expansion
batch-downloader-control
batch-downloader-graph
batch-uploader-role
batch-uploader-attack
batch-uploader-adapter
batch-uploader-campaign
batch-uploader-upload-url
batch-uploader-expansion
batch-uploader-control
batch-uploader-graph
batch-launcher-role
batch-launcher-attack
batch-launcher-adapter
batch-launcher-campaign
batch-launcher-file-path
batch-launcher-expansion
batch-launcher-control
batch-launcher-graph
batch-impact-role
batch-impact-attack
batch-impact-adapter
batch-impact-campaign
batch-impact-note-name
batch-impact-expansion
batch-impact-control
batch-impact-graph
batch-chain-role
batch-chain-attack
batch-chain-adapter
batch-chain-campaign
batch-chain-next-stage
batch-chain-expansion
batch-chain-control
batch-chain-graph
batch-relay-role
batch-relay-attack
batch-relay-adapter
batch-relay-campaign
batch-relay-next-stage
batch-relay-expansion
batch-relay-control
batch-relay-graph
```

## 👶 Hex Appeal

- **ID:** `warmups-day-03`
- **Lane:** `warmups`

### Prompt

Sixteen seems like a perfectly reasonable number of fingers.

### Artifact

- **SHA-256:** `8a5302f05b0a7a2b6bfd542f11a5de1e4a842ff3db18a3fe2fa5f68f4e5a92b8`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`message`** - Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
   - Artifact: `blob.txt`
   - Format: `pattern`

### Answer IDs

```text
message
```

## 👶 Hex Appeal

- **ID:** `warmups-day-03`
- **Lane:** `warmups`

### Prompt

Sixteen seems like a perfectly reasonable number of fingers.

### Artifact

- **SHA-256:** `8a5302f05b0a7a2b6bfd542f11a5de1e4a842ff3db18a3fe2fa5f68f4e5a92b8`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`message`** - Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
   - Artifact: `blob.txt`
   - Format: `pattern`

### Answer IDs

```text
message
```

## 👶 Hex Appeal

- **ID:** `warmups-day-03`
- **Lane:** `warmups`

### Prompt

Sixteen seems like a perfectly reasonable number of fingers.

### Artifact

- **SHA-256:** `8a5302f05b0a7a2b6bfd542f11a5de1e4a842ff3db18a3fe2fa5f68f4e5a92b8`
- **Download:** `[retired artifact download capability omitted]`

### Questions

1. **`message`** - Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
   - Artifact: `blob.txt`
   - Format: `pattern`

### Answer IDs

```text
message
```
