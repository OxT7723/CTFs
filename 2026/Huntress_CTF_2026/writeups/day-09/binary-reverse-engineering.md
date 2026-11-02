# Nimble

Day 9 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `binary-reverse-engineering-day-09-nim-generated-runtime`

## Later Homebase account

### Nimble — Day 9 Binary Reverse Engineering

### Result

Single Solve, regular Time Trial, and regular Mastery are all complete. The
Game Master returned `CORRECT` for all three modes. Single Solve had 90 fields,
Time Trial had 90, and Mastery had 450 across five assigned evidence bundles.
The user’s files and candidate maps are kept under this directory.

### Analysis

The protected archives were extracted with `infected`. The samples are
identified from their downloaded bytes: ELF, PE, and JAR container signatures;
managed runtime metadata; compiler/runtime symbols; ELF sections and symbols;
and embedded HCFG v1 records. HCFG data is XOR-decoded and checked against its
CRC32 before using any recovered values.

Format strings are case-sensitive. The accepted values were lowercase `elf`
and `jar`, with `PE_CLI` for the managed PE. For the Time Trial and Mastery
archive questions, include all observed ZIP compression methods, including
stored directory entries: `[0,8]`. Single Solve accepted `[8]` for its bundle.

### Reuse

Run `python3 solve.py` to build an answer map from `extracted/`. Set
`NIMBLE_EXTRACTED_DIR` to another extracted delivery to analyze that bundle.
For Time Trial or Mastery, also set
`NIMBLE_INCLUDE_DIRECTORY_COMPRESSION_METHODS=1` to include stored ZIP
directory entries. `candidate-answers.json` contains the accepted Single Solve
answers. Mastery answers and evidence are saved by delivery in the `mastery-...`
directory.

Two optional timed Hall of Fame runs expired at their 10-second deadlines. The
regular untimed Time Trial and Mastery runs are solved and scored.

## Retained sources

- [early/09-Nimble/readme.md](../../source-notes/early/09-Nimble/readme.md)
- [later/writeups/day-09/nimble.md](../../source-notes/later/writeups/day-09/nimble.md)
