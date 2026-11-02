> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 14 Warmups: Seven Steps

Challenge ID: `warmups-day-14`

Completed Single Solve, Time Trial, and Mastery. The Mastery timed submission
was incorrect within its deadline because the decoder lacked row 14; the
supported untimed practice continuation completed all 68 questions.

The single artifact uses Caesar shift −7. Mastery provides numbered fragments
whose row numbers select codecs 1–13 from the existing Warmups decoder, then
uses Caesar shift −7 for row 14. The decoded fragments join into the instruction
and answer slug. `warmup-tools/run_modes.py` extracts each assigned artifact,
decodes it, derives the slug from the live answer format, submits by the exact
answer IDs, and saves the Game Master responses under `work/day-14/warmups/`.

The decoder is reusable and keeps artifact-specific values out of its logic.
The accepted Game Master status for all three modes was `CORRECT`; the final
responses did not report scoring as pending.
