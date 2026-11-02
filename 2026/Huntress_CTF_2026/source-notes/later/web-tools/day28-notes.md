> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 28 Web Exploitation

Both released challenges and all six modes are complete:

- **Fail Open Friday:** malformed remote policy decoding returns the
  fail-open evidence. Read the target's policy format route and use its
  disclosed query field and prefix.
- **If a Breach Falls in a Log:** run the protected export, compare its
  operation with the event recorded for that export, then submit the
  discrepancy to the disclosed report route.

Time Trial attempts used regular untimed play (`run_for_time:false`). The
server requires solving Time Trial before it opens Mastery.

## Mastery bundles

Each five-target bundle mixed challenge types. Across the two bundles, the
targets used backup exposure, IDOR, SQL injection, path traversal, and the
Day 28 challenge's named technique. Select a solver from each current target's
own pages and route clues; do not assume the named vulnerability repeats in
Mastery.

`solve_day28.py` handles the two new techniques. `auto_solve_target.py` now
dispatches those clue patterns and recognizes PHP document viewers for bounded
path traversal. Existing dispatch covers backup exposure, IDOR, and SQL
injection.

Game Master status returned `CORRECT` for all six entries, every answer ID was
accepted, and no scoring response was pending.
