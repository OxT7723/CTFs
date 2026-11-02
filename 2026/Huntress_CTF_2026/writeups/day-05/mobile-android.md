# Backup Spill

Day 5 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `mobile-android-day-05-backup-spill`

## Earlier local account

---

The assigned APK enables Android backup (`android:allowBackup="true"`) and identifies
backup-admitted `SharedPreferences` as its mechanic. The APK is a ZIP archive,
so its packaged files can be inspected without installing or executing it.

- Single Solve case: `MOB-05-9E90479049`, package
  `com.huntress.mobile.d05.v9e904790496a`.
- Downloaded backup_spill.apk (source reference: `backup_spill.apk`; not linked in this draft) for that attempt and verified
  SHA-256 `50345aca4361eb555258e7bbf3afd862d01c64945c52b8e5af8d1498f7f99719`.
- Read `assets/huntress_puzzle.json` directly from the APK. Its `parts` are
  `0A353BE7B`, `ANS-5`, and `709E18`, with `order` `[2, 0, 1]`.
- Placing each part at its corresponding output position gives
  `ANS-5` + `709E18` + `0A353BE7B`.
- Submitted the assembled value under answer ID `answer`; the Game Master
  returned `CORRECT`.

From this challenge directory:

```sh
sha256sum backup_spill.apk
unzip -l backup_spill.apk
unzip -p backup_spill.apk assets/huntress_puzzle.json
jadx -d /tmp/backup_spill_jadx "$PWD/backup_spill.apk"
```

The same extraction works for each assigned APK. This reproducer reads the
downloaded bytes directly and validates the output format:

```python
import json
import re
import sys
import zipfile

with zipfile.ZipFile(sys.argv[1]) as apk:
    puzzle = json.loads(apk.read("assets/huntress_puzzle.json"))

assert puzzle["codec"] == "split"
parts = [""] * len(puzzle["parts"])
for fragment, position in zip(puzzle["parts"], puzzle["order"]):
    parts[position] = fragment
answer = "".join(parts)
assert re.fullmatch(r"ANS-[0-9A-F]{16}", answer)
print(answer)
```

- Game Master answer: `ANS-5709E180A353BE7B`
- Completion flag: `5dac801ab25c6edc38ce127d7d6a250b`

The manifest confirms the backup setting, while the decisive data for these
assigned samples was available in the packaged JSON asset. No Android backup
command or app execution was needed for this solution. Use the `order` array as
destination positions for the fragments; simply concatenating in array order
gives a different value.

- The first assignment (`MOB-05-597E34370B`) expired before submission.
- Renewed attempt `7943714f-6886-4ae0-ba80-ef00f7c24b85` assigned case
  `MOB-05-54D127541A` in package `com.huntress.mobile.d05.v54d127541a3a`.
- Downloaded the renewed backup_spill_time_trial.apk (source reference: `backup_spill_time_trial.apk`; not linked in this draft) and verified SHA-256
  `bb7a619f44edc26183b5d8b2dff7191ee65e68e55ea7f8133e1b588be404db8c`.
- Reassembled `assets/huntress_puzzle.json` fragments using their destination
  positions, yielding `ANS-AD1CBF1D66373FA7`.
- Submitted under `answer` before the renewed deadline; Game Master returned
  `CORRECT` with completion flag `2f73dea4f251ad82f0c35b0360bc4acb`.

- The first bundle expired before submission. The renewed attempt was
  `5701c120-3645-416d-b75a-9b15407af11f` with deadline
  `2026-10-06T13:35:12.871Z`.
- Downloaded and verified all three renewed APKs, then used each file's
  `assets/huntress_puzzle.json` fragment positions to assemble its answer.

| Answer ID | Case and package | Assigned APK and SHA-256 | Accepted answer |
| --- | --- | --- | --- |
| `set1.answer` | `MOB-05-DFFBEAF93A` · `com.huntress.mobile.d05.vdffbeaf93a68` | delivery 1 (source reference: `backup_spill_mastery_01.apk`; not linked in this draft) · `768fa966c536a9ea648773cf054330c28db4f9c73af34cdaeec4d214e7d522db` | `ANS-398BF0E4C7421F41` |
| `set2.answer` | `MOB-05-9229AB2583` · `com.huntress.mobile.d05.v9229ab258374` | delivery 2 (source reference: `backup_spill_mastery_02.apk`; not linked in this draft) · `b26eb8ed97d604f351e010825151e8a5391580db230ad4083581a45958a1166f` | `ANS-151E79107F2B75ED` |
| `set3.answer` | `MOB-05-50CB5CDC9F` · `com.huntress.mobile.d05.v50cb5cdc9fe7` | delivery 3 (source reference: `backup_spill_mastery_03.apk`; not linked in this draft) · `489b632cbea74b15aabba7ff8a28e3acfcd6f2e7fbfb152f97b21914222b5a22` | `ANS-C325BF2DEBDA1C24` |

The Game Master returned `CORRECT` and completion flag
`19550bae5aac44a085968f843b253bca`.

## Retained sources

- [early/05-Backup_Spill/readme.md](../../source-notes/early/05-Backup_Spill/readme.md)
