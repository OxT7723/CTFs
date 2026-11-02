> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Challenge solving and learning

## Single Solve
- Inspect only the target challenge's existing README, state, relevant scripts, and assigned artifact. Prefer existing local Single Solve artifact if confirmed to be the current assignment.
- Understand what is tested and how each answer is derived. Distinguish challenge-level rules from attempt-specific data (URLs, hashes, wallets, mutexes, addresses, markers, ATT&CK classifications, and IDs).
- Create a reusable solver where practical, accepting current artifact/input and producing structured results. Avoid hardcoding values from one instance. Do not auto-submit from a general-purpose parser.
- Record useful commands, evidence, confirmed and incorrect answers, methodological lessons, and reproducible steps in the challenge state/write-up without overwriting manual notes.
- Download assigned bytes rather than retyping; never blindly execute downloaded content.

## Showing versus solving
- If asked to show a challenge, retrieve current player-facing instructions, modes, answer IDs/formats, and artifact references, but do not solve or submit until asked.
- If explicitly asked to solve, use the live Game Master and submit through the supported interface. Interpret incorrect, partial/accepted, CORRECT, and pending states honestly; CourseStack remains the official score ledger.

## Continuing to timed modes
- Preserve the solver and concise method from Single Solve. Read `docs/TIMED_MODES.md` before starting Time Trial or Mastery.
- A new mode or retry can generate new artifacts, answer IDs, and values. Always verify the CURRENT attempt.

## Writing results
- Keep original Single Solve evidence when practical. Update the target `readme.md`, `challenge_state.json`, and solver with meaningful results; avoid verbose repetitive logs in the model context.
- Use root index update only when an existing safe updater is available; don't rewrite root README manually in bulk.

## Publication-ready write-up after completion
- When every mode actually offered for the challenge is confirmed complete, finalize its existing `readme.md` in the SAME Codex session while the evidence and reasoning remain in context. Do not wait until the end of the CTF.
- Include objective, artifacts/target, analysis, verified derivation of answers, commands/tools, reusable solver usage, mode differences, errors and corrections worth learning from, and a clear reproducible walkthrough. Distinguish verified steps from assumptions; never fabricate output.
- Preserve manually written notes and existing generated-section boundaries. Do not publish, commit, or push automatically.
- Add a brief retention inventory: files essential for reproduction/publication, useful reference samples, and potentially disposable temporary or duplicate artifacts. Keep original Single Solve evidence and essential scripts; never delete automatically.
- If the challenge cannot be fully completed, update the write-up with accurate partial progress and unresolved questions rather than claiming publication readiness.

## Post-completion artifact management 
- After all available modes are successfully completed, finalize the challenge write-up and review generated files. 
- Keep reusable solver scripts, verified results, required evidence, and files needed to reproduce the solution. 
- Place disposable extraction outputs and intermediate analysis files under a challenge-local scratch/ directory when practical. 
- Do not move existing files if doing so would break scripts or references. 
- Do not recursively read historical artifact directories just to perform cleanup.
