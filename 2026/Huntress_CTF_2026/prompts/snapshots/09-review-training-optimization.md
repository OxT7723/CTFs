# Huntress CTF 2026 — Challenge Solver Review, Training & Optimization

**Primary Goal:** Review the previously completed challenge, improve its reusable solver, test against available randomized artifacts, and prepare for fast, reliable Hall of Fame attempts in BOTH Time Trial and Mastery when qualified ranked attempts remain.

This is a **training and optimization session**, NOT an instruction to immediately launch a timed challenge.

You are authorized to work autonomously through the phases below, but you must respect the execution restrictions and phase ordering.

## Core Rules

1. Work ONLY on the specified challenge and its Single Solve, Time Trial, and Mastery modes. Identify the correct challenge IDs and category from the Game Master. Do not start other challenges.
2. **Do not initiate ANY server-timed attempt until Phase 5**, including legacy timed-by-default `op=start` or `op=retry` calls. `run_for_time:true` is authorized only in Phase 5.
3. Check `op=list`, current attempt status, supported modes, remaining regular variants, and remaining ranked attempts before starting anything.
4. If a mode supports `run_for_time_supported:true`, use its regular untimed mode for training. `op=start` reconnects to an existing attempt; after confirmed completion, use the supported **regular** `op=retry` mechanism to get another regular attempt, never a timed variant during training.
5. If a mode is timed by default and no safe untimed option is available, DO NOT start it during preparation. Investigate supported alternatives and report the limitation.
6. Do not waste ranked timed attempts during testing.
7. Reuse the existing challenge folders, tools, scripts, and notes. Do not recreate tools unnecessarily or overwrite previous work.
8. Work autonomously. Do not stop between phases unless a restriction, error, or unavailable feature prevents safe continuation.
9. Minimize AI credits and unnecessary tool calls. Prefer deterministic scripts and concise output.

## Important — Previously Solved Challenges and Replay Behavior

**All challenges targeted by this workflow have already been solved previously. This is expected and must NOT prevent further training or replay attempts.**

Some challenges were originally completed manually, some with AI assistance, and others using deterministic solvers. The purpose of this workflow is to revisit them, improve automation, and test their reliability.

### Historical Solves vs. Current Attempts

Treat historical challenge completion and the current attempt as separate things.

A challenge marked `solved:true` means it was successfully completed previously. It does NOT automatically mean no additional regular, practice, or ranked attempts are possible.

Always inspect the Game Master's available replay mechanisms and attempt pools. **A normal `op=start` reconnects to the existing attempt; it does not advance a previously solved mode to a new attempt.** Use `op=retry` only when its mode and effect are known and permitted by the current phase.

**Do not skip a challenge simply because it has already been solved.**

### Regular and Practice Replay

The objective during training is to perform real end-to-end solves, including Game Master submissions, whenever a supported non-ranked replay is available.

For each supported regular or practice attempt:

1. Start or resume the appropriate non-ranked attempt. If the historical attempt is already complete, advance using a documented **non-ranked** retry or practice mechanism; do not mistake reconnecting to it for a new replay.
2. Retrieve the assigned artifact or artifacts.
3. Run the deterministic solver against those artifacts.
4. Generate the complete set of answers using the exact required answer IDs.
5. Submit the answers to the Game Master.
6. Verify that the current attempt's answers were accepted.
7. Record the outcome, errors, and execution performance.
8. Improve the solver and retest when necessary.

**Previously accepted answers from historical attempts must NOT cause the AI to skip submissions for a new replay attempt.**

However, do not unnecessarily resubmit individual answers already accepted within the SAME current attempt.

### Exhausted Regular Variants

When `regular_variants_remaining` reaches zero, investigate whether the Game Master allows continued regular retries using the final artifact with `variant_fresh:false`.

For legacy routes, investigate whether `op=practice` is available after the qualified rotation is exhausted.

These replay mechanisms may reuse an existing artifact rather than generate a new randomized artifact.

If replay submissions are supported, use them for end-to-end validation even when the artifact is not fresh.

If only previously completed attempts are accessible and no supported replay is available, perform offline regression testing without unnecessary submissions.

Do NOT assume regular replay is unlimited unless the Game Master documents or confirms that behavior.

### Ranked Attempts Are Separate

Time Trial and Mastery may have separate ranked attempt pools.

