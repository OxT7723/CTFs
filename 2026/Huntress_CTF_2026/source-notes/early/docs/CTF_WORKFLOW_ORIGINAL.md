> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Huntress CTF 2026 — Codex Workflow

This repository is my working repository for Huntress CTF 2026.

This file defines how Codex should synchronize, solve, document, and track Huntress CTF challenges.

## Instruction Priority

Before doing challenge work:

1. Read the existing `AGENTS.md` supplied by Huntress.
2. Read this `CTF_WORKFLOW.md`.
3. Read the target challenge's existing `README.md`.
4. Read the target challenge's persistent state and existing solution scripts/files.
5. Preserve existing repository conventions unless there is a strong reason to change them.

If `AGENTS.md` and this file appear to conflict, stop and point out the conflict before making a destructive or significant change.

Do not overwrite existing user notes or completed challenge work.

---

# Environment

Primary environment:

- Kali Linux
- VS Code
- Codex VS Code extension
- Git repository
- Python virtual environment
- Huntress CTF 2026 Game Master API

The Game Master can be accessed directly from Kali over HTTPS after one-time pairing.

Public Game Master endpoint:

```text
https://2026.huntress.ctf.games/
```

Authentication is supplied through the environment variable:

```text
HUNTRESS_GM_TOKEN
```

In Python:

```python
token = os.environ.get("HUNTRESS_GM_TOKEN")
```

Never ask the user to paste the token into Codex chat.

---

# Credential Safety

The pairing token is a secret.

NEVER:

- print it
- log it
- write it into source code
- put it in Markdown
- save it in challenge state
- include it in debugging output
- commit it
- push it
- expose it unnecessarily in process arguments

Assume the user has loaded `HUNTRESS_GM_TOKEN` into the shell environment.

Before commits or pushes, verify that no token or Authorization header has entered the repository.

Do not automatically reset or rotate the pairing token. Pairing reset invalidates the previous token and should only be done when explicitly needed.

---

# Game Master Architecture

There are two Game Master addresses.

## Internal Pairing Endpoint

```text
http://192.0.2.1/huntress-ctf-proxy
```

This is the inside CTF address. It is used for initial pairing and explicit token replacement.

Normal Codex challenge work should not need this address after pairing.

## Public Game Master Endpoint

```text
https://2026.huntress.ctf.games/
```

Use this endpoint with bearer authentication from the local Kali/VS Code/Codex environment.

The Huntress organizer described the intended model as:

```text
Pair on the inside, play on the outside.
```

The public Game Master is intended to allow players to:

- access challenges without keeping Homebase running
- access challenges directly without requiring the normal VPN/SSH jumpbox path for Game Master interaction
- use their own AI/tooling environment without consuming Homebase AI/model credits merely to interact with Game Master

Challenge-specific infrastructure may still expose its own requirements. Follow the current challenge/Game Master information instead of assuming all targets have identical networking behavior.

---

# Game Master API

Known operations include:

```text
GET  ?op=openapi
GET  ?op=list
GET  ?op=list&day=<day>
GET  ?op=list&day=<day>&lane=<lane>
POST challenge start
GET  ?op=status&challenge=<challenge-id>
GET  ?op=artifact&challenge=<challenge-id>
POST answer submission
```

Gameplay POST requests use JSON.

Direct requests use:

```text
Authorization: Bearer <token>
```

The current OpenAPI document is authoritative:

```text
https://2026.huntress.ctf.games/?op=openapi
```

Inspect OpenAPI when:

- initially implementing Game Master support
- API behavior differs from expectations
- Game Master has been updated
- an operation or response format is unclear
- new functionality appears

Do not guess API formats when OpenAPI can answer the question.

The start response may return exact `answer_ids`. Always use the answer IDs returned for the CURRENT attempt.

Submission results may include values such as:

```text
CORRECT
incorrect
accepted
```

`accepted` may indicate partial progress. If `remaining` or equivalent information is returned, persist it and focus subsequent work on unresolved answers.

