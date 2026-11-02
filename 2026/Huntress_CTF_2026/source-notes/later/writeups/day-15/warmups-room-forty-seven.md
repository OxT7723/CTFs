> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 15 Warmups: Room Forty-Seven

Completed Single Solve, Time Trial, and Mastery through the regular untimed
routes. The Game Master reports `CORRECT` for all three; Mastery accepted all
73 answers, and no result was pending.

The numbered-fragment decoder needed codec 15, ROT47. Adding it to
`warmup-tools/decode_base64_layers.py` handled the Mastery bundle's final row.
The first Mastery submission was incorrect because that codec was missing;
after the reusable decoder update, the same attempt completed successfully.
The runner now checks that decoded text matches the live answer format before
submitting, preventing malformed candidates from being sent.
