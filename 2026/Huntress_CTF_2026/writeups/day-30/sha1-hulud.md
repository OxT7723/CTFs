# SHA1-Hulud

Day 30 · Binary reverse engineering · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

> **Consolidation update:** The author reports solving SHA1-Hulud with ChatGPT Pro on the web. The account below reports successful instrumented forward-checker verification; the later repository review records Game Master acceptance, though the raw response and accepted submission payload were not supplied. The local archive and executable sizes and SHA-256 hashes match this writeup, and its recorded plaintext blocks decode to the stated 38-byte flag. The original harness, verification logs, and companion bundle were not attached, so the dynamic verification and arithmetic test results below remain attributed to that session.

## Final scoring evidence

The supplied scoreboard independently records the **5-point SHA1-Hulud award** at `2026-10-31T15:32:27.237Z`. That corroborates challenge completion. It does not recover the submitted flag text or reproduce the instrumented checker described in the supplied account.

Source: [scoreboard-derived challenge completion](../../results/challenge-completion.csv).

## Subsequent Game Master confirmation

The updated repository writeup records a read-only status check on October 31: `CORRECT`, with answer ID `flag` accepted for attempt `353f3c79-6a5e-42b3-b061-0b531ec2e59e`, and completion time `2026-10-31T15:32:26.832Z`. Only Single Solve is offered. This supplements the original Pro-session account below; its statement that no acceptance response was captured refers to that analysis session. The successful submission text was not retained, so the status record alone does not establish the submitted string.

## Challenge information

| Field | Value |
| --- | --- |
| Challenge | SHA1-Hulud |
| Event | Huntress CTF 2026 |
| Category | Binary Reverse Engineering |
| Day | 30 |
| Author | Nordgaren |
| Challenge ID | `binary-reverse-engineering-day-30-sha1-hulud` |
| Mode | Single Solve |
| Archive | `sha1_hulud.zip` |
| Archive password | `infected` |
| Analysis date | October 31, 2026 |

> **Spoilers:** This write-up includes the recovered flag, important code locations, and the inversion method.

### Challenge prompt

> I made this challenge because I was really upset that TeamPCP dropped the ball with this payload name. Anyway, here's Wonder Wall!
>
> The password for this archive is **`infected`**.

### Recovered flag

```text
flag{036ab4254094db8ace3a9e87d45bffe3}
```

### How the solve progressed across AI tools

We first worked on SHA1-Hulud with Codex, but reached the usage limit before getting a solve. We then spent hours working with the Homebase VM AI without reaching a solution. Those attempts left useful investigation notes, but the challenge remained unresolved.

The breakthrough came after moving the analysis to ChatGPT on the web with Pro mode selected. That session recovered the flag and reported the instrumented forward-checker verification described below. This was an AI-assisted solve across several sessions; ChatGPT in Pro mode produced the successful recovery.

### Summary

SHA1-Hulud is an obfuscated, Rust-based Windows x64 flag checker. Its hashing, exception-dependent helpers, environment checks, and encoded data made it difficult to reach the actual validation logic. The successful approach was to recover the checker's expected encrypted bytes and reverse the transformations applied to the input, rather than guess hashes or words from the prompt.[^artifact][^record]

The decisive sequence was:

1. Trace the normalized input into the validation routine.
2. Capture the expected byte stream at the final comparison, after its decoding layers.
3. Reverse a backward-running block transform, then a stateful forward-running transform.
4. Decode the resulting length-prefixed plaintext records and distinguish the actual flag from decoys.
5. Supply the recovered flag to the forward checker without the recovery hooks and inspect the comparison result.

The recorded verification run had **zero mismatches across the final 48-byte comparison**, a zero comparison-difference accumulator, and a success accumulator of `1`.[^record]

**Evidence scope:** This documents an AI-assisted solve grounded in the uploaded executable and recorded analysis output. Verification was performed in a controlled, instrumented analysis harness, not by launching the unmodified executable in a normal Windows session. No Game Master acceptance response was captured in the analysis record.

---

## 1. Artifact identification and initial inspection

The supplied archive contains one executable, `sha1-hulud.exe`. Its hashes and PE metadata were rechecked while preparing this write-up.[^artifact]

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `sha1_hulud.zip` | 226,112 bytes | `9fc7b3bcb00c9b6ea174ac6cd17729912aa7588838722959e5cac9611aff8c38` |
| `sha1-hulud.exe` | 632,832 bytes | `c03f48392c8bbfd5ba3faf5260b6ca658e08b099aef0f5c8dbf782edd5d13e89` |