CourseStack remains the official scoring ledger. If Game Master reports a pending state, do not assume scoring is final until the platform state supports that conclusion.

Some introductory/native CourseStack questions may require submission on the lesson page instead of through Game Master. Follow the challenge instructions.

---

# Primary Goal

The normal workflow should eventually be close to:

```bash
source .venv/bin/activate
python huntress_sync.py
```

followed by a request such as:

```text
Solve Day 4 Table Manners.
```

The user should not normally need to:

1. manually copy challenge JSON from the website
2. manually create challenge directories
3. manually create challenge Markdown files
4. manually download every new artifact
5. manually update the root challenge table

Game Master should become the source for current challenge metadata and state while the repository remains the durable source for investigation notes, scripts, artifacts, write-ups, and historical attempts.

---

# Existing Repository and Code

Existing repository content is valuable.

Earlier tooling may include:

```text
coursestack_sync.py
```

The previous workflow may have used manually obtained JSON.

Before replacing or restructuring anything:

- inspect the entire repository tree
- inspect `AGENTS.md`
- inspect the root README
- inspect current sync scripts
- inspect several challenge directories from different days
- inspect how artifacts are currently stored
- inspect how solved state is currently represented
- inspect existing naming conventions

Prefer refactoring existing working behavior over rewriting everything from scratch.

Preserve useful historical data.

Do not perform large renames or reorganizations merely for stylistic reasons.

---

# Repository Synchronization

Synchronization should query the authenticated public Game Master directly.

It must be safe to run repeatedly.

The synchronization system should:

1. Query all currently available challenges.
2. Discover newly released days.
3. Discover newly added challenges.
4. Detect changed challenge metadata.
5. Create missing challenge directories.
6. Create missing challenge README files.
7. Retrieve challenge status.
8. Update mode/solve status.
9. Download artifacts when appropriate.
10. Preserve existing artifacts and derived analysis.
11. Update the root challenge index.
12. Preserve previous days and historical challenge data.
13. Preserve all manually written notes.
14. Never delete challenge work merely because an API response temporarily omits something.
15. Avoid unnecessary network/download/analysis work.

Do not automatically submit challenge answers as part of a normal repository sync.

Sync and solve are separate operations.

---

# Generated Content vs User Content

Never overwrite user-written notes.

If generated metadata is stored in Markdown, use explicit boundaries such as:

```markdown
<!-- BEGIN GENERATED METADATA -->

...

<!-- END GENERATED METADATA -->
```

Only the generated region may be replaced automatically.

Everything outside generated regions must be preserved.

If the repository already uses another reliable convention, keep it.

---

# Root README

Maintain the root README as a useful challenge index while preserving manually written content.

Useful columns may include:

```text
Day
Lane
Challenge
Single Solve
Time Trial
Mastery
Local Link
```

Adapt to the actual Game Master status model rather than inventing status values.

Do not replace unrelated root README content.

---

# Shared Game Master Client

Prefer a reusable API client rather than duplicating HTTP logic throughout scripts.

A structure such as this is desirable:

```text
gm.py
huntress_sync.py
```

The Game Master client should expose logical operations such as:

```python
gm.openapi()
gm.list_challenges()
gm.list_challenges(day=4)
gm.start(challenge_id)
gm.status(challenge_id)
gm.get_artifact(challenge_id)
gm.submit(challenge_id, answers)
```

Authentication, endpoint handling, errors, timeouts, and response parsing should live in the shared client.

Other tools, including sync scripts and future UI tooling, should reuse it.

Use sensible request timeouts and clear errors. Never include the bearer token in an error message.

---

# Challenge Modes

The normal conceptual progression is:

```text
Single Solve
    ↓
Time Trial
    ↓
Mastery
```

When the user says:

```text
Solve Day <N> <challenge name>.
```

determine the challenge's current state first.

If Single Solve remains unsolved, work on Single Solve.

If Single Solve is complete and Time Trial is next, work on Time Trial.

