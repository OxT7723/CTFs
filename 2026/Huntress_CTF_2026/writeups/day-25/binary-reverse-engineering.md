# Out of Bounds

Day 25 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 25: Out of Bounds

Challenge: `binary-reverse-engineering-day-25-synthetic-vulnerability-root-cause`

The evidence archive contains paired vulnerable and corrected JAR specimens.
The Day 25 questions classify each specimen from its bytes and extract HCFG
configuration values from Base64 constants in classfiles. The shared
configuration fields are valid only after both decoded payloads match.

The binary analyzer now applies its paired-JAR format and configuration checks
to Day 25 as well as Day 24. It uses the parsed JAR/classfile content and does
not infer format from the `.jar` suffix.

All modes completed with every answer accepted:

- Single Solve: 300/300
- Time Trial: 300/300
- Mastery: 2700/2700 across nine sets

Attempt responses and downloaded evidence are preserved under
`work/day-25/binary/` by attempt ID.

## Retained sources

- [later/writeups/day-25/binary-out-of-bounds.md](../../source-notes/later/writeups/day-25/binary-out-of-bounds.md)
