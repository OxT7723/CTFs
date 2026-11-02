# Jack in the Box

Day 19 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 19 Binary Reverse Engineering — Jack in the Box

### Results

| Mode | Attempt | Accepted | Game Master result | Deadline |
| --- | --- | ---: | --- | --- |
| Single Solve | `835f7d73-0741-4331-ab82-93fd1766dd2a` | 228 / 228 | `CORRECT` | None |
| Time Trial, regular untimed route | `8fd35f2e-591c-4602-8912-e7e0ba7c54bd` | 228 / 228 | `CORRECT` | None |
| Mastery, regular untimed route | `b9dbeebd-4806-442e-ad7a-797f4908d518` | 1,140 / 1,140 | `CORRECT` | None |

Fresh Game Master status checks returned `CORRECT` for all three attempts.
They expose no CourseStack points total or separate pending-scoring field, so
points could not be independently confirmed.

### Challenge and records

Challenge ID: `binary-reverse-engineering-day-19-static-unpacking`.
**Jack in the Box** asks for static recovery of a payload hidden behind a
decoder stub. Each attempt's full player-facing prompt, questions, answer
formats, exact answer IDs, and artifact metadata are preserved in its start
response:

- Single Solve response (source reference: `../../work/day-19/binary/835f7d73-0741-4331-ab82-93fd1766dd2a/start-response.json`; not linked in this draft)
- Time Trial response (source reference: `../../work/day-19/binary/8fd35f2e-591c-4602-8912-e7e0ba7c54bd/start-response.json`; not linked in this draft)
- Mastery response (source reference: `../../work/day-19/binary/b9dbeebd-4806-442e-ad7a-797f4908d518/start-response.json`; not linked in this draft)

All artifacts were downloaded from their assigned attempts and SHA-256 checked
by the runner.

| Mode / set | Artifact | SHA-256 |
| --- | --- | --- |
| Single Solve | evidence.zip (private download link removed) | `8617b900a67c73c10c428c74879a0ad0790b1e5c767ca983234d599ec9278be7` |
| Time Trial | evidence.zip (private download link removed) | `b7ded485fc0afcb7cdd952724f067c9cb1b143c038b32c095da8397bb7089d9c` |
| Mastery set 1 | evidence.zip (private download link removed) | `bf4349d7ec224eff1623524d58308498f0daadb6d698aa275219dffb27b2425b` |
| Mastery set 2 | evidence.zip (private download link removed) | `a12a7aec5537a1d567e5709a7920aea7882f7e3e15c6580d8997c74ad9c5e4b6` |
| Mastery set 3 | evidence.zip (private download link removed) | `326bede4e1174ad2cb19f881a7fcaaa9f5f2a292b77d2003d7b5185d42e3603d` |
| Mastery set 4 | evidence.zip (private download link removed) | `39bf67cf4e34627360bc000397a9faf7d6e1bb5b4ebd8be5da89ee5c7327aa96` |
| Mastery set 5 | evidence.zip (private download link removed) | `222fac8cdfb98db615bddfdefc485e1c4fb740c6c6fc2ea323deb9235961801e` |

### Solver update

The Day 19 specimen has a final `PK19` overlay containing packed HCFG data.
The reusable analyzer now finds the final `PK19` or `RS20` overlay, applies
the per-byte rotate/XOR transform, verifies the unpacked SHA-256, and reads
the HCFG record at offset zero. It also reports the overlay offset and size.
Answer formatting now follows the live enum values for ELF classes and
container formats.

The reusable solver is
[analyze_evidence.py](../../tools/later/binary-reverse-engineering-tools/analyze_evidence.py).
Attempt archives, extracted files, candidates, submissions, and summaries are
under `work/day-19/binary/<attempt-id>/`.

## Retained sources

- [later/writeups/day-19/binary-jack-in-the-box.md](../../source-notes/later/writeups/day-19/binary-jack-in-the-box.md)
