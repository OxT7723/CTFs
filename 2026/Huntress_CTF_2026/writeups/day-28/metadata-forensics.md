# Where It All Began

Day 28 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Single Solve completed with `CORRECT` (1/1). The resumed assignment was
already accepted for this team and had no deadline.

| Attempt | Artifact | SHA-256 |
| --- | --- | --- |
| `9495ed82-21b4-4ecd-b644-8dac14620e40` | metadata-day-28-evidence.zip (private download link removed) | `1b305bfd7e3fb5cc679b65fd8c8ac2e6344135064f6b4b70c7fa6c3c82753ce6` |

The question targets `disk-001.img`. Its LBA 1 contains the GPT signature.
Read the GPT header's partition-array location, entry count, and entry size;
collect the starting LBA from each allocated entry in table order. Submit
that sequence as a compact JSON array.

The assigned archive, candidate answer, and status response are saved under
`metadata-forensics-tools/attempt-records/metadata-forensics-day-28-where-it-all-began/9495ed82-21b4-4ecd-b644-8dac14620e40` (source reference: `/home/HuntressCTF/metadata-forensics-tools/attempt-records/metadata-forensics-day-28-where-it-all-began/9495ed82-21b4-4ecd-b644-8dac14620e40`; not included).

## Retained sources

- [later/writeups/day-28/metadata-forensics-where-it-all-began.md](../../source-notes/later/writeups/day-28/metadata-forensics-where-it-all-began.md)
