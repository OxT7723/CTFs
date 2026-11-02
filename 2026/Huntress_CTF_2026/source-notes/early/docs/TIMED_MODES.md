> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Time Trial and Mastery

## Before the timer
- Read only target README/state, current solver, concise methodology, and reusable failure rules. Do NOT load expired attempts, historical artifacts, all old answers, or other completed challenges.
- Ensure tooling, parsing, archive extraction, current-answer-ID mapping, and submission path are ready. Prefer local offline tests on retained representative samples.
- Do not start/retry a short timer merely to explore an artifact format unless unavoidable.

## During the timer
1. Start/resume the current mode; capture current attempt ID, deadline, and answer IDs.
2. Fetch the CURRENT artifact/input once. A new mode or retry may produce new material.
3. Run the prepared parser/solver directly; compute only values needed for answers or a specific safety check.
4. Map current outputs to CURRENT answer IDs and submit efficiently, preferably as one confident batch.
5. Persist accepted/remaining results and any useful diagnostic evidence.

- Avoid repeated `file`, `strings`, hashing, listing, decompilation, manual extraction, or exploratory loops that the solver doesn't need.
- Avoid serial answer-probing and speculative bulk guesses. HTTP 429 means stop new attempts/submission experiments and work offline until an appropriate cooldown.
- If a new variant breaks the solver, preserve useful evidence, debug offline, test, then retry. Don't burn repeated timers rediscovering the same failure.

## Retention
- Preserve Single Solve original artifact as a reproducible reference where practical.
- Retain timed artifacts only for unresolved failures, new variants, regression tests, or meaningful learning. Do not automatically delete existing files.
- Promote reusable methodological lessons into solver/README; don't carry stale instance-specific values into future attempts.
