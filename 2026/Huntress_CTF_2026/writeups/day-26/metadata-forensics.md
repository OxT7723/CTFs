# Before You Go

Day 26 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 26 Metadata Forensics — Before You Go

**Challenge ID:** `metadata-forensics-day-26-before-you-go`

**Description:** Prefetch evidence records what Windows prepared to execute
even after filenames changed. Recover executable identities and connect
execution traces to the correct hosts.

All released modes completed with `CORRECT`. The assigned Prefetch trace was
MAM XPRESS-Huffman compressed; its Prefetch header identifies `CMD.EXE`.
The runner now handles compressed Prefetch files from their downloaded bytes.

| Mode | Attempt | Answers | Artifact and SHA-256 |
| --- | --- | ---: | --- |
| Single Solve | `973ca308-08b2-435e-b451-d0e773372b44` | 1 / 1 | metadata-day-26-evidence.zip (private download link removed) — `de23c0842380e7db67a452debc91d6732d0e34072dd5f9bd4db8a7f07538eb0a` |
| Time Trial | `07cc6448-f379-4883-8c59-60e986bc6802` | 31 / 31 | evidence.zip (private download link removed) — `29aa31f400e2fa59164b5354d38830982a1e56fd98989a6922612eb65466bf67` |
| Mastery | `d9d76105-af80-4a4a-aa9a-0d515f807bfc` | 310 / 310 | metadata-forensics-day-26-before-you-go-mastery.zip (private download link removed) — `6d3303769eb963681e5a3bc680b8943716e64c7832f19cb32922d68b9228961c` |

All three runs used regular play (`run_for_time: false` where applicable)
and had no deadline. Single Solve asks `Determine prefetch.executable_name
for trace-001.pf.` Submit the exact artifact-derived text (or literal `none`
if absent) under `d26-prefetch-001-prefetch-executable-name`; the accepted
value was `CMD.EXE`. Time Trial and each of Mastery's ten sets include their
own exact question IDs and formats in the saved live start responses.

All three live status checks returned `CORRECT`; none reported scoring as
pending. The Game Master response did not include a CourseStack point total.

The full questions, answer IDs, formats, and artifact descriptors from each
live start response are preserved in
Single Solve (source reference: `/home/HuntressCTF/metadata-forensics-tools/attempt-records/metadata-forensics-day-26-before-you-go/973ca308-08b2-435e-b451-d0e773372b44/start-response.json`; not linked in this draft),
Time Trial (source reference: `/home/HuntressCTF/metadata-forensics-tools/attempt-records/metadata-forensics-day-26-before-you-go/07cc6448-f379-4883-8c59-60e986bc6802/start-response.json`; not linked in this draft), and
Mastery (source reference: `/home/HuntressCTF/metadata-forensics-tools/attempt-records/metadata-forensics-day-26-before-you-go/d9d76105-af80-4a4a-aa9a-0d515f807bfc/start-response.json`; not linked in this draft).

## Retained sources

- [later/writeups/day-26/metadata-forensics-before-you-go.md](../../source-notes/later/writeups/day-26/metadata-forensics-before-you-go.md)
