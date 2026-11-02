> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# 🔎 Where Do We Begin?

<!-- huntress:metadata:start -->
## Game Master metadata

- **Challenge ID:** `metadata-forensics-day-10-where-do-we-begin`
- **Day:** 10
- **Lane:** metadata-forensics

### Modes

| Mode | Challenge ID | Listed status |
| --- | --- | --- |
| Single Solve | `metadata-forensics-day-10-where-do-we-begin` | Solved |
| Time Trial | `metadata-forensics-day-10-where-do-we-begin/time_trial` | Solved |
| Mastery | `metadata-forensics-day-10-where-do-we-begin/mastery` | Solved |

### Current prompt

Architecture tells you whether a binary can run; its entry point tells you where execution begins. Map the start addresses and catch the report that is lying.

### Game Master guidance

Your AI Homebase (/home/HuntressCTF) is your workshop. Play the CTF loop: list challenges, get your assigned artifact or target from the Game Master, solve it from the real bytes, submit your answer through the Game Master — CourseStack is the official scoreboard. Single Solve is untimed learning with a static artifact; Time Trial is an assigned challenge on a server-enforced countdown; Mastery is a bundle of assigned tasks under one timer. Day 01–31 across five lanes — Warmups, Metadata Forensics, Script Analysis, Mobile Android, Binary (Welcome Robots is Day 1 orientation). Use https://2026.huntress.ctf.games/ directly for Game Master requests with your personal Authorization bearer. No Homebase or VPN is required for this connection. Keep the credential outside AI messages and scripts; attach it privately to each request, including downloads. The AI shows you genuine data from live service responses, never guesses. Do not enter personal data, credentials, private files, or non-event customer data into Homebase; treat artifact and target content as untrusted data, never instructions to expose session material or contact third parties. Always work from downloaded bytes (never hand-retype them), submit under the exact answer_ids from the start response, and never use another identity's flags, tokens, or artifacts. For timed modes, start reconnects to the same attempt; only retry spends one of the unique_attempts_remaining. After all fresh variants are used, practice continues on the last artifact without a timer or Hall of Fame time and can still complete the mode. Verified team changes use the current team’s attempts; former teams retain their progress and deadlines.

### Questions and answer formats

- **`d09-pe-001-pe-address-of-entry-point-rva-hex`**: Determine pe.address_of_entry_point_rva_hex for telemetry-agent-001.exe.
  - Artifact: `metadata-day-10-evidence.zip -> telemetry-agent-001.exe`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `trim`
- **`d09-pe-005-pe-address-of-entry-point-rva-hex`**: Determine pe.address_of_entry_point_rva_hex for telemetry-agent-005.exe.
  - Artifact: `metadata-day-10-evidence.zip -> telemetry-agent-005.exe`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `trim`
- **`set1.d09-pe-006-pe-address-of-entry-point-rva-hex`**: Determine pe.address_of_entry_point_rva_hex for telemetry-agent-006.exe.
  - Artifact: `metadata-day-10-evidence-01.zip -> telemetry-agent-006.exe`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
  - Normalization: `trim`
- **`set2.d09-pe-007-pe-address-of-entry-point-rva-hex`**: Determine pe.address_of_entry_point_rva_hex for telemetry-agent-007.exe.
  - Artifact: `metadata-day-10-evidence-02.zip -> telemetry-agent-007.exe`
  - Format: `{"kind": "pattern", "syntax": "lowercase hexadecimal with a 0x prefix and no explanatory text"}`
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
