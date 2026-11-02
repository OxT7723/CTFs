# Percent Percent

Day 30 · Warmups · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 30 Warmups: Percent Percent

Single Solve, regular Time Trial, and regular Mastery all returned `CORRECT`.
Mastery accepted all 148 answers (`set1.message` through `set148.message`).
Each mode used the regular untimed route; no Hall of Fame attempt was requested.
The Game Master list now marks all three modes solved. Its status and list
responses did not include a separate CourseStack points field.

On October 31, ten fresh ranked Time Trial variants also returned `CORRECT`
and were Hall of Fame eligible. Each used the existing persistent-connection
runner with artifact hashing skipped. Their single-blob artifacts were
945–990 bytes; local decode times were 4.319–8.863 ms (4.764 ms median).
The decoder handled all ten without changes.

A fresh regular Mastery variant also returned `CORRECT` for all 148 answers.
Its 333,906-byte ZIP decoded in 405.44 ms with artifact hash verification on.
One fresh ranked Mastery run returned `CORRECT` for all 148 answers in 393.46 ms
of local decoding and was Hall of Fame eligible.

Ten more fresh ranked Mastery variants all returned `CORRECT`, each accepting
all 148 answers. Their ZIPs were 325,745–334,126 bytes; local decode times were
389–526 ms, with a 419.1 ms median. The Game Master confirmed Hall of Fame
eligibility but did not return per-run ranked times.

On October 31, another ten fresh ranked Mastery variants returned `CORRECT`,
each accepting all 148 answers and marked Hall of Fame eligible. Their ZIPs
were 326,394–336,256 bytes; local decode times were 410.198–715.935 ms, with
a 423.820 ms median. Replaying the slowest variant locally five times took
408.931–467.500 ms, so its original 715.935 ms measurement appears to be
runtime variance rather than a newly expensive blob. All ten variants used
formats the current decoder already handles; no solver change was needed.

Profiling showed repeated regular-expression work and pointless Ook!/Brainfuck
parser calls dominated avoidable decoder overhead. The decoder now reuses
compiled hot patterns and rejects those parsers quickly when their required
marker is absent. Interleaved offline runs on three saved 148-answer archives
matched every prior answer and reduced median local decode time from
405.2–425.6 ms to 378.2–394.5 ms (about 7%). A fresh ranked attempt is needed
to measure whether this improves the official time.

Then 25 fresh ranked Time Trial and 25 fresh ranked Mastery variants all
returned `CORRECT` and were Hall of Fame eligible. Time Trial artifacts were
945–1,017 bytes; local decode was 3.849–19.151 ms (4.103 ms median). Mastery
ZIPs were 325,755–340,366 bytes; local decode was 383.952–1,035.4 ms
(409.251 ms median), with all 148 answers accepted in every run. The Mastery
bundles kept the same 148-file, 30-row structure; no new decoder path was
needed. Replaying the apparent outliers took 1.4 ms for Time Trial and
380–395 ms for Mastery, indicating runtime jitter rather than harder variants.

Another 20 fresh ranked Time Trial and 20 fresh ranked Mastery variants all
returned `CORRECT` and were Hall of Fame eligible. Time Trial artifacts were
954–999 bytes; local decode was 3.873–5.778 ms (4.069 ms median). Mastery ZIPs
were 324,819–338,656 bytes; local decode was 382.308–1,492.383 ms
(402.040 ms median), with all 148 answers accepted. Every file in all 20
Mastery bundles again had the same 30-row layout. Replaying the two slowest
decodes took 369.9–414.2 ms and 395.7–413.6 ms, respectively; no new decoder
case or artifact structure was found.

One variant exposed an ambiguous suffix: ROT13 followed by Base64 could be
mistaken for reversed hex. The decoder now keeps the direct Base64 reading as
an alternate and lets the complete answer format select the valid candidate.
This recovered the active attempt without starting another variant.

The question asks for the slug named by the final decoded instruction. Mastery
uses one ZIP containing 148 numbered mixed-codec blobs. The assigned bytes are
saved under `work/day-30/warmups/` with their attempt records and SHA-256 hashes.

`warmup-tools/decode_base64_layers.py` now decodes nested percent escapes in
mixed-codec fragments and can decode a completed instruction when its encoded
layer spans fragments. Its command-line decoder also initializes the optional
Rail Fence setting before displaying intermediate layers.
`warmup-tools/run_modes.py` downloads and verifies each assigned artifact,
extracts the answers, submits them, and records final status.

## Retained sources

- [later/writeups/day-30/warmups-percent-percent.md](../../source-notes/later/writeups/day-30/warmups-percent-percent.md)
