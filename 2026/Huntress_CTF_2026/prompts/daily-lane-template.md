# Daily category assignment — reusable adaptation

> This template was prepared after the event from the saved daily prompts. Fill in the fields and adapt the platform operations before use.

## Assignment

- Event: `[EVENT]`
- Authorized category/lane: `[LANE]`
- Assigned day: `[DAY]`
- Release date and time, including timezone: `[RELEASE]`
- Authorized challenge environment: `[SCOPE]`
- Existing workspace and tool directory: `[PATH]`
- Allowed gameplay: regular, non-ranked attempts only unless separately authorized.

## Prepare

Read the current challenge index and only the notes and tools relevant to this assignment. Confirm the platform's current operation names, mode behavior, and deadlines. Do not assume that a mode named Time Trial is necessarily timed, or that a retry is untimed.

Inspect existing deterministic solvers before writing another one. Prepare dependencies and input handling before starting an attempt that has a deadline. If waiting for release, use a bounded check that respects the service's documented rate limits and stops after `[MAXIMUM_WAIT]`.

## Solve and verify

Use the current attempt's artifacts, question IDs, and answer formats. Reuse extraction methods rather than historical answer values. Match every candidate answer to evidence from the assigned artifact.

Retain answers already accepted within the same attempt. If a grouped submission is partly incorrect, inspect per-answer results instead of discarding accepted progress. After `[REASSESS_AFTER]` failed submissions for one answer, reassess the method. After `[STOP_AFTER]`, document the blocker and continue other authorized work.

Do not initiate ranked attempts or potentially timed legacy retries without explicit authorization for that phase. Check supported regular/practice behavior and remaining attempt pools instead of probing through destructive or attempt-consuming operations.

Verify the final service result and, where separately available, the scoring result. Record uncertainty if either cannot be observed.

## Improve the reusable solver

Keep parsing and decoding separate from platform requests. Avoid fixed artifact names, expected hashes, instance-specific answers, and order assumptions that are not part of the format. Validate behavior on additional supplied or explicitly authorized fresh artifacts where available.

When measuring speed, record what the timer covers: local solver execution, full client wall time, or the platform's official recorded time. Do not label one measurement as another.

## Save the work

Save a concise method, commands or relevant code, the evidence supporting key conclusions, corrections to earlier hypotheses, and the completion result. Preserve useful scripts and notes. Keep secrets, connection settings, and transient download capabilities out of public documentation.

Conclude with solved modes, observed scoring status, unresolved questions, solver changes, and any missing evidence needed for a reproducible writeup.
