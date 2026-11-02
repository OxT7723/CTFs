> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 28 — Family Resemblance

Completed the regular Single Solve, Time Trial, and Mastery modes. The Game
Master reports `CORRECT` for all three, with 392/392, 392/392, and 4,704/4,704
accepted answer fields. All attempts were untimed; no Hall of Fame run was
requested. The status endpoint exposes completion but no separate CourseStack
point total.

The deterministic solver selects Day 28's false-friend, family-a, and family-b
specimens by filename role, parses their final containers and ELF machine
fields, and checks that the family A/B HCFG payloads match byte for byte before
using the shared configuration. Structural archive fields use ZIP
central-directory order. ELF symbol parsing preserves spaces in resolved names;
the Crystal symbol-count field uses symbol-table rows from `objdump -t`.

Attempt archives, candidate answers, and final status responses are preserved
under `work/day-28/binary/`.
