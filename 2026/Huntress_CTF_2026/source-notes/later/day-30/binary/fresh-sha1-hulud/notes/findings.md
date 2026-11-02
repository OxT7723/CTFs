> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

> **SHA1-Hulud chronology:** The original Game AI investigation predates the successful account in `source-notes/user-updates/sha1-hulud-web-pro-writeup.md`. Earlier claims that the flag check was an irreversible input KDF are superseded. A recorded local verification and a Game Master completion claim are distinct evidence. The complete successful emulator and its companion files are not present in these uploads.

# SHA1-Hulud — Findings Record

## Completion update (2026-10-31)

The Game Master status endpoint now returns `CORRECT` for the existing
Single Solve attempt and lists answer ID `flag` as accepted. The service
recorded completion at `2026-10-31T15:32:26.832Z`. The successful submission
text was not preserved in this workspace. The unresolved conclusion and
candidate hypotheses below describe the investigation before that completion
and should not be treated as current status.

Challenge: `binary-reverse-engineering-day-30-sha1-hulud` (Day 30 Binary, Single Solve, untimed)
Artifact: `sha1_hulud.zip` SHA256 `9fc7b3bcb00c9b6ea174ac6cd17729912aa7588838722959e5cac9611aff8c38`
Binary: `extracted/sha1-hulud.exe` (PE32+ x86-64, Rust), 632832 bytes,
SHA256 `c03f48392c8bbfd5ba3faf5260b6ca658e08b099aef0f5c8dbf782edd5d13e89`
Zip password: `infected`
Prompt theme: "SHA1-Hulud" (pun: Dune sandworm / Sept-2025 npm "Shai-Hulud" worm + SHA1);
"TeamPCP dropped the ball with this payload name"; "Anyway, here's Wonder Wall!"

## VERIFIED FINDINGS

1. **Rust PE with `embre` encrypted-string crate.** Two schemes, both reversed:
   - `.xsobf` seed scheme: splitmix64-style keystream from a u32 seed.
     Verified keystream fn (see `analysis/decrypt_all.py`):
     rol(seed,17)^C0 -> per-byte: z=(x^x>>29)*MA; z=(z^z>>27)*MB; out=(z>>55)^((z&0xffffffff)>>24).
     Constants C0=0x5d2e9c47a1b386f0 MA=0x41169ddc6c156db1 MB=0xa3d1f5bb9847a411 STRIDE=0x065767ac2ba816c3.
   - `.rdata` adjacent cipher+key XOR scheme via helper `0x14005dc8a`.
2. **All 37 `.xsobf` secrets decrypted = anti-analysis only** (no password/flag embedded).
   Blocklist (process/tool names): x64dbg, x32dbg, ollydbg, windbg, kd, cdb, ida/ida64/idaq/idaq64,
   ghidrarun, dnspy, wireshark, fiddler, httpdebuggerpro, procmon/procmon64, procexp/procexp64,
   processhacker, systeminformer, pestudio, die, hxd, rehex, cheatengine, scylla/scylla_x64, autoruns,
   tcpview, regmon, filemon, apimonitor, immunitydebugger, kd. Registry: `SOFTWARE`,
   `SYSTEM\CurrentControlSet\Services`, `\drivers` (driver enumeration).
3. **Anti-debug** via API-hash resolver `0x140064480` (ecx=0x130ab4b2 base, edx=per-API hash) ->
   NtQueryInformationProcess with classes DebugPort=7, DebugObjectHandle=0x1e, DebugFlags=0x1f,
   and SystemKernelDebuggerInformation=0x23. Each sets a flag combined into the check.
4. **Control-flow flattening**: `main` is one giant dispatch loop (0x14003c1c0 .. 0x14005a200).
5. **Hash pipeline** (the gate):
   - First SHA-1 init at `0x14003cbbd` (H0..H4 = 67452301 efcdab89 98badcfe 10325476 c3d2e1f0; standard SHA-1
     IV present in image; round constants K are compiler-inlined/not stored). Operates over input.
   - **Custom slow KDF** at `0x14004194d`: loop count **0x2aea540 = 44,901,696 iterations**. Each round:
     gather 8 bytes from buffer `rdi=[rbp+0x608]` (len `rsi=[rbp+0x6d8]`) at offset
     `((state>>32)*(rsi-7))>>32` (with 8-byte wrap when near end) into `[rbp+0x7d0]`, then
     `state ^= *(u64*)[rbp+0x7d0]; state *= 0xf8714df9dba9a23d; state ^= state>>29`.
     After loop: `[rbp+0x7a8] ^= (u32)state; [rbp+0xd08] ^= (u32)(state>>32)`.
   - 20-byte digest (5 u32: [0x7a8],[0xd08],r13,[0x708]+...) hex-formatted (fmt helper `0x1400638fe`,
     structs 0x1400882d8/0x1400882f0) for comparison.
