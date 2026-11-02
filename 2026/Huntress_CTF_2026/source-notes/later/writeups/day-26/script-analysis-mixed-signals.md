> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 26 Script Analysis — Mixed Signals

**Challenge:** 📜 Mixed Signals  
**Base ID:** `script-analysis-day-26-beam-message-flow`  
**Description:** “An Erlang escript passes messages between processes, and some of its indicators look suspiciously familiar. Trace the message flow, and separate the true cross-language indicators from deterministic collision decoys planted to look like old friends.”

The live start responses are preserved in each attempt record. They contain
the complete player-facing question wording, exact answer IDs, artifact
references, answer formats, normalizations, mode guidance, and other fields.
This is especially useful for Mastery, whose response contains all 16,770
questions.

## Assigned artifacts

Each archive belongs to its own mode attempt. The regular Time Trial and
Mastery attempts were untimed; `run_for_time` was not requested.

| Mode | Artifact and purpose | SHA-256 |
| --- | --- | --- |
| Single Solve | Download evidence.zip (retired artifact link; see artifact inventory) — script-analysis samples for the message-flow and indicator questions. | `f2c857779744caf0a2f99191e3bce6795ee8e839241a121e468fac48d7c8dce5` |
| Time Trial | Download evidence.zip (retired artifact link; see artifact inventory) — fresh regular variant of the same analysis assignment. | `7768d4196a078a9be2bf95342512953a2231ef34900876723faf5c0008935913` |
| Mastery | Download script-analysis-day-26-beam-message-flow-mastery.zip (retired artifact link; see artifact inventory) — ten bundled sets of script-analysis samples. | `b0adca5eb4cb6e2bc6b4733bab4787c39e27c9bb742f61f4054a972de9ead6cf` |

## Questions and answer formats

There were 1,615 Single Solve questions, 1,677 Time Trial questions, and
16,770 Mastery questions (ten sets). The API provides one answer ID per
question. Formats include exact artifact-derived text and enumerated values;
the exact format, accepted values where applicable, normalization, and
artifact filename are recorded with every question in the live response.

Example question from Single Solve:

- **Question:** “What scenario best describes resource-sample.ps1?”
- **Answer ID:** `resource-scenario`
- **Format:** enum — `resource_hijacking`, `synthetic_collection`, or `synthetic_impact`
- **Normalization:** trim

Example from Time Trial and each corresponding Mastery set:

- **Question:** “What exact reserved-domain URL is embedded in d8219f.ps1?”
- **Answer ID:** `powershell-d8219f-url` (Mastery example: `set1.powershell-d8219f-url`)
- **Format:** exact text, artifact-derived value only
- **Normalization:** trim

Full question lists and exact submission fields:

- Single Solve start response (historical reference: `../../work/day-26/script-analysis/b94b45e8-cb11-445d-a1d3-e3ad8679434e/start-response.json`; not included)
- Time Trial start response (historical reference: `../../work/day-26/script-analysis/9a9adeb1-fa31-412c-a5f8-9e1da7b53e17/start-response.json`; not included)
- Mastery start response (historical reference: `../../work/day-26/script-analysis/49eb4a2b-271f-4af6-93b1-506be4e661b1/start-response.json`; not included)

**Done** meant submitting every answer under its exact answer ID. Each mode
returned `CORRECT`, with no unresolved answers.

## Results

| Mode | Attempt | Accepted | Questions | Game Master |
| --- | --- | ---: | ---: | --- |
| Single Solve | `b94b45e8-cb11-445d-a1d3-e3ad8679434e` | 1,615 | 1,615 | `CORRECT` |
| Time Trial | `9a9adeb1-fa31-412c-a5f8-9e1da7b53e17` | 1,677 | 1,677 | `CORRECT` |
| Mastery | `49eb4a2b-271f-4af6-93b1-506be4e661b1` | 16,770 | 16,770 | `CORRECT` |

The existing `script-analysis-tools/run_modes.py` and
`script_analysis_solver.py` handled all three assigned archives without
changes. The runner downloaded each attempt's assigned bytes, verified the
archive hash, generated candidates from the live questions, and saved the
candidate map and submission/status responses in the attempt record.

Fresh Game Master status requests and the filtered challenge list confirm all
three modes are solved. The responses contained no `pending` scoring status,
but the proxy did not expose a CourseStack point total, so the ledger posting
could not be independently verified here.
