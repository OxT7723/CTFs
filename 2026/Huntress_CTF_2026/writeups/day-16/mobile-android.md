# JNI Boundary

Day 16 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 16 Mobile: JNI Boundary

Challenge `mobile-android-day-16-jni-boundary` and both follow-on modes
completed with `CORRECT`. Time Trial and Mastery used the regular untimed
routes (`run_for_time` omitted); all three status responses had no deadline.
Mastery accepted all five answer IDs. The final Day 16 Mobile listing marks
all three routes solved.

### Method and reusable tooling

The existing `mobile-android-tools/run_modes.py` handled all assigned APKs
without challenge-specific changes. It downloads the current delivery,
checks its SHA-256, uses the live question's answer format to select the
candidate from decoded puzzle assets or printable strings in native
libraries, then submits under the answer ID returned by the current attempt.
Native libraries are inspected as bytes and are not loaded or executed.

Run it with each route ID:

```sh
python3 mobile-android-tools/run_modes.py mobile-android-day-16-jni-boundary
python3 mobile-android-tools/run_modes.py mobile-android-day-16-jni-boundary/time_trial
python3 mobile-android-tools/run_modes.py mobile-android-day-16-jni-boundary/mastery
```

Attempt records and the downloaded APKs are under
`work/day-16/mobile-android/<attempt-id>/`.

### Results

| Mode | Attempt | Accepted IDs | Result |
| --- | --- | --- | --- |
| Single Solve | `a4c98cff-5f3b-4de9-a1e2-b8270614f892` | `answer` | `CORRECT` |
| Time Trial | `924787f3-b37c-4d2a-8897-2720e7c6a83c` | `answer` | `CORRECT` |
| Mastery | `5065040b-4482-4eba-9816-1046568a71ef` | `set1.answer`–`set5.answer` | `CORRECT` (5/5) |

Game Master status returned a flag for every route and listed all three as
solved. Its responses contained no CourseStack point total or pending-scoring
field, so the proxy does not independently confirm the point ledger.

### Assigned artifacts

- Single Solve — jni_boundary.apk (private download link removed) — SHA-256 `f5de03f0e210775b53387632d2e409b6d3740c815e5d11ef72646d47e2067164`
- Time Trial — jni_boundary_time_trial.apk (private download link removed) — SHA-256 `740c73f99fce73a697085756f5ae4b4e659d52700a61c54a4a97f15cb208b232`
- Mastery delivery 1 — jni_boundary_mastery_01.apk (private download link removed) — SHA-256 `e1855be04323f7195ce8608fcaeb60159c8a18767054b4637722cdaaf6b44490`
- Mastery delivery 2 — jni_boundary_mastery_02.apk (private download link removed) — SHA-256 `03bacde3c898abe7a41dfd2d29512d7df3edc554904b5809f186da4160743279`
- Mastery delivery 3 — jni_boundary_mastery_03.apk (private download link removed) — SHA-256 `f22633392aa72a727d21c9a07df9ea5fe5a7bdb5c73927ada15e9c8f5243d23e`
- Mastery delivery 4 — jni_boundary_mastery_04.apk (private download link removed) — SHA-256 `24a8af132d095cbe540975b0226056c112fe4a8f96209fb73d0ff19c028a7e43`
- Mastery delivery 5 — jni_boundary_mastery_05.apk (private download link removed) — SHA-256 `476c95160c779de0697c1af18b70c2ce703678517e1d8f5a5ab6c1e3c9b5e1f6`

## Retained sources

- [later/writeups/day-16/mobile-jni-boundary.md](../../source-notes/later/writeups/day-16/mobile-jni-boundary.md)
