> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Mobile Android tools

`decode_puzzle_assets.py` scans APK JSON assets for a declared codec and
decodes plain text, indexed characters, ordered split pieces, reversed text,
Base64, direct hex, Caesar-shifted text, Base64 plus single-byte XOR payloads,
indexed byte tables, direct answer strings in reflection-dispatch assets, and
string tables in referenced secondary DEX files. Length-prefixed `HA` packets
are decoded in their declared byte order, leaving trailing protocol fields
outside the answer payload. DEX files are read as data; their header integrity
fields are checked by default, and bytecode is never loaded or executed. The runner's
`--fast` option skips those embedded DEX hash checks on the timed path. It uses the
codec, permutation, path, and key stored in each asset rather than a
challenge-specific answer. It also statically scans APK shared libraries
that export a secret or proof getter and reports their printable strings
without loading or executing the library. For APK-set bundles, it scans each
nested APK and joins indexed split fragments to the base split's decoded data.
The static DEX evaluator also reads secondary DEX files from APK assets as
data, verifies their header integrity, and follows reflective
`InMemoryDexClassLoader` calls without loading or executing that code. It
supplies `Assets.readSplit` from another APK in a bundle and emulates static
object fields needed by runtime-loaded modules.
`run_modes.py` matches these values
against the current mode's live answer format, so the same runner handles
randomized native-library and indexed-asset variants.
Indexed byte tables subtract the declared key plus the per-index step
(default `3`) from each encoded byte.
The `layered` codec Base64-decodes its payload, XORs each byte with the
declared key plus its byte index, then reverses the result.

`inspect_dex.py` prints DEX methods and instructions from the APK. Narrow its
output with `--class-regex` and `--method-regex`; its disassembly is kept free of
Androguard's internal log output. The Android SDK's `aapt`
can also display the binary manifest:

```sh
python3 -m pip install -r mobile-android-tools/requirements.txt
python3 mobile-android-tools/decode_puzzle_assets.py app.apk
python3 mobile-android-tools/inspect_manifest.py app.apk
python3 mobile-android-tools/inspect_dex.py app.apk --method-regex onCreate
aapt dump xmltree app.apk AndroidManifest.xml
```

On externally managed Python installations, create a virtual environment and
install the requirements there:

```sh
python3 -m venv mobile-android-tools/.venv
mobile-android-tools/.venv/bin/pip install -r mobile-android-tools/requirements.txt
mobile-android-tools/.venv/bin/python mobile-android-tools/run_modes.py CHALLENGE_ID
```

`inspect_manifest.py` reports exported activities and their intent-filter
actions, categories, and URI data. This is a quick way to identify externally
reachable deep links before following their handlers in DEX code. It reads the
manifest with `aapt`; it does not install or execute the APK.

## Safe attempt runner and offline regression

`run_modes.py` matches answers to the live response's exact question IDs.
When the start response includes a capability download path, the runner uses
the Game Master's `op=download` proxy operation for that artifact; it falls
back to `op=artifact` when no capability is provided. Single-artifact downloads
run directly; Mastery downloads run concurrently. The runner skips IDs already
accepted in the same attempt and submits outstanding answers together. A
`CORRECT` submission is treated as completion without an extra status request;
other results are checked with `op=status`. APK SHA-256 verification is
available with `--verify-sha256`; it is off by default. `--fast` skips the
embedded DEX SHA-1 and Adler-32 checks as well. ZIP structure, DEX sizes and
bounds, and answer format checks still run.
The Android decoder is imported before the start or retry request so its module
load does not fall inside the timed attempt.

Offline regression does not contact the Game Master or submit answers. Save a
response containing `questions`, `answer_ids`, and `artifacts`, then pass APKs
in the same order:

```sh
python3 mobile-android-tools/run_modes.py \
  --offline-response attempt.json \
  --offline-artifact task-1.apk \
  --offline-artifact task-2.apk
```

Time Trial and Mastery may start timers on legacy routes. Choose a route after
checking current Game Master metadata:

```sh
# Supported regular untimed route
python3 mobile-android-tools/run_modes.py CHALLENGE_ID --regular-untimed

# Legacy untimed practice after its ranked rotation is exhausted
python3 mobile-android-tools/run_modes.py CHALLENGE_ID --practice-untimed --fast

# Opt-in timed route
python3 mobile-android-tools/run_modes.py CHALLENGE_ID --ranked --run-for-time

# Legacy timed-by-default route; omit run_for_time
python3 mobile-android-tools/run_modes.py CHALLENGE_ID \
  --ranked --legacy-timed-default --retry --fast
```

If the untimed route is already solved, `start --run-for-time` can reconnect
to that solved attempt. Use `--retry --ranked --run-for-time` to advance to a
fresh timed variant after the previous attempt has ended.

Add `--fast` for a timed run when you accept skipping embedded DEX integrity
verification. It cannot be combined with `--verify-sha256`. For Exported Trust,
the assigned answer assets currently use the `plain` codec, so no embedded DEX
hash is calculated; `--fast` is retained for randomized and future DEX-backed
variants.

`--retry` advances to a new attempt. Use it only when the current attempt has
ended and the mode's retry is authorized. On a legacy route that has never
been started, `--ranked --legacy-timed-default` uses `op=start`, which may
start the timer. `--practice-untimed` sends the legacy `op=practice`
continuation and does not request a ranked attempt; use it only after status
and API metadata confirm the qualified ranked rotation is exhausted. Use
offline mode for preparation and regression work.

The `analysis` puzzle codec is handled by `solve_analysis_codec.py`. It follows
the app's reachable `Release.code` call chain and statically interprets the
needed DEX instructions, including arithmetic decoys, array-based steps,
immediate shifts, packed-switch dispatch, and reflective method calls. For JNI
`nativeShare` implementations in x86_64 libraries, it reads `nm` and `objdump`
output and emulates the arithmetic and supported conditional branches without
loading the library. This codec needs Androguard (from `requirements.txt`) plus
`nm` and `objdump`. The evaluator handles signed byte-array reads and writes,
and ignores continuation rows where `objdump` prints the remaining bytes of a
long immediate without a mnemonic.
