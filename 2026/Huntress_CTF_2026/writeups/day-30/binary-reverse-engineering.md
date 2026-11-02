# Campaign Trail and the SHA1-Hulud investigation

Day 30 · Binary reverse engineering · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

> The SHA1-Hulud handoff below is an October 30 investigation snapshot. The later [successful-session account](sha1-hulud.md) and October 31 status review supersede its unresolved outcome.

## Later Homebase account

### Day 30 Binary Reverse Engineering

Challenge IDs:

- `binary-reverse-engineering-day-30-multi-binary-campaign`
- `binary-reverse-engineering-day-30-multi-binary-campaign/time_trial`
- `binary-reverse-engineering-day-30-multi-binary-campaign/mastery`
- `binary-reverse-engineering-day-30-sha1-hulud`

### Results

Campaign Trail completed through shared team state in all three modes:

- Single Solve: 420/420 answers accepted.
- Time Trial: 420/420 accepted; no deadline, regular route.
- Mastery: 5880/5880 accepted; no deadline, regular route.

Game Master status returned `CORRECT` for all three modes. The per-attempt
summaries and accepted answer records are in `work/day-30/binary/`.

The campaign mixes Neko bytecode and PE specimens with backward-embedded
CRC32-valid HGRF graph records. The analyzer now selects specimens by role,
validates that loader/library/config graphs match after removing `this_role`,
and reads shared values from `graph.config`. See
`binary-reverse-engineering-tools/analyze_evidence.py` and its README for the
reusable implementation.

### SHA1-Hulud

The Game Master now reports Single Solve as `CORRECT`. A read-only status
check on 2026-10-31 confirmed that answer ID `flag` is accepted for attempt
`353f3c79-6a5e-42b3-b061-0b531ec2e59e`; the service recorded completion at
`2026-10-31T15:32:26.832Z`. SHA1-Hulud has no Time Trial or Mastery mode.
The successful submission payload was not preserved in this workspace, so
this update records verified completion without inferring the accepted text.

The assigned ZIP has SHA-256
`9fc7b3bcb00c9b6ea174ac6cd17729912aa7588838722959e5cac9611aff8c38`; its
password-protected member `sha1-hulud.exe` has SHA-256
`c03f48392c8bbfd5ba3faf5260b6ca658e08b099aef0f5c8dbf782edd5d13e89`.
Assigned artifact: Download sha1_hulud.zip (private download link removed).

The local submission records preserve six earlier rejections: SHA-1 of the
executable, SHA-1 of the archive, `Shai-Hulud`, `SHA1-Hulud`, `Wonderwall`,
and the SHA-1 digest of the code range the binary hashes internally. The
accepted submission is not among the saved JSON responses.
The binary is a Rust PE with a custom `.xsobf` section. Static decoding
recovered an anti-analysis registry path and a list of reverse-engineering
tools. The code also hashes a code range and decrypts a small block behind
environment checks.

Speakeasy emulation reached the console prompt after filling emulator API gaps.
Further tracing found that the code hashes a copy of the mapped image from
RVA `0x1000` for `0x7e044` bytes. A local emulation produced
`2269a01611eb34111181af2201b7f649cb38e67e`, but this depends on the emulator's
mapped image and is not established as the expected answer.

The protected SHA-1 routine uses an `int3` breakpoint and a vectored exception
handler at `0x140065baa`. The handler sets `R15` from the exception address and
rewrites `RIP` from `RDI`. Reproducing the thread ID and breakpoint register
state lets Speakeasy decode an actual SHA-1 round, but later `iretq` control
flow still reaches an invalid context. No new answer was submitted from this
analysis.

### SHA1-Hulud continuation handoff (snapshot from 2026-10-30)

At the time of this snapshot, attempt `353f3c79-6a5e-42b3-b061-0b531ec2e59e`
was active in Single Solve, with answer ID `flag` and no deadline. The
subsequent completion is recorded above.

#### What worked

- Static inspection confirms a Rust PE64 with a custom `.xsobf` section and
  anti-analysis data. The `int3`/VEH path can be partially modeled when the
  emulated thread ID is `0x434` and the breakpoint context carries the
  expected `RDI` value.
- The temporary Speakeasy harness substitutes the protected SHA-1 compression
  routine with a standard round implementation. It completes 8,067 block
  calls, including the pass over a copied mapped image at RVA `0x1000`, length
  `0x7e044`. The caller performs the feed-forward step after each substituted
  round.
- The harness can inject a console line, suppress debugger checks, convert
  wide text, and capture the prompt. It has been saved at
  `work/day-30/binary/353f3c79-6a5e-42b3-b061-0b531ec2e59e/analysis/solve_sha1_hulud_trace.py`.
  Run from the repository root with:

  ```sh
  PYTHONPATH=/tmp/huntress-speakeasy python3 work/day-30/binary/353f3c79-6a5e-42b3-b061-0b531ec2e59e/analysis/solve_sha1_hulud_trace.py
  ```

#### What has not worked

- The harness prints `What is the flag?` but does not reach a visible
  acceptance/rejection message for either `flag{test}` or a 40-character dummy
  line. The captured reads show the dummy input copied and its CR/LF trimmed,
  but no confirmed comparison against an expected flag.
- The local mapped-image digest
  `2269a01611eb34111181af2201b7f649cb38e67e` depends on Speakeasy's memory
  image and is not a defensible answer. The later one-block state beginning
  `2aa619afefd13f5018b9c12b8b7c9e0a881aec2b` is likewise only an emulator
  trace value. Neither was submitted.
