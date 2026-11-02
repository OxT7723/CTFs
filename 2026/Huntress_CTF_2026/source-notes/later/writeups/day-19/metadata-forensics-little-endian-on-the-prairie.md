> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 19 Metadata Forensics — Little Endian on the Prairie

Single Solve completed with `CORRECT` (1/1). The attempt was already accepted
for this team; the resumed assignment included its artifact, which was
downloaded and checked against the API SHA-256. No timer was running.

| Attempt | Artifact | SHA-256 |
| --- | --- | --- |
| `acf587e5-895f-47f4-9302-47b93ed1956e` | metadata-day-19-evidence.zip (retired artifact link; see artifact inventory) | `f0d3930a139e5a1de770a34b2fb278422caf64110757ab339a073df7f749b86c` |

The question targets `collector-001.elf`. Read the ELF header directly:
`e_machine` is the 16-bit little-endian field at offset 18. Format the value
as lowercase hexadecimal with a `0x` prefix, as requested. The Game Master
status confirms the answer was accepted.

The start response, downloaded bundle, candidate answer, and status are saved
under
`metadata-forensics-tools/attempt-records/metadata-forensics-day-19-little-endian-on-the-prairie/acf587e5-895f-47f4-9302-47b93ed1956e` (historical reference: `</home/HuntressCTF/metadata-forensics-tools/attempt-records/metadata-forensics-day-19-little-endian-on-the-prairie/acf587e5-895f-47f4-9302-47b93ed1956e>`; not included).