Some previously completed challenges may have ZERO ranked attempts remaining because earlier sessions consumed them.

This must NOT prevent the AI from reviewing the challenge, improving its solver, or performing supported regular/practice runs.

When ranked attempts remain, preserve them until the designated ranked phase.

When ranked attempts are exhausted, skip ranked execution for that mode and continue all other available training and optimization work.

Never use a potentially timed legacy `op=retry` during preparation merely to test whether a replay is available.

### Required Behavior

The objective is NOT merely to confirm that the historical answers can still be extracted.

The objective is to:

- Build or improve a reusable deterministic solver.
- Run complete, non-ranked challenge attempts whenever supported.
- Test against fresh randomized artifacts whenever safely available.
- Test the complete answer submission process.
- Identify failures and optimize the solver.
- Prepare for ranked Time Trial and Mastery attempts when eligible attempts remain.

**Historical completion is not a reason to skip training. Exhausted ranked attempts are not a reason to skip regular practice. Accepted historical answers are not a substitute for validating a new attempt.**

These rules apply throughout Phases 1–6 and override any conflicting instructions.

## Phase 1 — Review the Completed Single Solve

Locate the existing challenge directory, notes, artifacts, scripts, solver implementations, and previously accepted answers.

Review how the challenge was originally solved.

Identify the required inputs, extraction techniques, decoding steps, answer formats, and any manual operations.

Look for potential weaknesses such as hardcoded filenames, artifact-specific values, assumptions about ordering, fixed offsets, unreliable regex patterns, and unnecessary processing.

Determine whether a reusable deterministic solver already exists.

**Goal:** Have a working solver that can process a completely new artifact without depending on known answers.

Improve the existing solver where necessary. Preserve working functionality and previously saved notes.

## Phase 2 — Untimed Time Trial Training

Inspect the Time Trial mode and confirm whether an untimed regular attempt is supported.

If supported, start or resume a regular untimed attempt WITHOUT `run_for_time:true`. Since this challenge was solved previously, first determine whether `op=start` would merely reconnect to the historical completed attempt. If so, use a documented **regular-mode retry** after CourseStack confirmation; do not initiate a legacy timed-by-default retry during training.

Download the assigned artifacts and use the solver developed or reviewed in Phase 1.

Attempt to solve the entire challenge using the existing automation first.

If the solver fails or requires manual intervention, investigate the cause and fix it.

Validate all required answers against the current artifact and submit using the exact answer IDs returned by the Game Master.

Preserve accepted partial answers instead of repeatedly submitting them.

Once solved, confirm completion and CourseStack scoring status.

**Then improve the solver based on anything learned.**

The objective is to eliminate manual steps, reduce unnecessary processing, handle randomized values, and produce correctly formatted answers reliably.

Perform a local end-to-end test and measure approximate processing time, separating solver execution from network and Game Master overhead where possible.

Do not begin a timed run yet.

## Phase 3 — Untimed Mastery Training

Inspect Mastery Mode and confirm whether a regular untimed attempt is supported.

If supported, start or resume a regular untimed Mastery attempt WITHOUT `run_for_time:true`. If the prior attempt is already complete, use a documented **regular-mode retry** after CourseStack confirmation rather than reconnecting to the old solved attempt. Never use legacy timed-by-default retries during training.

Mastery may contain multiple tasks or randomized variants. Identify every required artifact, question, answer ID, and output format.

Use the same reusable solver wherever possible, extending it to handle multiple artifacts automatically.

Ensure the solver can:

- Discover and process all required artifacts.
- Handle variations without hardcoded values.
- Associate answers with their correct question IDs.
- Preserve and track accepted partial submissions.
- Detect missing answers or extraction failures.
- Produce consistent results across multiple variants.

Complete the regular Mastery attempt and verify Game Master and CourseStack completion.

Update the existing solver to address any issues discovered.

**Goal:** One reusable solution that can handle Single Solve, Time Trial, and Mastery with minimal manual interaction.

Do NOT attempt timed Mastery.

## Phase 4 — Additional Practice and Fresh Artifact Testing

Before launching the timed attempt, investigate what additional practice opportunities are available.

Check Game Master capabilities, `regular_variants_remaining`, `ranked_attempts_remaining`, `variant_fresh`, and any supported retry or practice mechanisms.

