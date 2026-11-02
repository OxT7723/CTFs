> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 30 Metadata Forensics — Seeing Double

Challenge ID: `metadata-forensics-day-30-seeing-double`

All three modes completed on the regular, untimed route:

- Single Solve: 1/1 answer accepted.
- Time Trial: 35/35 answers accepted.
- Mastery: 490/490 answers accepted.

The prompt asks for a relationship map across exact identity, semantic
identity, containment, and claimed provenance, then identification of the
fabricated cluster. Full live questions and answer IDs are preserved in each
attempt's `start-response.json`; candidate answers, submission results, and
final status are saved beside them under
`metadata-forensics-tools/attempt-records/metadata-forensics-day-30-seeing-double/`.

## Reusable solver notes

- `relation.identical_sha256_groups` now hashes actual archive member bytes.
  It uses artifact IDs and member paths from `delivery-manifest.json` when
  present; otherwise it groups member basenames. Groups and their values are
  sorted for stable JSON output across randomized variants.
- Some evidence ZIPs have a central-directory/local-header filename mismatch.
  `pyzipper.BadZipFile` is now handled alongside the stdlib ZIP error so the
  malformed archive remains available for raw metadata parsing without
  blocking other answers.
- Do not trust manifest-declared digests for the grouped-hash answer; compute
  SHA-256 from each member's downloaded bytes.

The generic implementation is in
`metadata-forensics-tools/run_challenge.py`.

## Ranked timing sample

Five fresh Time Trial variants were completed on the ranked route. All five
were Hall-of-Fame eligible and accepted all 35 answers. The saved
`performance-profile.json` files are in their corresponding attempt folders.

- Answer building: 85.9–96.8 ms; median 88.1 ms.
- Artifact processing: 14.4–15.1 ms.
- Client estimate from retry through submit: 1.33–1.69 s; median 1.60 s.
- Median request times: retry 365 ms, artifact 350 ms, submit 611 ms.

The client estimate sums those three request timings with local artifact and
answer processing. It is not the Game Master's recorded solve time. The
earlier 1.69 s answer-build measurement was an outlier; all five 35-question
samples put answer building below 100 ms. Network round trips now
dominate, so changing the metadata parsers is unlikely to improve the record
by much. Keep the warmed connection and submit the full answer batch at once.

## Ranked Mastery run

A fresh ranked Mastery variant completed with all 490 answers accepted and
Hall-of-Fame eligibility. The 445-second deadline was ample: the client
profile estimated about 4.43 seconds from retry through submit, including
about 1.21 seconds building answers and 197 ms processing the artifact.
Request timings were 782 ms for retry, 1.33 s for the artifact, and 916 ms
for submission. The Game Master status does not report its recorded solve
time.

An offline profile of this assignment found 1,144 extracted files and about
151 ms spent in repeated target lookup. The runner now builds an artifact-name
and descendant index once and reuses it for target and synthesis-file
selection. Two ranked runs with the indexed solver both accepted all 490
answers and remained Hall-of-Fame eligible:

- Answer building: 1.09–1.25 s (1.17 s mean), versus 1.21 s in the previous
  unindexed run. This small sample does not show a clear speedup.
- Artifact processing: 253–288 ms; the previous run was 197 ms.
- Client estimate from retry through submission: 4.09–4.70 s (4.40 s mean),
  versus 4.43 s previously.
- Across the two runs, retry took 788–822 ms, artifact download 1.35–1.53 s,
  and submission 613–814 ms.

The full answer batch succeeded each time. Artifact delivery and network
round trips take longer than the lookup work, so they remain the main timing
cost; local answer building is the next useful area to profile. Estimates use
client request and processing timings and are not the Game Master's recorded
solve time.

An offline profile of a 490-question variant measured answer construction at
1.11 s. About 0.81 s was spent waiting for 84 external-tool processes:
ffprobe for audio and video, `msiinfo`, and `aapt`. The runner now evaluates
independent answers in a bounded eight-thread pool, preserving answer order so
these process waits can overlap. This change has not yet been measured on a
ranked run.

Ten ranked Mastery runs with the thread pool all completed CORRECT with 490
answers accepted and Hall-of-Fame eligibility. Answer building took
732.6–751.0 ms (740.0 ms mean), about 37% below the 1.17 s mean from the two
indexed serial runs. Artifact processing averaged 201.7 ms. The retry-through-
submission client estimate averaged 3.86 s, ranging from 3.14 to 4.81 s as
network timings varied; it is not the official Game Master solve time. The
Game Master result/status response contains no per-run elapsed-time field, so
these runs do not establish whether the reported 3.013 s official time
improved. The ten-run profiles and aggregate are saved in the Mastery attempt
records directory.
