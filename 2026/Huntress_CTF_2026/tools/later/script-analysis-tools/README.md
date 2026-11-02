> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Script analysis helpers

This directory contains the maintained Script Analysis solver and general
mode runner. Earlier challenge-specific scripts are kept in
`archive/day-specific/` (historical reference: `archive/day-specific/`; not included) as historical examples.

## Main reusable solver

- `script_analysis_solver.py` — canonical descriptor parser and answer builder.
  It reads extracted artifact files as data, never executes specimens, handles
  numbered Mastery sets, validates that candidate IDs exactly match the API
  question IDs, rejects empty candidates, and checks enum answers against the
  API's accepted values.
- `09-solve.py` — compatibility command line wrapper for the Day 09 filename.
- `run_modes.py` — maintained proxy-based runner for randomized timed modes.

For a saved response and already extracted artifacts:

```sh
python3 script-analysis-tools/script_analysis_solver.py extracted-artifacts \
  --answer-map start-or-status.json \
  --output candidate-answers.json
```

The older Day 03–07 and Day 10 scripts are grouped in
`archive/day-specific/` (historical reference: `archive/day-specific/`; not included); see its README for an
inventory.

Add reusable decoding or answer logic to `script_analysis_solver.py`; keep
challenge-specific snapshots in the archive when they are useful for reference.

## Solver history

- Day 02: `script_analysis_solver.py` processed the PowerShell and JScript
  specimens for Host With the Most. The ranked Time Trial and Mastery results,
  artifact hashes, and legacy-route training limits are in
  `../writeups/day-02/script-analysis-host-with-the-most.md`.
- Day 06: the current complete Single Solve candidate builder is
  `work/day06/build_answers.py`. `work/day06/build_answers_historical.py`
  preserves an earlier grouped candidate-map workflow.
- Day 08: `work/day-08/build_lost_candidates.py` delegates Batch expansion
  classification to `script_analysis_solver.py`; its saved Mastery submission
  history and accepted-answer map remain under `work/day-08/`.
- Day 11: `script_analysis_solver.py` reconstructs the 811-question
  Native API Semantics evidence set. Its Batch expansion classifier
  distinguishes CALL expansion in `hN` fragment assembly from other
  delayed-expansion specimens. Incorrect submission groups should be split
  and reconciled by accepted answer IDs.
- Day 15: `script_analysis_solver.py` classifies Batch expansion from the
  descriptor-reconstruction assignment itself. This avoids mistaking
  `EnableDelayedExpansion` in unrelated code for the expansion form used to
  rebuild the descriptor; CALL double expansion, percent expansion, delayed
  expansion, and FOR-indirect expansion are handled separately.
- Day 24: `script_analysis_solver.py` handled the JSP host and polyglot
  descriptors through its existing generic decoding and answer mapping.
  `writeups/day-24/script-analysis-web-of-lies.md` records the completed
  Single Solve, Time Trial, and Mastery attempts.

For a fresh randomized Day 11 Time Trial or Mastery assignment, install the
AES ZIP reader and pass the exact challenge ID from the Game Master:

```sh
python3 -m pip install -r script-analysis-tools/requirements.txt
python3 script-analysis-tools/run_modes.py "$CHALLENGE_ID"
```

For a fresh ranked timed variant when explicitly requested, use
`--retry --run-for-time --fast`. `--retry` advances the mode to another
variant, while `--run-for-time` asks the Game Master for the timed Hall of
Fame route. The runner does not automatically replay an `op=retry` request
after a network error, since doing so could consume more than one variant.

The runner preloads its parser and AES ZIP dependency before starting an
attempt, then reuses an HTTP session for the single-artifact route. It
downloads multiple assigned artifacts concurrently, validates each archive,
extracts it with the event password `infected`, builds candidates from the
live questions, and splits incorrect answer groups into individual
submissions. It records download, processing, submission, and status-request
timings in the run summary. Transient 502,
503, 504, and URL errors are retried with bounded backoff, and each completed
submission batch is checkpointed in `submission-outcomes.json` so a later
failure does not erase the progress record. The final response is saved in
`final-submission-response.json`, including any scoring status.

For numbered Mastery sets, the runner decodes nested AES ZIPs in memory with
up to four workers and writes the extracted specimens to the attempt record
after submission. The solver caches each specimen's text and repeated source
classifications during answer generation.

To rebuild the saved Day 06 candidate map from its verified response and
extracted assigned archive:

```sh
python3 work/day06/build_answers.py
```

## Submission reconciliation

Treat each aggregate submission result as a report about that request. Do not
mark every answer in a group invalid based on one group's result. After any
submission, compare the exact IDs with the Game Master's current
`accepted_ids`; the timed runner records this status separately. Older
`answers-accepted-*.json` and pending files remain useful history, while a
fresh status response is authoritative for current progress.

Timed attempts use the supported proxy, and the runner records its assigned
archive, hash, candidate map, submission response, and status in the relevant
day folder. Before reusing a day specific example, check its challenge ID,
artifact handling, and mode against the current assignment.