Determine whether we can obtain **new randomized artifacts without consuming ranked timed attempts**.

For supported regular attempts, a completed attempt may be advanced through `op=retry` after CourseStack confirms completion. Keep retries in regular mode.

If fresh regular variants are available, use them to test the solver against new inputs.

For each fresh artifact:

1. Run the solver without modifying it first.
2. Record whether every answer was extracted correctly.
3. Validate and submit when appropriate.
4. Identify failures, edge cases, or slow operations.
5. Update the solver if necessary.
6. Re-test to ensure the change does not break previously successful artifacts.

If older `op=practice` continuation is available, inspect its restrictions. Do not assume that practice produces fresh artifacts; the Game Master documentation indicates that some continuations reuse the final regular artifact.

Never consume a ranked timed attempt just to obtain another testing file.

Continue useful regular testing while fresh eligible variants remain, but avoid redundant runs when the solver is consistently successful.

At the end of this phase, assess reliability against all **available** variants. If no new untimed variants were obtainable, document that limitation; successful testing of old artifacts must not be presented as proof of correctness on unseen randomized variants.

## Phase 5 — Ranked Hall of Fame Attempts (Time Trial AND Mastery)

Begin this phase ONLY after completing the available training, offline regression tests, solver improvements, and safe practice from Phases 1–4. The goal is to make **one well-prepared ranked attempt per eligible mode**, not to burn attempts searching for a favorable artifact.

**Maximum authorization during this session: ONE newly initiated ranked Time Trial attempt and ONE newly initiated ranked Mastery attempt.** They have separate budgets. A single intentional `op=retry` per mode **is permitted when necessary to begin that one new ranked attempt on an already solved or expired mode**. No second timed attempt in the same mode is authorized, whether the first succeeds, fails, or expires.

### Step 1 — Preflight and Identify the Correct Timed Route

Before either ranked mode:

1. Confirm the correct challenge ID and mode, current attempt state, exact answer IDs, and all required artifacts.
2. Read `op=list` and `op=status`, and distinguish **opt-in timed routes** (`run_for_time_supported:true`) from **legacy timed-by-default routes** (which may report `false`). `false` alone does NOT mean ranked attempts are unavailable.
3. Inspect qualified ranked attempt availability, published rotation, counters, scoring confirmation, and eligibility evidence for **each mode separately**. `unique_attempts_remaining` does not, by itself, prove a Hall of Fame-qualified retry is currently available.
4. Check for an already active timed attempt. Do not assume repeating `op=start` restarts its clock. If an active/shared team timer or an unresolved scoring state makes a new attempt unsafe, report it and skip rather than initiating another attempt.
5. Prepare the complete automated download → process → answer → submit workflow, including dependencies, permissions, paths, and network access.
6. Verify the solver against all available saved and regular artifacts, and note any untested randomized behaviors. Do not claim unseen-variant reliability without evidence.
7. Remove unnecessary logging, file reads, hashing, checksum verification, and AI deliberation from the speed-critical path. **Keep hashing if a challenge answer actually requires it.**
8. Confirm the correct method to start **one** new ranked attempt:
   - **Opt-in route:** For a never-started timed attempt, use `op=start` with `"run_for_time":true`. If the prior timed attempt is already completed or expired, use `op=retry` with `"run_for_time":true` after required scoring confirmation. `op=start` alone merely reconnects to an existing attempt.
   - **Legacy timed-by-default route:** If documented qualified timed retries are available and the previous attempt has ended, use `op=retry` **without** `run_for_time:true`; on a never-started mode, a legacy `op=start` may itself begin a timed attempt. Do not use either during Phases 1–4.
9. Never use a timed `op=retry` as a *probe*. When definitive `hall_of_fame_eligible` is only supplied in the new attempt's response, proceed only if non-consuming status and the documented rules provide a reasonable basis to expect an eligible qualified attempt. Immediately inspect the new response and report the actual eligibility. If it is ineligible, **do not** start another attempt.

**If ranked attempts are exhausted, unqualified, unavailable, or unsafe for a mode, SKIP its ranked execution but continue the rest of the workflow. Historical `solved:true`, an expired earlier deadline, zero regular variants, or `run_for_time_supported:false` alone is not grounds to skip.**

### Step 2 — ONE Ranked Time Trial Attempt

