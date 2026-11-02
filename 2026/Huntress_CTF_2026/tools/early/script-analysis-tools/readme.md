> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Script analysis helpers

These tools collect the completed day specific workflows and one canonical
static parser for future Huntress CTF Script Analysis challenges.

## Main reusable solver

- `script_analysis_solver.py` — canonical descriptor parser and answer builder.
  It reads extracted artifact files as data, never executes specimens, handles
  numbered Mastery sets, validates that candidate IDs exactly match the API
  question IDs, rejects empty candidates, and checks enum answers against the
  API's accepted values.
- `09-solve.py` — compatibility command line wrapper for the Day 09 filename.
- `07-solve_node_by_node.py` — Day 07 response adapter that imports the
  canonical parser.
- `07-run_timed.py` — proxy based timed runner. It stores per-attempt evidence
  under the matching `work/day-NN/attempt-records/` folder and saves the
  post-submit status so accepted IDs come from the Game Master.

For a saved response and already extracted artifacts:

```sh
python3 script-analysis-tools/script_analysis_solver.py extracted-artifacts \
  --answer-map start-or-status.json \
  --output candidate-answers.json
```

For Day 07:

```sh
python3 script-analysis-tools/07-solve_node_by_node.py start-response.json extracted-artifacts \
  --mode single_solve --output answers.json
```

The day specific scripts below are retained as workflow history and examples.
Update the canonical parser when adding reusable decoding or answer logic;
keep challenge specific wrappers when they preserve useful invocation formats.

## Day specific scripts

- Day 03: `03-solve_expansion.py`, `03-run_mastery.py`.
- Day 04: `04-decode_dimmer.py`, `04-build_dimmer_answers.py`,
  `04-run_time_trial.py`, `04-run_time_trial_fast.py`,
  `04-run_mastery_fast.py`.
- Day 05: `05-solve_hatch.py`, `05-static_recover.py`,
  `05-run_time_trial.py`, `05-run_mastery.py`.
- Day 06: `06-timed_solver.py`, `06-run_timed.py`; the current complete
  single solve candidate builder is `work/day06/build_answers.py`.
  `work/day06/build_answers_historical.py` preserves the earlier grouped
  candidate-map workflow.
- Day 09: `09-solve.py` remains available as a compatibility entry point.

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
