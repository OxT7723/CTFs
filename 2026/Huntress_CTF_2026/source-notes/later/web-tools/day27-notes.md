> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 27 Web and Web Exploitation

Day 27 released three challenges: Double Spent, Socket to Me, and Forwarded
Misgivings. Each has Single Solve, Time Trial, and Mastery. All nine modes
were completed through regular play; the timed-mode entries had
`run_for_time:false`, no deadline, and were not Hall of Fame attempts.

## Reusable techniques

- **Double Spent:** read the current feature and audit routes from `/api/clues`,
  issue two same-origin POSTs concurrently, then read the audit response.
- **Socket to Me:** use the current `feature_route` and `stream_reference` to
  open a TLS WebSocket with `stream=<stream_reference>` and read the first data
  event.
- **Forwarded Misgivings:** GET the disclosed feature route with
  `X-Forwarded-For: 127.0.0.1`.

Run these with `solve_day27.py`, or use `auto_solve_target.py` for automatic
selection. Solvers save response bodies, SHA-256 hashes, current route clues,
and recovered proofs under `web-tools/evidence/`.

## Mastery bundles

Mastery targets can mix vulnerability types instead of repeating the named
challenge. Inspect each assigned target and select a solver from its own clues
and behavior. The existing tools cover backup exposure, IDOR, SQL injection,
path traversal, and the Day 27 techniques above. Submit each recovered proof
under the exact `answer_ids` returned for that attempt.

## Completion

The Game Master reports `result: CORRECT` and all answer IDs accepted for all
nine Day 27 entries. Its list response marks all nine solved. Time Trial and
Mastery status report `run_for_time:false`; no score response contained a
pending marker.
