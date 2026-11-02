# Room Forty-Seven

Day 15 · Warmups · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 15 Warmups: Room Forty-Seven

Completed Single Solve, Time Trial, and Mastery through the regular untimed
routes. The Game Master reports `CORRECT` for all three; Mastery accepted all
73 answers, and no result was pending.

The numbered-fragment decoder needed codec 15, ROT47. Adding it to
`warmup-tools/decode_base64_layers.py` handled the Mastery bundle's final row.
The first Mastery submission was incorrect because that codec was missing;
after the reusable decoder update, the same attempt completed successfully.
The runner now checks that decoded text matches the live answer format before
submitting, preventing malformed candidates from being sent.

## Retained sources

- [later/writeups/day-15/warmups-room-forty-seven.md](../../source-notes/later/writeups/day-15/warmups-room-forty-seven.md)
