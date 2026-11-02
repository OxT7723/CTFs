> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Binary reverse engineering tools

`analyze_evidence.py` builds answers from the live start response and an
extracted evidence directory. It reads ELF headers, sections, symbols and
disassembly with `readelf`/`objdump`, reads PE section names and CLI metadata,
recognizes WebAssembly modules and role-named variants, locates and validates
HCFG records, and reads JAR compression methods. It does not contain campaign
IDs, URLs, file names, or expected answer values.
It also maps plain ELF field IDs and `slotN_...` fields to standalone or
slot-named binaries, including numbered Mastery sets.
Fields prefixed with an exact filename label such as `c_` or `cpp_` select the
matching specimen in a mixed archive. Unprefixed HCFG and C++ symbol fields are
resolved against the binary containing that configuration or symbol.
For PE specimens, it checks C++ RTTI and vtable markers in the assigned bytes.
The HCFG section check handles both ELF and PE section tables.
For RS20 resource overlays, it checks the declared HCFG resource and scratch
bounds, verifies the scratch SHA-256, then parses the HCFG record at the
resource start.
Archive member order is recorded during extraction so numbered artifact hash
fields follow the delivered order even when filenames sort differently. The
Day 15 stripped and symbolized ELF fields are selected by their role in the
assigned filenames.
The artifact index accepts both `dNN--variant-*` and `dNN--sample*` names.
For managed/native bridge evidence, it selects the Day 21 loader ELF and
plugin by role, parses the plugin HCFG, and reads normalized PE machine labels
from `objdump -f`. Fields that explicitly request a numeric ELF machine code
remain numeric.
For paired JAR builds, it selects the vulnerable and corrected specimens by
their filename roles, classifies JARs only when they contain valid classfiles,
and extracts CRC32-valid HCFG records from Base64 constant-pool strings.
Shared configuration answers are emitted only after the two decoded HCFG
payloads match byte for byte.
For Day 03 managed PE evidence, it resolves the primary CLR assembly from its
metadata rather than archive order, requires one CRC32-valid HCFG record, and
reads the metadata-root version using the declared length after trimming
trailing NUL bytes. See the [Table Manners writeup](../../../source-notes/later/writeups/day-03/binary-table-manners.md)
for its answer contract, mode availability, artifacts, and measured results.
The Day 25 paired-JAR fields use the same role selection and byte-for-byte
configuration check; their format answers distinguish JARs by valid classfile
magic rather than by the filename extension.
For Day 27 compiler attribution, it selects GCC and TCC ELF specimens by
filename role, classifies their final containers, reads numeric ELF machine
codes, and scans backward for the last CRC32-valid raw HCFG record. Shared
configuration answers are emitted only after both decoded payloads match.
Day 28 family-clustering fields select the false-friend, family-a, and family-b
specimens by filename role, classify their final containers, read numeric ELF
machine codes, and validate that the two family HCFG payloads match byte for
byte before using the shared configuration. Structural archive fields use
central-directory order for member counts and ordered-set hashes. ELF symbol
name parsing preserves spaces in resolved names.
Day 29 optimization-diffing fields select O0 and O3 ELF specimens from their
delivered filename suffixes, classify their final containers, read numeric ELF
machine codes, and validate that their backward-scanned HCFG payloads match.
Repeated parser requests reuse cached ELF headers and section tables, PE section
tables, managed metadata versions, and Java Main-Class metadata. On a resumed
attempt, an existing artifact archive is reused only after its SHA-256 matches
the current Game Master assignment.
Day 30 multi-binary campaign fields select loader, library, and config capsule
specimens by role. The analyzer reads the last CRC32-valid HGRF record from
each file, confirms their graph payloads match after removing `this_role`,
then reads shared values from `graph.config`. Neko `.n` bytecode is recognized
as a binary container and reported as `neko_bytecode`.
Day 31 gauntlet fields select the delivered ELF, scan backward for the final
CRC32-valid HGAU record, and read its decoded config, trace branch, CRC32, and
XOR key. The HGAU parser uses the same bounded 12-byte record layout and CRC
validation as HCFG.

Extract the Game Master AES ZIP with the event password, then build candidates:

```sh
python3 -m venv binary-reverse-engineering-tools/.venv
binary-reverse-engineering-tools/.venv/bin/python -m pip install \
  -r binary-reverse-engineering-tools/requirements.txt
binary-reverse-engineering-tools/.venv/bin/python binary-reverse-engineering-tools/extract_zip.py evidence.zip extracted/
binary-reverse-engineering-tools/.venv/bin/python binary-reverse-engineering-tools/analyze_evidence.py extracted/ \
  --answer-map start-response.json --output candidate-answers.json
```

The HCFG reader validates its CRC after XOR decoding. For HCFG records stored
as Base64 strings in a binary or archive, it records the offset of the encoded
record in the containing file. It labels direct records by their container:
ELF `.data`/`.rodata` arrays as `raw_const_array`, ELF `.hcfg` sections as
`raw_hcfg_section`, PE records as `raw`, and WebAssembly data-segment records
as `wasm_data_segment`.
For PE C++ symbol questions, the answer may be the section-qualified COFF
symbol (for example `.text$<mangled-name>` or `.rdata$<typeinfo-name>`), rather
than the bare symbol returned by `nm`.

To run a mode directly from the Game Master, use its exact challenge ID.
The runner sends as many answers as fit in the Game Master's 4 MiB JSON limit.
Use `--batch-size` to impose a smaller answer-count cap. It skips answers
already accepted on a resumed attempt. If a group is incorrect, it bisects the
group to isolate unresolved fields while continuing past individual incorrect
answers.
Artifact archives download concurrently with three workers by default; use
`--download-workers` to select 1–8 workers. Downloads stream to temporary files,
are checked against the Game Master SHA-256, and are renamed into place only
after validation. Archives are then extracted in delivery order. With
`--keep-alive`, the runner opens its persistent connection before starting the
attempt and uses it for sequential Game Master requests. A single-artifact
assignment also downloads over that connection; multi-artifact assignments
keep concurrent downloads. The analyzer is loaded before the attempt starts.
The run summary records the worker count and total download time.
If a completed challenge returns `CORRECT` without an active attempt ID, the
runner exits without downloading or treating the previous assignment as new.
Use `--retry` only when you want the Game Master to assign another variant.

```sh
binary-reverse-engineering-tools/.venv/bin/python \
  binary-reverse-engineering-tools/run_modes.py "$CHALLENGE_ID"
```

For a fresh timed Hall of Fame attempt on a supported Time Trial or Mastery
route, pass `--run-for-time` explicitly. If the regular route is already
complete, `start` reconnects to that completed attempt; use `--retry
--run-for-time` to request the next fresh timed variant:

```sh
binary-reverse-engineering-tools/.venv/bin/python \
  binary-reverse-engineering-tools/run_modes.py "$CHALLENGE_ID" \
  --retry --run-for-time
```

The runner refreshes its persistent Game Master connection after local
analysis, since solving a large Mastery bundle can exceed the proxy's
keep-alive idle timeout.

For example, to use four workers:

```sh
binary-reverse-engineering-tools/.venv/bin/python \
  binary-reverse-engineering-tools/run_modes.py "$CHALLENGE_ID" \
  --download-workers 4
```

The persistent client reconnects and retries once if the proxy closes an idle
keep-alive socket before a request can be sent.

If the Game Master reports that timed variants are exhausted, `--practice`
continues the last assigned material without a running clock:

```sh
binary-reverse-engineering-tools/.venv/bin/python \
  binary-reverse-engineering-tools/run_modes.py "$CHALLENGE_ID" --practice
```

When an answer remains unresolved after the allowed investigation, the runner
can preserve progress on the other fields without submitting that answer again:

```sh
binary-reverse-engineering-tools/.venv/bin/python \
  binary-reverse-engineering-tools/run_modes.py "$CHALLENGE_ID" \
  --skip-answer-suffix analysis_hcfg_storage
```

## Finding the released challenge

The documented `lane=binary` list filter did not match the live Day 14 lane
slug (`binary-reverse-engineering`). If a Day-and-lane filtered list is empty
at release time, query that day without a lane filter and inspect each
challenge's returned `lane` before concluding the release is unavailable or
starting a polling loop.

```sh
curl -fsS 'http://192.0.2.1/huntress-ctf-proxy?op=list&day=14'
```
