# What’s My Name Again?

Day 11 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `metadata-forensics-day-11-whats-my-name-again`

## Later Homebase account

### Day 11 Metadata Forensics: What’s My Name Again?

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

## Retained sources

- [early/11-Whats_My_Name_Again/readme.md](../../source-notes/early/11-Whats_My_Name_Again/readme.md)
- [later/writeups/day-11/metadata-forensics-name-again.md](../../source-notes/later/writeups/day-11/metadata-forensics-name-again.md)
- [later/writeups/day-11/progress-notes.md](../../source-notes/later/writeups/day-11/progress-notes.md)
