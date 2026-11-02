> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 16: Wasm Up

Challenge: `binary-reverse-engineering-day-16-webassembly-optimization-equivalence`

The evidence bundle contains role-named `direct` and `compact` WebAssembly
modules. The analyzer selects each variant from the answer ID, hashes archive
members in delivered order, reads the module format and architecture, and
recovers the XOR-decoded HCFG configuration only after validating its CRC.
`run_modes.py` handles the regular Single Solve, Time Trial, and five-set
Mastery assignments from their live artifacts.

All modes completed with Game Master result `CORRECT`: Single Solve accepted
160/160 answers, Time Trial 160/160, and Mastery 800/800. The regular timed-mode
routes were used without `run_for_time:true`; all three server statuses showed
no deadline.
