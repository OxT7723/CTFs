> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

> **SHA1-Hulud chronology:** The original Game AI investigation predates the successful account in `source-notes/user-updates/sha1-hulud-web-pro-writeup.md`. Earlier claims that the flag check was an irreversible input KDF are superseded. A recorded local verification and a Game Master completion claim are distinct evidence. The complete successful emulator and its companion files are not present in these uploads.

# SHA1-Hulud — Focused Reversing Handoff

Scope: consolidates evidence already collected (disasm dumps `analysis/full_main_a.txt`
0x14003c1c0–0x140042000, `analysis/full_main_b.txt` 0x140059c00–0x14005a200, plus targeted
disasm of the trim/validation/compare functions). **Not** a fresh broad pass.

- Binary: `extracted/sha1-hulud.exe`, PE32+ x86-64, Rust. ImageBase **0x140000000**. RVA = VA − 0x140000000.
  SHA256 `c03f48392c8bbfd5ba3faf5260b6ca658e08b099aef0f5c8dbf782edd5d13e89`.
- Artifact `sha1_hulud.zip` (pw `infected`) SHA256 `9fc7b3bcb00c9b6ea174ac6cd17729912aa7588838722959e5cac9611aff8c38`.
- `main` is one control-flow-flattened dispatch function spanning ~0x14003c1c0–0x14005a200.

Legend: **[E]** directly established from bytes/disasm · **[I]** inferred/not yet byte-verified.

---

## 1. Input-handling and validation functions

### Input read + storage  [E/I]
- [I] Input is read via Rust std `io::Stdin::read_line` (exact call site not pinpointed; prompt string
  "What is the flag?" is an embre `.rdata` secret). The resulting `String` lives at **`[rbp+0x180]`**
  (ptr,len,cap) — confirmed because the success path formats `[rbp+0x180]` as "the flag" (§5). [E]

### Trailing-whitespace trim — `0x14003be92` (RVA 0x3be92)  [E]
Generic `str::trim_end_matches(ch)`; `rcx`=ptr, `rdx`=len, `r8d`=char to strip. Called twice (`\n` then `\r`).
```
0x14003be92: ...                      ; prologue, r14 = &range{start=rsi, end=rsi+rdx}
0x14003beba: call 0x14003be14         ; decode last char / char-boundary classify -> eax, edx=char
0x14003bebf: cmp eax,1                 ; valid 1-char?
0x14003bec2: jne  -> done
0x14003bed0: cmp ecx,edi               ; char == trim target?
0x14003bed2: je   loop                 ; yes -> shrink len, repeat
0x14003bed6: xor ebx,ebx               ; (empty)
0x14003bed8: mov rax,rsi; mov rdx,rbx; ret   ; returns (ptr, new_len)
```
Pseudocode: `fn trim_end(s, c) { while s.ends_with(c) { s = &s[..len-1] } s }`.

### Anti-analysis aggregator / final validation — `0x14003c33b` (RVA 0x3c33b)  [E]
Called at `0x14005a005` with `rcx` = &results slice (the booleans assembled at 0x140059f99–0x14005a001).
Scans bytes for the first `== 1`; returns `al = (found_before_end)`.
```
0x14003c33b: r8=[rcx]; rax=[rcx+8]          ; start,end of &[u8]
loop: cmp r8,rax; je end
      [rcx]=r8+1; cmp byte[rdx],1; jne loop ; advance until a byte==1
end:  cmp rdx,rax; setne al; ret            ; al=1 if a tripped check was found
```
Caller: `call 0x14003c33b; test al,al; jne 0x14005a158` → **any tripped check ⇒ skip success**.
(Nearby `0x14003c35d` = u16-slice length-to-NUL helper; `0x14003c38a` = large 0x1238-frame subroutine,
not required for the gate.)

Environment/anti-analysis inputs feeding that results array (all **[E]**, assembled 0x140059dca–0x14005a001):
- API-hash resolver `0x140064480` (base hash ecx=0x130ab4b2) → `NtQueryInformationProcess`
  classes 7 (DebugPort), 0x1e (DebugObjectHandle), 0x1f (DebugFlags); and SystemInformation
  class 0x23 (SystemKernelDebuggerInformation).
- `rdtsc` + KUSER_SHARED_DATA timing reads `0x7ffe0008/000c/0010` (0x14003d39a–0x14003d3bf).
- `cpuid` leaf 0x80000002–4 brand-string scan for "Intel" (0x65746e49 + 'l'=0x6c) / "AMD" (0x444d41)
  at ~0x140040128 (hypervisor/VM + vendor detection).
- Process/driver blocklist: 37 `.xsobf` secrets (§6).

---

## 2. Exact input processing

