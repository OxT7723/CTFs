# All the World's a Stager

Day 9 · Script analysis · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `script-analysis-day-09-stager-relationships`

## Earlier local account

---

The Game Master asks for classifications, ATT&CK IDs, exact indicators, encoding details, syntax forms, and ordered stage relationships from the final bytes of script fixtures. Each regular archive contains 83 files. Single Solve and Time Trial each ask 695 questions. Mastery wraps five independent 83-file archives and asks 3,475 questions, with answer IDs prefixed `set1.` through `set5.`.

The assigned Single Solve archive is `evidence.zip` (SHA-256 `770311a8a2f653916aa9c636e8ae9112a40c1115beeae026971d4a407a3a15db`). The Time Trial archive is `scratch/time_trial/evidence.zip` (SHA-256 `0c6ec00380129f7dd22183409554e4568def11ac6021e87fc0c90c95b82f24cb`). The Mastery wrapper is `scratch/mastery/assigned.zip` (SHA-256 `a5bffbcf3811c821e8e337765fa77c8e6b7a8ede3970716ea611e6d288a1ad4b`); it contains `evidence-01.zip` through `evidence-05.zip`. All were downloaded from the current authenticated Game Master assignments and checked against its SHA-256 values. No extracted script was executed.

`solve.py` statically reconstructs each script's descriptor. It reads marker payloads (`B64`, `HB64`, `HEX`, `FRAG`), language-specific literal material, or explicit fragment assignments. It decodes Base64, URL-safe and reversed Base64, percent hex, Unicode escapes, hexadecimal and decimal lists, then reversals, XOR, rolling XOR, and modular arithmetic as directed by the artifact. JScript and Batch fixtures need additional parsing of their reconstruction functions or fragment assignments. The recovered descriptor supplies ordered `steps`, `stage_count`, `graph`, `next_language`, role-specific indicators, and campaign data. The solver derives classifications and ATT&CK IDs from those steps and the source language, and reads syntax questions from the source text. It maps only the current response's answer IDs to values from the matching current archive.

For example, `memory-stage.vbs` in the Single Solve archive reconstructs `acquire_remote,dispatch_memory`, the `Microsoft.XMLHTTP` adapter, and a reserved-domain URL. Those bytes support the stager role and its exact indicators. The collection PowerShell sample's accepted primary ATT&CK ID is `T1555.003`; earlier plausible collection/exfiltration IDs were rejected. The stage relationship answers come from the descriptor's ordered steps, graph, next-language, next-stage, and handoff fields rather than from filenames alone.

The most troublesome questions asked for the fixture generator's exact control and expansion labels. For Single Solve, accepted Batch controls included `if_guard` and `call_subroutine`; VBScript controls included `while_once`, `do_once`, `error_guard`, and `for_once`. Later variants also used Batch `errorlevel_guard`, `goto_dispatch`, and `direct`, plus VBScript `select_case` and `direct`. A `For...Next` loop used only to assemble decoded bytes does not by itself change the VBScript control label. The `for %%G ... do call set` assembly can coexist with Batch `direct` or `goto_dispatch` control. For JScript property style, inspect the descriptor's actual dot and bracket accesses, including obfuscated variable names. The updated solver encodes the labels verified across all seven assigned archives.

Extract the assigned bytes with 7-Zip and the archive password `infected`:

```sh
7z x -pinfected -o09-All_the_Worlds_a_Stager/scratch/single 09-All_the_Worlds_a_Stager/evidence.zip
7z x -pinfected -o09-All_the_Worlds_a_Stager/scratch/time_trial/extracted 09-All_the_Worlds_a_Stager/scratch/time_trial/evidence.zip
7z x -pinfected -o09-All_the_Worlds_a_Stager/scratch/mastery/archives 09-All_the_Worlds_a_Stager/scratch/mastery/assigned.zip
# Extract each evidence-0N.zip into scratch/mastery/setN with -pinfected.
```

