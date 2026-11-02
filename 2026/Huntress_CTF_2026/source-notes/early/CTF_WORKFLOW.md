> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Huntress CTF 2026 - Workflow router

This is the short operational guide. Detailed instructions are separated by task so Codex does not load a large manual for every challenge.

## Normal request: Solve Day N / Challenge Name
1. Read the root `README.md` challenge table to resolve the exact existing root-level `NN-Name/` folder. Follow its relative `readme.md` link; do not recursively scan the repo. The index is a navigation aid, not proof of current live status.
2. Read only that folder's `readme.md`, `challenge_state.json`, and relevant existing solver scripts. Check Game Master status and current available modes.
3. Read `docs/SOLVE.md` for Single Solve. If a timed mode is next, read `docs/TIMED_MODES.md` and prepare the solver BEFORE starting the timer.
4. For each new attempt, use current Game Master response, answer IDs, and artifacts. Reuse solving METHODS, not instance-specific answers.
5. Submit when solving was requested, persist progress, update the target write-up/state, and update the root index only through an existing safe updater (or make a minimal targeted change within its generated section). After all offered modes are confirmed complete, finalize a publication-ready write-up before ending the session.
6. Keep the same Codex session for all modes of this challenge. Resume it when revisiting this challenge if practical.

## Other tasks
- Sync, discover new days, or repair index: `docs/SYNC.md`.
- Interpret or modify completion/status data: `docs/STATE.md`.
- API, authentication, pairing, or new API operation: `docs/GAME_MASTER.md`.
- Initial repo-wide architecture work: `docs/SYNC.md` (only when explicitly requested).
- Organizer-specific gameplay question: `docs/HUNTRESS_ORIGINAL_AGENTS.md` (on demand).

## Root challenge index
- The root `README.md` is a small generated challenge table with links and Single Solve / Time Trial / Mastery columns. It is useful to read for challenge selection and progress checks.
- Preserve text outside `<!-- huntress:index:start -->` and `<!-- huntress:index:end -->`; do not regenerate the table manually when the existing sync script can update it.
- Treat `?`, `Historical`, `Solved`, and checkmarks according to actual state and Game Master; do not assume every row has three modes.

## Completed challenges
- Do not move or delete completed challenge folders. Their `readme.md`, state, scripts, and artifacts remain available for explicit review and technique reuse.
- Do not load completed challenges in normal solving sessions or bulk status checks. Have Python or the existing sync script aggregate status into a short report and maintain the existing root README index; do not paste all state JSON into context.
- A challenge can have Single Solve completed while Time Trial or Mastery remains open: do not archive it prematurely.

## Archive handling
- When working with ZIPs, consult `docs/ARCHIVES.md`. Prefer `7z` and try `infected` for password-protected challenge archives before other approaches.

## Non-negotiable rules
- No secret exposure, destructive changes, blind execution of artifacts, or unauthorized Git push.
- Do not overwrite user notes; preserve generated/user content boundaries.
- Do not infer current answers or completion from historical artifacts alone.
- Existing code and API responses are authoritative for their own behavior; inspect selectively when needed.
