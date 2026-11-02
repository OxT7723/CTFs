# You Must Be This Hash to Ride

Day 1 · Metadata forensics · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `metadata-forensics-day-01-hash-to-ride`

## Earlier local account

**Release:** Day 01 Challenges

| Author | Category |
|---|---|
| [John Hammond](https://youtube.com/@_JohnHammond), and [Just Hacking Training](https://justhacking.com) | 🔎 Metadata Forensics |

Three ordinary files arrived without trustworthy labels. Build an identity inventory from the bytes themselves and prove which labels can—and cannot—be trusted.

You can download the **single-solve file** for this challenge here:

**Challenge file:** you_must_be_this_hash_to_ride.zip

or ask the Game Master for your single-solve file in the **AI Homebase** virtual machine.

**System:** Start/connect through CourseStack or the challenge instructions.

**Scored task:** Single Solve: Submit the flag for 1 static task. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 2

Use the Game Master to get fresh targets for Time Trial and Mastery Mode.

**Scored task:** Time Trial: Submit the flag for 1 new dynamic task in under 4 seconds. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 3

**Scored task:** Mastery Mode: Submit the flag after completing 2 new dynamic tasks in under 2 seconds. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 5

---

## Later Homebase account

### You Must Be This Hash to Ride

Challenge ID: `metadata-forensics-day-01-hash-to-ride`

### Solver

Use the shared metadata runner from the repository root. It reads the current
questions, answer IDs, and artifact descriptors from the Game Master on every
attempt, so randomized filenames and Mastery set IDs do not need to be edited
in the solver.

```sh
export GAME_MASTER_PROXY_URL='http://10.0.0.219/huntress-ctf-proxy'
python3 metadata-forensics-tools/run_challenge.py \
  'metadata-forensics-day-01-hash-to-ride'
```

For an ended attempt, `--retry` advances to another regular untimed variant.
The Time Trial and Mastery routes support this regular mode:

```sh
python3 metadata-forensics-tools/run_challenge.py \
  'metadata-forensics-day-01-hash-to-ride/time_trial' --retry
python3 metadata-forensics-tools/run_challenge.py \
  'metadata-forensics-day-01-hash-to-ride/mastery' --retry
```

Only for a deliberately authorized ranked run, add both `--retry` and
`--run-for-time`. `--run-for-time` selects a timed Hall of Fame attempt. A
normal invocation does not opt into a timer.

The runner downloads the assigned archive bytes, recursively opens ZIP
members, matches each question to its described artifact, and derives the
requested filename, byte count, and digest. It builds answers from question
IDs returned for that attempt, verifies that the full answer-ID set matches,
and submits only fields that the current attempt has not already accepted.
The archive and attempt records are saved under
`metadata-forensics-tools/attempt-records/metadata-forensics-day-01-hash-to-ride/`.

Timed runs keep the downloaded bundle but skip its outer SHA-256 verification
on the speed-critical path; that checksum is not one of this challenge's
answers. The requested member hashes are still computed. The saved attempt
response contains the Game Master's expected bundle checksum, and the local
manifest can be verified after the run.

### Dependencies and limits

Python 3. The Day 1 bundles are ordinary ZIP files and require no external
metadata utility. `pyzipper` is optional for encrypted ZIP members; the shared
metadata requirements are documented in
`metadata-forensics-tools/README.md`.

The runner relies on the question's artifact descriptor and the archive
member names. If a future variant changes the evidence format or asks for a
field not handled by `answer_for`, it stops with an extraction error instead
of guessing. The solver has been exercised on the historical Single Solve
artifact, thirteen fresh regular Time Trial variants, thirteen fresh regular
Mastery variants, and three ranked variants in each timed mode. All 16
artifacts in each timed mode had distinct checksums.

### Session results

- Single Solve was already complete. Its saved archive produced five offline
  candidates, and historical status lists all five answer IDs as accepted.
- Regular Time Trial: thirteen fresh variants completed, **13/13 successful**,
  with all five answers accepted per run. The latest replay was attempt
  `b5103fe1-6400-43d4-89f4-95fe0f55c90e`. Full runner wall time ranged from
  about 5.7–10.4 seconds; 19 fresh regular variants remain.
- Regular Mastery: thirteen fresh variants completed, **13/13 successful**,
  with all ten answers accepted across two sets per run. The latest replay was
  attempt `811d5d85-ba46-4eb0-a2ad-a7dcf6df3e0f`. Full runner wall time ranged
  from about 2.8–17.7 seconds; 19 fresh regular variants remain.
- Ranked Time Trial: three fresh eligible attempts completed correctly; all
  five answers were accepted in each. Attempt
  `bab1c64a-540f-4ff0-ac1d-08e30943b8c8` had deadline
  `2026-10-28T15:18:43.941Z` and took about 8.7 seconds. Attempt
  `8d615671-86c6-4b22-b78c-64ac50d6d1df` had deadline
  `2026-10-28T17:54:31.721Z` and took about 11.2 seconds. Attempt
  `e396e918-ff17-4cfe-88db-35262ccfe934` had deadline
  `2026-10-28T18:14:10.510Z` and took about 14.9 seconds.
- Ranked Mastery: three fresh eligible attempts completed correctly; all ten
  answers were accepted in each. Attempt
  `d8b92598-7f1a-4ad4-9ab1-53d2566c1914` had deadline
  `2026-10-28T15:19:36.714Z` and took about 7.6 seconds. Attempt
  `f4fff78c-0572-4faf-9e69-168be726701f` had deadline
  `2026-10-28T17:55:19.231Z` and took about 12.1 seconds. Attempt
  `2e89ea34-71f8-45b5-b410-fb6b50c99e1e` had deadline
  `2026-10-28T18:15:02.286Z` and took about 7.5 seconds.
- Both ranked pools report 28 attempts remaining. No additional ranked retry
  has been started since these runs.

The additional regular variants changed which evidence-note or roster files
and fields appeared and varied their answer IDs. All were handled by the
existing question-driven archive resolver; no new extraction handler was
needed.

The Game Master returned `CORRECT` for every replay and ranked run. Its status
responses did not include a completion timestamp or a separate CourseStack
points field, so the recorded end-to-end wall times are approximate and the
report does not infer a points total from them.

## Retained sources

- [early/01-You_Must_Be_This_Hash_to_Ride/readme.md](../../source-notes/early/01-You_Must_Be_This_Hash_to_Ride/readme.md)
- [later/writeups/day-01/metadata-forensics-you-must-be-this-hash-to-ride.md](../../source-notes/later/writeups/day-01/metadata-forensics-you-must-be-this-hash-to-ride.md)
