# Reflection Maze

Day 19 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 19 Mobile: Reflection Maze

- Challenge: `mobile-android-day-19-reflection-maze`
- Modes completed: Single Solve, regular Time Trial, regular Mastery (five cases)
- Each mode returned `CORRECT`; the Day 19 Mobile listing marks all three solved.
- The proxy status response has no CourseStack point-total field.

### Solve method

The assigned APK contains `assets/huntress_puzzle.json` with codec `reflection`
and a `data` string. The data matches the live `ANS-` plus 16 uppercase
hexadecimal answer format. The Mobile decoder now handles this codec and the
existing mode runner validates and submits the current attempt's answer IDs.

Single Solve APK SHA-256:
`8457f9fe2db0f217efcc0385776150328884bc3af1852112e8a5371ef1ef621d`

## Retained sources

- [later/writeups/day-19/mobile-android-reflection-maze.md](../../source-notes/later/writeups/day-19/mobile-android-reflection-maze.md)
