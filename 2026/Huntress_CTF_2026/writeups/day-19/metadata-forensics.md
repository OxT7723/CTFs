# Little Endian on the Prairie

Day 19 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Single Solve completed with `CORRECT` (1/1). The attempt was already accepted
for this team; the resumed assignment included its artifact, which was
downloaded and checked against the API SHA-256. No timer was running.

| Attempt | Artifact | SHA-256 |
| --- | --- | --- |
| `acf587e5-895f-47f4-9302-47b93ed1956e` | metadata-day-19-evidence.zip (private download link removed) | `f0d3930a139e5a1de770a34b2fb278422caf64110757ab339a073df7f749b86c` |

The question targets `collector-001.elf`. Read the ELF header directly:
`e_machine` is the 16-bit little-endian field at offset 18. Format the value
as lowercase hexadecimal with a `0x` prefix, as requested. The Game Master
status confirms the answer was accepted.

The start response, downloaded bundle, candidate answer, and status are saved
under
`metadata-forensics-tools/attempt-records/metadata-forensics-day-19-little-endian-on-the-prairie/acf587e5-895f-47f4-9302-47b93ed1956e` (source reference: `/home/HuntressCTF/metadata-forensics-tools/attempt-records/metadata-forensics-day-19-little-endian-on-the-prairie/acf587e5-895f-47f4-9302-47b93ed1956e`; not included).

## Retained sources

- [later/writeups/day-19/metadata-forensics-little-endian-on-the-prairie.md](../../source-notes/later/writeups/day-19/metadata-forensics-little-endian-on-the-prairie.md)
