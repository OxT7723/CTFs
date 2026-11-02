> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 27 Warmups: Monkey Business

All available modes completed from their assigned artifacts: Single Solve,
regular Time Trial, and regular Mastery. The Game Master returned `CORRECT`
for each, and the Day 27 Warmups list reports all three as solved.

The question asks for the slug on the artifact's final non-empty decoded line.
Its answer format is three lowercase words separated by hyphens, followed by a
hyphen and a two-digit number. Mastery contains 133 questions, with answer IDs
`set1.message` through `set133.message`.

`warmup-tools/decode_base64_layers.py` now translates standard Ook! instruction
pairs to Brainfuck and executes the result. Numbered mixed-codec samples can
also end in Ook! or Brainfuck fragments; the decoder evaluates those
programs directly and uses the decoded text when assembling the final slug.

Run any mode with the challenge ID from the Day 27 Warmups list:

```sh
binary-reverse-engineering-tools/.venv/bin/python \
  warmup-tools/run_modes.py warmups-day-27
binary-reverse-engineering-tools/.venv/bin/python \
  warmup-tools/run_modes.py warmups-day-27/time_trial
binary-reverse-engineering-tools/.venv/bin/python \
  warmup-tools/run_modes.py warmups-day-27/mastery
```

The runner uses the regular pool by default and does not request a timed Hall
of Fame attempt.
