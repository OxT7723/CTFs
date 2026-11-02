> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 31 Metadata Forensics — No Artifact Left Behind

Challenge ID: `metadata-forensics-day-31-no-artifact-left-behind`

## Completion

- Single Solve: solved.
- Time Trial: solved on the fourth regular, untimed variant. The earlier
  three attempts remain incomplete; accepted answers were preserved.
- Mastery: solved. All 540 answer fields were accepted, including all 15
  execution-chain questions.
- The Day 31 Game Master listing reports all three modes as solved. The
  supported proxy reports `CORRECT`; it does not expose a separate numeric
  CourseStack point tally.

Attempt records, downloaded artifacts, candidates, and submission responses
are under
`metadata-forensics-tools/attempt-records/metadata-forensics-day-31-no-artifact-left-behind/`.

## Solver notes

`metadata-forensics-tools/metadata_graph.py` extracts artifact references from
ZIP run files, SQLite launch queues, PNG text chunks, JSON `next` fields, email
route attachments, and literal PowerShell targets. It prefers a path to an
explicit terminal marker. When a corpus has no terminal marker, discard
directed cyclic components if an acyclic source-to-sink path exists; the
longest such path identifies the delivery route. The unresolved Mastery
variants contained tempting large cycles beside shorter delivery paths.

The challenge runner submits graph fields separately from standard metadata
answers. This preserves already accepted answers while graph interpretation
is being refined. The accepted alternate delivery routes and the earlier
cycle guesses are recorded in the Mastery attempt directory.
