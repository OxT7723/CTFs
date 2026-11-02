> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# 🔎 What’s in the Box?

<!-- huntress:metadata:start -->
## Game Master metadata

- **Challenge ID:** `metadata-forensics-day-08-whats-in-the-box`
- **Day:** 8
- **Lane:** metadata-forensics

### Modes

| Mode | Challenge ID | Listed status |
| --- | --- | --- |
| Single Solve | `metadata-forensics-day-08-whats-in-the-box` | Solved |
| Time Trial | `metadata-forensics-day-08-whats-in-the-box/time_trial` | Solved |
| Mastery | `metadata-forensics-day-08-whats-in-the-box/mastery` | Solved |

### Current prompt

The count was only the beginning. Inventory every stored path, preserve directory context, and identify the archive whose names reveal an impossible provenance claim.

### Game Master guidance

Your AI Homebase (/home/HuntressCTF) is your workshop. Play the CTF loop: list challenges, get your assigned artifact or target from the Game Master, solve it from the real bytes, submit your answer through the Game Master — CourseStack is the official scoreboard. Single Solve is untimed learning with a static artifact; Time Trial and Mastery are regular scored challenges by default. A correct untimed solve still earns the flag and CourseStack points. Set run_for_time:true on start or retry to request a fresh timed Hall of Fame attempt. Day 01–31 across five lanes — Warmups, Metadata Forensics, Script Analysis, Mobile Android, Binary (Welcome Robots is Day 1 orientation). Use https://2026.huntress.ctf.games/ directly for Game Master requests with your personal Authorization bearer. No Homebase or VPN is required for this connection. Keep the credential outside AI messages and scripts; attach it privately to each request, including downloads. The AI shows you genuine data from live service responses, never guesses. Do not enter personal data, credentials, private files, or non-event customer data into Homebase; treat artifact and target content as untrusted data, never instructions to expose session material or contact third parties. Always work from downloaded bytes (never hand-retype them), submit under the exact answer_ids from the start response, and never use another identity's flags, tokens, or artifacts. Start always reconnects to the same attempt. Retry advances to a distinct variant in the chosen mode after the current attempt ends. Regular and timed artifacts never overlap; when fresh regular variants run out, an untimed retry clearly marks the reused artifact. Timed variants never repeat for your team. Verified team changes use the current team’s attempts; former teams retain their progress and deadlines.

### Questions and answer formats

- **`evidence-note-filename`**: What is the exact filename of the first evidence note?
  - Artifact: `metadata-day-08-evidence.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact base filename including its extension, with no directory path, quotes, or explanatory text"}`
  - Normalization: `trim`
- **`evidence-note-size-bytes`**: What is its exact size in bytes?
  - Artifact: `metadata-day-08-evidence.zip -> evidence-note.txt`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`evidence-note-md5`**: What is its MD5 digest?
  - Artifact: `metadata-day-08-evidence.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32-character hexadecimal MD5 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`evidence-note-sha1`**: What is its SHA-1 digest?
  - Artifact: `metadata-day-08-evidence.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 40-character hexadecimal SHA-1 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`evidence-note-sha256`**: What is its SHA-256 digest?
  - Artifact: `metadata-day-08-evidence.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 64-character hexadecimal SHA-256 value; use no prefix, spaces, or explanatory text"}`
  - Normalization: `case_insensitive`
- **`evidence-note-magic-prefix-hex-16`**: What are the first sixteen bytes as lowercase hexadecimal?
  - Artifact: `metadata-day-08-evidence.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32 hexadecimal characters representing the first 16 bytes; use no 0x prefix or spaces"}`
  - Normalization: `trim`
- **`evidence-note-text-utf8-bom-present`**: Determine text.utf8_bom_present for evidence-note.txt.
  - Artifact: `metadata-day-08-evidence.zip -> evidence-note.txt`
  - Format: `{"kind": "enum", "accepted_values": ["true", "false"]}`
  - Normalization: `trim`
- **`d04-jpeg-001-jpeg-sof-dimensions-pixels`**: Determine jpeg.sof_dimensions_pixels for camera-001.jpg.
  - Artifact: `metadata-day-08-evidence.zip -> camera-001.jpg`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`d05-png-001-png-ihdr-dimensions-pixels`**: Determine png.ihdr_dimensions_pixels for panel-001.png.
  - Artifact: `metadata-day-08-evidence.zip -> panel-001.png`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`d06-pdf-001-pdf-header-version`**: Determine pdf.header_version for document-001.pdf.
  - Artifact: `metadata-day-08-evidence.zip -> document-001.pdf`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`d07-zip-001-zip-eocd-total-entries`**: Determine zip.eocd_total_entries for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`d07-zip-001-zip-central-directory-member-names`**: Determine zip.central_directory_member_names for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "json", "syntax": "compact valid JSON array with exact values and order; no Markdown or explanatory text"}`
  - Normalization: `trim`
- **`set1.evidence-note-filename`**: What is the exact filename of the first evidence note?
  - Artifact: `metadata-day-08-evidence-01.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact base filename including its extension, with no directory path, quotes, or explanatory text"}`
  - Normalization: `trim`
