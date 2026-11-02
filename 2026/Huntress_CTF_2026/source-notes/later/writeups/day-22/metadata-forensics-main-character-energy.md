> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 22 Metadata Forensics — Main Character Energy

All three regular modes returned `CORRECT`; each status response lists every
answer ID as accepted. The Time Trial and Mastery attempts were regular untimed
attempts (`run_for_time: false`, no deadline).

| Mode | Attempt | Accepted | Assigned artifact |
| --- | --- | ---: | --- |
| Single Solve | `e6cf9743-1048-4dde-b2ee-463f2f01c238` | 1 / 1 | metadata-day-22-evidence.zip (retired artifact link; see artifact inventory) — SHA-256 `8cbaee5dd7800c8afd80ae9030b3fc419b965dd3b9f63ce2489cd4e96f64343a` |
| Time Trial | `d7ca2b58-e312-4d0d-b1d0-5104552524ca` | 27 / 27 | evidence.zip (retired artifact link; see artifact inventory) — SHA-256 `1fffc92693cbbbd8625d40c5eee82cf3001b8da2db8ac47ea29af3e6b3118e34` |
| Mastery | `53b83b00-4298-44e1-9e45-688a266d6454` | 162 / 162 | metadata-forensics-day-22-main-character-energy-mastery.zip (retired artifact link; see artifact inventory) — SHA-256 `08511f61e5ca539f294f7d6e350be0a4d72ae060d3966c8afafc3203156a95f3` |

The Single Solve JAR's main manifest section specifies
`Main-Class: arena.evidence.ArtifactMain`.

Added reusable readers for JAR manifest `Main-Class` attributes and Android
APK package names. APK extraction uses `aapt dump badging`. The shared runner
uses these helpers for the corresponding answer IDs.

The Game Master submission and status responses contain no pending-scoring
indicator or point total. Attempt records, downloaded artifacts, candidates,
submissions, and status responses are saved under
`attempt-records/metadata-forensics-day-22-main-character-energy/`.
