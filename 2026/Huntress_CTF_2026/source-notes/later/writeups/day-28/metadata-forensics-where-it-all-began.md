> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 28 Metadata Forensics — Where It All Began

Single Solve completed with `CORRECT` (1/1). The resumed assignment was
already accepted for this team and had no deadline.

| Attempt | Artifact | SHA-256 |
| --- | --- | --- |
| `9495ed82-21b4-4ecd-b644-8dac14620e40` | metadata-day-28-evidence.zip (retired artifact link; see artifact inventory) | `1b305bfd7e3fb5cc679b65fd8c8ac2e6344135064f6b4b70c7fa6c3c82753ce6` |

The question targets `disk-001.img`. Its LBA 1 contains the GPT signature.
Read the GPT header's partition-array location, entry count, and entry size;
collect the starting LBA from each allocated entry in table order. Submit
that sequence as a compact JSON array.

The assigned archive, candidate answer, and status response are saved under
`metadata-forensics-tools/attempt-records/metadata-forensics-day-28-where-it-all-began/9495ed82-21b4-4ecd-b644-8dac14620e40` (historical reference: `</home/HuntressCTF/metadata-forensics-tools/attempt-records/metadata-forensics-day-28-where-it-all-began/9495ed82-21b4-4ecd-b644-8dac14620e40>`; not included).
