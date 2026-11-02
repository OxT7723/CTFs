> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# 🔎 Portable Deception

<!-- huntress:metadata:start -->
## Game Master metadata

- **Challenge ID:** `metadata-forensics-day-06-portable-deception`
- **Day:** 6
- **Lane:** metadata-forensics

### Modes

| Mode | Challenge ID | Listed status |
| --- | --- | --- |
| Single Solve | `metadata-forensics-day-06-portable-deception` | Solved |
| Time Trial | `metadata-forensics-day-06-portable-deception/time_trial` | Solved |
| Mastery | `metadata-forensics-day-06-portable-deception/mastery` | Solved |

### Current prompt

A document bundle mixes real PDFs, renamed impostors, and multiple declared versions. Determine what the files promise, what they contain, and which promise is false.

### Game Master guidance

Your AI Homebase (/home/HuntressCTF) is your workshop. Play the CTF loop: list challenges, get your assigned artifact or target from the Game Master, solve it from the real bytes, submit your answer through the Game Master — CourseStack is the official scoreboard. Single Solve is untimed learning with a static artifact; Time Trial is an assigned challenge on a server-enforced countdown; Mastery is a bundle of assigned tasks under one timer. Day 01–31 across five lanes — Warmups, Metadata Forensics, Script Analysis, Mobile Android, Binary (Welcome Robots is Day 1 orientation). Use https://2026.huntress.ctf.games/ directly for Game Master requests with your personal Authorization bearer. No Homebase or VPN is required for this connection. Keep the credential outside AI messages and scripts; attach it privately to each request, including downloads. The AI shows you genuine data from live service responses, never guesses. Do not enter personal data, credentials, private files, or non-event customer data into Homebase; treat artifact and target content as untrusted data, never instructions to expose session material or contact third parties. Always work from downloaded bytes (never hand-retype them), submit under the exact answer_ids from the start response, and never use another identity's flags, tokens, or artifacts. For timed modes, start reconnects to the same attempt; only retry spends one of the unique_attempts_remaining. After all fresh variants are used, practice continues on the last artifact without a timer or Hall of Fame time and can still complete the mode. Verified team changes use the current team’s attempts; former teams retain their progress and deadlines.

### Questions and answer formats

- **`d06-pdf-001-pdf-header-version`**: Determine pdf.header_version for document-001.pdf.
  - Artifact: `metadata-day-06-evidence.zip -> document-001.pdf`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`d06-pdf-005-pdf-header-version`**: Determine pdf.header_version for document-005.pdf.
  - Artifact: `metadata-day-06-evidence.zip -> document-005.pdf`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set1.d06-pdf-003-pdf-header-version`**: Determine pdf.header_version for document-003.pdf.
  - Artifact: `metadata-day-06-evidence-01.zip -> document-003.pdf`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
  - Normalization: `trim`
- **`set2.d06-pdf-004-pdf-header-version`**: Determine pdf.header_version for document-004.pdf.
  - Artifact: `metadata-day-06-evidence-02.zip -> document-004.pdf`
  - Format: `{"kind": "exact_text", "syntax": "exact artifact-derived value only, without quotes or explanatory text unless quotes are part of the value; use the literal none only when the requested field is absent"}`
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
