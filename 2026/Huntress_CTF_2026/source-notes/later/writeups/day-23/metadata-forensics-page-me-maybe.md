> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 23 Metadata Forensics — Page Me Maybe

All regular modes are complete. Each Game Master submission and status returned
`CORRECT`; no CourseStack pending-scoring status was reported. Attempts used
regular untimed play (`run_for_time: false`).

| Mode | Attempt | Accepted | Assigned artifact |
| --- | --- | ---: | --- |
| Single Solve | `2380497b-2c3a-47dd-9feb-9c7583aebda0` | 1 / 1 | metadata-day-23-evidence.zip (retired artifact link; see artifact inventory) — SHA-256 `f2540b81c5f76f7467452c021d3b84363185525ae894134ee13da209146781f2` |
| Time Trial | `61c05b41-45c7-4243-bc60-c89dfba7caf5` | 28 / 28 | evidence.zip (retired artifact link; see artifact inventory) — SHA-256 `81374aa828a22bae7a78500abbb8db6e5b2582898250ef2980570268fb763a29` |
| Mastery | `d7df2fb1-32fb-4935-963a-37f8cdd0a0f6` | 196 / 196 | metadata-forensics-day-23-page-me-maybe-mastery.zip (retired artifact link; see artifact inventory) — SHA-256 `3c2ade5158b790b39f0b1988cab9d396856071332058607696e956d6de961306` |

Added a reusable SQLite database-header reader for page size and other common
header fields. ZIP central-directory member names are now returned in sorted
order, matching the expected JSON answer order for these questions.

Attempt artifacts, answer candidates, submissions, and final status responses
are saved under `metadata-forensics-tools/attempt-records/metadata-forensics-day-23-page-me-maybe/`.
