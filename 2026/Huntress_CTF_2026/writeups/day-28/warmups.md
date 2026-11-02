# Back in Sixteen

Day 28 · Warmups · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 28 Warmups: Back in Sixteen

All three modes are complete from their current assigned artifacts: Single
Solve, regular Time Trial, and regular Mastery. Each Game Master status returned
`CORRECT`; Mastery accepted all 138 answer IDs. These runs used the standard
untimed path, with no Hall of Fame request.

The question asks for the slug on the artifact's final non-empty decoded line.
Its answer format is three lowercase words separated by hyphens, followed by a
hyphen and a two-digit number.

Single Solve and Time Trial use hexadecimal text with its characters reversed.
Mastery has 138 blobs. Each is a numbered stream of fragments: the first
seventeen use the listed mixed codecs, while later fragments include reversed
text and hex, BOM-marked UTF-16, compressed Base64, ASCII85, counted characters,
Unicode code points, Brainfuck, and Ook!. The decoder assembles the readable
message and extracts the slug using the live answer format.

`warmup-tools/decode_base64_layers.py` handles reverse-ordered hexadecimal
text and bounds candidate selection for large mixed-codec bundles.
`warmup-tools/run_modes.py` downloads, hash-checks, decodes, submits, and records
the current assignment:

```sh
binary-reverse-engineering-tools/.venv/bin/python \
  warmup-tools/run_modes.py warmups-day-28
binary-reverse-engineering-tools/.venv/bin/python \
  warmup-tools/run_modes.py warmups-day-28/time_trial
binary-reverse-engineering-tools/.venv/bin/python \
  warmup-tools/run_modes.py warmups-day-28/mastery
```

## Retained sources

- [later/writeups/day-28/warmups-back-in-sixteen.md](../../source-notes/later/writeups/day-28/warmups-back-in-sixteen.md)
