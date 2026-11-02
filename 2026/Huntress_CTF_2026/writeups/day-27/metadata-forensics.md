# Packet Loss Prevention

Day 27 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 27 Metadata Forensics — Packet Loss Prevention

**Challenge ID:** `metadata-forensics-day-27-packet-loss-prevention`

**Description:** Packet captures, exports, and host artifacts describe the
same incident from different angles. Count traffic, reject malformed captures,
and find the host narrative missing network evidence.

All three released modes completed with `CORRECT` on the regular untimed
routes. The assigned Single Solve capture contains three PCAP records; the
third has fewer captured bytes than its original wire length, which is valid
snap-length truncation and still counts as a packet. Its accepted answer was
`3` under `d27-pcap-001-pcap-packet-count`.

| Mode | Attempt | Accepted | Artifact and SHA-256 |
| --- | --- | ---: | --- |
| Single Solve | `c0b28533-0f78-43d8-8a3f-d0368b2f9d6e` | 1 / 1 | metadata-day-27-evidence.zip (private download link removed) — `3aff14dbde990236abbb1cc9ffb5f71a96b910070e1854037854336fdddc5e32` |
| Time Trial | `c877aeab-e4f1-4216-98aa-eb29bdaffc82` | 32 / 32 | evidence.zip (private download link removed) — `c9a3bdafdda81eff4a2f4707cf5f7c09ea2321435e2c9cbf926d18e4f352bcfd` |
| Mastery | `637e9175-0be8-4331-bf83-b9eab54fb6c0` | 352 / 352 | evidence.zip (private download link removed) — `27b84e93769abee8f97c86dfc47a2a93d875816d26eca19cf498f0c0b2b39001` |

Time Trial and Mastery both reported `run_for_time: false` and no deadline.
Each Game Master status check returned `CORRECT`; none reported scoring as
pending. The status responses did not include a CourseStack point total.

The live questions, exact answer IDs and formats, candidate answers, and
service responses are preserved under
`metadata-forensics-tools/attempt-records/metadata-forensics-day-27-packet-loss-prevention/` (source reference: `/home/HuntressCTF/metadata-forensics-tools/attempt-records/metadata-forensics-day-27-packet-loss-prevention/`; not linked in this draft).

## Retained sources

- [later/writeups/day-27/metadata-forensics-packet-loss-prevention.md](../../source-notes/later/writeups/day-27/metadata-forensics-packet-loss-prevention.md)
