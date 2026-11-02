> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 25: Out of Bounds

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