From the repository root, the saved `challenge_state.json` supplies the answer IDs and question-to-file mapping. These commands emit current-artifact answer maps as JSON; submit through the authenticated Game Master only after checking that the state and archive belong to the same attempt:

```sh
python 09-All_the_Worlds_a_Stager/solve.py 09-All_the_Worlds_a_Stager/scratch/single --answer-map 09-All_the_Worlds_a_Stager/challenge_state.json --mode single_solve > single-answers.json
python 09-All_the_Worlds_a_Stager/solve.py 09-All_the_Worlds_a_Stager/scratch/time_trial/extracted --answer-map 09-All_the_Worlds_a_Stager/challenge_state.json --mode time_trial > time-trial-answers.json
python 09-All_the_Worlds_a_Stager/solve.py 09-All_the_Worlds_a_Stager/scratch/mastery --answer-map 09-All_the_Worlds_a_Stager/challenge_state.json --mode mastery > mastery-answers.json
```

All offered modes are confirmed `CORRECT` by the live Game Master: Single Solve **695/695**, Time Trial **695/695**, and Mastery **3,475/3,475**. The Time Trial and Mastery attempts used the regular untimed pool (`deadline: null`); no optional timed Hall of Fame attempt was requested.

The game AI's `game_ai/` files preserve its 683/695 Single Solve progress and failed guesses. The last twelve fields were syntax-label mismatches; the source interpretation was largely sound. The first Time Trial and Mastery submissions exposed additional encoding and syntax variants, which were isolated by answer group and corrected from the current source. No answer value was carried from one assignment to another.

Keep `solve.py`, this write-up, `challenge_state.json`, `evidence.zip`, and `game_ai/` for reproduction and provenance. The Time Trial and Mastery archives are useful regression samples. The extracted copies and diagnostic JSON under `scratch/` are potentially disposable after review; none were deleted.

## Later Homebase account

### All the World's a Stager

### Current completion state

The live Game Master listing checked on 2026-10-31 marks Single Solve, Time
Trial, and Mastery as solved. This supersedes the older partial-progress
snapshot below. The completion record and exact accepted submission are not
saved in this challenge folder.

### Earlier partial-progress snapshot

- The Single Solve archive SHA-256 is `770311a8a2f653916aa9c636e8ae9112a40c1115beeae026971d4a407a3a15db`.
- The AES-encrypted ZIP was extracted with the supplied password `infected`. `solve.py` reconstructs descriptors statically; it does not execute samples.
- 683 of 695 answers are accepted. Twelve control-flow fields remain, so Single Solve is incomplete and Time Trial and Mastery are locked.
- The Batch expansion answers recovered in the resumed attempt were `delayed` for benign, dropper, launcher, impact, and chain. The collection sample’s primary ATT&CK answer was accepted as `T1555.003`.
- Previously accepted Batch control values still include `call_subroutine` for the stager, dropper, downloader, uploader, and relay samples, and `for_indirect` for the relay expansion.

### Attempt history from the partial-progress snapshot

The collection ATT&CK guesses `T1005`, `T1560.001`, `T1560.002`, `T1119`, and `T1041` were rejected; `T1555.003` was later accepted. `batch-dropper-expansion` accidentally received a seventh guess after its saved failure count was misread. The detailed progress ledger referenced by the original notes is not present in this workspace.

The older progress snapshot had twelve unresolved control-flow fields. The live
listing now marks every mode solved, but the completion response and final
answer map are not present locally.

### Decoder

```sh
python3 solve.py extracted
```

To build a candidate answer map from a saved start response:

```sh
python3 solve.py extracted --answer-map start-response.json
```

Only this writeup is present for this challenge in the current workspace; the
assigned archive, reconstructed files, solver, and progress records are absent.

## Retained sources

- [early/09-All_the_Worlds_a_Stager/readme.md](../../source-notes/early/09-All_the_Worlds_a_Stager/readme.md)
- [later/writeups/day-09/all-worlds-a-stager.md](../../source-notes/later/writeups/day-09/all-worlds-a-stager.md)