- Natural execution of the protected routine still fails at its later
  `iretq` transition. Replacing the routine allows tracing to continue, but
  does not prove that the resulting image state matches Windows.
- The newest trace sees execution through `0x14003d310` and into the timing
  loop around `0x14003d39a`; the focused trace does not provide a reliable
  post-hash path to the input check. Earlier snapshots showed `0x14003d408`,
  but this was not reproduced consistently. Do not treat the earlier
  “panic path” interpretation as confirmed: the watched global at
  `0x140098070` was written to `1` and later cleared, and was zero at the
  captured `0x14003d310` snapshot.
- Console emulation still needs validation. The injected text is
  `flag{test}\r\n` (12 characters), while the API report shows a
  `WideCharToMultiByte` call with input length `0x2a`. Check the read-count
  pointer and surrounding wide buffer before assuming the emulated input
  length is correct.

#### Next useful steps

1. Inspect the read-count pointer and wide input buffer immediately before
   `WideCharToMultiByte`; correct the console shim if it is converting 42
   characters instead of the injected line.
2. Trace instructions and memory writes after `0x14003d310`, especially the
   path through the shared-user-data timing reads around `0x14003d39a`.
   Record the exact exit PC and panic/global state; the existing focused trace
   script is a starting point.
3. Determine how the mapped image is constructed under real Windows semantics
   before using either observed digest. Continue to avoid submissions based on
   emulator-derived values.
4. This investigation is historical. The Game Master now confirms completion;
   retain the traces as analysis notes rather than using them to generate
   further submissions.

The temporary environment also contains
`/tmp/solve_sha1_hulud_trace.log`,
`/tmp/sha1-second-block.json`, `/tmp/sha1-first-block.json`, and the Speakeasy
report under `/tmp/sha1-hulud-replacement-report.json`. The harness requires
the local Speakeasy checkout at `/tmp/huntress-speakeasy` and config at
`/tmp/speakeasy-lenient.json`.

### Timed Campaign Trail runs (2026-10-31)

Both timed runs used fresh ranked variants via `retry` with
`run_for_time:true`. A plain `start` on an already-completed regular route
reconnected to the old `CORRECT` result and did not consume a ranked attempt;
the live ranked-attempt counters stayed unchanged. Use
`run_modes.py "$CHALLENGE_ID" --retry --run-for-time` for the next fresh timed
variant after a completed regular run.

- **Time Trial** attempt `5c5ecf4e-eb7a-4f09-b469-88be992bf3a9`: Game Master
  returned `CORRECT`, all 420/420 answers were accepted, and
  `hall_of_fame_eligible` was true. The runner recorded 7.2674 seconds total
  against an 80-second deadline. One fresh artifact was verified and analyzed.
- **Mastery** attempt `a2a96204-7753-4375-82a5-2081323c548a`: Game Master
  status returned `CORRECT`, all 5,880/5,880 answers were accepted, and
  `hall_of_fame_eligible` was true against a 665-second deadline. The 14
  assigned archives were verified and expanded to 644 files. The runner hit a
  broken pipe on its idle persistent connection after local analysis; the
  complete 5,880-answer candidate map was preserved and submitted successfully
  over a new connection. Elapsed wall time from the start response to saving
  the successful submission response was about 159.8 seconds; the runner did
  not save a phase breakdown for this run.

The Game Master responses were `CORRECT` with no pending-scoring result.
Its status payload does not expose a numeric CourseStack score or Hall of Fame
time, so those values were not independently visible in the proxy response.

#### Improvements for future timed runs

- `binary-reverse-engineering-tools/run_modes.py` now supports
  `--run-for-time` and explicitly sends `op:"start"` for normal starts.
- Use `--retry --run-for-time` to get a fresh ranked variant after the regular
  route is already solved; `--run-for-time` alone reconnects to the completed
  regular result in this state.
- The runner refreshes its persistent Game Master connection after local
  analysis. The 14-set Mastery analysis can exceed the proxy's keep-alive idle
  timeout, so this avoids resubmitting through a stale socket.
- For a fresh attempt, `--skip-initial-status` saves one request. Keep the
  final status request enabled to verify completion and accepted-answer count.
- The deterministic analyzer handled both randomized timed artifacts without
  edits: 420 Time Trial answers in about 2 seconds of solver time; the 5,880
  Mastery candidates were generated before the stale-socket failure.

### Successful recovery in ChatGPT Pro

See [SHA1-Hulud](sha1-hulud.md) for the recovered flag, method and author’s account of the AI tools used. The updated repository status review records acceptance, while the successful submission payload remains unavailable.

## Retained sources

- [later/writeups/day-30/binary-multi-binary-campaign.md](../../source-notes/later/writeups/day-30/binary-multi-binary-campaign.md)
- [later/day-30/binary/fresh-sha1-hulud/resume-notes.md](../../source-notes/later/day-30/binary/fresh-sha1-hulud/resume-notes.md)
- [later/day-30/binary/fresh-sha1-hulud/notes/HANDOFF.md](../../source-notes/later/day-30/binary/fresh-sha1-hulud/notes/HANDOFF.md)
- [later/day-30/binary/fresh-sha1-hulud/notes/findings.md](../../source-notes/later/day-30/binary/fresh-sha1-hulud/notes/findings.md)
- [later/day-30/binary/fresh-sha1-hulud/attempted-flags.md](../../source-notes/later/day-30/binary/fresh-sha1-hulud/attempted-flags.md)
