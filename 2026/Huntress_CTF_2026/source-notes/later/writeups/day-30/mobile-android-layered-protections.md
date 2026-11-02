> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 30 Mobile: Layered Protections

Completed Single Solve, regular untimed Time Trial and Mastery, plus timed
ranked Time Trial and Mastery. Each Mastery contained 14 deliveries and all
14 answer IDs were accepted.

The Single Solve APK uses the `layered` asset codec: Base64-decode the payload,
XOR each byte with `key + index` modulo 256, then reverse the bytes.

The Time Trial and Mastery APKs use the `analysis` codec. Follow the reachable
`Release.code` call chain and evaluate DEX as data; do not run the APK. This
variant needed `and-long/2addr` and `xor-int/lit16` support in the static
evaluator. Mastery also included one APK-set bundle, handled by the existing
split-asset reader. A timed Mastery variant loaded `assets/payload.dex` through
`InMemoryDexClassLoader`; the evaluator now checks and parses secondary DEX
assets as data, follows the reflective call, and tracks the context static
field without executing the APK.

The Mobile runner now handles these transforms and submits only answers that
match the live answer format and IDs. The Game Master returned `CORRECT` for
all five attempts. The timed Time Trial finished in 2.73 seconds end to end.
Timed Mastery decoding took 3.81 seconds after the analyzer update; the whole
attempt took about 126 seconds while diagnosing the missing secondary DEX
support.

When the regular mode is already solved, `start --run-for-time` can reconnect
to that old solve. Use `--retry --ranked --run-for-time` to get a fresh timed
variant after the prior attempt has ended.