Use the correct opt-in or legacy route determined above to initiate **at most ONE new ranked Time Trial attempt**. If the challenge was already completed, this may require a deliberate, authorized `op=retry`; that is allowed **only for this first new ranked attempt**.

Immediately obtain the newly assigned artifact, execute the prepared solver, and submit the exact answers. Use the Game Master's UTC deadline as authoritative. Verify the new attempt ID, deadline, and `hall_of_fame_eligible` field if provided.

If successful:
- Record the completion time, scoring confirmation, and Hall of Fame status.
- Analyze avoidable delays, improve the solver, and regression-test against existing artifacts.
- **Do NOT begin a second ranked Time Trial attempt.**

If unsuccessful or expired:
- **Do NOT retry ranked Time Trial.**
- Preserve the artifact and attempt details, diagnose the failure offline using those same files, and fix the solver.
- Test corrected output and previous artifacts without another timed start or retry. Do not submit late answers for expired timed credit.

Continue to Mastery after Time Trial review, even if the Time Trial ranked attempt was skipped or unsuccessful, provided Mastery itself can be prepared and attempted safely.

### Step 3 — ONE Ranked Mastery Attempt

Before starting, resolve any Time Trial issues relevant to Mastery. Confirm all required tasks, answer IDs, and multi-artifact handling are ready. The multiple Mastery tasks may share **one server-enforced deadline**.

Use the correct opt-in or legacy route to initiate **at most ONE new ranked Mastery attempt**. As with Time Trial, a deliberate first ranked `op=retry` is permitted when needed to advance a historically completed mode; a second one is not.

The solver should automatically:

1. Retrieve every required artifact and exact answer ID.
2. Process all tasks without hardcoded artifact-specific answers.
3. Format and submit answers efficiently.
4. Track accepted partial answers and submit only outstanding answers.
5. Verify completion before the shared deadline.

Inspect the new attempt's actual Hall of Fame eligibility, record its attempt ID and server deadline, and avoid AI analysis during the clock whenever deterministic scripts suffice.

If successful:
- Record the completion time, completed tasks, scoring confirmation, and Hall of Fame status.
- Diagnose bottlenecks, improve the solver, and regression-test it.
- **Do NOT begin a second ranked Mastery attempt.**

If unsuccessful or expired:
- **Do NOT retry ranked Mastery.**
- Preserve all assigned artifacts and existing accepted progress.
- Diagnose and fix the solver using the same files, testing without further ranked attempts.

### Step 4 — Final Optimization

Review lessons from both modes. Apply and test reusable improvements, without overwriting historical notes or functioning scripts. Confirm what has actually been tested across Single Solve, regular Time Trial, ranked Time Trial, regular Mastery, and ranked Mastery; explicitly identify any untested categories or randomized behavior.

### Critical Restrictions

- No timed start or timed retry during Phases 1–4, including on legacy routes.
- At most ONE newly initiated ranked Time Trial attempt **and** ONE newly initiated ranked Mastery attempt during Phase 5.
- The authorized first ranked `op=retry` on a previously completed mode is **not** a prohibited second attempt. Every further ranked retry in that mode **is** prohibited.
- Never spend a ranked attempt to obtain a test artifact or explore availability.
- Do not treat `solved:true`, `run_for_time_supported:false`, a historical `hall_of_fame_eligible:false`, or exhausted regular variants as automatic proof that ranked replay is unavailable.
- Do not treat remaining `unique_attempts` alone as proof that an attempt is qualified and Hall of Fame eligible.
- Respect Game Master deadlines and CourseStack scoring confirmation; never assume reconnecting resets an attempt.
- If a safe qualified ranked attempt cannot be established using available rules and status, skip ranked execution for that mode, document why, and continue other work.

**The priority is reliable, fast Hall of Fame results for BOTH eligible modes without wasting ranked attempts.**

## Phase 6 — Save Improvements and Final Report

After completing all available training and practice, and attempting or safely skipping the ranked Hall of Fame runs for BOTH Time Trial and Mastery, consolidate everything learned.

### 1. Save and Finalize Solver Improvements

