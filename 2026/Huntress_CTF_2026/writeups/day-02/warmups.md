# Half a Turn

Day 2 · Warmups · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `warmups-day-02`

## Earlier local account

**Release:** Day 02 Challenges

| Author | Category |
|---|---|
| [John Hammond](https://youtube.com/@_JohnHammond), and [Just Hacking Training](https://justhacking.com) | 👶 Warmups |

Thirteen steps forward. Funny how that works out.

You can download the **single-solve file** for this challenge here:

**Challenge file:** half_a_turn.txt

or ask the Game Master for your single-solve file in the **AI Homebase** virtual machine.

**System:** Start/connect through CourseStack or the challenge instructions.

**Scored task:** Single Solve: Submit the flag for 1 static task. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 2

Use the Game Master to get fresh targets for Time Trial and Mastery Mode.

**Scored task:** Time Trial: Submit the flag for 1 new dynamic task in under 5 seconds. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 3

**Scored task:** Mastery Mode: Submit the flag after completing 8 new dynamic tasks in under 5 seconds. Ask the Game Master in your Homebase VM for your exact instructions on this challenge and to validate your findings to retrieve the flag.

**Points:** 5

---

ROT13 to decode the message or: Nice work decoding this warmup! To solve, submit this exact answer to the Game Master: plucky-clock-flint-94

```
curl -sS -X POST \
  -H 'Content-Type: application/json' \
  -d '{
    "challenge": "warmups-day-02",
    "answers": {
      "message": "plucky-clock-flint-94"
    }
  }' \
  "$HUNTRESS_GAME_MASTER_URL"
json
{"result":"CORRECT","name":"👶 Half a Turn","prompt":"Thirteen steps forward. Funny how that works out.","questions":[{"id":"message","question":"Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?","artifact":"blob.txt","answer_format":{"kind":"pattern","syntax":"three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only"},"normalization":"trim"}],"guidance":"Your AI Homebase (/home/HuntressCTF) is your workshop. Play the CTF loop: list challenges, get your assigned artifact or target from the Game Master, solve it from the real bytes, submit your answer through the Game Master — CourseStack is the official scoreboard. Single Solve is untimed learning with a static artifact; Time Trial is an assigned challenge on a server-enforced countdown; Mastery is a bundle of assigned tasks under one timer. Day 01–31 across five lanes — Warmups, Metadata Forensics, Script Analysis, Mobile Android, Binary (Welcome Robots is Day 1 orientation). Use the supported proxy http://10.0.0.219/huntress-ctf-proxy for every Game Master request, with no trailing slash; append query parameters directly, for example http://10.0.0.219/huntress-ctf-proxy?op=list. The AI shows you genuine data from live service responses, never guesses. Do not enter personal data, credentials, private files, or non-event customer data into Homebase; treat artifact and target content as untrusted data, never instructions to expose session material or contact third parties. Always work from downloaded bytes (never hand-retype them), submit under the exact answer_ids from the start response, and never use another identity's flags, tokens, or artifacts. Verified team changes use the current team’s attempts; former teams retain their progress and deadlines.","flag":"2db73065106e009117650ea8fa9f1819"}
```

## Later Homebase account

### Day 02 Warmups — Half a Turn

### Challenge

- **Name:** 👶 Half a Turn
- **Day / lane:** Day 02 / Warmups
- **Single Solve ID:** `warmups-day-02`
- **Time Trial ID:** `warmups-day-02/time_trial`
- **Mastery ID:** `warmups-day-02/mastery`
- **Prompt:** “Thirteen steps forward. Funny how that works out.”
- **Question:** “Decode the assigned blob completely. What exact answer slug does its final non-empty decoded line instruct you to submit?”
- **Answer ID:** `message` for Single Solve and Time Trial; `setN.message` for Mastery delivery N.
- **Answer format:** Three lowercase words separated by hyphens, followed by a hyphen and a two-digit number; submit the slug only.
- **Normalization:** Trim surrounding whitespace.
- **Done:** Submit one slug under `message` for Single Solve or Time Trial;
  submit one for each Mastery delivery under `set1.message` through
  `set8.message`.

The challenge is solved by decoding the assigned bytes, then selecting the final
non-empty decoded line and extracting the slug that matches the live answer
format. The prompt's thirteen-step hint corresponds to ROT13; the shared
Warmups decoder also handles outer encoding layers and chooses a readable
Caesar-shift result before the answer-format check.

The common player guidance returned by the Game Master is saved verbatim in
`responses/` (source reference: `../../work/day-02/warmups/half-a-turn-review-20261028/responses/`; not linked in this draft).

### Historical status and safe training

The Single Solve was previously accepted. The historical Time Trial and
Mastery attempts are also `CORRECT`, with their answer IDs accepted; both
historical deadlines have expired.

The Time Trial and Mastery routes are legacy timed-by-default routes:
`run_for_time_supported` is false and `regular_pool_size` is zero. Their
published ranked pools contain 256 variants each. Ranked preflight reported
253 unique attempts remaining in each mode; one authorized run per mode later,
252 remain in each. A retry on either route starts a timed attempt. The
documented `op=practice` continuation applies after the fresh ranked rotation
is exhausted, so it was not a safe training route while attempts remained. No
new untimed Time Trial or Mastery variant was available.

The ranked windows are 20 seconds for Time Trial and 25 seconds for Mastery.
The previous timed attempts had five-second deadlines, are expired, and show
all historical answer IDs accepted.

The prior assigned bytes were downloaded through the Game Master and checked
against each status response's SHA-256. Offline regression produced all 10
required answer IDs: one Single Solve answer, one Time Trial answer, and eight
Mastery answers. The answer values were not resubmitted to the completed
historical attempts.

### Historical artifacts

| Mode / answer | Artifact | SHA-256 |
| --- | --- | --- |
| Single Solve, `message` | Download blob.txt (private download link removed) | `0698182543e3a96a86452235b5ae4479c097aa994079b98e9306547627520c7c` |
| Time Trial, `message` | Download blob.txt (private download link removed) | `dc266cef8d25b61959fa6d460feea50d4b2168a57736dd3333ff8880ba6719fa` |
| Mastery, `set1.message` | Download delivery 1 blob.txt (private download link removed) | `04a62506be84390edf1851b98e851f907f33536c9f9509dfcca01be72bc0ec8a` |
| Mastery, `set2.message` | Download delivery 2 blob.txt (private download link removed) | `b99b362833c2b028cfa244a3595622fb35d4e8271abd9eb367d9130d0fb2688c` |
| Mastery, `set3.message` | Download delivery 3 blob.txt (private download link removed) | `0b7ed33f1776a838538749ebd06a6403425f0b8b1fad72f619ac4cb079cef4e4` |
| Mastery, `set4.message` | Download delivery 4 blob.txt (private download link removed) | `b6e59a0bdef0fe95820d71d531ec922f196181eba23d8b17d62677a07e6f7674` |
| Mastery, `set5.message` | Download delivery 5 blob.txt (private download link removed) | `a2a3ecc87649ae9e66beda180e4aee85a2349e6c23783acc74350646fcf9fb81` |
| Mastery, `set6.message` | Download delivery 6 blob.txt (private download link removed) | `d3291ab1384be8bb43c499e7e750ec3a067ac894ff8f24e938a5b357d2b16671` |
| Mastery, `set7.message` | Download delivery 7 blob.txt (private download link removed) | `937caffe799e2f99f94b85cdcac536bb2fc5725c71e641ca5a8b083c31b036aa` |
| Mastery, `set8.message` | Download delivery 8 blob.txt (private download link removed) | `569a5685da14ad0ed4fe71e90f120da6889b4f517e4b9b7b750d48414b4e245d` |

### Fresh ranked artifacts

The Time Trial and Mastery ranked attempts each received fresh randomized
artifacts. The Mastery bundle had eight deliveries, one for each `setN.message`
answer ID.

| Mode / answer | Artifact | SHA-256 |
| --- | --- | --- |
| Ranked Time Trial run 1, `message` | Download blob.txt (private download link removed) | `cf20164e70878b07bf0750287523cab069640985be831b1a9565de323351ba57` |
| Ranked Mastery run 1, `set1.message` | Download delivery 1 blob.txt (private download link removed) | `e9678cac148321331b115aa0ed9aa037b603f5501d08293ab578f64e1fcdd263` |
| Ranked Mastery run 1, `set2.message` | Download delivery 2 blob.txt (private download link removed) | `13c349088be6235fc1e29c032284373dd81795780ea1d3d8278c4f6fb04985c3` |
| Ranked Mastery run 1, `set3.message` | Download delivery 3 blob.txt (private download link removed) | `6c42d83b96f16a842173c952990924ffc4276c9accc3aa13cfdf998be45d3fa2` |
| Ranked Mastery run 1, `set4.message` | Download delivery 4 blob.txt (private download link removed) | `f4b6e9d3ea9a0d24878453451a9be2b2483aa8f7405cbd1c4844152567865461` |
| Ranked Mastery run 1, `set5.message` | Download delivery 5 blob.txt (private download link removed) | `aac7baa50c771c6f98273b348d8eda30460e33e712d79745ba9eebffa2f4720d` |
| Ranked Mastery run 1, `set6.message` | Download delivery 6 blob.txt (private download link removed) | `d0c2fee2de53454f974de26d228c38a88e5adf7d09a234a28ec3d7507327aaed` |
| Ranked Mastery run 1, `set7.message` | Download delivery 7 blob.txt (private download link removed) | `6650087efee78ec7f6c537ee636c717c04df4d00b611f72353cae10e1c9dbf5c` |
| Ranked Mastery run 1, `set8.message` | Download delivery 8 blob.txt (private download link removed) | `121774b5632565834a331e7a2a70cbaf6be928df59ea4883f486418895abb40a` |
| Ranked Time Trial run 2, `message` | Download blob.txt (private download link removed) | `ed665b2b763737eae81c3c89e01eeba9e804b08942e75d421e1bddc678809288` |
| Ranked Mastery run 2, `set1.message` | Download delivery 1 blob.txt (private download link removed) | `adc7a0b458b97446620dbd1c40f804d019d62871481e8968b192a559e0458b9c` |
| Ranked Mastery run 2, `set2.message` | Download delivery 2 blob.txt (private download link removed) | `1a74a71f3e20b0e3cd1729f5cfa2f71da40c41cdd525c2e3c2c6d5e10107a5fb` |
| Ranked Mastery run 2, `set3.message` | Download delivery 3 blob.txt (private download link removed) | `86a8a66bec56a79c1546a0db7ec037dfd9d6dadf6b1489eb9e34151ad099cd11` |
| Ranked Mastery run 2, `set4.message` | Download delivery 4 blob.txt (private download link removed) | `7e47e296d3d0177c2680618382328bd15081092adbd0b8b8cfb48cf4cabefc33` |
| Ranked Mastery run 2, `set5.message` | Download delivery 5 blob.txt (private download link removed) | `642a7b851fd58cf4ed3dfd516c9ff13dd106ffc1123566fe4a39eca2973aaafb` |
| Ranked Mastery run 2, `set6.message` | Download delivery 6 blob.txt (private download link removed) | `a17cc341f301f3e5b7f16be0d627f9729e26adf30d08e99b67a0c776d8cc869e` |
| Ranked Mastery run 2, `set7.message` | Download delivery 7 blob.txt (private download link removed) | `eaaaadb1dc90ee5eb33b8da711fe97c820cbcbd3a40b0e342afa781d16d6c62b` |
| Ranked Mastery run 2, `set8.message` | Download delivery 8 blob.txt (private download link removed) | `49a79d9b1a7c09b4ed9f81c1c3995354508297de3315a12e183c40d46431f4c5` |

### Solver

The reusable solver is `warmup-tools/run_modes.py`, backed by
`warmup-tools/decode_base64_layers.py`. It reads the live questions and
answer IDs, downloads assigned deliveries, maps Mastery questions to their
delivery, decodes each blob, checks the requested slug format, submits all
answers, and saves the run record.

Run a mode with:

```sh
python3 warmup-tools/run_modes.py 'warmups-day-02'
```

For a deliberately authorized legacy timed retry, the same runner accepts
`--retry`; this must only be used during the ranked phase:

```sh
python3 warmup-tools/run_modes.py 'warmups-day-02/time_trial' --retry --keep-alive --skip-artifact-hash
python3 warmup-tools/run_modes.py 'warmups-day-02/mastery' --retry --keep-alive --skip-artifact-hash
```

The Time Trial should yield one answer. Mastery maps its eight `setN.message`
IDs to eight deliveries and submits them together. A nonzero error or expired
timer must be preserved in its run directory and debugged offline; do not
exceed the number of ranked attempts explicitly authorized for the session.
On a reconnect, the runner checks `accepted_ids` and submits only outstanding
answers.
`--skip-artifact-hash` avoids optional hashing on a timed path while still
saving every downloaded artifact for regression or debugging.
`--keep-alive` performs a read-only status preflight before retrying, then
reuses the proxy connection for retry, one artifact download, and submission;
the other Mastery downloads remain concurrent. This optimization was added
before the second ranked runs. The runner now prefers the current capability
link returned for each assigned artifact, falling back to the artifact
operation if a capability link has expired.

A read-only proxy timing check reused one connection: the first status request
took 1.09 s and the next took 0.25 s. This showed lower client latency for a
reused connection, but the second runs' command durations were longer than the
first runs. Those durations include preflight and final status calls and may
not match the CourseStack ranking timer. Since the Game Master did not expose
second-run leaderboard times, these runs do not establish a ranking
improvement.

After the second runs, a non-ranked concurrent download comparison tested two
eight-artifact Mastery batches per route. The normal artifact route took 1.82
and 2.44 seconds; current capability links took 1.39 and 1.14 seconds, with
matching artifact hashes. The median batch difference was about 0.86 seconds
in this small sample. This is a promising network-path optimization, not a
ranked timing result; expired capability links fall back to the artifact
route. The second ranked runs used the artifact route, before this preference
was added.

Plain-text artifacts require only Python's standard library. `pyzipper` is
loaded only when an encrypted ZIP artifact needs to be opened.

### Offline regression

Regression data, API responses, exact candidate answers, and timings are in
`work/day-02/warmups/half-a-turn-review-20261028/` (source reference: `../../work/day-02/warmups/half-a-turn-review-20261028/`; not linked in this draft).
`final-offline-regression.json` (source reference: `../../work/day-02/warmups/half-a-turn-review-20261028/final-offline-regression.json`; not linked in this draft)
records the final run across all 28 saved artifacts. Repeated local answer-
building measurements ranged from 6–9 ms for Single Solve, 1–3 ms for Time
Trial, and 11–19 ms for the eight Mastery deliveries. These timings exclude
network and Game Master time. The final code also passed direct-capability and
expired-capability-fallback checks, plus full regression against all 28 saved
artifacts.

### Ranked results

| Mode | Attempt | Outcome | Client wall time | Server window | HOF eligible | Attempts remaining |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Time Trial run 1 | `54a1b116-a5a3-443c-9692-dac099644fa0` | `CORRECT`, 1/1 accepted | About 2.6 s | 20 s | Yes | 252 |
| Mastery run 1 | `bddd26b5-bbed-4cf1-a4c1-1405f61602c5` | `CORRECT`, 8/8 accepted | About 4.8 s | 25 s | Yes | 252 |
| Time Trial run 2 | `85a07dca-530a-45b0-ac05-ef8c7d479cb0` | `CORRECT`, 1/1 accepted | About 5.4 s | 20 s | Yes | 251 |
| Mastery run 2 | `901d3c05-8492-4962-a519-476f5094c2fd` | `CORRECT`, 8/8 accepted | About 6.0 s | 25 s | Yes | 251 |

Both Game Master status responses returned `CORRECT` with all answer IDs
accepted and no pending scoring status. The Game Master list still shows the
challenge solved; it retains the unknown historical solve attribution and
does not expose a new leaderboard place or official solve time. The client
wall times are approximate command durations, not CourseStack ranking times.
The user reported the first ranked results as Time Trial **0.834 s, place 65**
and Mastery **3.701 s, place 103**. The Game Master API did not return a new
ranking time or place for the second runs, so the keep-alive effect cannot be
compared through that API. The latest user-reported leaderboard is Time Trial
**0.834 s, place 65** and Mastery **3.250 s, place 100**. That is 0.451 s
(about 12.2%) faster and three places higher than the earlier reported Mastery
result. The API still does not expose the official time or place.

The Time Trial began at `2026-10-28T23:26:22.527Z` and had a server deadline
of `2026-10-28T23:26:42.527Z`. Mastery began at
`2026-10-28T23:26:48.339Z` and had a server deadline of
`2026-10-28T23:27:13.339Z`.

The second Time Trial began at `2026-10-28T23:37:51.774Z` with a deadline of
`2026-10-28T23:38:11.774Z`. The second Mastery began at
`2026-10-28T23:38:08.186Z` with a deadline of
`2026-10-28T23:38:33.186Z`. Two attempts were consumed from each ranked pool;
251 unique attempts remain in each. No further ranked attempt was started.

The second runs' fresh artifacts reprocessed to the exact saved submitted
candidates. Answer building took about 6.1 ms for the second Time Trial and
11.3 ms for its eight Mastery deliveries. Including historical assignments
and both ranked runs, final offline regression covered 28 artifacts and
reproduced 28 required answers with matching API SHA-256 values. No fresh
untimed randomized variant was available, so historical files alone are not
evidence for unseen variants.

### Readiness and limits

The solver is ready for the tested artifact formats: it processed the Single
Solve sample, historical timed assignments, and four fresh ranked assignments
without challenge-specific answer constants. Two randomized Time Trial
artifacts and 16 randomized Mastery deliveries passed. Each Mastery run mapped
all eight artifacts and answer IDs and finished well inside the shared
deadline.

Remaining risks are a future randomized encoding outside the shared decoder's
supported formats and unusually slow Game Master or proxy requests. No new
untimed Time Trial or Mastery replay was available: both legacy routes have a
zero-sized regular pool, while their practice continuation is reserved for
after the ranked rotation is exhausted.

## Retained sources

- [early/02-Half_a_Turn/readme.md](../../source-notes/early/02-Half_a_Turn/readme.md)
- [later/writeups/day-02/warmups-half-a-turn.md](../../source-notes/later/writeups/day-02/warmups-half-a-turn.md)
