> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Game Master access and safety

- Normal direct endpoint: `https://2026.huntress.ctf.games/`.
- Use existing `gm.py` and authenticated HTTPS with bearer token from environment variable `HUNTRESS_GM_TOKEN`; do not expose the token in chat, logs, files, process arguments, commits, or exceptions.
- Internal `http://192.0.2.1/huntress-ctf-proxy` is for initial pairing or explicitly required internal operations, not routine direct play. The public endpoint avoids needing Homebase for ordinary listing, status, artifact download, and submissions.
- Known operations include `GET ?op=openapi`, `GET ?op=list`, filtered lists, status, artifact, challenge start, and answer submission. Consult current `?op=openapi` when implementing new behavior or if API responses differ; don't guess formats.
- Use exact current challenge IDs and answer IDs. A retry may reuse or replace the assigned artifact: trust current server response.
- `accepted` can mean partial progress; `CORRECT` may still have pending scoring. CourseStack is official scoring ledger.
- Do not reset pairing automatically. Do not attempt to access another player's or team's flags, artifacts, or credentials.
- Some CourseStack-native orientation tasks may require submission in CourseStack rather than Game Master.