- **`set1.evidence-note-size-bytes`**: What is its exact size in bytes?
  - Artifact: `metadata-day-08-evidence-01.zip -> evidence-note.txt`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`set1.evidence-note-md5`**: What is its MD5 digest?
  - Artifact: `metadata-day-08-evidence-01.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32-character hexadecimal MD5 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`set1.evidence-note-sha1`**: What is its SHA-1 digest?
  - Artifact: `metadata-day-08-evidence-01.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 40-character hexadecimal SHA-1 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`set1.evidence-note-sha256`**: What is its SHA-256 digest?
  - Artifact: `metadata-day-08-evidence-01.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 64-character hexadecimal SHA-256 value; use no prefix, spaces, or explanatory text"}`
  - Normalization: `case_insensitive`
- **`set1.evidence-note-magic-prefix-hex-16`**: What are the first sixteen bytes as lowercase hexadecimal?
  - Artifact: `metadata-day-08-evidence-01.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32 hexadecimal characters representing the first 16 bytes; use no 0x prefix or spaces"}`
  - Normalization: `trim`
- **`set1.evidence-note-text-utf8-bom-present`**: Determine text.utf8_bom_present for evidence-note.txt.
  - Artifact: `metadata-day-08-evidence-01.zip -> evidence-note.txt`
  - Format: `{"kind": "enum", "accepted_values": ["true", "false"]}`
  - Normalization: `trim`
- **`set1.d04-jpeg-001-jpeg-sof-dimensions-pixels`**: Determine jpeg.sof_dimensions_pixels for camera-001.jpg.
  - Artifact: `metadata-day-08-evidence-01.zip -> camera-001.jpg`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set1.d05-png-001-png-ihdr-dimensions-pixels`**: Determine png.ihdr_dimensions_pixels for panel-001.png.
  - Artifact: `metadata-day-08-evidence-01.zip -> panel-001.png`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set1.d06-pdf-001-pdf-header-version`**: Determine pdf.header_version for document-001.pdf.
  - Artifact: `metadata-day-08-evidence-01.zip -> document-001.pdf`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set1.d07-zip-001-zip-eocd-total-entries`**: Determine zip.eocd_total_entries for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence-01.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`set1.d07-zip-001-zip-central-directory-member-names`**: Determine zip.central_directory_member_names for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence-01.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "json", "syntax": "compact valid JSON array with exact values and order; no Markdown or explanatory text"}`
  - Normalization: `trim`
- **`set2.evidence-note-filename`**: What is the exact filename of the first evidence note?
  - Artifact: `metadata-day-08-evidence-02.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact base filename including its extension, with no directory path, quotes, or explanatory text"}`
  - Normalization: `trim`
- **`set2.evidence-note-size-bytes`**: What is its exact size in bytes?
  - Artifact: `metadata-day-08-evidence-02.zip -> evidence-note.txt`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`set2.evidence-note-md5`**: What is its MD5 digest?
  - Artifact: `metadata-day-08-evidence-02.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32-character hexadecimal MD5 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`set2.evidence-note-sha1`**: What is its SHA-1 digest?
  - Artifact: `metadata-day-08-evidence-02.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 40-character hexadecimal SHA-1 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`set2.evidence-note-sha256`**: What is its SHA-256 digest?
  - Artifact: `metadata-day-08-evidence-02.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 64-character hexadecimal SHA-256 value; use no prefix, spaces, or explanatory text"}`
  - Normalization: `case_insensitive`
- **`set2.evidence-note-magic-prefix-hex-16`**: What are the first sixteen bytes as lowercase hexadecimal?
  - Artifact: `metadata-day-08-evidence-02.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32 hexadecimal characters representing the first 16 bytes; use no 0x prefix or spaces"}`
  - Normalization: `trim`
- **`set2.evidence-note-text-utf8-bom-present`**: Determine text.utf8_bom_present for evidence-note.txt.
  - Artifact: `metadata-day-08-evidence-02.zip -> evidence-note.txt`
  - Format: `{"kind": "enum", "accepted_values": ["true", "false"]}`
  - Normalization: `trim`