The executable's SHA-1 is:

```text
2b99e45129c2a5fd194493ffc79672695cf9b1ed
```

That is an artifact identifier, **not the flag**.

Equivalent initial triage commands are:

```bash
sha256sum sha1_hulud.zip
mkdir -p artifact
7z x -pinfected sha1_hulud.zip -oartifact
file artifact/sha1-hulud.exe
sha256sum artifact/sha1-hulud.exe
sha1sum artifact/sha1-hulud.exe
objdump -p artifact/sha1-hulud.exe
strings -a artifact/sha1-hulud.exe
```

The archive uses AES-encrypted ZIP entries. A ZIP reader without that support will fail even with the correct password; this is an extraction-tool limitation, not another puzzle.

The PE is a 64-bit Windows console executable with nine sections. Rust runtime and source-path strings are visible in its ordinary strings output. Important metadata is:[^artifact]

```text
Machine:          0x8664 (x86-64)
Image base:       0x140000000
Entry-point RVA:  0x7a5c4
Image size:       0xa1000
```

Selected sections:

| Section | RVA | Virtual size | Raw size | Raw file offset |
| --- | --- | --- | --- | --- |
| `.text` | `0x1000` | `0x7d976` | `0x7da00` | `0x400` |
| `.rdata` | `0x7f000` | `0x18b34` | `0x18c00` | `0x7de00` |
| `.data` | `0x98000` | `0x1d84` | `0xc00` | `0x96a00` |
| `.xsobf` | `0x9e000` | `0x1ad` | `0x200` | `0x99a00` |

The distinction between raw size, virtual size, and mapped/page-rounded size mattered. Several early hash candidates were based on different interpretations of the code region.

**Handling note:** Treat the challenge executable as untrusted. Static inspection and the companion Python arithmetic examples do not require launching it. Reproducing the dynamic work belongs in a disposable analysis environment.

## 2. Early findings and false leads

Before the successful solve, the Game AI had already spent substantial effort on the executable. Its progress log was useful, but it also contained hypotheses that were later contradicted.[^game-log]

The most important early finding was the prompt:

```text
What is the flag?
```

It is stored as two XOR-obfuscated arrays. XORing 17 bytes at virtual addresses `0x140088548` and `0x140088559` reconstructs the 17-character prompt. This was independently rechecked against the uploaded executable.[^artifact]

That established a better starting point than the challenge title: the program asks for input, so the useful question is **how that input is validated**.

The earlier log reported rejected submissions based on the executable's SHA-1, the literal phrase `Wonder Wall!`, a mapped `.text` digest, a reconstructed code-region-plus-trailer digest, and SHA-1 of `Wonderwall`. Those experiments did not identify the expected answer.[^game-log]

The log also showed why the analysis kept stalling:

- Speakeasy reached the prompt but initially could not handle `ReadConsoleW`.
- Exception-driven code did not behave correctly under the emulator's Windows model.
- Thread/environment state was inconsistent, including a value read through `GS:[0x48]`.
- A later path accessed the shared-data region at `0x7ffe0000`, which was not initially mapped.

One particularly expensive detour was assuming that a long sequence of SHA-1 compression calls must produce the flag. The log eventually identified a `0x7e044`-byte hashing input: a page-rounded code region plus a 68-byte trailer. Submitting the reconstructed digest still failed.[^game-log]

The right conclusion was not "all hashing is irrelevant." Hash-related state was entangled with later processing. The useful distinction was:

> A hash can be part of integrity checking or key/state derivation without being the answer to submit.

## 3. Moving from general emulation to targeted instrumentation

The successful analysis used a custom C instruction interpreter, together with controlled native execution of selected protected helper routines. Windows API calls and environment-dependent behavior were handled through explicit hooks and modeled memory.[^record]

This was a hybrid approach: it was neither a full Windows environment nor a purely static decompiler pass. The harness mapped the PE image, supplied stack and heap memory, provided consistent thread state, and modeled required Windows behavior. Recorded work also included a local LZNT1 decompression implementation; a relevant decompression produced 8,717 bytes.[^record]

The important engineering choices were:

**Preserve the distinction between environment fixes and answer manipulation.** Timing checks, API behavior, and protected-helper dispatch needed analysis-specific handling. That did not justify forcing the final comparison to succeed.

**Keep the hashing behavior faithful enough for downstream state.** The successful harness called selected original protected helpers rather than assuming that every SHA-1-looking routine could safely be replaced with a generic hash function.