If Time Trial is complete and Mastery is next, work on Mastery.

Do not skip modes unless Game Master allows/requires it or the user explicitly requests a particular mode.

---

# Critical Rule: Modes May Produce New Instances

Do NOT assume Single Solve, Time Trial, and Mastery use identical files or values.

A new attempt or mode may provide:

- a new artifact
- a new filename
- different hashes
- different embedded constants
- different URLs
- different identifiers
- different credentials
- different randomized values
- different answer IDs
- other new instance-specific data

Therefore:

```text
REUSE:
    solving method
    scripts
    parsing logic
    analysis knowledge
    tool choices
    answer-format knowledge
    methodological lessons

REFRESH/CHECK FOR EACH CURRENT ATTEMPT:
    answer IDs
    artifact/input
    generated values
    hashes when they are themselves required answers
    URLs
    identifiers
    addresses
    flags
    instance-specific constants
```

The goal is to reuse the METHOD, not blindly reuse old instance data.

---

# Single Solve Strategy

Single Solve is primarily the learning and automation phase.

During Single Solve:

- retrieve the current challenge instance
- inspect its artifact/input
- understand what the challenge is testing
- determine how each answer is derived
- identify static versus instance-specific information
- document useful observations
- record useful commands
- track confirmed answers
- track failed answers/approaches
- develop reusable solution scripts where practical
- produce enough documentation to make later modes fast

The ideal outcome is not merely a list of answers.

The ideal outcome is a repeatable process capable of solving another instance.

## Single Solve Artifact Retention

Preserve the original Single Solve artifact whenever practical.

Single Solve is the durable reference instance used to:

- reproduce the solution later
- verify or improve the solver
- document how answers were derived
- compare behavior across modes
- recover from future Codex sessions without redownloading or rediscovering work

Keep extracted or derived files when they materially help reproduce,
understand, or improve the solution.

Do not repeatedly download the Single Solve artifact if the assigned local
copy already exists and belongs to the current attempt.

For example, prefer:

```python
wallet = extract_wallet(current_artifact)
entry_point = find_entry_point(current_elf)
```

over hardcoding values from the first instance.

When practical, solver scripts should output structured results, preferably JSON or another easy-to-map format.

---

# Time Trial Strategy

Time Trial is optimized for speed.

Assume it MAY provide a fresh instance, and assume a retry MAY assign another fresh artifact.

Before starting or retrying a timed attempt:

- read the challenge README and concise reusable knowledge
- read the current solver
- understand the established method
- make sure required local tooling is ready
- make sure the automated path can fetch the newly assigned artifact
- make sure known archive extraction is automated
- make sure the solver can parse the expected artifact family
- make sure answers can be mapped to CURRENT answer IDs
- make sure submission can happen without manual copying

Do not intentionally start or retry a very short timed attempt merely to investigate its artifact format unless learning a new variant is unavoidable.

Once the timed attempt begins:

1. Capture CURRENT Game Master response/state.
2. Capture CURRENT answer IDs.
3. Retrieve the CURRENT assigned artifact/input if provided.
4. Feed the current input directly into the existing reusable solver/runner.
5. Derive CURRENT instance values.
6. Map them to CURRENT answer IDs.
7. Submit efficiently.
8. Persist only information useful for current progress, debugging, or future solver improvement.

Do not spend leaderboard time rediscovering conceptual knowledge already learned in Single Solve.

Do not manually inspect, inventory, rename, hash, or reorganize a timed artifact before solving unless the solver specifically requires it.

If a fresh artifact introduces an unsupported variant:

1. do not make a speculative bulk submission
2. preserve the artifact if useful for debugging
3. allow the attempt to expire if necessary
4. improve the solver offline
5. retry only after the solver handles the newly learned variant

---

# Mastery Strategy

Mastery should also be treated as potentially producing new instances.

By Mastery, the preferred path is highly automated:

```test
start/retry
    ↓
fresh current artifact/input
    ↓
existing reusable solver/runner
    ↓
current answers
    ↓
submit
```