6. **Constant-time compare**: dispatch block ending `0x140059cd9` does `bl=sil^dl; or [rbp+0xca8],bl`
   over the byte stream (indexed `[rbp+rcx+0x7d0]` vs `[rbp+rcx+0x7ce]`). `[rbp+0xca8]==0` iff all match.
7. **Success gate** `0x140059ce9`: `[rbp+0xca8]==0` -> sets `[rbp+0x5f8]`; at `0x14005a019` if nonzero it
   decrypts "correct, the flag is " (adjacent-key secret data=0x14008856e key=0x140088583, len 0x15) and
   prints it followed by the **trimmed user input** (trim fn `0x14003be92` strips \n then \r;
   formatter `0x14005acd0`; input String at `[rbp+0x180]`).
   => **THE FLAG EQUALS THE CORRECT INPUT** (the binary echoes your input verbatim as the flag).

## CONCLUSION
The gate is a genuine **one-way function** (input -> SHA-1 -> 44.9M-round slow mix -> digest -> compare to
fixed target). It cannot be inverted. The flag is whatever input produces the matching digest; the binary
just echoes that input back. So the flag must be RECOVERED (guessed/known) and VERIFIED by running — it is
not stored anywhere in the binary (full two-scheme embre sweep in `analysis/sweep_embre.py` found no
embedded flag/password, only anti-analysis strings).

## ENVIRONMENT / ORACLE OPTIONS (what can verify a guess)
- No `wine`, `qemu`, `box64`; **no network**; `apt` needs root -> cannot run the Windows PE locally.
- `unicorn` 2.1.4 is installed, but emulation only runs the check FORWARD (verify a guess); it cannot
  reveal the flag and has no more solving power here than the Game Master, which already knows the answer
  and (untimed Single Solve) imposes no penalty for an incorrect guess.
- Therefore the practical oracle is the **Game Master** itself: submit a candidate under answer_id "flag".

## HYPOTHESES (themed candidate flags to verify)
Pun/meme/worm theme. Format likely `flag{...}`. Candidates (Shai-Hulud worm + Oasis "Wonderwall" meme):
  flag{shai-hulud} / flag{shai_hulud} / flag{sha1_hulud} / flag{sh41_hulud}
  flag{wonderwall} / flag{anyway_heres_wonderwall} / flag{heres_wonderwall}

## ADDITIONAL VERIFIED (closes extraction avenues)
- KDF source buffer `[rbp+0x608]`/len `[rbp+0x6d8]` = the UTF-8-validated **input** itself
  (set at 0x14003d34a from input ptr `[rbp+0x7d8]`+off, len `[rbp+0x7e0]`). So the slow mix runs
  over the INPUT -> pure one-way input->digest. It is NOT "KDF over fixed data producing the flag",
  so the flag cannot be extracted by computing anything; it can only be verified.
- More anti-analysis: `rdtsc` + KUSER_SHARED_DATA (0x7ffe0008/000c/0010) timing checks;
  `cpuid` brand-string scan for "Intel"/"AMD" (0x65746e49 + 'l' / 0x444d41) = VM/sandbox CPU-vendor
  detection at ~0x140040128. The `cmp ...,0x6c`('l') is "Intel", NOT a leaked flag byte.

## FAILED / RULED OUT
- Themed `flag{}` guesses submitted to Game Master, ALL incorrect:
  flag{sha1_hulud} flag{sha1-hulud} flag{shai-hulud} flag{shai_hulud} flag{sh41_hulud}
  flag{sh4i_hulud} flag{sha1hulud} flag{wonderwall}
- Direct char-compare "flag leak" hypothesis: ruled out (the compares are Intel/AMD vendor detection).
- "Wonderwall"/"Wonder Wall" as a plain submission: tried by prior agent, incorrect.
- Embedded-plaintext-flag hypothesis: ruled out (full embre sweep = anti-analysis strings only).
- Local execution to brute-force: infeasible (one-way; 44.9M-round cost is deliberate anti-bruteforce)
  and no Windows runtime available.
- unzip (AES zip) -> use pyzipper; 7z absent -> pyzipper; crates.io/docs.rs for embre -> 403/offline.

## Emulator progress update — 2026-10-31

The original conclusion above that no emulator harness had been run is stale.
Speakeasy 1.5.11 was installed in an isolated `/tmp/sha1-hulud-venv`, and
instrumented runs executed the assigned binary without changing it.

- The binary compares `rsi` and `rdx` byte values at `0x140059cd9`; the loop
  processes 32 bytes. The prior durable note records the generated target as
  `bca76889233d3ef978581f9e11f788daf6397ca3045c979b70867fdcd3fd5cbe`.
- A TEB mismatch was fixed in the emulator: at `0x14002b872`, the runner writes
  Speakeasy's current thread ID (`0x434`) into `GS:[0x48]`. Before that, the
  binary generated invalid dynamic code.
- Dynamic code and the helper at `0x14001dfc0` implement SHA-1 compression.
  The caller performs the five-word feed-forward after the helper returns.
  Native C hooks for the transform and the input mixer let execution get past
  the earlier timeouts.
