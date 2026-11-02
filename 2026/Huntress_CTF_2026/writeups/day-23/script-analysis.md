# Press Start to Decode

Day 23 · Script analysis · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 23 Script Analysis — Press Start to Decode

### Results

Completed the regular Single Solve, Time Trial, and Mastery routes. No Hall of
Fame timing was requested.

| Mode | Attempt | Answers accepted | Evidence SHA-256 | Game Master |
| --- | --- | ---: | --- | --- |
| Single Solve | `4e216559-172c-49e6-90d4-6d0387650741` | 1,461 / 1,461 | `0e6b2bb25abd2bbf6e42fc8620b9dd8a5dc07118e9d84bd308347679c62d5e55` | `CORRECT` |
| Time Trial | `874b1a3f-3699-40f6-b212-c2da4d85d180` | 1,495 / 1,495 | `68f9e49f229737ba2061b1c9f668615c72e0321f4283b322943b3d723752cec3` | `CORRECT` |
| Mastery | `776fc4ad-3342-4f64-86aa-fcd01e09c77e` | 10,465 / 10,465 | `b022ade59aa9942bcd73354f45c77e305efdbf91504d2efbf0da6e18c7077de8` | `CORRECT` |

The first Time Trial variant left one VBScript composite-style answer
unresolved after six submissions. Its details and submitted candidates are in
that attempt's `unresolved-question.json`. A supported retry assigned a fresh
variant, which was completed. The later Time Trial and Mastery attempt records
contain no unresolved IDs.

The Game Master status responses confirm completion and do not report a
pending score. The supported proxy does not expose CourseStack point totals,
so the ledger total could not be independently verified.

### Method and tool updates

Used the downloaded, password-protected evidence for each current attempt and
the reusable Script Analysis parser. The parser now handles the layered
`LYR` encodings and split Google Apps Script payloads, plus the randomized
composite answer formats for Python, JScript, Batch, PowerShell, and VBScript.
It maps PowerShell secondary and tertiary indicators by the decoded sample
type and applies the terminal-dispatch ATT&CK rule. The mode runner now keeps
accepted IDs in a compact checkpoint and resumes only unresolved answers on
reconnect.

All specimens were analyzed as inert data and were not executed.

## Retained sources

- [later/writeups/day-23/script-analysis-press-start-to-decode.md](../../source-notes/later/writeups/day-23/script-analysis-press-start-to-decode.md)
