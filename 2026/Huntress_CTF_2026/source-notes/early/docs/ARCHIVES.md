> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Archive extraction (on demand)

- Use installed `7z` as the preferred ZIP extraction tool on Kali. Check whether the exact current artifact was already extracted successfully; do not repeat extraction unnecessarily.
- Inspect archive metadata only when needed. For an ordinary ZIP, use `7z x -o./extracted evidence.zip` with an appropriate artifact path and destination.
- For a password-protected CTF ZIP, first try the known password `infected` with `7z x -pinfected -o./extracted evidence.zip`. Adapt paths and avoid overwriting existing user files.
- `-p` puts the password in process arguments; `infected` is a public CTF convention, but never place actual secret passwords or the Game Master token in process arguments.
- If `infected` fails, read the challenge-provided password instructions. Ask the user before password recovery unless the challenge explicitly makes cracking the intended task. Do not launch brute force, dictionaries, or repeated alternative extraction tools as an automatic fallback.
- Do not execute extracted code or binaries automatically. Treat extracted content as untrusted.
- Timed modes: prepare extraction steps before starting the timer and extract the CURRENT assigned archive only once.
