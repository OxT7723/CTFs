# Under Pressure

Day 21 · Warmups · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Under Pressure — Warmups, Day 21

Completed Single Solve, regular untimed Time Trial, and regular untimed
Mastery. All three Game Master status responses returned `CORRECT`; Mastery
accepted all 103 assigned answers.

The blobs use Base64-wrapped gzip followed by numbered mixed-codec text.
Mastery adds independently encoded trailing fragments: infer the shared
three-rail Rail Fence transposition from the assigned set, decode the
UTF-16 BOM and compressed fragments, then assemble each slug and validate it
against the live answer format.

The reusable implementation is in `warmup-tools/decode_base64_layers.py`.
`warmup-tools/run_modes.py` resumes the current attempt, downloads and
hash-checks its artifact, builds answers using live answer IDs, submits them,
and saves the response and artifact under `work/day-21/warmups/<attempt-id>/`.

The Time Trial and Mastery attempts used the default regular untimed pool;
no Hall of Fame timed run was requested. The Game Master responses confirmed
completion but did not include a separate CourseStack points total.

## Retained sources

- [later/writeups/day-21/warmups-under-pressure.md](../../source-notes/later/writeups/day-21/warmups-under-pressure.md)
