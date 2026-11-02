# How the AI-assisted workflow developed

The most reusable outcome of this CTF was a collection of deterministic analyzers, paired with prompts that kept the AI focused on the current challenge and current attempt. The uploaded material records both early Codex work and later work with the event-provided AI Homebase and Game Master.

The Game Master handled challenge assignment, artifacts, answer IDs, attempts, deadlines, and submission results. The AI Homebase supplied the working environment. The saved organizer instructions use those terms; this collection retains them instead of treating the AI and the scoring service as the same system. See the preserved [Homebase workflow instructions](source-notes/later/workflow-instructions.md).

## What the surviving files show

| Stage represented by the files | Organization | Practical change |
| --- | --- | --- |
| Early Codex workspace | Day-and-challenge folders, `challenge_state.json`, a generated root index, and individual solver scripts | Capture the method, assigned evidence, and state together; distinguish a navigation table from live service state. |
| Task-specific workflow documentation | Short workflow router plus separate solve, timed-mode, state, and sync guides | Load the instructions needed for the current task instead of repeatedly reading a large manual. |
| Later AI Homebase workspace | Six category toolkits and concise day/category notes | Reuse parsing and decoding logic across changing artifacts and answer sets. |
| Final daily prompts | One assignment per category, current-attempt answer IDs, bounded failure handling, and credit-efficiency rules | Reduce repeated model work and keep concurrent category agents from editing shared files unnecessarily. |
| Review and optimization prompt | Regular practice, fresh-variant validation, then a separately authorized ranked phase | Improve reliability before spending ranked attempts; distinguish prior accepted answers from a newly assigned artifact. |

This is a reconstruction from the surviving files, not a complete timestamped prompt revision history. The final daily snapshots still contain assignment values from particular days. The [prompt index](prompts/README.md) documents those values and separates exact snapshots from a cleaned template.

## The useful design decisions

### Reuse methods across changing artifacts

The late prompts explicitly discourage hardcoded answers, hashes, URLs, and filenames. Solvers read the current artifact and map extracted values to the exact answer IDs supplied for that attempt. This matters when Single Solve, Time Trial, and Mastery use different randomized material or multiple evidence sets. Sources: [final binary prompt](prompts/snapshots/04-binary-reverse-engineering.txt), [binary toolkit guide](tools/later/binary-reverse-engineering-tools/README.md), and [mobile toolkit guide](tools/later/mobile-android-tools/README.md).

The implementation examples include CRC-checked configuration-record parsers in the binary analyzer, nested archive and format readers in the metadata toolkit, a shared multi-codec script analyzer, and APK asset decoders. Their value is the extraction logic that survives an artifact change. The historical orchestration code still depends on the retired event environment.

### Treat completion and speed as different evidence

A route named “Time Trial” could be completed through regular untimed play in later event workflows. A null deadline, a successful result, a client wall time, and an official Hall of Fame time describe different things. The final prompts explicitly separated regular preparation from `run_for_time:true` ranked attempts. Sources: [review and optimization prompt](prompts/snapshots/09-review-training-optimization.md) and [Protocol Reconstruction notes](source-notes/later/writeups/day-28/mobile-protocol-reconstruction.md).

Saved performance notes also distinguish local analysis from request latency and reconnect behavior. For example, the [Trust Issues notes](source-notes/later/writeups/day-29/metadata-forensics-trust-issues.md) describe profiling PE resource parsing and an offline replay, while [Campaign Trail notes](source-notes/later/writeups/day-30/binary-multi-binary-campaign.md) describe recovering from a stale persistent connection. These are historical records; many underlying per-attempt logs were not included in the supplied archives.

### Preserve accepted progress within an attempt

The prompts tell the AI to retain already accepted answers in the same attempt, reassess repeated failures, and avoid mistaking a partially incorrect group for a completely rejected submission. They also warn against carrying accepted values from one randomized attempt into the next. Sources: [script-analysis prompt](prompts/snapshots/03-script-analysis.txt) and [review prompt](prompts/snapshots/09-review-training-optimization.md).

### Spend model work on investigation and improvements

The final prompts favor deterministic decoders, narrow source reads, and lightweight availability checks. The goal is to use the AI to understand an unfamiliar format or failure, then retain that knowledge in a reusable script. The preserved prompts contain the original polling instructions, including very short intervals; those are historical settings, not a recommendation for another service. Source: [warmups prompt](prompts/snapshots/01-warmups.txt).

## A lesson from SHA1-Hulud

The original Game AI investigation accumulated substantial emulation and anti-analysis work, but an early conclusion classified the validator as an irreversible input-hash problem. Later notes corrected the interpretation of long image-mixing loops. A separate, later user-supplied successful account describes recovering expected comparison bytes and reversing two block transformations.

That later account is preserved at [SHA1-Hulud successful-session account](source-notes/user-updates/sha1-hulud-web-pro-writeup.md). It distinguishes arithmetic examples and historical instrumented verification from a complete reproducible emulator. The complete successful harness, its companion files, and the original full transcript are not in the supplied archives. The older [findings record](source-notes/later/day-30/binary/fresh-sha1-hulud/notes/findings.md) remains useful evidence of the investigation, with its superseded claims identified.

The publishing lesson is to retain an investigation's corrections and evidence limits. A polished AI summary should not turn an old hypothesis into a confirmed fact, or turn a recorded success into a claimed fresh reproduction.

## What is included here

- [Exact final prompt snapshots and a cleaned template](prompts/README.md).
- [Preserved working notes](source-notes/README.md), with provenance and historical-status notices.
- [Reusable analyzer and orchestration source](tools/README.md), with original dependency files where available.
- [Artifact inventory](source-artifact-inventory.csv), recording supplied specimen paths, sizes, and SHA-256 values without bundling executable challenge material.
- [Source manifest](source-manifest.json), recording input/output hashes and editorial changes.

The publication review checked Python syntax without importing or executing the scripts. It did not rerun challenge solvers, launch challenge programs, contact the event services, or independently reproduce historical timing claims.