- Two image-mixer loops each have `0x2aea540` (45,000,000) rounds. Native
  helpers bypass them; both operate on the executable image. Candidate input
  affects their seed but is not the mixer source.
- Speakeasy does not deliver the binary's registered access-violation handler
  for the deliberate writes at `0x14003fad1` and `0x1400462e4`. Temporary
  hooks reproduced the handler's register changes and resumed at the intended
  instruction after each write. Both were observed to work.
- A later run completed three 8,066-block SHA-1 passes and moved into
  decompression/module checks. It did not reach the final comparison before
  timing out. The longer run was still active after about 140 seconds, but its
  process and `/tmp` logs did not survive the environment reset. Treat those
  counts and addresses as observations from that run, not as a saved report.
- A saved 600-second run stopped in a second 45,000,000-round loop at
  `0x1400481db`. A later complete run showed that both this loop and the earlier
  loop at `0x14004194d` mix the executable image, not the entered candidate.
- `analysis/solve_sha1_hulud_narrow.py` now contains the durable runner, with
  the thread-ID/VEH fixes, native SHA-1 and both mixer hooks, plus new captures
  for each comparison end, equality bit, and success gate. The full capture
  has since been executed; see the candidate-specific entries below.

### Full comparison reached — `Wonder Wall` rejected

The expanded runner completed a full run with `Wonder Wall` as input and
reached `0x14005a019`. The final success gate was `0`; the candidate is locally
rejected and was not submitted. The complete 816-byte-pair trace and 18
comparison-end records were logged in
`/tmp/sha1-hulud-narrow-2026-10-31d.log`. The committed
`analysis/local-comparison-capture.json` contains the latest completed
candidate, `flag{anyway_heres_wonder_wall}`. Every comparison ended with
mismatch `0xff`; these staged comparisons alone do not identify the flag
validator.

The two optimized 45,000,000-round mixer calls at `0x14004194d` and
`0x1400481db` both read the executable image at `0x140001000` with length
`0x7e000` (SHA-1 `d1c05014e162a7f2efffd2efe294aa5c46f232c8`). They are image
integrity work, not the flag-input KDF. This corrects the earlier handoff
interpretation of those mixers as input processing. The run recorded 59,359
SHA-1 compression calls, then exited with return value 0 after the failed
success check. No Game Master answer was submitted.

### Follow-up local candidate — `flag{wonder_wall}` rejected

On 2026-10-31, the durable runner completed a full run with
`flag{wonder_wall}`. It reached `0x14005a019`, all 18 mismatch accumulators
were `0xff`, and the final success gate was `0`. This candidate was not
submitted. Its full emulator output is in
`/tmp/sha1-hulud-narrow-flag-wonder-underscore-2026-10-31.log`.
The committed generic capture file records the later wrapped candidate.

No artifact was downloaded, changed, or re-hashed for this run. Keep this
candidate in the local-rejection ledger and avoid repeating it.

### Exact prompt text in flag wrapper — `flag{Wonder Wall}` rejected

The exact prompt phrase and capitalization wrapped as `flag{Wonder Wall}` was
run through the full local validator on 2026-10-31. All 18 mismatch
accumulators were `0xff`, the success gate at `0x14005a019` was zero, and the
module returned normally. It was not submitted. The full log is
`/tmp/sha1-hulud-narrow-flag-Wonder-Wall-2026-10-31.log`.

No artifact was downloaded, changed, or re-hashed. The two tested wrapper
spellings around “Wonder Wall” are both rejected locally.

### Full three-operand trace — `flag{anyway_heres_wonder_wall}` rejected

This prompt-derived candidate completed the full local path on 2026-10-31.
All 18 groups had mismatch `0xff`; the final gate was zero. It was not
submitted. The 816-pair current capture now also records `BL`, `SIL`, and
`DL` at each XOR, along with the iterator value. All groups' OR-reduced
mismatches remain `0xff`; the full log is
`/tmp/sha1-hulud-narrow-flag-anyway-heres-wonder-wall-2026-10-31.log`.

Captures from the earlier `Wonder Wall` and wrapped variants showed that both
previously recorded byte streams change with the candidate. Those captures
did not include `BL`, so they could not identify a fixed expected operand.
The current capture closes that instrumentation gap, but does not by itself
reveal the expected input or comparison target.

No new Game Master answer was submitted in this update. Do not resubmit any
answer already marked rejected in `attempted-flags.md`.

### Incomplete unwrapped replay — `anyway_heres_wonder_wall`

The unwrapped input was replayed, but execution stopped before the full
comparison finished. The partial trace contains 400 of 816 byte pairs across
9 of 18 comparison groups and has no success-gate observation. It is not a
pass/fail result and was not submitted. The trace is preserved in
`analysis/partial-no-wrapper-capture.json`; the temporary log is
`/tmp/sha1-hulud-replay-no-wrapper.log`.
