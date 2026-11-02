# Opposite Day

Day 13 · Warmups · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 13 Warmups: Opposite Day

All three regular modes returned `CORRECT`: Single Solve, Time Trial, and
Mastery. The regular Time Trial and Mastery starts had no deadlines. Mastery
contained 63 blobs; all 63 answers were accepted. Game Master status confirms
all three modes as solved. Its responses did not include CourseStack point
totals or a pending-scoring state.

The clue “A met Z” indicates Atbash. Single Solve and Time Trial use readable
Atbash text. Each Mastery blob has 13 numbered fragments: the existing 12
fragment codecs plus Atbash on row 13. The Warmups decoder now supports both
forms, and the runner accepts challenge IDs ending directly in a day number
when choosing the attempt directory.

| Mode | Attempt | Artifact SHA-256 | Result |
| --- | --- | --- | --- |
| Single Solve | `85bad46e-93bb-4943-a40d-8608f10a4b7b` | `ecf0b43b2012a5377380ae8e8885ed2c836bf6c79bd2b91ee0049afc49294eab` | `CORRECT` |
| Time Trial | `8031d0ff-07c5-4af0-a787-ffc250a8420b` | `538e3a0b235aa18e84f105c7bd13b201664eafaecb2e63359323efc942a4da6f` | `CORRECT` |
| Mastery | `12db47dd-f3f2-441a-87a6-883c26579f27` | `31138eba1fda10ff86ed0818df5eb38b69ff73e4ac17f638a14552952d04a42e` | `CORRECT` |

## Retained sources

- [later/writeups/day-13/progress-notes.md](../../source-notes/later/writeups/day-13/progress-notes.md)