Reuse the established automation and methodology against the CURRENT Mastery
instance.

If Mastery contains repeated iterations, design the solution pipeline so the same process can be applied repeatedly with minimal manual work.

Do not assume exact answers from Single Solve, Time Trial, or a previous Mastery iteration remain valid.

If Mastery reveals a new artifact variant or solver weakness, preserve the useful evidence long enough to improve the solver.

Preserve the learned rule; do not automatically retain every redundant artifact forever.


---


# Artifact Handling

Artifacts should be treated as belonging to a challenge instance/attempt when appropriate.

For a new challenge or new attempt:

1. Check the current Game Master response.
2. Determine whether the attempt exposes an artifact.
3. Retrieve the artifact needed for THIS attempt.

        For Single Solve, reuse the existing locally preserved assigned artifact when Game Master indicates the same Single Solve instance/assignment is still current. Do not redownload it merely because another answer submission is being attempted.

        If Game Master indicates that the Single Solve assignment/instance changed, retrieve and preserve the newly assigned artifact.

4. Run the appropriate analysis/solver against it.
5. Preserve it according to the retention rules below.

Do not repeatedly download the SAME artifact during the SAME attempt.

Do not repeatedly hash, extract, decompile, scan, or statically analyze an unchanged local artifact merely as a synchronization ritual.

However, do not skip retrieval for a new timed attempt merely because Single Solve or a prior timed attempt already has an artifact. A new start/retry may provide a different instance.

Never automatically execute downloaded binaries, scripts, APKs, documents, or archive payloads merely because they were downloaded.

Analysis/execution should be deliberate and appropriate to the CTF task.

---

# Archive Password Handling

Some Huntress artifacts may be password-protected ZIP archives.

For a password-protected ZIP, first try:

```text
infected
```

If `infected` works, continue normally.

If `infected` does not work:

- stop and ask the user for guidance
- do not brute-force, dictionary-attack, crack, or otherwise attempt to
  recover the ZIP password automatically
- do not assume the password can be derived from challenge metadata unless
  the challenge explicitly indicates that

Password recovery/cracking is permitted only when:

- the user explicitly instructs Codex to attempt it, or
- the challenge instructions clearly establish password recovery/cracking
  as part of the intended task

During timed modes, do not waste attempt time trying alternate ZIP passwords unless password recovery itself is the intended challenge.

---


## Artifact Retention Policy

Use different retention behavior for learning mode and timed modes.

### Single Solve

Preserve the original assigned artifact whenever practical.

Keep useful extracted/derived files when they materially help reproduce the solution, explain it, or improve the reusable solver.

Single Solve artifacts are durable reference evidence.

### Time Trial and Mastery

The current timed artifact should remain available while solving or debugging the current attempt.

Do NOT permanently retain every timed artifact merely because it existed.

Retain a timed artifact when it is useful because it:

- exposed a previously unsupported encoding, format, or generator variant
- caused a parser or solver bug
- produced an unexpected answer structure
- is needed to reproduce an unresolved failure
- provides evidence needed to improve or validate the reusable solver

Once useful knowledge has been incorporated into the solver/state and the artifact is no longer needed for debugging, redundant old timed artifacts may be discarded or left untracked.

A successful timed artifact is optional to retain unless it has unique diagnostic or learning value.

When multiple retained timed artifacts exercise the same already-supported variant, keep only the artifacts that provide unique debugging or regression value.

The guiding retention principle is:

Single Solve preserves the evidence.
Timed modes preserve the knowledge.

Do not create large attempt-by-attempt artifact archives unless actual debugging needs justify them.

---

# Artifact Verification and Performance

Leaderboard time matters.

For Single Solve, artifact verification and inspection are useful when they contribute to understanding or reproducibility.

For Time Trial and Mastery, prioritize solve speed.

During a timed attempt:

- do not calculate hashes unless the hash itself is required by the challenge
  or the solver uses it for a specific safety check