- Update the existing solver scripts with all improvements discovered during testing and ranked attempts.
- Preserve previous notes, working scripts, artifacts, and accepted answers.
- Keep reusable logic independent of challenge-specific values.
- Avoid hardcoded hashes, filenames, URLs, answer values, or assumptions about randomized artifacts.
- Ensure improvements made for one mode do not break another.
- Re-test the final solver against previously completed artifacts.
- Prefer deterministic automation over repeated AI analysis.
- Optimize processing time, unnecessary file operations, and Game Master interactions.
- Keep optional hashing and checksum verification outside the speed-critical timed execution path unless required to answer a challenge question.
- Where practical, provide a single command that processes new artifacts and prepares or submits all required answers.

### 2. Document the Final Solution

Update the existing challenge documentation with:

- Required tools, dependencies, and execution commands.
- How the solver processes new randomized artifacts.
- How it handles Single Solve, Time Trial, and Mastery.
- Known edge cases and limitations.
- Changes made during training and ranked attempts.
- Any remaining opportunities for speed or reliability improvements.

Preserve existing documentation and avoid unnecessary duplicate files.

### 3. Final Results Report

Provide a concise but complete report covering the following:

**Single Solve**
- Previous completion status.
- Solver review findings.
- Improvements made.

**Time Trial — Regular (Untimed)**
- Completion status.
- Number of variants tested.
- Success rate.
- Approximate solver execution time.
- Issues encountered and resolved.

**Mastery — Regular (Untimed)**
- Completion status.
- Number of variants and tasks processed.
- Success rate.
- Approximate solver execution time.
- Improvements made to handle multiple artifacts and answer IDs.

**Additional Practice**
- Practice mechanisms discovered.
- Number of fresh randomized artifacts tested.
- Reliability across different variants.
- Edge cases discovered.
- Remaining limitations.

**Time Trial — Ranked Hall of Fame**
- Whether a ranked attempt was performed.
- Success or failure.
- Completion time, if available.
- Hall of Fame eligibility and recorded result.
- Any delays or failures encountered.
- Improvements learned and applied.
- Ranked attempts remaining.

**Mastery — Ranked Hall of Fame**
- Whether a ranked attempt was performed.
- Success or failure.
- Total completion time, if available.
- Number of required tasks completed.
- Hall of Fame eligibility and recorded result.
- Any delays or failures encountered.
- Improvements learned and applied.
- Ranked attempts remaining.

**Final Solver Improvements**
- Files created or modified.
- Major fixes and optimizations.
- Reliability improvements.
- Performance improvements.
- Regression testing results.
- Any unresolved issues.

### 4. Final Readiness Assessment

Evaluate whether the final solver is ready to process previously unseen randomized artifacts quickly and reliably.

Provide:

- **Correctness:** Can it reliably produce all required answers?
- **Automation:** Can it complete the workflow with minimal AI intervention?
- **Speed:** What is the approximate end-to-end execution time?
- **Reliability:** How consistently did it work across available variants?
- **Mastery Support:** Can it process multiple tasks within one deadline?
- **Remaining Risks:** What could still cause a timed attempt to fail?
- **Future Improvements:** What should be optimized before another ranked attempt on a future day or in a separately authorized session?

### 5. Final Restrictions

- Do NOT start any additional ranked attempts during Phase 6.
- Do NOT automatically retry failed or expired ranked attempts.
- Do NOT consume ranked attempts for additional testing.
- Do NOT modify unrelated challenge directories or shared tooling unnecessarily.
- Do NOT overwrite previous working solutions or documentation.
- If either ranked attempt was unsuccessful, preserve its artifacts and use them for offline debugging.
- If an answer cannot be validated, report the uncertainty rather than claiming success.
- Keep AI credit consumption low and avoid unnecessary repeated analysis.

### Final Priority

**Correctness → Reliability across randomized variants → Automation → Speed → Ranked Hall of Fame performance.**

The objective is to finish with a reusable, optimized, and thoroughly tested solver capable of handling Single Solve, Time Trial, and Mastery challenges.

**Maximum ranked attempts authorized for this session: ONE Time Trial and ONE Mastery.**

After both have been attempted or safely skipped, stop ranked execution, save all improvements, and provide the final report.

Do not sacrifice correctness for a faster result. Do not consume ranked attempts during preparation. **Never initiate a second ranked attempt in either mode during this session.**

Use as few AI credits as practical and prioritize reusable improvements that will help with the remaining days of Huntress CTF 2026.