- **Encoding** [E]: UTF-8. While feeding SHA-1, chars are validated/decoded via `0x140064168`,
  `0x1400641b3`, `0x140064146`, copy `0x140066aac` (0x14003d2a3–0x14003d302); invalid input bails to
  `0x14003c33b`/cleanup.
- **Trimming** [E]: trailing `\n` then `\r` removed via `0x14003be92` (§1) before use.
- **Length checks** [E]: KDF requires **len ≥ 8** (`cmp qword [rbp+0x6d8],8` @0x1400418d4; it uses `rsi-7`).
  No other explicit length/equality gate observed. [I] No fixed-length requirement found.
- **Prefix removal** [E]: **none** found. The `cmp …,'l'` / "Intel"/"AMD" compares are CPU-vendor
  detection, **not** a `flag{` prefix strip.
- **Whole input vs slices** [E]: The KDF **source buffer = the whole input** — ptr `[rbp+0x608] =
  input_ptr([rbp+0x7d8]) + off`, len `[rbp+0x6d8] = input_len([rbp+0x7e0])` (set @0x14003d34a/0x14003d35b).
  Each KDF round reads an **8-byte window** from that whole buffer at a PRNG-chosen offset (§3). So the
  KDF consumes the entire input as a lookup table, indexing 8-byte slices — not fixed chunks.
- SHA-1 is also computed over the whole input (streaming, big-endian word packing `bswap` @0x14003d332).

---

## 3. KDF / hash identification and parameters

### Stage A — SHA-1 over input  [E]
Standard SHA-1. Init vector loaded @`0x14003cbbd`:
`H0=67452301 H1=efcdab89 H2=98badcfe H3=10325476 H4=c3d2e1f0` (little-endian in image; present verbatim).
Round constants K are compiler-inlined (not stored as data). [I] Standard padding/80-round schedule
assumed (Rust `sha1` crate) — not byte-audited.

### Stage B — custom slow KDF — loop @`0x14004194d` (RVA 0x4194d)  [E]
- **Rounds / cost**: `cmp r9, 0x2aea540` ⇒ **44,901,696 iterations** (anti-bruteforce).
- **Multiplier**: `rbx = 0xf8714df9dba9a23d`.
- **State init** (0x1400418d4–0x140041943): `rcx = [rbp+0x708] ^ rdx ^ rol(r13,17)`, where `rdx`,`r13`
  derive from the Stage-A SHA-1 words. [I] exact word→rcx packing not fully re-derived.
- **Per round**:
  ```
  off = ((rcx>>32) * (len-7)) >> 32           ; PRNG-selected byte offset into input buffer
  if off+8 <= len: g = u64 at input[off..off+8]
  else:            g = 8 bytes wrap-read mod len   ; (0x14004196e loop)
  rcx ^= g
  rcx  = rcx * 0xf8714df9dba9a23d
  rcx ^= rcx >> 29
  ```
- **After loop** (0x1400419c5): `[rbp+0x7a8] ^= (u32)rcx ; [rbp+0xd08] ^= (u32)(rcx>>32)`.

### Salt  [I]
None established. No distinct salt constant observed; the only "seed" into Stage B is SHA-1(input).

### Output length  [E/I]
- [E] 20-byte digest assembled from 5 u32: `[0x1a8]=[0x7a8]`, `[0x1ac]=[0xd08]`, `[0x1b0..]=r13`,
  `[0x1b8]=[0x708]` (0x140041a00–0x140041a26), then **hex-encoded** (5× loop, fmt helper `0x1400638fe`,
  structs 0x1400882d8/0x1400882f0) producing a **40-char lowercase hex** string, `bswap`-normalized
  into `[rbp+0xd10]` (0x140041ac3–0x140041ad9).
- [I] "20-byte digest → 40 hex chars compared" is the strong reading; exact word order in the final
  string not byte-audited.

### Target bytes  [I — NOT RECOVERED]
The comparison target (the 40-hex expected string, or 20 raw bytes) has **not** been extracted. It is the
*other* operand of the zip-compare iterator (§4) and is not among the decoded `.xsobf` secrets. **Open item.**

---

## 4. KDF output → final decision

1. Fold KDF result into SHA-1 words (§3 "After loop").
2. Assemble 5-u32 digest, hex-encode to 40 chars, store at `[rbp+0xd10]` (big-endian normalized).
3. **Constant-time comparison** — flattened zip-iterator, dispatch head `0x140058a14`:
   - Iterates two byte sequences in **8-byte (u64) chunks** (`[rbp+0x818]=8` set @0x140058ae4).
   - Tail arithmetic (`full_main_b.txt` 0x140059c00–0x140059cd9): masks the final partial chunk, then
     ```
     xor bl, sil        ; sil,dl = corresponding bytes/limbs of the two operands
     xor bl, dl
     or  byte [rbp+0xca8], bl     ; accumulate ALL differences (no early exit = constant-time)
     ```
   - [E] **Comparison is equality of the two byte sequences, OR-accumulated into `[rbp+0xca8]`.**
   - [I] **Bytes compared = 40** (the hex digest; 5 u64 chunks). Exact count not asserted from a
     terminating constant — inferred from the hex-encode length.
