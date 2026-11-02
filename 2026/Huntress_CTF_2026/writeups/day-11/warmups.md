# Safe Travels

Day 11 · Warmups · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `warmups-day-11`

## Later Homebase account

### Day 11 Warmup: Safe Travels

- Challenge ID: `warmups-day-11`
- Mode: Single Solve
- Artifact: `blob.txt`
- SHA-256: `1f6973da33ec0f62a34edb86b36fa720885f979149e8db64775dca2dbb9aaf2f`

Single Solve uses Base64. Its 53-question Mastery bundle uses 11 numbered
fragments per blob, each with a different representation (Base64, ROT13, hex,
binary, decimal, octal, URL escapes, HTML entities, Unicode escapes, Base32,
and Base64URL). Decode in row order, concatenate the text, then take the slug
from the final non-empty line. `warmup-tools/decode_base64_layers.py` and
`warmup-tools/run_modes.py` keep this logic separate from assigned values.

The Single Solve blob decoded to `crisp-starfish-petal-89`. Single Solve,
Time Trial, and the 53-question Mastery bundle all returned `CORRECT`.

## Retained sources

- [early/11-Safe_Travels/readme.md](../../source-notes/early/11-Safe_Travels/readme.md)
- [later/writeups/day-11/warmup-safe-travels.md](../../source-notes/later/writeups/day-11/warmup-safe-travels.md)
- [later/writeups/day-11/progress-notes.md](../../source-notes/later/writeups/day-11/progress-notes.md)
