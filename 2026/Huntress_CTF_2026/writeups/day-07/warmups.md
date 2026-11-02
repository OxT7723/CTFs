# Percent Chance

Day 7 · Warmups · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `warmups-day-07`

## Earlier local account

Prompt: “My address bar is having a moment.” Decode the assigned `blob.txt` completely and submit the exact answer slug from its final nonempty decoded line under the current attempt's `message` answer ID. The format is three lowercase words separated by hyphens, then a hyphen and two digits.

For a simple blob, read its assigned bytes and repeatedly percent decode until the text stops changing. Extract the slug from the final nonempty line. Mastery uses a ZIP containing 33 numbered blobs. Each blob has seven numbered fragments encoded, in order, as Base64, ROT13, hex, binary byte values, decimal byte values, octal byte values, and percent encoding. Decode each fragment, concatenate them, and extract the slug from the resulting sentence.

`solve.py` implements both formats. It fetches the current assigned artifact and maps each question's filename to its current answer ID. Run `python 07-Percent_Chance/solve.py mastery` to start or resume Mastery, or append `--retry` after an expired attempt. Use `time_trial` for that mode. Passing a local blob path only prints its slug and never submits. The script reads the bearer from `HUNTRESS_GM_TOKEN` without storing it.

The preserved reference artifact is blob.txt (source reference: `artifacts/single_solve/blob.txt`; not linked in this draft), SHA-256 `210648ada053fb7d20c65ba66f379abc17b4e02cff6d9a3508a3b595f0195a89`. One percent-decoding pass produced the instruction to submit `witty-storm-fern-77`; Game Master returned `CORRECT`.

The current assigned artifact decoded to `happy-starfish-quartz-38`, submitted under the current `message` ID. Game Master returned `CORRECT`. The successful timed artifact was not retained because it added no new decoding rule.

The first timed attempt revealed the numbered, mixed-encoding format and expired without submission. Its artifact was used offline to implement and verify the decoder across all 33 blobs. A prepared retry decoded and submitted all 33 current answers in one request; Game Master returned `CORRECT`. The diagnostic ZIP was removed after the decoding rule was incorporated. No timed artifact needed permanent retention.

## Retained sources

- [early/07-Percent_Chance/readme.md](../../source-notes/early/07-Percent_Chance/readme.md)
