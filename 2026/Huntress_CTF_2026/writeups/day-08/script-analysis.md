# Lost in Translation

Day 8 · Script analysis · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `script-analysis-day-08-cross-language-iocs`.

## Final scoring evidence

The supplied scoreboard records all three Lost in Translation awards: Single Solve on October 9, Time Trial on October 9, and **Mastery on October 10 at `2026-10-10T22:33:44.094Z`**. Together they account for 10 points. The historical notes below explain the earlier partial state and the later accepted regular attempts; the scoreboard supplies the final scoring evidence.

A mode award alone does not prove that the corresponding run was a ranked timed attempt. Source: [scoreboard-derived challenge completion](../../results/challenge-completion.csv).

## Method in the saved account

The evidence was a password-protected ZIP (`infected`) containing inert scripts in multiple languages. The account describes decoding each descriptor with its declared codec and mapping the recovered behavior graph, indicators, and syntax properties to the exact answer IDs. Day 9 helper logic supplied reusable role, ATT&CK, Batch-expansion, and control-flow classifications.

The initial local note recorded only **15 of 615** Single Solve fields accepted. That was an intermediate snapshot. The later Homebase progress note records **615/615 accepted** for Single Solve and **615/615 accepted** for the regular, untimed Time Trial route.

## Reconciled saved results

| Mode | Strongest retained evidence |
| --- | --- |
| Single Solve | Later progress note records 615/615 accepted; saved challenge state reports `CORRECT` |
| Time Trial | Later progress note records 615/615 accepted in a regular untimed attempt |
| Mastery | The scoreboard records its 5-point award on October 10; the saved Day 8 narrative has no detailed Mastery execution trail |

The older statement that Time Trial and Mastery “have not been started” is not a final event result. This article preserves the chronology and uses the later accepted records where available.

## Recorded evidence hashes

| Assignment | ZIP SHA-256 |
| --- | --- |
| Single Solve | `82856ed6ca80c3db2e2528c4dbee30874b9643c8d6f5652b7761e7439f8548fe` |
| Regular Time Trial | `537201df52e7dc32f6926efa3e3fdc1cf69ea2431e5b0fd3f31caf137504475c` |

The progress note names start responses, candidate files, and submission histories that are not all present in the supplied archive. The account is useful for the decoding strategy and outcome history, but is not a complete reproducible transcript.

## Retained sources

- [early/08-Lost_in_Translation/readme.md](../../source-notes/early/08-Lost_in_Translation/readme.md)
- [later/writeups/day-08/progress-notes.md](../../source-notes/later/writeups/day-08/progress-notes.md)
- [early/08-Lost_in_Translation/challenge_state.json](../../source-notes/early/08-Lost_in_Translation/challenge_state.json)
