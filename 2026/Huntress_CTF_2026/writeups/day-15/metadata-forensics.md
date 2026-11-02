# A Word to the Wise

Day 15 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 15 Metadata Forensics — A Word to the Wise

### Results

All modes returned `CORRECT`; every submitted answer ID was accepted:

| Mode | Attempt | Accepted |
| --- | --- | --- |
| Single Solve | `7cbff865-810d-4b3d-883d-a1869cd9e24f` | 1 / 1 |
| Time Trial | `8d41d4d3-15c3-41cb-b898-e546bb3095ce` | 20 / 20 |
| Mastery | `46878ce2-7a53-4cd1-9635-b08c72006a28` | 100 / 100 |

Time Trial and Mastery used regular attempts (`run_for_time: false`) and had no
deadline. The live status endpoint returned `CORRECT` for every mode, and
`op=list&day=15&lane=metadata-forensics` marks all three solved. No response
reported pending CourseStack scoring.

### Assigned artifacts

- Single Solve: Download metadata-day-15-evidence.zip (private download link removed) — SHA-256 `279a8e98087f8a538f5560aed881723f9da90dc8062619d369dc1234fb48a3eb`.
- Time Trial: Download assigned bundle (private download link removed) — SHA-256 `223f42a169fa8f261b8e318119ded403274b6084bf7ba216ed936c8c2b1a7fad`.
- Mastery: Download assigned bundle (private download link removed) — SHA-256 `f478ac798fdf8c34410128123859b5f04c7a467e273fe6632d53418ffa79245e`.

### Solver updates

The reusable metadata runner now extracts and sorts external OOXML relationship
targets, selects named files such as evidence-note copies within nested bundles,
and computes each mastery set's SHA-256 filename ordering within its own bundle.
The Single Solve answer was accepted with the target array in ascending
lexicographic order. Helper logic is in `metadata-forensics-tools/ooxml_metadata.py`
and `metadata-forensics-tools/run_challenge.py`.

## Retained sources

- [later/writeups/day-15/metadata-forensics-word-to-the-wise.md](../../source-notes/later/writeups/day-15/metadata-forensics-word-to-the-wise.md)
