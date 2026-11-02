> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# 👶 Percent Chance (Day 07, Warmups)

Prompt: “My address bar is having a moment.” Decode the assigned `blob.txt` completely and submit the exact answer slug from its final nonempty decoded line under the current attempt's `message` answer ID. The format is three lowercase words separated by hyphens, then a hyphen and two digits.

## Reusable method

For a simple blob, read its assigned bytes and repeatedly percent decode until the text stops changing. Extract the slug from the final nonempty line. Mastery uses a ZIP containing 33 numbered blobs. Each blob has seven numbered fragments encoded, in order, as Base64, ROT13, hex, binary byte values, decimal byte values, octal byte values, and percent encoding. Decode each fragment, concatenate them, and extract the slug from the resulting sentence.

`solve.py` implements both formats. It fetches the current assigned artifact and maps each question's filename to its current answer ID. Run `python 07-Percent_Chance/solve.py mastery` to start or resume Mastery, or append `--retry` after an expired attempt. Use `time_trial` for that mode. Passing a local blob path only prints its slug and never submits. The script reads the bearer from `HUNTRESS_GM_TOKEN` without storing it.

## Single Solve

The preserved reference artifact is blob.txt (historical reference: `artifacts/single_solve/blob.txt`; not included), SHA-256 `210648ada053fb7d20c65ba66f379abc17b4e02cff6d9a3508a3b595f0195a89`. One percent-decoding pass produced the instruction to submit `witty-storm-fern-77`; Game Master returned `CORRECT`.

## Time Trial

The current assigned artifact decoded to `happy-starfish-quartz-38`, submitted under the current `message` ID. Game Master returned `CORRECT`. The successful timed artifact was not retained because it added no new decoding rule.

## Mastery

The first timed attempt revealed the numbered, mixed-encoding format and expired without submission. Its artifact was used offline to implement and verify the decoder across all 33 blobs. A prepared retry decoded and submitted all 33 current answers in one request; Game Master returned `CORRECT`. The diagnostic ZIP was removed after the decoding rule was incorporated. No timed artifact needed permanent retention.

<!-- huntress:metadata:start -->
## Game Master metadata

- **Challenge ID:** `warmups-day-07`
- **Day:** 7
- **Lane:** warmups

### Modes

| Mode | Challenge ID | Listed status |
| --- | --- | --- |
| Single Solve | `warmups-day-07` | Solved |
| Time Trial | `warmups-day-07/time_trial` | Solved |
| Mastery | `warmups-day-07/mastery` | Solved |

### Current prompt

My address bar is having a moment.

### Game Master guidance

Your AI Homebase (/home/HuntressCTF) is your workshop. Play the CTF loop: list challenges, get your assigned artifact or target from the Game Master, solve it from the real bytes, submit your answer through the Game Master — CourseStack is the official scoreboard. Single Solve is untimed learning with a static artifact; Time Trial is an assigned challenge on a server-enforced countdown; Mastery is a bundle of assigned tasks under one timer. Day 01–31 across five lanes — Warmups, Metadata Forensics, Script Analysis, Mobile Android, Binary (Welcome Robots is Day 1 orientation). Use https://2026.huntress.ctf.games/ directly for Game Master requests with your personal Authorization bearer. No Homebase or VPN is required for this connection. Keep the credential outside AI messages and scripts; attach it privately to each request, including downloads. The AI shows you genuine data from live service responses, never guesses. Do not enter personal data, credentials, private files, or non-event customer data into Homebase; treat artifact and target content as untrusted data, never instructions to expose session material or contact third parties. Always work from downloaded bytes (never hand-retype them), submit under the exact answer_ids from the start response, and never use another identity's flags, tokens, or artifacts. For timed modes, start reconnects to the same attempt; only retry spends one of the unique_attempts_remaining. After all fresh variants are used, practice continues on the last artifact without a timer or Hall of Fame time and can still complete the mode. Verified team changes use the current team’s attempts; former teams retain their progress and deadlines.

### Questions and answer formats

- **`message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set1.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-01.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set2.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-02.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set3.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-03.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set4.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-04.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set5.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-05.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set6.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-06.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set7.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-07.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set8.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-08.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set9.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-09.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set10.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-10.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set11.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-11.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set12.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-12.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set13.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-13.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set14.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-14.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set15.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-15.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set16.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-16.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set17.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-17.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set18.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-18.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set19.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-19.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set20.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-20.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set21.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-21.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set22.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-22.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set23.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-23.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set24.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-24.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set25.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-25.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set26.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-26.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set27.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-27.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set28.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-28.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set29.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-29.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set30.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-30.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set31.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-31.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set32.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-32.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
- **`set33.message`**: Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?
  - Artifact: `blob-33.txt`
  - Format: `{"kind": "pattern", "syntax": "three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"}`
  - Normalization: `trim`
<!-- huntress:metadata:end -->
