# Rotten Base

Day 29 · Warmups · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 29 Warmups: Rotten Base

Single Solve, Time Trial, and Mastery are solved. The Game Master list marks
all three modes solved.

The artifacts use ROT13 before Base64. Mastery contains 143 numbered
mixed-codec files in one ZIP; some suffix fragments need alternate decoding
paths. The reusable decoder handles these cases and avoids treating embedded
Brainfuck/Ook! fragments as whole-file programs.

The 15-run ranked Time Trial batch completed 15/15 `CORRECT`, all
Hall-of-Fame eligible, with artifact hashing disabled. Ranked attempts
remaining after that batch: 240. Measured wall time averaged 5.08 seconds
(3.54–7.94 seconds).

The 10-run ranked Mastery batch completed 10/10 `CORRECT`, all Hall-of-Fame
eligible, with artifact hashing disabled. Each run accepted all 143 answer
fields. Ranked attempts remaining after the batch: 246. Eight automated runs
were timed at an average of 10.63 seconds (9.43–12.15 seconds). Two runs
needed recovery: one after a dropped submit connection and one after the
decoder selected a format-shaped prefix instead of the full value explicitly
named by the decoded instruction.

`run_modes.py` now refreshes its persistent connection after long local
decoding and reconciles dropped submit responses against the same attempt.
When decoded instructions explicitly say “submit this exact answer to the
Game Master,” answer extraction preserves the complete instructed token even
if it extends beyond the suggested answer pattern.

Profiling a 143-file Mastery bundle showed the generic Caesar and Rail Fence
fallbacks dominated local decode time. A numbered-fragment fast path reduced
offline decoding from 7.2 seconds to an average of 0.435 seconds across the ten
saved ranked bundles (0.427–0.471 seconds). All 1,430 generated answers matched
the accepted answer sets. Timed runs also skip writing duplicate extracted
files while retaining the original archive. These are local replay benchmarks,
not new timed Game Master runs.

The Game Master returned `CORRECT` and its challenge list marks all three
modes solved. Its responses expose no separate CourseStack points field or
pending-scoring status.

## Retained sources

- [later/work/day-29/warmups/notes.md](../../source-notes/later/work/day-29/warmups/notes.md)
