> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 31 Mobile: Mobile Arena Gauntlet

Completed Single Solve, regular untimed Time Trial, and regular untimed Mastery.
Mastery contained 15 APK deliveries; all 15 answer IDs were accepted. Every
Game Master status check returned `CORRECT`, with no pending scoring status.

The APKs expose the backend answer code in
`assets/huntress_puzzle.json`. The existing Mobile decoder handled the
Single Solve, Time Trial, and all Mastery variants without artifact-specific
logic. Keep Time Trial and Mastery on `--regular-untimed`; timed Hall of Fame
play is opt-in for these routes.

The runner now closes its idle keep-alive connection before submitting answers.
Long APK analysis had left that connection stale, causing the proxy to close
the socket during the Single Solve and Mastery submissions. Status was checked
before resubmitting those saved candidate answers.