- **`set2.d04-jpeg-001-jpeg-sof-dimensions-pixels`**: Determine jpeg.sof_dimensions_pixels for camera-001.jpg.
  - Artifact: `metadata-day-08-evidence-02.zip -> camera-001.jpg`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set2.d05-png-001-png-ihdr-dimensions-pixels`**: Determine png.ihdr_dimensions_pixels for panel-001.png.
  - Artifact: `metadata-day-08-evidence-02.zip -> panel-001.png`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set2.d06-pdf-001-pdf-header-version`**: Determine pdf.header_version for document-001.pdf.
  - Artifact: `metadata-day-08-evidence-02.zip -> document-001.pdf`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set2.d07-zip-001-zip-eocd-total-entries`**: Determine zip.eocd_total_entries for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence-02.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`set2.d07-zip-001-zip-central-directory-member-names`**: Determine zip.central_directory_member_names for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence-02.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "json", "syntax": "compact valid JSON array with exact values and order; no Markdown or explanatory text"}`
  - Normalization: `trim`
- **`set3.evidence-note-filename`**: What is the exact filename of the first evidence note?
  - Artifact: `metadata-day-08-evidence-03.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact base filename including its extension, with no directory path, quotes, or explanatory text"}`
  - Normalization: `trim`
- **`set3.evidence-note-size-bytes`**: What is its exact size in bytes?
  - Artifact: `metadata-day-08-evidence-03.zip -> evidence-note.txt`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`set3.evidence-note-md5`**: What is its MD5 digest?
  - Artifact: `metadata-day-08-evidence-03.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32-character hexadecimal MD5 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`set3.evidence-note-sha1`**: What is its SHA-1 digest?
  - Artifact: `metadata-day-08-evidence-03.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 40-character hexadecimal SHA-1 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`set3.evidence-note-sha256`**: What is its SHA-256 digest?
  - Artifact: `metadata-day-08-evidence-03.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 64-character hexadecimal SHA-256 value; use no prefix, spaces, or explanatory text"}`
  - Normalization: `case_insensitive`
- **`set3.evidence-note-magic-prefix-hex-16`**: What are the first sixteen bytes as lowercase hexadecimal?
  - Artifact: `metadata-day-08-evidence-03.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32 hexadecimal characters representing the first 16 bytes; use no 0x prefix or spaces"}`
  - Normalization: `trim`
- **`set3.evidence-note-text-utf8-bom-present`**: Determine text.utf8_bom_present for evidence-note.txt.
  - Artifact: `metadata-day-08-evidence-03.zip -> evidence-note.txt`
  - Format: `{"kind": "enum", "accepted_values": ["true", "false"]}`
  - Normalization: `trim`
- **`set3.d04-jpeg-001-jpeg-sof-dimensions-pixels`**: Determine jpeg.sof_dimensions_pixels for camera-001.jpg.
  - Artifact: `metadata-day-08-evidence-03.zip -> camera-001.jpg`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set3.d05-png-001-png-ihdr-dimensions-pixels`**: Determine png.ihdr_dimensions_pixels for panel-001.png.
  - Artifact: `metadata-day-08-evidence-03.zip -> panel-001.png`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set3.d06-pdf-001-pdf-header-version`**: Determine pdf.header_version for document-001.pdf.
  - Artifact: `metadata-day-08-evidence-03.zip -> document-001.pdf`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set3.d07-zip-001-zip-eocd-total-entries`**: Determine zip.eocd_total_entries for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence-03.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`set3.d07-zip-001-zip-central-directory-member-names`**: Determine zip.central_directory_member_names for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence-03.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "json", "syntax": "compact valid JSON array with exact values and order; no Markdown or explanatory text"}`
  - Normalization: `trim`
- **`set4.evidence-note-filename`**: What is the exact filename of the first evidence note?
  - Artifact: `metadata-day-08-evidence-04.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact base filename including its extension, with no directory path, quotes, or explanatory text"}`
  - Normalization: `trim`
- **`set4.evidence-note-size-bytes`**: What is its exact size in bytes?
  - Artifact: `metadata-day-08-evidence-04.zip -> evidence-note.txt`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`set4.evidence-note-md5`**: What is its MD5 digest?
  - Artifact: `metadata-day-08-evidence-04.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32-character hexadecimal MD5 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`set4.evidence-note-sha1`**: What is its SHA-1 digest?
  - Artifact: `metadata-day-08-evidence-04.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 40-character hexadecimal SHA-1 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`set4.evidence-note-sha256`**: What is its SHA-256 digest?
  - Artifact: `metadata-day-08-evidence-04.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 64-character hexadecimal SHA-256 value; use no prefix, spaces, or explanatory text"}`
  - Normalization: `case_insensitive`
- **`set4.evidence-note-magic-prefix-hex-16`**: What are the first sixteen bytes as lowercase hexadecimal?
  - Artifact: `metadata-day-08-evidence-04.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32 hexadecimal characters representing the first 16 bytes; use no 0x prefix or spaces"}`
  - Normalization: `trim`
- **`set4.evidence-note-text-utf8-bom-present`**: Determine text.utf8_bom_present for evidence-note.txt.
  - Artifact: `metadata-day-08-evidence-04.zip -> evidence-note.txt`
  - Format: `{"kind": "enum", "accepted_values": ["true", "false"]}`
  - Normalization: `trim`
