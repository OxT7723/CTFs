> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 11 Warmup: Safe Travels

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
