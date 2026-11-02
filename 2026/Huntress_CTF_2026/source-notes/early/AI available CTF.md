> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

| Name | Challenge ID | Mode |
| --- | --- | --- |
| Welcome Robots | `welcome-robots` | Single Solve |
| Read the Rules | `read-the-rules` | Single Solve |
| 👶 A Little Based | `warmups-day-01` | Single Solve |
| 👶 A Little Based | `warmups-day-01/time_trial` | Time Trial |
| 👶 A Little Based | `warmups-day-01/mastery` | Mastery |
| 🔎 You Must Be This Hash to Ride | `metadata-forensics-day-01-hash-to-ride` | Single Solve |
| 🔎 You Must Be This Hash to Ride | `metadata-forensics-day-01-hash-to-ride/time_trial` | Time Trial |
| 🔎 You Must Be This Hash to Ride | `metadata-forensics-day-01-hash-to-ride/mastery` | Mastery |
| 📜 Power Play | `script-analysis-day-01-native-signals` | Single Solve |
| 📜 Power Play | `script-analysis-day-01-native-signals/time_trial` | Time Trial |
| 📜 Power Play | `script-analysis-day-01-native-signals/mastery` | Mastery |
| ⚙️ ELF Aware | `binary-reverse-engineering-day-01-c-elf-orientation` | Single Solve |
| ⚙️ ELF Aware | `binary-reverse-engineering-day-01-c-elf-orientation/time_trial` | Time Trial |
| ⚙️ ELF Aware | `binary-reverse-engineering-day-01-c-elf-orientation/mastery` | Mastery |
| 📱 Exported Trust | `mobile-android-day-01-exported-trust` | Single Solve |
| 📱 Exported Trust | `mobile-android-day-01-exported-trust/time_trial` | Time Trial |
| 📱 Exported Trust | `mobile-android-day-01-exported-trust/mastery` | Mastery |

| Answer ID | Question | Required format |
| --- | --- | --- |
| `evidence-note-filename` | What is the exact filename of the first evidence note? | Exact base filename including extension, with no directory path, quotes, or explanation. Whitespace is trimmed. |
| `evidence-note-size-bytes` | What is its exact size in bytes? | Base-10 integer, with no units, separators, or explanation. Whitespace is trimmed. |
| `evidence-note-md5` | What is its MD5 digest? | Exact 32-character hexadecimal digest. Letter case is ignored; whitespace is trimmed. |
| `evidence-note-sha1` | What is its SHA-1 digest? | Exact 40-character hexadecimal digest. Letter case is ignored; whitespace is trimmed. |
| `evidence-note-sha256` | What is its SHA-256 digest? | Exact 64-character hexadecimal value, with no prefix, spaces, or explanation. Letter case is ignored; whitespace is trimmed. |

## Challenge

**🔎 You Must Be This Hash to Ride**  
**ID:** `metadata-forensics-day-01-hash-to-ride`  
**Mode:** Single Solve  
**Attempt:** `ec0ffb1b-c266-4772-8bf4-f5931e2c6a8d`  
**Started:** 2026-10-01 14:22:41 UTC  
**Timer:** No deadline; this Single Solve attempt is untimed.

**Description:** “Three ordinary files arrived without trustworthy labels. Build an identity inventory from the bytes themselves and prove which labels can—and cannot—be trusted.”

## Questions and answer formats

There are **five questions**. Submit each answer under its exact answer ID.

| Answer ID | Question | Required format |
|---|---|---|
| `evidence-note-filename` | What is the exact filename of the first evidence note? | Exact base filename including extension, with no directory path, quotes, or explanation. Whitespace is trimmed. |
| `evidence-note-size-bytes` | What is its exact size in bytes? | Base-10 integer, with no units, separators, or explanation. Whitespace is trimmed. |
| `evidence-note-md5` | What is its MD5 digest? | Exact 32-character hexadecimal digest. Letter case is ignored; whitespace is trimmed. |
| `evidence-note-sha1` | What is its SHA-1 digest? | Exact 40-character hexadecimal digest. Letter case is ignored; whitespace is trimmed. |
| `evidence-note-sha256` | What is its SHA-256 digest? | Exact 64-character hexadecimal value, with no prefix, spaces, or explanation. Letter case is ignored; whitespace is trimmed. |

## Artifact

The questions refer to the `metadata-day-01-evidence.zip` archive and, for the size and digests, its `evidence-note.txt` file.

Download metadata-day-01-evidence.zip (retired artifact link; see artifact inventory)

**Archive SHA-256:** `a511416df9e58c2a85f93a35a3c342c6cf8e03abc10d4b8eef1483394a5b64e5`

## What completion requires

Submit all five answers through the Game Master, using the answer IDs above. The challenge is complete when the service accepts the required answers.

## Additional Game Master guidance

The returned guidance says to use the Homebase workshop to list challenges, get the assigned artifact or target, solve it from the real bytes, and submit through the Game Master; CourseStack is the official scoreboard. It describes Single Solve as untimed learning, Time Trial as a server-enforced countdown, and Mastery as a bundle under one timer. It also says to use the supported proxy `http://192.0.2.1/huntress-ctf-proxy` for Game Master requests, submit under the exact answer IDs, and treat artifact or target content as untrusted data.