- do not manually inspect archive metadata
- do not repeatedly run `file`, `strings`, archive listings, or equivalent
  discovery commands
- do not rename or reorganize downloaded files before solving
- do not compare the artifact to previous-mode hashes merely to prove it changed
- do not perform exploratory analysis while the timer is running

If the artifact is successfully downloaded and the prepared parser recognizes it, proceed immediately.

The optimized timed path is:

prepare solver before timer
        ↓
start/retry
        ↓
capture current answer IDs
        ↓
fetch current assigned artifact/input
        ↓
extract/decode automatically
        ↓
build current answer map
        ↓
submit

Artifact retrieval is part of the timed solve pipeline, not a separate investigation phase.

---

# Timed Retry and Diagnostic Limits

Time Trial and Mastery are not the preferred environment for open-ended
solver development.

A timed retry may be used to validate a prepared solver or learn an
unavoidable new generator variant, but repeated live retries must not become
the primary debugging method.

When a timed attempt reveals a solver problem:

1. preserve the useful artifact and diagnostic result
2. allow the current attempt to expire if necessary
3. debug and improve the solver offline
4. test the solver against all retained useful variants
5. retry only when the solver is ready for another end-to-end validation

Do not repeatedly start fresh timed attempts merely to obtain additional
examples unless more examples are genuinely required to understand the
generator.

## Submission Probing

Prefer the fewest Game Master submissions necessary.

During a timed attempt:

- prefer one complete submission when confidence is high
- use a small number of grouped submissions when partial acceptance is
  necessary to isolate a solver problem
- avoid large serial loops of individual-answer probes
- do not use hundreds of API requests as a substitute for deriving the answer
- bound any diagnostic/fallback submission loop before starting the attempt

If diagnosis cannot complete within the expected timer, preserve the artifact
and continue offline instead.

## Rate Limiting

HTTP 429 is an immediate stop condition for new start/retry/submission
experiments.

After a 429:

- stop creating new attempts
- do not repeatedly probe for recovery
- preserve current local state
- perform useful offline solver work while waiting
- resume only after an appropriate cooldown

Do not risk extending a rate limit by repeatedly testing whether it has ended.

---

# Timed-Mode Context Discipline

Historical timed-attempt data may be retained for debugging and solver development, but it is NOT part of the normal timed-attempt context.

Before Time Trial or Mastery, Codex should load only what is useful for fast execution:

- the finalized reusable methodology
- the current solver
- concise reusable classifications/mappings/rules
- reusable known-wrong methodological conclusions
- current mode/challenge metadata

Do not reread historical timed artifacts, expired-attempt transcripts, verbose submission logs, or instance-specific incorrect values before starting a new timed attempt unless actively debugging a known solver problem.

Knowledge learned from failed timed attempts should be promoted into the solver, README, or concise reusable-knowledge state.

Old attempts are supporting evidence, not required input.

--- 


# Persistent Challenge State

Each challenge should have persistent machine-readable state in addition to its human-readable README.

A suggested file is:

```text
challenge_state.json
```

Do not replace an existing equivalent state system if the repository already has one.

State should survive between Codex sessions.

Separate reusable challenge knowledge from attempt-specific data.

Conceptually:

```json
{
  "challenge_id": "...",
  "day": 4,
  "lane": "...",
  "knowledge": {
    "technique_known": true,
    "solution_script": "solve.py"
  },
  "single_solve": {
    "attempts": []
  },
  "time_trial": {
    "attempts": []
  },
  "mastery": {
    "attempts": []
  }
}
```

Each attempt may track:

- mode
- attempt identifier if available
- Game Master status
- answer IDs
- artifact filename/path
- artifact metadata
- candidate answers
- confirmed answers
- incorrect answers
- remaining answers
- submission results
- timestamps where useful

Do not store secrets such as the Game Master bearer token.

---

# Answer Tracking

Some Huntress challenges may contain many answer fields, potentially dozens.

Persistent answer tracking is essential.

