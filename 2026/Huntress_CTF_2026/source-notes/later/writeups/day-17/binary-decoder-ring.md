> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 17: Decoder Ring

Challenge: `binary-reverse-engineering-day-17-encoded-configuration-recovery`

The Single Solve artifact SHA-256 is
`cdbe7f081670e4bf6164bc4a1bb60b4c671da60bb1a47499df538fdacef5434f`.
The analyzer was extended for HCFG storage classes, absent Day 1 markers and
return values, PE symbol and section metadata, Go runtime detection in PE
files, C++/Rust symbol checks, Java class-file metadata, and coroutine-runtime
detection.

Single Solve is complete: all 204 fields were accepted. The live Game Master
initially described `d12_analysis_hcfg_storage` and
`d14_analysis_hcfg_storage` only as `exact_text`. After the host's Discord
message, the live status response exposed the enum
`raw`, `base64`, `raw_const_array`, `raw_hcfg_section`, and
`wasm_data_segment`, with exact case-sensitive spelling required. The d12
record in ELF `.data` is `raw_const_array`; d14's `.hcfg` section is
`raw_hcfg_section`. Both were accepted.

The d12 and d14 binaries are byte-for-byte identical to the Day 12 and Day 14
Single Solve specimens previously analyzed in this workspace. Their older
question contracts asked for HCFG offsets and section presence, but supplied
no storage vocabulary.

The d12 and d14 ELF files contain no Base64-encoded HCFG copies; each has only
the validated direct record already analyzed.

The website's “Decoder Ring” prompt matches the Game Master prompt. “Ring”
alludes to the bytewise XOR decoder, but `xor` is not an HCFG storage class.
The host's message was the useful clue that the missing information was the
exact answer vocabulary; the subsequent live enum response resolved both
labels.

The literal `none` was subsequently submitted alone for both fields and was
rejected for each.

Further isolated submissions tested `xor` for both fields, then `GLOBAL` and
`OBJECT`, `global`, and `symbol` for d14 based on the `huntress_config` ELF
symbol metadata; `global`, section flag constants, and `absolute` were also
tested against the corresponding field. Then segment names (`PT_LOAD`, `text`,
`executable`, `RX`), Unix-style permissions, and ELF load addresses were tried
separately. Section-index, nm symbol-class, and lower-case permission variants
were also rejected. ELF `PF_*` program-header flag expressions, and anonymous
or global-symbol storage labels, were rejected too. The attempt log is in
`rejected-storage-candidates.json`.

Before the enum was exposed, isolated guesses `XOR`, the literal
`byte_arrary`, and the conventional `byte_array` were each submitted alone for
both fields; all six were rejected. The other unsuccessful candidates remain
recorded in `rejected-storage-candidates.json`.

The byte-content interpretation was also checked: each full HCFG record was
submitted as hex and Base64, and each XOR-decoded JSON payload was submitted as
UTF-8 text. All six singleton submissions were rejected. Exact values are
preserved in the attempt's `rejected-byte-candidates.json`.

## Historical question comparison

Read-only Game Master status requests were used to review the Single Solve
question contracts for Binary Days 1–17; no older attempts were started. The
closest prior questions ask for the exact string in a custom `.huntress`
section (Day 1), section-name arrays, HCFG offsets, or a `has_hcfg_section`
boolean (Days 10 and 14). None of the Day 1–16 contracts has an
`analysis_hcfg_storage` field.

That storage field first appears in the Day 17 bundle. Within that bundle,
d08, d09, d11, and d13 have accepted value `base64`; those records are Base64
wrapped. They do not establish a label for d12's direct `.data` record or
d14's direct `.hcfg` record. The previous Binary question sets therefore add
no missing vocabulary for the two unresolved answers.

Time Trial is complete in the regular untimed mode: all 204 fields were
accepted after recovering the `.huntress` marker `BR01-CATALOG-014` from d01.
Mastery is complete in the regular untimed mode: all 1,020 fields were
accepted. The PE d02 variants required section-qualified COFF symbol names:
`.text$_ZNK15DiscoveryEngine5scoreEPKc` and
`.rdata$_ZTI15DiscoveryEngine`.

Game Master reports Single Solve, Time Trial, and Mastery as solved. Its list
response does not include CourseStack point totals, and the CourseStack ledger
was not reachable at the local web root during this check, so point posting
remains unconfirmed. No ranked `run_for_time:true` attempt was requested.
