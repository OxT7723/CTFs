> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Metadata Forensics: Trust Issues

All three regular modes completed with Game Master result `CORRECT`. No mode
returned a pending CourseStack scoring status.

| Mode | Attempt | Accepted answers | Artifact |
| --- | --- | ---: | --- |
| Single Solve | `4c74d0a6-3db8-418e-9b1f-b74742d5e43c` | 1 / 1 | metadata-day-29-evidence.zip (retired artifact link; see artifact inventory) — SHA-256 `7e100a9dadaca752a47a6599af7b0b0bbeab734c3140276e8c375f9b5abde3d9` |
| Time Trial, regular untimed | `4441e3a6-1017-4468-b83b-978cc0cce35a` | 34 / 34 | evidence.zip (retired artifact link; see artifact inventory) — SHA-256 `c2042b57804d14f1510a71cadd02005c4bacaf60c437da53d8c130346f2bc519` |
| Mastery, regular untimed | `4ff52e6a-6c87-448a-afe6-d4907bf95eab` | 442 / 442 | metadata-forensics-day-29-trust-issues-mastery.zip (retired artifact link; see artifact inventory) — SHA-256 `3d27682a082b4efce5e4c4c1539b7b354f76dbc2c2c34ba5fe8b9d671fbdcc58` |
| Time Trial, timed Hall of Fame | `30eb4707-a5d9-46bd-9050-ba43e21487e6` | 34 / 34 | evidence.zip (retired artifact link; see artifact inventory) |

Added X.509 certificate fingerprint support to the reusable runner. The
`x509.sha256_fingerprint` value is calculated from the certificate's DER
encoding, including when the assigned bytes are PEM. The runner now opens a
fresh connection before its pre-submit status check, avoiding a stale
keep-alive connection after artifact delivery.

The timed attempt used `run_for_time:true`, was marked Hall of Fame eligible,
and completed `CORRECT` within its 50-second deadline. End-to-end runner time
was about 7.2 seconds. The outer archive was not hashed; per-file hashes
requested by challenge questions were still calculated.

## Ten-run timed Time Trial sample

Ran ten additional fresh Hall of Fame variants. All ten returned `CORRECT`,
accepted all 34 answers, and were Hall of Fame eligible. Ranked attempts
remaining afterward: 21.

| Attempt | Client wall time |
| --- | ---: |
| `c2f5eaaa-b302-45b1-9450-30244022feaf` | 3.142 s |
| `24b4f56a-607e-42c8-a430-94b8cbfefff0` | 4.938 s |
| `96f6315e-22c6-4774-a914-58c26ecc00d9` | 4.339 s |
| `ef4da22c-cc44-4669-956e-0326480ba27b` | 6.528 s |
| `ccad635a-45cc-49fe-9a1a-103e9d271e6a` | 4.155 s |
| `a98a585c-dc21-493d-815d-d0daab8c32fb` | 4.334 s |
| `3a809cac-5fe9-4331-a802-02adb3ef7679` | 5.715 s |
| `d631cc3a-0530-445d-bc05-15cb61875cf5` | 4.372 s |
| `27abb711-140e-4705-9bdf-54681dd62dbf` | 4.401 s |
| `ac17d4e7-f6f9-4f20-a334-b19718da897d` | 3.765 s |

Client wall time averaged 4.569 s (median 4.356 s). From retry/start through
artifact download and submission, the profiled request round trips averaged
about 3.03 s; local answer construction averaged 0.228 s and artifact
processing 0.014 s. Submit latency varied most, from 0.519 s to 3.792 s.
This points to proxy/service latency as the main source of variation; local
solver changes are unlikely to improve Time Trial meaningfully. The runner
already reuses one connection and skips the optional outer ZIP hash.

## Ten-run timed Mastery sample

Ran ten fresh timed Hall of Fame variants. All ten returned `CORRECT`, accepted
all 442 answers, and were Hall of Fame eligible. Ranked attempts remaining
afterward: 22.

| Attempt | Client wall time |
| --- | ---: |
| `72c40636-9476-44cd-b00f-b4fc47fb1f5d` | 8.642 s |
| `e96f5e86-6867-4bb0-86c1-fc0869ff8b03` | 8.208 s |
| `0dd0a640-af66-45a7-8ccb-e6924a30b84f` | 7.943 s |
| `05890b68-6580-400d-afa5-e8d8f0ad744b` | 7.554 s |
| `68141c0f-f80c-45d8-ac09-51d5e1dedf98` | 7.703 s |
| `04901268-b389-4223-8b8e-72df92bd3dd0` | 7.418 s |
| `98e7c66f-d84a-4dc0-9e5b-f6d945887f16` | 7.532 s |
| `f9abfa1b-cea2-4833-93f5-113883aa0926` | 9.091 s |
| `5605c62c-7412-4f7f-9b4e-8554b6f5bd72` | 6.768 s |
| `9df9e60f-c182-4b30-81da-539aa3607d9a` | 6.394 s |

Before optimization, Mastery answer construction averaged 2.747 s. Profiling
showed `pefile` fully parsing relocation data for each PE version-resource
question. Changed [pe_metadata.py](../../../../tools/later/metadata-forensics-tools/pe_metadata.py)
to parse only the resource directory. Replaying the latest assigned 442
questions from its saved artifact took 0.886 s and produced candidates
identical to the accepted submission. This replay did not start or consume an
attempt. An eight-worker experiment on the same artifact yielded only a 2%
improvement, so the runner remains sequential.

Attempt records, candidate answers, submission results, and final statuses are
under
`metadata-forensics-tools/attempt-records/metadata-forensics-day-29-trust-issues/` (historical reference: `/home/HuntressCTF/metadata-forensics-tools/attempt-records/metadata-forensics-day-29-trust-issues/`; not included).
