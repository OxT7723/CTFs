> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 24 Binary Reverse Engineering — Spot the Difference

The team's regular Single Solve attempt is `CORRECT` with all 288 answer fields
accepted. The current start request confirmed the challenge was already
complete and did not issue another assignment. The archived attempt used
regular untimed play.

| Attempt | Accepted | Assigned artifact SHA-256 |
| --- | ---: | --- |
| `bf93a7e6-c895-4676-aa6f-37f57698756d` | 288 / 288 | `34d32411f3103f9e3dcd36ac768ceeb34b27a66785c3fd6a6a5f6cb6efcb6628` |

The bundle contains role-labeled vulnerable and corrected JARs. Comparing the
`score(String)` bytecode shows the vulnerable build calls Scala's
`nonEmpty` check directly on its input, then reads character zero; the
corrected build wraps the value in `Option`, filters empty strings, maps the
first character, and supplies a fallback. Passing `null` to the vulnerable
method reaches the unchecked string operation and throws, while the corrected
path handles it. This establishes the null-input failure path statically.

The JARs also contain Base64-held HCFG records in their class constant pools.
Decode the record, XOR the payload with its one-byte key, verify its CRC32,
and parse the JSON. The role-specific configurations agree.

The live Single Solve response had no separate answer field for a method diff
or reproduction; its D24-specific fields cover the two member hashes,
container types, and configuration. The archived bytecode provides the
failure-path comparison above, but I did not execute either JAR: this
environment has no Java runtime.

Attempt artifacts, extracted files, candidates, submissions, and status are
under `work/day-24/binary/bf93a7e6-c895-4676-aa6f-37f57698756d` (historical reference: `</home/HuntressCTF/work/day-24/binary/bf93a7e6-c895-4676-aa6f-37f57698756d>`; not included). The API assignment linked evidence.zip (retired artifact link; see artifact inventory).
