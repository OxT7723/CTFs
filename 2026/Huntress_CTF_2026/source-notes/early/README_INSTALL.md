> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Install notes

These are proposed replacements, NOT modifications to your live Kali repository.

1. Commit or back up your current `AGENTS.md` and `CTF_WORKFLOW.md` first.
2. Copy the two root files into `~/repos/ctf-huntress-ctf-2026/`.
3. Copy the `docs/` directory into the repository. The `*_ORIGINAL.md` files preserve both original uploads for reference.
4. Start a NEW Codex session to ensure the new `AGENTS.md` is used. Keep one session per challenge across Single Solve, Time Trial, and Mastery.
5. Test a read-only prompt: `Identify the next available challenge from existing state and Game Master without scanning artifacts or modifying files. Report which files you read.`
6. Review behavior before enabling any index generation or modifying the sync scripts.

No challenge directories were moved. No sync code or JSON schema was changed. Completion status cannot be validated from the directory tree alone.

The root `README.md` challenge index remains in place; this package does not overwrite it. ZIP instructions are in `docs/ARCHIVES.md`. Completed challenges get a write-up finalization pass, but no files are deleted.
