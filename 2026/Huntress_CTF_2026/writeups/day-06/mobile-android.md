# Provider Paths

Day 6 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `mobile-android-day-06-provider-paths`

## Earlier local account

---

The assigned APK is a ZIP archive. Its manifest exposes a ContentProvider, and its packaged `assets/huntress_puzzle.json` contains the answer encoding for this instance.

For Single Solve, the packaged JSON declares `codec: hex`; decoding its `data` as ASCII yields an `ANS-` code. The same rule solved the current Time Trial and three Mastery deliveries. Each delivery had its own answer, so prior instance values were not reused.

```text
unzip -p provider_paths.apk assets/huntress_puzzle.json
python solve_mastery.py
```

- Single Solve: `ANS-46A24BCDAE5C6E1B`; Game Master returned `CORRECT`.
- Time Trial: `ANS-0090EF7564889C06`; Game Master returned `CORRECT` on the renewed attempt.
- Mastery: `set1.answer` = `ANS-33A870AFFE22E0E7`, `set2.answer` = `ANS-B7957DDF4DCCEF26`, `set3.answer` = `ANS-38F3A9DAE14EAF31`. One grouped submission returned `CORRECT`; flag `0448269ed0dae09fdaaa308f7825a622`.

Decode each current APK rather than carrying an earlier answer forward. `solve_mastery.py` fetches the three current deliveries, decodes them in order, checks the answer format, and submits under the answer IDs supplied by that attempt. The original Single Solve APK is retained as reference evidence; successful timed APKs are unnecessary once the rule is captured.

For a future attempt, run `python solve_mastery.py` after setting `HUNTRESS_GM_TOKEN`. Use `python solve_mastery.py --retry` only when intentionally renewing an expired attempt. The script retains downloaded APKs only if solving or submission fails, so that failure can be debugged offline.

## Retained sources

- [early/06-Provider_Paths/readme.md](../../source-notes/early/06-Provider_Paths/readme.md)
- [later/writeups/day-06/decode-summary.txt](../../source-notes/later/writeups/day-06/decode-summary.txt)