4. Decision `0x140059ce9`: `cmp byte [rbp+0xca8],0 ; sete al` ⇒ `[rbp+0x5f8] |= al` (hash match = 1).
5. Separately, `0x14005a005` calls the anti-analysis aggregator (§1); **any tripped check skips success**.
6. Success gate `0x14005a019`: proceeds only if `[rbp+0x5f8] != 0`.

**Net:** success ⇔ (hex(digest(input)) == target) **AND** (no anti-analysis check tripped).

---

## 5. Success branch — what it does  [E]

It does **not** decrypt or construct a different flag. On success (0x14005a02b–0x14005a114):
- Decrypts the embre `.rdata` secret **"correct, the flag is "** (adjacent-key pair data=0x14008856e,
  key=0x140088583, len 0x15) via helper `0x14005dc8a`.
- Formats that literal **followed by the trimmed user input at `[rbp+0x180]`** (formatter `0x14005acd0`,
  stdout path 0x14005a0a9) and prints it.
⇒ **The flag is echoed verbatim from the input.** The binary reveals nothing new; it only confirms a
correct candidate. (Failure path: cleanup → `0x14005a158`, no output.)

---

## 6. embre extraction results already obtained

Two embre schemes, both reversed (scripts below). **No password/flag embedded** — only anti-analysis.

### Scheme A — `.xsobf` seed/keystream  [E]
`.xsobf` section RVA 0x9e000. Keystream from u32 `seed` (verified in `analysis/decrypt_all.py`):
```
state = rol(seed,17) ^ 0x5d2e9c47a1b386f0 ; r9=0
per byte: x = r9 ^ state
          z = (x ^ x>>29) * 0x41169ddc6c156db1
          z = (z ^ z>>27) * 0xa3d1f5bb9847a411
          out = (z>>55) ^ ((z & 0xffffffff)>>24)
          r9 += 0x065767ac2ba816c3
ct byte at .xsobf[off]; pt = ct ^ keystream
```
37 secrets decoded (offset/len/seed in sweep output). Plaintext set:
- Registry: `SOFTWARE`, `SYSTEM\CurrentControlSet\Services`, `\drivers`.
- Tool/process blocklist: cheatengine, httpdebuggerpro.exe, pestudio.exe, hxd.exe, wireshark.exe,
  procexp.exe/procexp64.exe, tcpview.exe, autoruns.exe, scylla_x64.exe/scylla.exe, cdb.exe, die.exe,
  procmon.exe/procmon64.exe, ghidrarun.exe, idaq64.exe/idaq.exe/ida64.exe/ida.exe, rehex.exe,
  processhacker.exe, x32dbg.exe/x64dbg.exe, ollydbg.exe, regmon.exe, filemon.exe, fiddler.exe,
  systeminformer.exe, apimonitor, immunitydebugger.exe, windbg.exe, kd.exe, dnspy.exe.

### Scheme B — `.rdata` adjacent cipher+key XOR  [E]
Helper `0x14005dc8a`; struct {data_ptr,len,key_ptr,key_len}; `pt = data ^ key`. Recovered:
- "What is the flag?" (prompt).
- "correct, the flag is " (success literal; data=0x14008856e key=0x140088583 len=0x15).

### Unexplained blobs  [I]
- The **comparison target** (§3/§4) — location unknown; not in decoded `.xsobf`. Likely a Scheme-B
  adjacent-key secret or a runtime-built string. **Not recovered.**
- `analysis/sweep_embre.py` Scheme-B (adjacent-key) detector returned **0 hits** — a detector bug
  (the two known Scheme-B strings were decoded by hand, not by the sweep). So Scheme-B secrets are
  **not** exhaustively enumerated; the target may be among them.
- A few 1–2 byte `.rdata` "seed" hits in the sweep (off 0x88388/0x88398/0x88420/0x88438) are noise.

---

## 7. Scripts and their actual test results

All under `analysis/`. **Executed** unless marked otherwise.

- `decrypt_all.py` — **EXECUTED**. Decoded all 37 `.xsobf` secrets (region 0x14003e400–0x14003fe00);
  keystream function verified (readable ASCII output). Trustworthy.
- `decrypt_xsobf.py` — earlier variant of the above; superseded by `decrypt_all.py`.
- `sweep_embre.py` — **EXECUTED**. Full-binary resilient scan. Seed-scheme results = the 37 anti-analysis
  strings + noise. Adjacent-key results = **0 (detector bug, see §6)**. Found **no** embedded flag/password.