**Inspect meaningful checkpoints instead of tracing everything equally.** Once execution reached the actual transformation and comparison code, snapshots of registers, local state, and block data were much more useful than another long stream of anti-analysis instructions.

There were two separate uses of instrumentation. During recovery, hooks injected inverse-derived intermediate values so the program could advance its state with the recovered plaintext. During verification, the candidate was supplied as ordinary input to the forward checker; those inverse-recovery hooks were not used.[^record]

This separation matters: a success branch reached after forcing an answer is not verification.

## 4. Following the input

The normalization code trims surrounding whitespace and converts ASCII uppercase letters to lowercase. The explicit `A` through `Z` conversion is visible around `0x14004a6c3`. The normalized input pointer and length are then retained for block construction.[^static]

For the recovered ASCII flag, the plaintext record has this layout:

```text
little-endian uint64 input_length
input_length bytes of normalized input
zero padding to a 16-byte boundary
```

The flag is 38 bytes long. Therefore:

```text
8-byte length + 38-byte flag + 2-byte padding = 48 bytes
```

The checker operates on three 16-byte blocks, not just the 38 printable flag characters. Recovering and validating the length prefix was a useful consistency check.

### Important code locations

All addresses below are virtual addresses at image base `0x140000000`, not raw file offsets. Subtract that base to obtain an RVA.[^static][^record]

| Address | Role in the analysis |
| --- | --- |
| `0x14004a6c3` | ASCII input-lowercasing loop |
| `0x14004a702` | Post-normalization checkpoint and block-count setup |
| `0x14005833b` | Forward-pass key/state setup |
| `0x140058548` | Forward block-transform input; inverse-recovery hook point |
| `0x14005868d` | Forward block-transform output |
| `0x14005887d` | Backward block-transform round loop; capture state at round zero |
| `0x1400589cd` | Start of the final byte-comparison phase |
| `0x140058b0f` | Capture the current transformed-input byte |
| `0x140059cd9` | Combine comparison terms and accumulate differences |
| `0x140059ce9` | Convert a zero difference into a successful match |

## 5. Recovering the expected comparison bytes

The expected ciphertext was not presented as one convenient, contiguous plaintext constant. The validation code decoded and combined data as it compared each byte.

Instead of completely reconstructing every upstream encoding layer first, the analysis captured values immediately before the comparison accumulated its result.

The relevant instructions are:[^static]

```asm
0x140059cd9: xor  bl, sil
0x140059cdc: xor  bl, dl
0x140059cde: or   BYTE PTR [rbp+0xca8], bl
```

At `0x140058b0f`, the harness saved the transformed-input byte from `RDX`. At `0x140059cd9`, it recorded the three low-byte terms about to be XORed. Conceptually:

```python
# Capture at 0x140058b0f:
actual_byte = rdx & 0xff

# Capture immediately before 0x140059cd9:
difference = (rbx ^ rsi ^ rdx) & 0xff
expected_byte = actual_byte ^ difference
```

The original logging hook expressed the second operation as:

```c
(rawcmp ^ r[3] ^ r[6] ^ r[2]) & 255
```

Here, the interpreter's register slots `r[3]`, `r[6]`, and `r[2]` represented `RBX`, `RSI`, and `RDX`.

This exposed the expected bytes at the point where all the preceding decoding mattered, without treating the program's current input as the answer. The captured records were grouped by the checker's loop indices, labeled `i` and `j` in the analysis.[^record]

At the end of each comparison, the binary performs:[^static]

```asm
0x140059ce9: cmp  BYTE PTR [rbp+0xca8], 0
0x140059cf0: sete al
0x140059cf3: mov  rcx, QWORD PTR [rbp+0x5f8]
0x140059cfa: or   cl, al
0x140059cfc: mov  QWORD PTR [rbp+0x5f8], rcx
```

Thus, `rbp+0xca8` is the comparison-difference byte at this point, and `rbp+0x5f8` accumulates successful matches. These became the decisive verification checkpoints.

## 6. Reversing the block transformations

The input processing contained two custom reversible passes over 16-byte blocks. Each block consists of two little-endian 64-bit words. Each pass applies 16 rounds, using combinations of addition, XOR, multiplication, rotations, shifts, and word swaps.[^static][^record]

All word arithmetic wraps modulo `2**64`.

### The 64-bit mixing function

The key-mixing operation reconstructed from the code was:

```python
MASK = (1 << 64) - 1

def mix64(x):
    x &= MASK
    x = ((x ^ (x >> 29)) * 0xB89294A129AD1091) & MASK
    x = ((x ^ (x >> 35)) * 0xF6E2E6BFAB39E8F7) & MASK
    return x ^ (x >> 26)
```

The inverse rounds do not need to invert this function: with the relevant key words and tweak captured, its output can simply be recomputed.

### The nonlinear operation

One operation initially looks less friendly:

```python
def nonlinear(x):
    return (x + ((x * x) | 5)) & MASK
```

It can be inverted one bit at a time, starting at the least significant bit:

```python
def inverse_nonlinear(y):
    y &= MASK
    x = 0
    for bit in range(64):
        if (nonlinear(x) ^ y) & (1 << bit):
            x |= 1 << bit
    assert nonlinear(x) == y
    return x
```

The useful property is that choosing a higher input bit does not disturb already-correct lower output bits. For bit positions above zero, changing bit `k` in `x` changes `x*x` only above bit `k`; the added `x` term determines the correction at that bit. At bit zero, the `| 5` term fixes the square expression's low bit. The resulting inverse avoids a search across possible 64-bit inputs.

### Undoing XOR-shifts

The rounds also contain operations such as `x ^= x >> n` and `x ^= x << n`. Their inverses can be obtained by repeatedly substituting the output back into the equation:

```python
def inverse_xorshift(y, shift, left=False):
    x = y & MASK
    y &= MASK
    for _ in range(1, 65 // shift + 1):
        moved = ((x << shift) & MASK) if left else (x >> shift)
        x = y ^ moved
    return x & MASK
```

### Parameters for the two passes

The forward and backward passes use the same general construction, but different constants, rotations, and XOR-shift distances.[^static]

| Parameter | Forward pass | Backward pass |
| --- | --- | --- |
| Rotation-table VA | `0x140088020` | `0x1400880c8` |
| Table format | 32 little-endian `uint32` values | 32 little-endian `uint32` values |
| Within-round tweak increment | `0x40714d53b9553253` | `0xb19e19b36281f0b9` |
| Between-round tweak increment | `0x80e29aa772aa64a6` | `0x633c3366c503e172` |
| First-word XOR-shifts | right 10, then left 21 | right 30, then left 26 |
| Second-word XOR-shifts | left 14, then right 33 | left 24, then right 29 |
| Rounds | 16 | 16 |

For a forward-pass round, the operations can be summarized as:

```text
a = nonlinear(a + mix64(key0 XOR round_tweak))
b = nonlinear(b XOR mix64(key1 XOR (round_tweak + within)))
a = a XOR rol64(b, rotation0)
b = b XOR rol64(a, rotation1)
a = a XOR (a >> 10)
a = a XOR (a << 21)
b = b XOR (b << 14)
b = b XOR (b >> 33)
swap(a, b)
```

Every addition and left shift is reduced to 64 bits where required. To decrypt, walk rounds 15 down to 0 and undo those operations in reverse order: undo the swap, undo the XOR-shifts, undo the two rotation-XORs in reverse order, invert the nonlinear mapping, then subtract or XOR the recomputed key term.

The supplied session account describes a `cipher_core.py` companion implementing both directions of both transforms. That file was not included in the supplied archives; the arithmetic description here does not provide a complete PE-to-flag solver.

## 7. Undoing the two passes in the correct order

### Backward pass: recover the forward-pass ciphertext

The second pass walks blocks from the end of the buffer toward the beginning. A block is XOR-chained with the already-processed block to its right before its backward-pass transformation.

Let `C[k]` denote the final encrypted blocks and `F[k]` the intermediate forward-pass blocks. With the appropriate captured key and tweak for each block:

```text
F[k] = decrypt_backward(C[k]) XOR C[k + 1]
```

For the last block, use an all-zero block instead of `C[k + 1]`.

The analysis captured the required state at the start of the backward round loop, including key words at `rbp+0xd10` and `rbp+0xd18`, and the current tweak in `RDX`. The original inversion script checked its implementation against captured intermediate input/output blocks before using it on the expected target bytes.[^record]

### Forward pass: recover the serialized plaintext

The first pass proceeds left to right, with previous-block state influencing later processing. Its block relationship can be expressed as:

```text
P[k] = decrypt_forward(F[k], current_forward_state) XOR F[k - 1]
```

The previous-ciphertext value for the first block is zero. Crucially, the forward state must advance consistently with the recovered plaintext. Reusing a single key pair for every block would not reproduce the observed behavior.

