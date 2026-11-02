> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 7 — Seven-Zip, No Relation

Challenge ID: `metadata-forensics-day-07-seven-zip-no-relation`

Prompt: “Files arrive inside and beside a collection of ZIP archives. Count
what the archives claim, distinguish empty space from evidence, and find the
census that does not add up.”

All three modes were solved. The parser and live runner are in
[`metadata-forensics-tools`](../../../../tools/later/metadata-forensics-tools/README.md). The
runner uses answer IDs and archive chains from the active Game Master response;
it does not store campaign IDs, artifact names, or answer values.

## Single Solve

Mode: `single_solve`; untimed, no deadline.

Question: determine `zip.eocd_total_entries` for `evidence-drop-001.zip`
(`integer`, base-10 with no extra text), answer ID
`d07-zip-001-zip-eocd-total-entries`.

The assigned `metadata-day-07-evidence.zip` contains the requested archive.
Its raw EOCD record reports 2 total entries. The submitted answer was accepted.

Artifact: metadata-day-07-evidence.zip (retired artifact link; see artifact inventory)  
SHA-256: `160901875ab2ef41499ba2ded8511765a9ae82e00196c6956067836ed7649f2a`

## Time Trial

The first available Time Trial variant was untimed practice (`run_for_time:
false`). Its 11 accepted questions covered:

- Evidence note filename (`exact_text`), size (`integer`), MD5, SHA-1, SHA-256,
  16-byte magic prefix (`hex`), and UTF-8 BOM (`true`/`false`).
- JPEG SOF dimensions and PNG IHDR dimensions (`WIDTHxHEIGHT`), PDF header
  version, and ZIP EOCD total entries.

All 11 answers were accepted. The evidence note was `evidence-note.txt`
(33 bytes); its MD5 was `2273cbe05fb33268a4b9952b5a5855a7`,
SHA-1 `8bfeeaa22e670092e238548c1abe83d42de896f9`, SHA-256
`06675ef93d261ba55c4e9bc12bf88941a69a597793e3a34f4ca44fdf94c4c287`,
magic prefix `43617365203939373339333033393634`, and it had no UTF-8 BOM.
The camera dimensions were `257x146`; the panel dimensions were `269x153`;
the PDF header version was `1.4`; the first nested archive reported 2 entries.

The ranked attempt was started with `run_for_time:true` and had a 14-second
deadline (`2026-10-10T22:40:46.540Z`). Its question asked for
`zip.eocd_total_entries` from `evidence-drop-002.zip` as a base-10 integer,
answer ID `d07-zip-002-zip-eocd-total-entries`. The raw EOCD reported 3 and the
answer was accepted before the deadline.

Practice artifact: metadata-day-07-evidence.zip (retired artifact link; see artifact inventory)  
SHA-256: `34429d4d37ee73bd099ba2ded8511765a9ae82e00196c6956067836ed7649f2a`

Ranked artifact: metadata-day-07-evidence.zip (retired artifact link; see artifact inventory)  
SHA-256: `8bfad1bf061e00992ea9384429d237c882e11182d3a3cfa4bb55a83d8c3d5eaf`

## Mastery

Started with `run_for_time:true`; the deadline was
`2026-10-10T22:40:55.532Z`. The two questions requested `zip.eocd_total_entries`
for `evidence-drop-003.zip` and `evidence-drop-004.zip`, each in base-10 integer
format. Their answer IDs were
`set1.d07-zip-003-zip-eocd-total-entries` and
`set2.d07-zip-004-zip-eocd-total-entries`. The EOCD records reported 4 and 5;
both answers were accepted before the deadline.

Artifact bundle: metadata-forensics-day-07-seven-zip-no-relation-mastery.zip (retired artifact link; see artifact inventory)  
SHA-256: `fea81c477d8d746bb9838217c6311cc938c812d02d5b1b8052a91ce79b1bcee1`

## Records

Raw start responses, downloaded bytes, candidate answers, submissions, and
status responses are saved under `work/day-07/` by attempt ID.
