> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 16 Warmups — 👶 Dot Com

**Challenge:** `warmups-day-16`  
**Prompt:** “Sixteen little symbols are calling. Dot dot dot.”  
**Question:** Decode the assigned blob and submit the exact slug from its final
non-empty line. The answer field is `message`; the required format is three
lowercase hyphen-separated words followed by a two-digit number.

## Solve

The Single Solve artifact is whitespace-separated Morse. Decoding it yields a
hexadecimal message; decoding those bytes gives the instructions and answer
slug. The first assigned answer was `silly-banner-marble-88`.

Mastery provides 78 samples using numbered mixed-codec rows. Row 16 is Morse;
after decoding all rows, some variants leave a suffix of the final slug in
hexadecimal. The Warmups tools now decode numbered rows recursively, support
Morse and hexadecimal layers, and resolve a hex suffix against the live answer
format.

## Results

| Mode | Attempt | Result |
| --- | --- | --- |
| Single Solve | `9f7f933c-6c2d-4430-843f-16c22e0cd886` | CORRECT |
| Time Trial, regular untimed route | `749c4ade-89de-4abb-8b75-f62dbb0c5fc6` | CORRECT |
| Mastery, regular untimed route (78 answers) | `796fab24-928f-4250-ac43-d8ecbef3cf59` | CORRECT |

The assigned bytes, start responses, candidate answers, submission results,
and final status responses are saved under `work/day-16/warmups/` by attempt
ID. Final Game Master status and the Day 16 Warmups list report all three
modes solved.