For each answer ID, track enough information to avoid repeating work.

Useful fields include:

```text
answer_id
current_candidate
confirmed
scope
evidence/source when useful
incorrect_candidates
last_submission_result
```

Conceptual example:

```json
{
  "answers": {
    "resource-attack": {
      "value": "T1496",
      "confirmed": true,
      "scope": "challenge",
      "incorrect": []
    },
    "resource-wallet": {
      "value": "wallet_example",
      "confirmed": true,
      "scope": "instance",
      "incorrect": []
    }
  }
}
```

Do not assume every confirmed answer is reusable forever.

---

# Challenge-Level vs Instance-Level Knowledge

Distinguish:

```text
challenge-level knowledge
```

from:

```text
instance-specific values
```

A technique classification that remains constant across generated instances might eventually be treated as challenge-level knowledge.

A generated wallet, URL, mutex, hash, address, marker, credential, or similar value is likely instance-specific unless evidence establishes otherwise.

Only promote a value to challenge-level reusable knowledge when evidence supports doing so.

Historical instance values should remain available for reference but should not automatically be submitted in later attempts.

---

# Classification and Technique Scope

Do not assume a classification, role, behavior label, ATT&CK technique, control-flow label, format label, or similar semantic answer is reusable merely because Game Master confirmed it for a previous instance.

Distinguish between:

- the reusable RULE used to derive a classification
- the classification RESULT produced for the current instance

Example:

Reusable:
    detected behavior X maps to ATT&CK technique Y

Not automatically reusable:
    specimen d17 uses ATT&CK technique Y

A confirmed or incorrect classification from a timed attempt may be useful for improving the classification rule, but the specific answer remains instance-scoped unless evidence establishes that the field is invariant across challenge instances.

For timed modes, prefer:

current artifact
    → detect current behavior
    → apply reusable classification rule
    → produce current answer

rather than carrying previous instance classifications forward as answers.

When uncertain whether a semantic answer is challenge-level or
instance-specific, treat it as instance-specific.

---

# Incorrect Answer Tracking

Whenever an answer/submission is reported incorrect, preserve the fact only at the level useful for avoiding repeated mistakes or improving the solver.

For Single Solve, detailed incorrect candidates are useful because the assigned reference instance normally remains stable.

For timed modes, distinguish reusable methodological failures from
instance-only failures.

## Reusable Methodological Failure

Examples:

- parser rule is wrong
- classification RULE is wrong
- ATT&CK mapping RULE is wrong
- format interpretation is wrong
- algorithm assumption is wrong
- generator variant is not handled correctly

Promote useful lessons from these failures into the solver, README, or concise reusable knowledge.

## Instance-Specific Failure

Examples:

- classification result for one generated specimen
- ATT&CK result tied to one generated behavior
- URL
- hash
- identifier
- generated string
- randomized address
- other ephemeral instance value

Do not burden future timed runs with large histories of stale
instance-specific incorrect values.

Before trying a candidate for the CURRENT attempt, check relevant known-wrong information for that attempt and any reusable methodological rules.

Do not submit the same known-wrong answer again unless:

- a new instance changes the underlying value
- challenge behavior changed
- the prior failure was caused by malformed submission rather than the semantic answer
- new evidence strongly justifies retrying

Incorrect attempts do not need to clutter the human-readable README unless they teach something useful.

The goal is to preserve lessons, not every stale value.

---

# Partial Progress

For challenges with many answers, preserve partial progress immediately.

If Game Master indicates accepted answers or returns `remaining`:

- record what is confirmed
- record what remains
- avoid recomputing confirmed work unnecessarily
- focus analysis on unresolved fields

Do not lose progress simply because Codex starts a new session.

---

# Submission Behavior

Syncing the repository must not automatically submit answers.

When the user explicitly asks to solve a challenge, submission through Game Master is part of the normal solve workflow unless the challenge instructions require CourseStack-native submission or the user says not to submit.

Before submitting:

1. Read existing challenge state.
2. Obtain the CURRENT attempt's answer IDs.
3. Preserve previously confirmed information.
4. Exclude known-wrong candidates for the relevant instance/scope.
5. Make sure instance-specific values belong to the CURRENT attempt.
6. Submit using exact current answer IDs.
7. Record the response immediately.
8. Update persistent state.

Do not submit speculative guesses carelessly, especially during timed modes.

---

# Challenge README / Write-Up

Each challenge should develop into a useful write-up.

A good README should eventually explain:

- challenge objective
- what the challenge was testing
- files/targets involved
- approach
- important observations
- tools used
- useful commands
- how answers were derived
- reusable solving method
- final solution
- lessons learned where useful

Do not fabricate steps that did not happen.

During active solving, the README may be incomplete.

Update it incrementally as meaningful discoveries are made.

After Single Solve, it should ideally contain enough information for the user or Codex to understand the solution later without rediscovering everything.

Do not necessarily dump every wrong answer into the README. Keep detailed failed-answer history in state unless the failure teaches something useful.

---

# Solver Development

Whenever practical, Single Solve should produce reusable automation.

Separate:

```text
challenge logic
```

from:

```text
challenge instance data
```

Avoid hardcoding values that could change between attempts.

Prefer functions such as:

```python
extract_wallet(current_artifact)
extract_url(current_artifact)
find_entry_point(current_elf)
decode_payload(current_input)
```

over fixed values copied from one instance.

If a challenge has many answers, the solver should ideally return a dictionary/JSON object keyed by meaningful names so current results can be mapped to current Game Master answer IDs.

A solver should be safe to rerun locally without submitting anything unless submission behavior is explicitly part of that tool.

---

# Solve Workflow

When the user says:

```text
Solve Day <N> <challenge name>.
```

use approximately this workflow.

## 1. Identify the Challenge

Use local state and Game Master to identify:

- challenge ID
- day
- lane
- current status
- next appropriate mode
- artifact/input availability

## 2. Read Existing Work

Before solving, read the information appropriate to the current mode.

For Single Solve, read as useful:

- challenge README
- challenge state
- existing solver scripts
- preserved Single Solve artifact/input
- confirmed answers
- incorrect-answer history
- prior analysis

For Time Trial and Mastery, load only the concise reusable context needed for fast execution:

- current solver/runner
- finalized methodology
- reusable classification/mapping rules
- reusable methodological failures
- current mode/challenge metadata

Do not load historical timed artifacts, verbose expired-attempt histories, or stale instance-specific answers unless actively debugging a solver problem.

Do not repeat work unnecessarily.

## 3. Determine Mode

Normally progress:

```text
Single Solve
→ Time Trial
→ Mastery
```

## 4. Prepare Before Timed Work

If the next mode is timed, load the known methodology and ensure tooling is ready BEFORE starting the timer whenever the platform permits.

Do not start a timed attempt and then spend time rereading the entire repository.

## 5. Start/Inspect Current Attempt

Use Game Master.

Immediately persist useful current-attempt metadata.

Capture exact current answer IDs.

## 6. Retrieve Current Input

If the attempt provides a fresh artifact/input, retrieve it once.

Do not assume an old instance is current.

## 7. Solve

For Single Solve:

```text
understand thoroughly
automate where practical
document
```

For Time Trial/Mastery:

```text
reuse methodology
process current instance
minimize redundant work
```

## 8. Track Answers

Persist:

- current candidates
- confirmed answers
- incorrect candidates
- remaining answers
- scope (challenge vs instance) where useful

## 9. Submit

Submit using exact current answer IDs.

Record the result immediately.

## 10. Update Repository

Update:

- challenge state
- meaningful README/write-up content
- reusable solver if improved
- root status/index

Do not automatically commit or push unless explicitly requested.

---

# Speed Strategy

For timed modes, the desired path is:

Load concise reusable knowledge BEFORE timer
        ↓
Ensure solver/runner is ready
        ↓
Start/retry current attempt
        ↓
