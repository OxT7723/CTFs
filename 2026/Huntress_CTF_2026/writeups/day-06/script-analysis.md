# Shell We Begin

Day 6 · Script analysis · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `script-analysis-day-06-bash-behavior-graphs`

## Earlier local account

---

The Single Solve attempt had 399 questions. The user supplied 388 previously accepted answers; eleven source control-form questions remained.

Downloaded the current `evidence.zip` from the authenticated Game Master and verified its SHA-256 against the active attempt. Extracted only the eleven relevant Batch and VBScript files with `7z` and the challenge archive password `infected`. The classifications describe the control structure around the reconstruction, not the ordinary byte-to-text loop. The staged VBScript handoff has an outer `If True Then`, but `On Error Resume Next` guards its decode, so its canonical label is `error_guard`.

| Answer IDs | Verified answer | Source evidence |
| --- | --- | --- |
| `batch-impact-control`, `batch-relay-control` | `if_guard` | `if defined HUNTRESS_READY ...` |
| `vbscript-benign-control` | `while_once` | `While ... Wend` single pass |
| `vbscript-impact-control` | `do_once` | `Do ... Exit Do ... Loop` |
| `vbscript-dropper-control`, `vbscript-launcher-control`, `vbscript-relay-control`, `vbscript-stager-control` | `for_once` | `For ... = 0 To 0 ... Next` |
| `vbscript-chain-control`, `vbscript-downloader-control`, `vbscript-uploader-control` | `error_guard` | `On Error Resume Next` around decode, followed by error restoration/check |

`solve/timed_solver.py` reconstructs each current artifact without executing its scripts. It decodes PowerShell JSON, Bash/VBScript/Python material with declared codecs, JScript literals and transforms, and Batch plan fragments. It derives current indicators and syntax labels from current bytes and checks behavior steps against the retained Single Solve reference. `solve/run_timed.py` starts an attempt, verifies each assigned ZIP hash, runs the solver, checks all current answer IDs, and submits only a complete batch. A synthetic two-delivery Mastery package validated all 798 answer mappings before the first timer.

Time Trial required several new decoder forms. The final successful attempt had 399 answers and returned `CORRECT`. Mastery uses two deliveries and a seven-second deadline. The parser fills all 798 IDs, but full submissions have returned `incorrect`. Exact campaign and URL singleton checks confirmed the delivery mapping. Batch expansion snippets can contain `FOR`, `CALL`, `%...%`, and delayed `!...!` in one source; the Game Master has rejected several plausible expansion labels. A bare VBScript `If True Then` control label also remains unverified. Responses of `accepted` to a batch can represent partial progress, so only `CORRECT` confirms mode completion. Saved attempt contracts, assigned ZIPs, and solver outputs under `solve/mastery/` and `artifacts/` retain the evidence for offline analysis. Preserve the 15 remaining fresh attempts until the label rule is established.

```text
7z x -pinfected -o06-Shell_We_Begin/solve/specimens 06-Shell_We_Begin/artifacts/evidence.zip <eleven selected members>
```

The eleven missing answers were submitted against the current Single Solve attempt. The Game Master returned `CORRECT` on 2026-10-09. The complete 399-answer record is in `solve/single_solve_answers.json`; the original assigned archive is retained in `artifacts/evidence.zip`. Time Trial also returned `CORRECT` on attempt `b3021eda-7bef-4c61-9c5e-b0205bacb4c1` using the static solver. Mastery remains incomplete; 15 fresh attempts remained at the last status check.

Exact control labels are specific to this challenge. Source-level control structures can be nested; classify the operative decode guard before a surrounding wrapper. Single-answer Game Master submissions returned `accepted` for correct partial answers, which allowed verification of the eleven labels without repeating the entire set.

## Retained sources

- [early/06-Shell_We_Begin/readme.md](../../source-notes/early/06-Shell_We_Begin/readme.md)
- [later/writeups/day-06/decode-summary.txt](../../source-notes/later/writeups/day-06/decode-summary.txt)
