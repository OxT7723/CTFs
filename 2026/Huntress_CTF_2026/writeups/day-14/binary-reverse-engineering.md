# Selective Memory

Day 14 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 14 Binary: Selective Memory

Challenge ID: `binary-reverse-engineering-day-14-objective-c-persistence-descriptor`.
The documented `lane=binary` list filter returned no entries; listing Day 14
without a lane filter and searching the challenge ID showed the live lane slug
`binary-reverse-engineering`.

The existing binary runner and analyzer handled all assignments from the
downloaded evidence without changes. They built answers from each live start
response and submitted every field successfully.

| Mode | Attempt | Answers accepted | Deadline | Result |
| --- | --- | ---: | --- | --- |
| Single Solve | `05ec780a-1990-4aac-a277-2936ff4403bc` | 140/140 | None | `CORRECT` |
| Time Trial | `51c7efd0-06f5-442c-8106-7bc49de72d79` | 140/140 | 2026-10-14 13:06:05 UTC | `CORRECT` |
| Mastery timed attempt | `2ad0eae1-169e-4eb1-978a-3933600d031a` | 200/420 | 2026-10-14 13:06:24 UTC | Expired |
| Mastery practice continuation | `6ee9e7af-b740-4366-a57a-49d9c8a57921` | 420/420 | None | `CORRECT` |

The Game Master status and filtered Day 14 list confirm all three modes solved.
The standard timed attempts are marked ineligible for the Hall of Fame; the
correct responses reported no pending-scoring state, and no CourseStack point
totals were included. Attempt records, assigned artifacts, candidates,
submissions, and status responses are under `work/day-14/binary/`.

This run exposed a runner bottleneck: its default batch size was 20, resulting
in 11 serial submissions before the timed Mastery attempt expired and 21
submissions in practice. The runner now defaults to one batch of up to 500
answers while enforcing the 512 KiB request limit, so equivalent future
Mastery assignments should need far fewer round trips.

## Retained sources

- [later/writeups/day-14/binary-selective-memory.md](../../source-notes/later/writeups/day-14/binary-selective-memory.md)