Capture current answer IDs
        ↓
Fetch current artifact/input once
        ↓
Extract/decode automatically
        ↓
Run reusable solver
        ↓
Perform only necessary current-instance work
        ↓
Submit

Avoid spending timed-mode seconds on questions that Single Solve should already have answered.

Do perform necessary current-instance work such as:

- decoding the current payload
- extracting the current URL
- calculating a required current hash
- extracting current generated identifiers
- analyzing current randomized binary values
- deriving current classifications from reusable rules

Do not load large historical attempt logs or redundant artifacts merely because they exist.

If a timed attempt exposes a new variant, use that failed/expired attempt to improve the solver offline, then return to the fast path.

---

# Do Not Waste Homebase Credits

Routine Game Master operations should use the authenticated public HTTPS endpoint from Kali.

Do not turn on Homebase merely to:

- list challenges
- check challenge status
- start normal Game Master attempts
- retrieve Game Master artifacts
- submit Game Master answers
- inspect Game Master OpenAPI

unless the event specifically requires Homebase for the operation.

Use Homebase/event AI only when there is a challenge-specific reason or the user intentionally chooses to use it.

---

# Git Safety

Do not automatically commit or push unless explicitly asked.

Before proposing or performing a commit:

- inspect `git diff`
- check for secrets
- verify `HUNTRESS_GM_TOKEN` is absent
- verify bearer Authorization headers are absent
- avoid virtual environments
- avoid caches/temp files
- consider artifact size before adding it
- avoid accidentally placing very large challenge files into Git history

Do not modify Git history destructively without explicit permission.

---

# Safety of Existing Work

Never overwrite or delete existing challenge investigation merely because automation wants a cleaner structure.

When uncertain whether a file is generated or manually maintained:

- preserve it
- inspect it
- ask before destructive replacement

Prefer additive/refactoring changes.

---

# Initial Codex Implementation Task

Before making significant changes to the repository:

1. Read `AGENTS.md` completely.
2. Read `CTF_WORKFLOW.md` completely.
3. Inspect the repository tree.
4. Inspect existing synchronization scripts.
5. Inspect the root README.
6. Inspect representative challenge folders from each existing day/lane.
7. Determine current folder/file naming conventions.
8. Determine how manual notes and generated content are currently separated.
9. Inspect how artifacts are currently stored.
10. Inspect the authenticated Game Master `?op=openapi`.
11. Query the current challenge list/status.
12. Compare Game Master state against the local repository.

Do not solve or submit a challenge during this initial architecture inspection unless explicitly requested.

Then recommend the smallest clean changes needed to:

- synchronize directly with Game Master
- preserve existing repository work
- automatically discover new days/challenges
- download appropriate new/current artifacts
- maintain per-challenge persistent state
- track confirmed and incorrect answers
- distinguish challenge-level knowledge from instance values
- support Single Solve → Time Trial → Mastery
- create/update useful challenge write-ups
- optimize timed modes for speed

Prefer adapting existing code over replacing it unnecessarily.

---

# Success Criteria

The system is successful when the user can open the repository in VS Code/Kali, load the Game Master token, and say:

```text
Sync the Huntress repo and solve Day 4 Table Manners.
```

Codex should be able to:

1. read project instructions
2. synchronize current Game Master state
3. identify the challenge
4. determine the next appropriate mode
5. read previous challenge knowledge/state
6. prepare appropriately for timed work
7. obtain the current attempt/input
8. retrieve a new artifact when the current instance requires one
9. reuse the established solving method
10. derive current instance-specific answers
11. avoid known failed answers/methods
12. submit through the correct path
13. preserve partial progress
14. update machine-readable state
15. update the challenge write-up
16. update the repository index/status
17. preserve all prior work

The guiding principle is:

```text
Learn thoroughly in Single Solve.
Automate what can be automated.
Persist what was learned.
Treat each timed attempt as potentially new data.
Reuse the method.
Minimize wasted time.
Never lose prior work.
```
