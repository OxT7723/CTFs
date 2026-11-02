> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Persistent state and completion rules

- Each existing root-level `NN-Name/challenge_state.json` is the local machine-readable record; `readme.md` is the human-readable write-up. Do not impose a new schema until inspecting actual state files and existing sync code.
- Track confirmed/incorrect answers, current candidates, attempt/mode IDs, useful evidence, remaining questions, and methodology separately from ephemeral instance-specific values. Never store tokens or bearer headers.
- A challenge is fully completed only if ALL modes actually offered by the authoritative Game Master for that challenge are confirmed complete. If only Single Solve exists, its completion may be sufficient. Unknown/unavailable is not automatically solved or unsolved: represent uncertainty explicitly.
- Preserve partial progress. A completed Single Solve with pending Time Trial/Mastery is ACTIVE, not fully archived.
- A compact challenge index is OPTIONAL; do not invent one or treat it as authoritative before inspecting `huntress_sync.py`, `gm.py`, the root README, and actual state shape. If implemented, generate it with Python, never by dumping all JSON files into Codex context. Include path, ID, offered modes, per-mode status, last sync, and completion state.
- Completed folders remain at their existing paths. Do not relocate, rename, delete, or rehash them automatically.
- Do not reanalyze historical artifacts or load verbose failed-attempt logs in routine sync/solve. Read them only for explicit review, debugging, or technique reuse.
- Keep generated sections clearly bounded; preserve all user-authored text and historic evidence.