The practical solution was an inverse hook at `0x140058548`. In simplified form:

```python
mixed_plaintext = decrypt_forward(
    recovered_forward_target_block,
    current_key_words,
    current_tweak,
)

plaintext = mixed_plaintext ^ previous_forward_ciphertext

# In the recovery harness only:
write_block(rbp + 0xcc0, mixed_plaintext)
write_block(rbp + 0x610, plaintext)

# Resume the original forward block processing and state updates.
```

The XOR above is blockwise. The original hook used the previous ciphertext words at `rbp+0x878` and `rbp+0x880`. Feeding both intermediate and plaintext values back into the recovery run let the surrounding program derive the state needed for the next block.[^record]

This was the central breakthrough: **use the program to manage its complicated state, while reversing the smaller, understood transformation at carefully chosen boundaries.**

## 8. Plaintext records and decoys

The inverse run produced several records. The significant readable results appeared in group `i=6`, using the analysis log's zero-based indices.[^record]

| Record | Decoded result |
| --- | --- |
| `i=6, j=0` | `flag{wrong_castle}` |
| `i=6, j=2` | `your flag is in another castle, sorry!` |
| `i=6, j=5` | The recovered 38-byte flag |

Other records in that group produced non-text bytes. The flag-shaped decoy was a reason not to stop at the first readable `flag{...}` string.

The successful record yielded these exact blocks:

```text
PLAINTEXT i=6 j=5 offset=0  data=2600000000000000666c61677b303336
PLAINTEXT i=6 j=5 offset=16 data=61623432353430393464623861636533
PLAINTEXT i=6 j=5 offset=32 data=613965383764343562666665337d0000
```

The first eight bytes are the little-endian integer `0x26`, or 38. The next 38 bytes are the flag, and the remaining two bytes are zero padding.

This self-contained snippet decodes those **recorded plaintext blocks**. It demonstrates the record format; it does not independently decrypt the executable:

```python
import struct

payload = bytes.fromhex(
    "2600000000000000666c61677b303336"
    "61623432353430393464623861636533"
    "613965383764343562666665337d0000"
)

length = struct.unpack_from("<Q", payload)[0]
assert len(payload) == 48
assert length == 38

flag = payload[8:8 + length].decode("ascii")
assert payload[8 + length:] == b"\x00\x00"
print(flag)
```

Output:

```text
flag{036ab4254094db8ace3a9e87d45bffe3}
```

The flag was therefore recovered from the checker's encrypted records, not generated by hashing the prompt or guessed from its wording.

## 9. Verification against the forward checker

Recovery alone was not the end of the solve. The candidate was passed to the forward analysis harness as input, without the inverse-recovery hook that wrote plaintext blocks.[^record]

The historical command was:

```bash
./emu_current 'flag{036ab4254094db8ace3a9e87d45bffe3}' \
    > verified.stdout 2> verified.log
```

`emu_current` was the custom analysis harness from the original session. It is not a standard tool or an executable included in the companion bundle.

The recorded post-run checks reported:

```text
SUCCESS_ACCUMULATOR = 0x1
FINAL_COMPARISON_DIFF = 0x0
last48 mismatches: 0
```

These values were read from the retained stack state and comparison log. In that run, the main frame had been at `0x101fde00`; the checked offsets were `rbp+0x5f8` for success and `rbp+0xca8` for the final difference byte.[^record]

The last 48 logged comparisons each satisfied:

```python
bl ^ sil ^ dl == 0
```

The successful execution path also reached the code associated with the text:

```text
correct, the flag is
```

That string and the recovered flag were present in the captured memory. The write-up does not present this memory inspection as an unmodified Windows console transcript.

The evidence is stronger than merely finding a plausible string: the candidate was transformed by the forward checker, all bytes of the relevant 48-byte encrypted comparison matched, and the checker set its success accumulator without an answer-forcing hook.

The Game Master answer object is:

```json
{"flag":"flag{036ab4254094db8ace3a9e87d45bffe3}"}
```

Submission and scoreboard confirmation remain separate from local binary verification.

## 10. What the prompt clues did and did not establish

The title made hashing an obvious area to investigate, and the binary did contain substantial hash-related processing. That did not make the executable's SHA-1, a section digest, or a hash of the song title the answer.

The earlier Game AI tried literal prompt-derived candidates. The successful recovery did not depend on interpreting `Wonder Wall` as the submitted flag or establishing it as a literal decryption key.[^game-log][^record]

