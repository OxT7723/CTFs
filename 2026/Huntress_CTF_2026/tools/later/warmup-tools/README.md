> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Warmups tools

`decode_base64_layers.py` reads an assigned file and decodes successive
standard or URL-safe Base64 layers, standalone Base32 layers, Adobe ASCII85,
numbered mixed-codec fragments (Base64, ROT13, hex, numeric byte forms,
URL/HTML/Unicode escapes, Base32, Base64URL, reversed text, Atbash, Caesar,
ROT47, Morse, and
Bacon-encoded hexadecimal nibbles), Ook! programs, count-prefixed
comma-separated character streams, percent-escaped bytes, decimal byte values,
whitespace-separated 8-bit binary bytes, hexadecimal byte strings,
reverse-ordered hexadecimal text, BOM-marked UTF-16/32 text, whitespace-
separated `U+` hexadecimal Unicode code points, gzip/bzip2/xz/zlib wrappers,
and Rail Fence transpositions. Counted character streams may include a
trailing separator while preserving literal commas as values. Readable
decompressed fragments stop before short words are
mistaken for another Base64 layer. Percent escapes are decoded as bytes, so
`+` stays literal and repeated encoding layers are handled alongside the
other formats. Numbered assignments can also contain
independently encoded trailing fragments; those are decoded before being
combined with the main text.
When the fragments directly reconstruct an instruction followed by a slug
after `Game Master:`, the decoder uses a fast path and skips exhaustive
Caesar, Rail Fence, and recursive fragment fallbacks. Unrecognized formats
still use the general decoder.
ROT13 may also wrap a Base64 layer. For numbered mixed-codec bundles, malformed
codec-shaped fragments are ignored, alternate suffix decodings are considered
alongside the plain text, and structured numbered parsing runs before generic
Brainfuck or Ook! detection.
For multi-artifact
bundles, `run_modes.py` infers a shared Rail Fence rail count from the assigned
blobs before preparing answers.
When a mode assigns separate deliveries, including Mastery, it downloads and
hash-checks each delivery and resolves questions to their matching set. It also
supports one archive containing multiple question-specific blobs.
`run_modes.py` starts or resumes a Warmups mode, downloads the assigned
artifact through its current capability link when available (falling back to
the artifact operation if that link has expired), uses the live answer format
to identify the slug (including hex-encoded fragments), submits it and saves
the attempt record. If the decoded final instruction explicitly names the
exact value to submit, extraction preserves that complete token even when it
does not fit the suggested pattern. If a multi-answer submission is incorrect,
it retries each answer ID separately to preserve accepted progress and identify
unresolved answers.

The runner needs only Python's standard library for text artifacts. It imports
`pyzipper` only when an assigned encrypted ZIP archive must be opened. For
those archives, use the binary tools virtual environment documented in
`binary-reverse-engineering-tools/README.md`. Run:

```sh
python3 warmup-tools/run_modes.py "$CHALLENGE_ID"
```

When a timed variant is exhausted, continue its last assigned material without
a clock using:

```sh
binary-reverse-engineering-tools/.venv/bin/python \
  warmup-tools/run_modes.py "$CHALLENGE_ID" --practice
```

For an explicitly authorized legacy timed retry, `--retry` advances the
completed attempt. `--keep-alive` first checks that the previous attempt has
ended, warms a persistent proxy connection, then reuses it for the retry, one
artifact download, submission, and status check. Other Mastery deliveries
remain concurrent. Current capability links are used for all assigned
deliveries; links that return 404 fall back to the artifact operation.
`--skip-artifact-hash` skips optional download hashing while keeping the
assigned bytes saved for later offline review. The runner submits only answer
IDs that are not already accepted in the current attempt.

For a separately authorized ranked run on a dual-pool route:

```sh
python3 warmup-tools/run_modes.py "$CHALLENGE_ID" \
  --run-for-time --skip-artifact-hash
```

The ranked runner reuses one proxy connection, selects a fresh ranked retry
after a completed attempt, resumes an active ranked attempt, and refuses to
advance while a regular attempt is still active. Its summary records the
ranked eligibility and timer fields. Skipping artifact hashing leaves the
artifact SHA-256 as `null`. After a slow local decode it refreshes the
keep-alive connection before submitting. If the submit response is lost, it
checks the same attempt's accepted answer IDs and resends only outstanding
answers. Timed runs save the original archive without expanding a duplicate
set of extracted files; the solver reads the archive directly.
Run summaries also include client-side timings for preflight, start, download,
artifact writes, decoding, submission, and final status. The elapsed time from
the start request through a correct submit response helps identify local and
network bottlenecks; the Game Master's deadline remains authoritative.
