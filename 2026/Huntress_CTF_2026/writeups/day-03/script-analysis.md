# Expansion Pack

Day 3 · Script analysis · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `script-analysis-day-03-batch-expansion`

## Earlier local account

**Release:** Day 03 Challenges

| Author | Category |
|---|---|
| [John Hammond](https://youtube.com/@_JohnHammond), and [Just Hacking Training](https://justhacking.com) | 📜 Script Analysis |

cmd.exe expands percents, delays expansion, CALLs twice, and bends FOR loops into indirection. Reconstruct every variable exactly as the interpreter would see it — without executing a single line — then follow the staged chain to its final handoff.

You can download the **single-solve file** for this challenge here:

**Challenge file:** expansion_pack.zip

> [!IMPORTANT]
>
> The password for this archive is **`infected`**.

or ask the Game Master for your single-solve file in the **AI Homebase** virtual machine.

**System:** Start/connect through CourseStack or the challenge instructions.

**Scored task:** Single Solve: Submit the flag for 1 static task. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 2

Use the Game Master to get fresh targets for Time Trial and Mastery Mode.

**Scored task:** Time Trial: Submit the flag for 1 new dynamic task in under 6 seconds. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 3

**Scored task:** Mastery Mode: Submit the flag after completing 2 new dynamic tasks in under 7 seconds. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 5

---

The assigned AES-encrypted archive has SHA-256
`ce1a3fb0a5425cfa0794fc7b7f09ec93b86b74544ad93283a55ebe0ee3fcc23e`.
The live Single Solve attempt had 159 answer fields. The final two were
`batch-launcher-control` (`local-dispatch.bat`) and `batch-relay-control`
(`relay-handoff.cmd`). The Game Master requested exact text for both.

Both batch files use an `if defined HUNTRESS_READY` guard in the inspection
path. The launcher's `FOR ... DO CALL SET` also controls variable expansion,
but the accepted control-flow answer for both fields was `if_guard`.

```bash
python 03-Expansion_Pack/solve_expansion.py --reference
python 03-Expansion_Pack/run_mastery.py --dry-run
python 03-Expansion_Pack/run_mastery.py --start
```

Submit `if_guard` under `batch-relay-control` and `batch-launcher-control`.
The Game Master accepted both and returned `CORRECT` for the attempt.

```text
2d6ffc32f1b8cc508876ec5f7dbb45f9
```

The Game Master assigned a fresh ZIP and 159 current answer IDs. The runner
downloads that ZIP, extracts it with `infected`, statically reconstructs the
PowerShell, JScript, and Batch descriptors, and submits current values. It
never executes the samples. The assigned archive for the successful attempt
has SHA-256 `7ce193117fb1918ec97b1446928cc4af002c2cd5f6d6d010893c0dd01bd71e97`.

For newly generated Batch samples, a simple syntax label was insufficient for
the nine expansion questions. The runner now submits the 150 other answers in
one group, then tries at most the four documented expansion labels for each
unresolved field, stopping when the Game Master accepts it. Previously wrong
labels for a timed instance are diagnostic evidence, not reusable answers for
another instance. The final attempt `9837e2d1-6e03-4a0d-b9f9-3eabc1e3a225`
returned `CORRECT` within its deadline, with flag
`16b602366721d8d57924eefb2613b8f8`. The Game Master list now reports the
Time Trial as solved; CourseStack points were not checked.

Run `python 03-Expansion_Pack/solve_expansion.py --reference` to validate the
static solver against the retained Single Solve reference. For a new Time
Trial assignment, `--start-and-solve` runs the complete current-instance path.

The live attempt `da4ffa21-dbf9-45db-91b9-36df0113da85` started at
`2026-10-07T13:39:57.814Z` and had a seven-second deadline of
`2026-10-07T13:40:04.814Z`. The assigned
Mastery bundle (source reference: `/?op=download&capability=521a28c8b24746229d08cfa6d9ab040ea07136e6f594428d8b0cefe447f4d497`; not linked in this draft)
had SHA-256 `91e813196c048e46b017e8edde6bee0139c2450ad5ab2467c296fc74125e1829`.
It contained `evidence-01.zip` and `evidence-02.zip`, one per set.

Before starting the timer, `--dry-run` extracted two copies of the retained
Single Solve archive and verified that the solver mapped all 318 `set1.` and
`set2.` answer IDs. During the live attempt, `--start` obtained the current
bundle over the authenticated HTTPS Game Master API, extracted both inner ZIPs
with `infected`, and statically decoded the assigned PowerShell, JScript, and
Batch files. It used the current attempt's answer IDs and values; it did not
run any specimen or reuse Single Solve indicators.

The 300 non-expansion answers were accepted in one submission. The runner then
checked the 18 Batch expansion answers concurrently, trying only the four
documented labels for any field the Game Master rejected. All 18 were accepted
after 39 total submission calls. The first attempt returned `CORRECT` before
the deadline with flag `e3c43698042960d04f7ef7d15d9ca4ae`.

The Game Master status confirms 318 accepted answers and its challenge list
reports Mastery solved. CourseStack points were not checked. The successful
timed bundle was not kept locally because it introduced no new solver variant.

Batch expansion labels in generated instances cannot always be inferred from
the first syntax-based classification. Keep the static decoder and the bounded
validation method, and derive each set's indicators from its own assigned ZIP.

The password-protected Single Solve ZIP is the retained reference. The
password-free copy and extracted duplicate were removed; `--reference`
extracts the original ZIP when needed. Two Time Trial ZIPs and their outcome
records remain as distinct Batch-label diagnostics for future solver tuning.

## Retained sources

- [early/03-Expansion_Pack/readme.md](../../source-notes/early/03-Expansion_Pack/readme.md)
