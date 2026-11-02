# Spot the Difference

Day 24 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

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
under `work/day-24/binary/bf93a7e6-c895-4676-aa6f-37f57698756d` (source reference: `/home/HuntressCTF/work/day-24/binary/bf93a7e6-c895-4676-aa6f-37f57698756d`; not included). The API assignment linked evidence.zip (private download link removed).

## Retained sources

- [later/writeups/day-24/binary-spot-the-difference.md](../../source-notes/later/writeups/day-24/binary-spot-the-difference.md)
