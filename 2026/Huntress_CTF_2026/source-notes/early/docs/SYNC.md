> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Repository synchronization and architecture

## Current layout
- Challenge directories are root-level names like `04-Dim_and_Dimmer/`, `05-Hatch_Careful/`, and `07-Percent_Chance/`, NOT `challenges/day-N/`.
- Each normally has `challenge_state.json` and `readme.md`; some contain solvers, APK/ELF/ZIP artifacts, `artifacts/{single_solve,time_trial,mastery}/`, extracted trees, and historical attempts.
- Root contains `gm.py`, `huntress_sync.py`, legacy `coursestack_sync.py`, `README.md`, `game_master/`, `Day1/`, `Welcome/`, and helper folders. Preserve conventions; do not migrate or rename as part of a context optimization.

## Normal sync
- Prefer existing `huntress_sync.py`/`gm.py`. Inspect their code narrowly before modifying behavior; don't replace working code just because a new architecture is described here.
- Query authenticated public Game Master for currently available challenges/status, discover new days and changed metadata, create only missing challenge directories/state/write-ups, and update the root index safely.
- Preserve existing manual notes, solved data, scripts, artifacts, and historic attempts. Do not delete work if an API response temporarily omits a challenge.
- Sync must not automatically submit answers or reanalyze/download every completed artifact.
- Use the existing root `README.md` generated challenge table as the navigation/status index; do not create a second index by default. Aggregate status with Python and print a short summary: total, complete, active, new, changed, errors. Avoid printing all challenge states or an unrestricted `tree`.
- If adding a machine-readable index, validate real existing state schema first, write atomically, and avoid regenerating it from verbose text read by the model.

## Architecture or migration work (ONLY when explicitly requested)
- Inspect root scripts, README, representative directories, generated-content boundaries, and state schema before proposing changes. Use bounded directory listings, never a full artifact-content dump.
- Prefer minimal changes and existing naming conventions. No automatic commits, pushes, destructive Git operations, large renames, or rewriting user notes.
- For new automation, keep shared API authentication/errors in `gm.py` and separate sync from solve. Use sensible timeouts and never leak credentials.