The author's complete intended wordplay was not established by the recorded analysis. Rather than invent an explanation after the fact, this write-up treats the prompt as investigative context and the executable's data flow as the evidence for the solve.

## 11. Lessons from the solve

**Start with what consumes the input.** Reaching a prompt is useful, but the important next step is following the input to the transformation and comparison that determine acceptance.

**Do not confuse anti-analysis progress with flag-recovery progress.** Fixing emulator behavior can be necessary, but a long chain of environment fixes is not automatically bringing the expected answer closer. The useful checkpoints were where input, target bytes, and comparison state became visible.

**Do not erase cryptographic state dependencies while bypassing protections.** A large hash loop may feed integrity checks, state derivation, or both. Replacing it without validating its outputs can make every later decryption look wrong.

**Recover data at the point of use.** The final comparison exposed an effective target-byte stream even though its constants were split, encoded, and mixed upstream.

**Validate the inversion, then validate the candidate.** The original analysis checked the reconstructed forward transform against 51 captured blocks. Candidate verification was a separate run through the forward checker. These answer different questions and should not be collapsed into one test.[^record]

**Expect decoys.** A readable flag-shaped record was not sufficient evidence. The length prefix, full plaintext record, final encrypted comparison, and success state provided a much stronger chain of support.

## 12. Companion files and reproducibility boundary

The supplied web-session account describes a companion bundle containing `cipher_core.py`, `decode_recovered_payload.py`, `artifact_metadata.json`, selected disassembly, and excerpts of the solve. **That companion bundle, the original emulator, and the dynamic verification logs were not supplied for this publication.** There are consequently no companion commands to run from this repository.

That earlier account reports an arithmetic checkpoint passing, 128 round-trip tests passing, and successful decoding of a 48-byte record containing a 38-byte flag and two padding bytes. These are attributed historical claims, not tests rerun during this publication review.

For this review, the supplied ZIP and executable sizes and SHA-256 hashes were checked against the table above. The recorded hexadecimal plaintext was also decoded and confirmed to contain the stated 38-byte string. Those limited checks support artifact identity and consistency of the written record. They do not independently reproduce the reversible-transform recovery or the full checker execution.

The Game Master completion statement comes from the later retained repository review. Its raw acceptance response and successful submission payload were not supplied. A reader can follow the recorded reasoning and arithmetic examples, but cannot reproduce the original full solve from this publication alone.

## Sources and evidence

The technical account above was supplied as a writeup from an earlier ChatGPT web session. Execution, instrumentation, and “rechecked” statements within that account describe that earlier session. This publication review did not execute the challenge, reconstruct the emulator, or rerun its dynamic checks.

[^artifact]: Supplied `sha1_hulud.zip` and `sha1-hulud.exe`; publication review confirmed their sizes and SHA-256 hashes. The earlier account additionally reports authenticated extraction and PE-header, section, Rust-string, XOR-prompt, and rotation-table inspection. Its mentioned `artifact_metadata.json` companion was not supplied.

[^game-log]: The earlier account attributes emulation obstacles and rejected candidates to a Game AI progress log called `Pasted text(20261031-142041).txt`. That exact attachment is not supplied here. Related Homebase investigation notes survive in the source archive, and are treated as provisional where later evidence differs.

[^record]: The supplied successful-session writeup reports preserved outputs from `emu_current.c`, `invert.py`, recovery hooks, plaintext output, a 51-block forward check, and `verified.log`/memory inspection. Those original source files, logs, and the mentioned `evidence/recorded_solve_excerpts.txt` companion were not supplied; the dynamic claims remain attributed to the writeup.

[^static]: The earlier account reports `objdump` inspection at the listed addresses. Its promised selected-disassembly companion was not supplied. Address-level descriptions are preserved as reported analysis, not independently reverified by this publication pass.

[^checks]: The earlier account reports arithmetic tests of its companion programs. Those programs were not supplied, and no such arithmetic or emulator tests were rerun during publication preparation. The limited plaintext-record consistency check described in Section 12 was performed separately.

## Retained sources

- [user-updates/sha1-hulud-web-pro-writeup.md](../../source-notes/user-updates/sha1-hulud-web-pro-writeup.md)
- [later/WRAP-UP.md](../../source-notes/later/WRAP-UP.md)
- [later/writeups/day-30/binary-multi-binary-campaign.md](../../source-notes/later/writeups/day-30/binary-multi-binary-campaign.md)
