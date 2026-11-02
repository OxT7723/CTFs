> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 11 Metadata Forensics: What’s My Name Again?

- Challenge ID: `metadata-forensics-day-11-whats-my-name-again`
- Mode: Single Solve
- Question: `d09-pe-001-pe-version-original-filename`
- Artifact SHA-256: `aadf2e31e4b4f6ef17927e90c9a46ba01e13468f99a4fd8a46706ae1b6055031`

The question asks for the PE `VERSIONINFO` `OriginalFilename` string, which
can differ from the delivered file's name. The updated
`metadata-forensics-tools/pe_metadata.py` reads PE version strings through
`pefile`, and `run_challenge.py` now maps this field to that resource value.
The Single Solve value was `pe-base-386.exe`. Single Solve, Time Trial, and
Mastery all returned `CORRECT`; timed modes use the same generic
`OriginalFilename` handler on each assigned executable.

Install the reusable metadata dependencies with
`python3 -m pip install -r metadata-forensics-tools/requirements.txt`.
