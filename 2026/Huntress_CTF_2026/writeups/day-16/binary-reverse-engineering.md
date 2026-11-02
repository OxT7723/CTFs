# Wasm Up

Day 16 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 16: Wasm Up

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

## Retained sources

- [later/writeups/day-16/binary-wasm-up.md](../../source-notes/later/writeups/day-16/binary-wasm-up.md)
