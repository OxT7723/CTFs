# Dim and Dimmer

Day 4 · Script analysis · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `script-analysis-day-04-shell-contrast`

## Earlier local account

---

The existing Single Solve attempt was resumed. Its assigned `evidence.zip` was retrieved from the Game Master, verified, and extracted with the challenge's stated password `infected`. The scripts were inspected as inert text and never executed.

The nine previously unresolved control-flow fields were resolved individually. Accepted forms were `direct` for `host-context.cmd`, `embedded-write.cmd`, `local-dispatch.bat`, `memory-stage.vbs`, and `local-dispatch.vbs`; `do_once` for `remote-write.vbs`, `outbound-transfer.vbs`, and `staged-handoff.vbs`; and `while_once` for `impact-plan.vbs`. `while_once` reflects the loop's counter progressing from 0 to 1 before the condition fails. The Game Master returned `CORRECT` for the complete 231-field Single Solve.

```text
sha256sum artifacts/single_solve/evidence.zip
7z t -pinfected artifacts/single_solve/evidence.zip
7z x -y -pinfected -o/tmp/huntress-d4-dim artifacts/single_solve/evidence.zip
rg -n -E 'If |Select Case|Do$|Exit Do|Loop|While |Wend|For |Next' /tmp/huntress-d4-dim/*.vbs
rg -n -E 'goto|call |for |if /i|exit /b' /tmp/huntress-d4-dim/*.cmd /tmp/huntress-d4-dim/*.bat
```

Single Solve is complete. The Game Master confirmed all 231 answer fields and returned `CORRECT`. Attempt and answer history, including previously rejected candidates, is tracked in `challenge_state.json`.

Time Trial completed on 2026-10-07. The Game Master returned `CORRECT` for attempt `50fe1331-9d38-4ed5-afc8-c5bddc32bb78` and confirmed all 231 answer IDs. The successful archive was processed temporarily and was not retained, per the timed-artifact retention policy. `tools/run_time_trial_fast.py` fetches the current artifact, extracts it with `infected`, builds current-instance answers, and checks uncertain syntax fields with bounded parallel submissions. The parser treats a harmless inline VBScript `If ... Else` as filler and prioritizes an actual error guard over an outer `If True` wrapper. The failed `attempt-aa3c4126-5587-46ee-b5e1-f4c51d4af61b` artifact was discarded after its useful Batch expansion lesson was incorporated into the solver.

The following notes describe earlier expired attempts and are retained as history.

An earlier expired attempt confirmed 213 of 231 fields; accepted values and rejected candidates are recorded in `challenge_state.json`. Its assigned archive is saved under `artifacts/time_trial/attempt-f6bc0867-22e9-48b2-b14a-1ff91baa8182/` (SHA-256 `04b8f8f2151567c2fea18feb4bb5e725913dcbea9539295f125ee7b477f6b4c9`). All nine Batch expansion labels were confirmed on that artifact. A grouped Batch control submission was rejected, then the timer expired before further controls could be tested. The saved runner and parsing helpers are in `tools/`.

Those earlier accepted submissions covered all artifact-derived literals, JScript syntax fields, all three scenarios, role classifications through `staged_chain`, confirmed ATT&CK IDs for benign, stager, dropper, downloader, launcher, uploader, impact, chain and relay, plus the resource and impact PowerShell samples, and accepted Batch/VBScript control groups. That attempt confirmed 213/231 before expiring, leaving eighteen Batch and VBScript control-flow fields. The runner and its parsing helpers are saved under `tools/`.

Mastery completed on 2026-10-07. Game Master confirmed all 462 answers across two assigned archive sets and returned `CORRECT` for attempt `1ca0d898-fd1f-4781-8b6f-62aeca999a39`. The timed solve took about two seconds from assignment to submission. The completed attempt's two archives were not retained; their SHA-256 values and attempt metadata are in `challenge_state.json`.

`tools/run_mastery_fast.py` is the reusable runner. Game Master returns two ordered artifacts both named `evidence.zip`; their order maps to set 1 and set 2. An initial timer expired before submission because the first runner incorrectly expected numbered filenames. The corrected runner downloads both current archives in parallel, extracts each with `infected`, uses `build_dimmer_answers.py` to derive 231 answers per set, prefixes each answer ID with its current set, checks the exact current answer IDs, then attempts one complete submission. A bounded grouped fallback handles an unsupported syntax variant. Pass `--retry` explicitly to request a new timed attempt after completion; keep the script for a future faster leaderboard run.

The reusable control-flow rule follows the code that gates or executes reconstruction, rather than a decoy conditional or the FOR loop used only to assemble fragments. In Batch, `if defined HUNTRESS_READY` is an `if_guard`; a FOR loop alone does not override that control label. In VBScript, a one-line `If (2 > 1) ... Else ...` assignment is harmless filler. The parser discards that line before classifying the actual recovery path. For Batch expansion, observed `h` fragments reconstructed through `CALL` require `call_double`; non-`h` FOR reconstruction uses `for_indirect`; direct or guarded `CALL` over `fragment`/`item` families uses `delayed`. These rules were checked against retained reference and failed-attempt evidence before the final Mastery run.

Two failed Mastery attempts' archives remain under `artifacts/mastery/` because they cover different syntax variants used to repair and regression-check the solver. Another redundant failed Mastery pair was discarded after those rules were validated. The original Single Solve archive remains preserved as the durable reference. Successful timed archives are optional and were not retained.

## Retained sources

- [early/04-Dim_and_Dimmer/readme.md](../../source-notes/early/04-Dim_and_Dimmer/readme.md)