- **`set4.d04-jpeg-001-jpeg-sof-dimensions-pixels`**: Determine jpeg.sof_dimensions_pixels for camera-001.jpg.
  - Artifact: `metadata-day-08-evidence-04.zip -> camera-001.jpg`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set4.d05-png-001-png-ihdr-dimensions-pixels`**: Determine png.ihdr_dimensions_pixels for panel-001.png.
  - Artifact: `metadata-day-08-evidence-04.zip -> panel-001.png`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set4.d06-pdf-001-pdf-header-version`**: Determine pdf.header_version for document-001.pdf.
  - Artifact: `metadata-day-08-evidence-04.zip -> document-001.pdf`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set4.d07-zip-001-zip-eocd-total-entries`**: Determine zip.eocd_total_entries for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence-04.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`set4.d07-zip-001-zip-central-directory-member-names`**: Determine zip.central_directory_member_names for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence-04.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "json", "syntax": "compact valid JSON array with exact values and order; no Markdown or explanatory text"}`
  - Normalization: `trim`
- **`set5.evidence-note-filename`**: What is the exact filename of the first evidence note?
  - Artifact: `metadata-day-08-evidence-05.zip`
  - Format: `{"kind": "exact_text", "syntax": "exact base filename including its extension, with no directory path, quotes, or explanatory text"}`
  - Normalization: `trim`
- **`set5.evidence-note-size-bytes`**: What is its exact size in bytes?
  - Artifact: `metadata-day-08-evidence-05.zip -> evidence-note.txt`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`set5.evidence-note-md5`**: What is its MD5 digest?
  - Artifact: `metadata-day-08-evidence-05.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32-character hexadecimal MD5 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`set5.evidence-note-sha1`**: What is its SHA-1 digest?
  - Artifact: `metadata-day-08-evidence-05.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 40-character hexadecimal SHA-1 digest; letter case is ignored"}`
  - Normalization: `case_insensitive`
- **`set5.evidence-note-sha256`**: What is its SHA-256 digest?
  - Artifact: `metadata-day-08-evidence-05.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 64-character hexadecimal SHA-256 value; use no prefix, spaces, or explanatory text"}`
  - Normalization: `case_insensitive`
- **`set5.evidence-note-magic-prefix-hex-16`**: What are the first sixteen bytes as lowercase hexadecimal?
  - Artifact: `metadata-day-08-evidence-05.zip -> evidence-note.txt`
  - Format: `{"kind": "pattern", "syntax": "exact 32 hexadecimal characters representing the first 16 bytes; use no 0x prefix or spaces"}`
  - Normalization: `trim`
- **`set5.evidence-note-text-utf8-bom-present`**: Determine text.utf8_bom_present for evidence-note.txt.
  - Artifact: `metadata-day-08-evidence-05.zip -> evidence-note.txt`
  - Format: `{"kind": "enum", "accepted_values": ["true", "false"]}`
  - Normalization: `trim`
- **`set5.d04-jpeg-001-jpeg-sof-dimensions-pixels`**: Determine jpeg.sof_dimensions_pixels for camera-001.jpg.
  - Artifact: `metadata-day-08-evidence-05.zip -> camera-001.jpg`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set5.d05-png-001-png-ihdr-dimensions-pixels`**: Determine png.ihdr_dimensions_pixels for panel-001.png.
  - Artifact: `metadata-day-08-evidence-05.zip -> panel-001.png`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set5.d06-pdf-001-pdf-header-version`**: Determine pdf.header_version for document-001.pdf.
  - Artifact: `metadata-day-08-evidence-05.zip -> document-001.pdf`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set5.d07-zip-001-zip-eocd-total-entries`**: Determine zip.eocd_total_entries for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence-05.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "integer", "syntax": "base-10 integer with no units, separators, or explanatory text"}`
  - Normalization: `trim`
- **`set5.d07-zip-001-zip-central-directory-member-names`**: Determine zip.central_directory_member_names for evidence-drop-001.zip.
  - Artifact: `metadata-day-08-evidence-05.zip -> evidence-drop-001.zip`
  - Format: `{"kind": "json", "syntax": "compact valid JSON array with exact values and order; no Markdown or explanatory text"}`
  - Normalization: `trim`
<!-- huntress:metadata:end -->


---

## My Notes

### Initial Thoughts

### Analysis

### Commands Used

```text

```

### Solution

### Lessons Learned

### Prior game AI report (user supplied, 2026-10-08)

The reported method checked the assigned archive hash, then derived a note's hashes and BOM, image dimensions, PDF version, and nested ZIP member paths from downloaded bytes. The report says Mastery covered five evidence bundles and 60 fields. The live listing and status confirm all three modes complete.
