> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Built Different

- Single Solve, Time Trial, and the 65-question Mastery bundle were accepted.
- The answers came from the assigned metadata evidence: note hashes and byte properties, image dimensions, PDF header, nested ZIP central directory, and PE COFF machine value.
- Reusable parser: `solve.py`. It reads the assigned ZIP and emits the answer map.
- PE machine values need four hex digits (for example, `0x014c`).

The downloaded evidence archives are saved here for faster repeat runs.
