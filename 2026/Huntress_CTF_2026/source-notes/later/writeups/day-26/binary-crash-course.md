> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 26 Binary Reverse Engineering — Crash Course

Single Solve completed with `CORRECT` (312/312). The archived team attempt is
untimed, and a current start request confirmed the challenge was already
complete without issuing a new assignment.

| Attempt | Accepted | Assigned artifact SHA-256 |
| --- | ---: | --- |
| `9a8bb83f-8523-44db-88c4-26eeaa63a6b1` | 312 / 312 | `fd52a098241e1d9b99c54da530b9185a29dc8269ee56edc3d36c237f2381b1e3` |

The crash trace is embedded as `crash/trace.json` in the assigned JAR. Read
its frames, compare them against the primary classfile's method table, and
count the declared methods. The configuration is stored in a Base64 constant:
decode its HCFG record, XOR the payload with the header key, and validate the
CRC32 before reading its JSON fields.

The Game Master accepted every submitted field. The assigned evidence.zip (retired artifact link; see artifact inventory), candidate answers, extracted JAR, and final status are saved
under `work/day-26/binary/9a8bb83f-8523-44db-88c4-26eeaa63a6b1` (historical reference: `</home/HuntressCTF/work/day-26/binary/9a8bb83f-8523-44db-88c4-26eeaa63a6b1>`; not included).
