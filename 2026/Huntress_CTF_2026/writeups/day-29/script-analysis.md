# Make It Make Sense

Day 29 · Script analysis · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 29 Script Analysis: Make It Make Sense

All three available regular modes completed with Game Master status `CORRECT`.
The maintained `script-analysis-tools/run_modes.py` runner downloaded and
verified each assigned artifact, built answers from the extracted bytes, and
confirmed zero unresolved answer IDs.

| Mode | Attempt ID | Accepted | Artifact SHA-256 |
| --- | --- | ---: | --- |
| Single Solve | `6419c2d1-0cab-40f4-93bb-0af8afc719a0` | 1,747/1,747 | `0ba75808186d63e2269cd7d69f2d6d2835cd6425300ce2aa9a389204218a1525` |
| Time Trial (regular) | `3e2285e6-3bf2-4385-aabd-0d7022f0701b` | 1,833/1,833 | `a5433de2fc72e83d31a4d3133636e375aa724a084c120486cd0fa0a5872d214c` |
| Mastery (regular) | `c75daf9b-37fc-40f5-a93f-9646846934ec` | 23,829/23,829 | `3d684142a01eb1be351d25189366979d2e31d7d0affe3ab30b5f3318c1075498` |

The Game Master status responses did not include a CourseStack points or
scoring-status field, and no response reported `pending`. No solver changes
were needed.

## Retained sources

- [later/writeups/day-29/script-analysis-make-it-make-sense.md](../../source-notes/later/writeups/day-29/script-analysis-make-it-make-sense.md)
