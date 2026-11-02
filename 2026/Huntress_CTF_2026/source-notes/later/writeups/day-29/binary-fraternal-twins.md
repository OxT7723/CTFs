> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Fraternal Twins

Day 29 Binary Reverse Engineering compares two ELF builds of the same program:
the unoptimized `O0` specimen and optimized `O3` specimen. The answer contract
asks for both delivered artifact hashes, each container and numeric
`e_machine`, and selected configuration fields.

The reusable analyzer selects the variants by their `O0.elf` and `O3.elf`
filename suffixes. It classifies each file from its final container, reads the
ELF machine value, and scans backward for the last CRC32-valid HCFG record.
For shared configuration answers it checks that both decoded HCFG payloads
match byte for byte before using the O3 payload. Artifact hashes follow the
archive's recorded delivery order.

The Single Solve, Time Trial regular attempt, and Mastery regular attempt all
returned `CORRECT`; the submitted answer sets had no unresolved IDs. Mastery
contained 13 evidence deliveries and 5,278 answer IDs. Time Trial and Mastery
were started without `run_for_time:true`, so both were non-Hall-of-Fame
attempts and had no server deadline.

Re-run a mode with the existing binary runner and the corresponding challenge
ID from the Game Master list. The runner verifies downloaded archive hashes and
uses the live answer IDs; it does not store challenge-specific answer values.
