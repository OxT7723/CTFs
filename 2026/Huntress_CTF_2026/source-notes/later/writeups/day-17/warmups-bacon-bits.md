> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 17 Warmups — 👶 Bacon Bits

**Challenge:** `warmups-day-17`
**Prompt:** “Sixteen guests. Five little a's and b's apiece.”

## Solve

Each five-character `a`/`b` group represents a four-bit value: interpret
`a` as 0 and `b` as 1, then convert the value to one hexadecimal digit.
Decoding the resulting hex bytes reveals the instructions and slug. The Single
Solve answer was `tidy-rocket-harbor-20`.

Mastery uses 83 numbered mixed-codec samples. Its seventeenth row adds the same
Bacon-nibble encoding; the Morse and Bacon rows form a hex-encoded slug suffix.
The Warmups decoder now recognizes Bacon nibble groups both directly and as
numbered codec 17, and checks that layer before treating the text as Base64.

## Results

| Mode | Attempt | Result |
| --- | --- | --- |
| Single Solve | `22f1c44b-b8e3-4537-83a2-34f26e347451` | CORRECT |
| Time Trial, regular untimed route | `41541506-bd61-4e6d-8b47-0772e01640d8` | CORRECT |
| Mastery, regular untimed route (83 answers) | `c9b6849c-eacf-44a7-897e-4c9d392ca256` | CORRECT |

The assigned artifacts, candidate answers, submissions, and status responses
are saved under `work/day-17/warmups/` by attempt ID. Live Game Master status
confirms all three modes solved.