- `disasm.py` — annotated linear disassembler tool (`python3 disasm.py <start_hex> <end_hex>`); used to
  produce `full_main_a.txt`, `full_main_b.txt`, and the §1/§4 targeted dumps.
- **No verifier / emulator exists.** `unicorn` 2.1.4 is installed but **no harness was written or run** —
  there are **no executed emulation results**. The KDF/SHA reimplementation described in §3 is **untested**.

---

## Open items (ordered)
1. **Recover the comparison target** (40-hex or 20 raw bytes) — fix `sweep_embre.py` Scheme-B detector
   and/or Unicorn-emulate to the compare and read the second operand.
2. Build a verified oracle: Unicorn-emulate Stage A+B on a candidate to read the computed digest and the
   target (stub anti-analysis resolver `0x140064480`→0). Then a native C reimpl for fast wordlist testing.
3. Flag itself: one-way over input + echoed on success ⇒ must be the specific themed input. GM guesses so
   far all incorrect (see `notes/findings.md`). An oracle only *verifies* a guess; it cannot invert.

## Addendum — emulator work on 2026-10-31

Sections above describe the state before the Speakeasy tracing work; their
claims that no emulator was run are historical. The final compare code around
`0x140059cd9` was observed processing byte streams. Earlier notes record a
runtime target of
`bca76889233d3ef978581f9e11f788daf6397ca3045c979b70867fdcd3fd5cbe`; it has
not yet been mapped to the final input comparison.

An instrumented Speakeasy 1.5.11 runner corrected the TEB thread ID at
`0x14002b872` and reproduced the binary's two deliberate write-fault handlers
at `0x14003fad1` and `0x1400462e4`. Both 45,000,000-round loops at
`0x14004194d` and `0x1400481db` read the executable image at
`0x140001000`, length `0x7e000`; they are image-integrity work, not the
candidate KDF.

The full `Wonder Wall` run completed and reached `0x14005a019` with its success
gate at zero. Its candidate is rejected locally and was not submitted. The run
recorded 59,359 SHA-1 compression calls and 816 compare-byte pairs across 18
comparison results. All 18 mismatch accumulators were `0xff`. The exact trace
was logged in `/tmp/sha1-hulud-narrow-2026-10-31d.log`. The committed
`analysis/local-comparison-capture.json` contains the latest completed run,
`flag{anyway_heres_wonder_wall}`. The durable runner is
`analysis/solve_sha1_hulud_narrow.py`; use it and
`attempted-flags.md`/`resume-notes.md` as the current state. The artifact
executable and assigned ZIP remain unchanged.

### Follow-up candidate — `flag{wonder_wall}` rejected

The same runner completed with `flag{wonder_wall}` on 2026-10-31. All 18
mismatch accumulators were `0xff`; the final success gate at `0x14005a019`
was zero. It was not submitted. The full log is
`/tmp/sha1-hulud-narrow-flag-wonder-underscore-2026-10-31.log`.
The committed generic capture file now records the later
`flag{anyway_heres_wonder_wall}` run.

No artifact download or hash check was performed. At the time this addendum
was written, the prompt's literal capitalization and spacing inside a
`flag{...}` wrapper remained untested; the follow-up below records that run.
Prefer extracting the comparison target or reducing the local run cost before
starting another full pass.

### Exact prompt spelling wrapped as a flag — rejected

`flag{Wonder Wall}` completed the full local run on 2026-10-31 and was
rejected: all 18 mismatch accumulators were `0xff` and the final gate was zero.
It was not submitted. Its full log is
`/tmp/sha1-hulud-narrow-flag-Wonder-Wall-2026-10-31.log`. This closes the
prior note's prompt-casing variant. No artifact was re-downloaded or hashed.

### Three-operand capture — `flag{anyway_heres_wonder_wall}` rejected

The untried full prompt phrase in a flag wrapper was also run locally and
rejected: all 18 mismatch accumulators were `0xff`; the final gate was zero.
The run was not submitted. The new capture hook saves `BL`, `SIL`, and `DL`
at each XOR and the iterator state; `analysis/local-comparison-capture.json`
now contains 816 such records. Full log:
`/tmp/sha1-hulud-narrow-flag-anyway-heres-wonder-wall-2026-10-31.log`.
The extra byte stream closes a tracing gap but has not exposed the expected
input.

### Incomplete unwrapped replay — `anyway_heres_wonder_wall`

The unwrapped input was also replayed, but execution stopped before the full
comparison finished. The partial trace contains 400 of 816 byte pairs across
9 of 18 comparison groups and has no success-gate observation. It is not a
pass/fail result and was not submitted. The trace is preserved in
`analysis/partial-no-wrapper-capture.json`; the temporary run log is
`/tmp/sha1-hulud-replay-no-wrapper.log`.
