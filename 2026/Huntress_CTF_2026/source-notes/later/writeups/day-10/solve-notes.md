> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 10 solve notes

All four in-scope challenges are accepted in Single Solve, Time Trial, and
Mastery. Bind Over Matter was skipped as requested. The Game Master contracts,
attempt records, candidate maps, and receipts are saved here:

- `completion-index.json` — all 12 accepted mode results, flags, assigned file
  links, hashes, and references to the raw API responses.
- `single-responses/` — player-facing Single Solve contracts and status.
- `runs/` — timed and mastery attempt records, including the exact questions,
  answer IDs, artifact manifests, submissions, and statuses.
- `solve_artifact.py` — artifact-driven solver and proxy runner.
- `requirements.txt` — AES ZIP support for the supplied encrypted evidence.

## Completion

| Challenge | Single Solve | Time Trial | Mastery |
| --- | --- | --- | --- |
| Thirty-Two Below | CORRECT | CORRECT | CORRECT |
| Where Do We Begin? | CORRECT | CORRECT | CORRECT |
| Zig Zag | CORRECT | CORRECT | CORRECT |
| Network Config Split | CORRECT | CORRECT | CORRECT |

`completion-index.json` records each accepted flag and its attempt. The raw
Game Master response files below retain the full player-facing prompt,
questions, answer formats, answer IDs, deadlines, and artifact metadata.

### Raw challenge contracts

- Thirty-Two Below: Single Solve (historical reference: `single-responses/warmups-day-10.json`; not included),
  Time Trial (historical reference: `runs/warmups-day-10/time_trial/4784035e-65e7-4a07-9123-dae94942ad9a/start-response.json`; not included),
  Mastery (historical reference: `runs/warmups-day-10/mastery/84e2bedd-d5bb-47f0-bc7b-77d47faf217a/start-response.json`; not included).
- Where Do We Begin?: Single Solve (historical reference: `single-responses/metadata-forensics-day-10-where-do-we-begin.json`; not included),
  Time Trial (historical reference: `runs/metadata-forensics-day-10-where-do-we-begin/time_trial/001e03f2-fbbc-44d4-8609-dfb0d5e9ac61/start-response.json`; not included),
  Mastery (historical reference: `runs/metadata-forensics-day-10-where-do-we-begin/mastery/e3ab0e4a-5e7e-423d-bdd6-d7a78d238a55/start-response.json`; not included).
- Zig Zag: Single Solve (historical reference: `zig-start.json`; not included),
  Time Trial (historical reference: `runs/binary-reverse-engineering-day-10-zig-cross-platform-services/time_trial/c3fdf96e-1e37-4c5a-9e52-318bef384502/start-response.json`; not included),
  Mastery (historical reference: `runs/binary-reverse-engineering-day-10-zig-cross-platform-services/mastery/1cbab494-d4c7-46b9-b965-3f5192954b6c/start-response.json`; not included).
- Network Config Split: Single Solve (historical reference: `single-responses/mobile-android-day-10-network-config-split.json`; not included),
  Time Trial (historical reference: `runs/mobile-android-day-10-network-config-split/time_trial/b9fed180-5d94-4939-a853-a00ceb0fbb50/start-response.json`; not included),
  Mastery (historical reference: `runs/mobile-android-day-10-network-config-split/mastery/21750c87-7f1a-4572-9bd9-d869e7228e65/start-response.json`; not included).

## Challenge notes

### Thirty-Two Below

ID: `warmups-day-10`

Prompt: “Same neighborhood. Smaller alphabet.”

The Single Solve asks for the slug on the final non-empty line after decoding
`blob.txt`. Its answer ID is `message`; the API format is three lowercase
words separated by hyphens, followed by a hyphen and a two-digit number.
Mastery contains 48 independent blobs. Each blob has numbered encoded chunks;
the solver decodes each chunk by its encoding, joins the text, and extracts
the final slug.

### Where Do We Begin?

ID: `metadata-forensics-day-10-where-do-we-begin`

Prompt: “Architecture tells you whether a binary can run; its entry point
tells you where execution begins. Map the start addresses and catch the report
that is lying.”

The Single Solve asks for `pe.address_of_entry_point_rva_hex` in
`telemetry-agent-001.exe`. Its answer ID is
`d09-pe-001-pe-address-of-entry-point-rva-hex`; submit lowercase hexadecimal
with a `0x` prefix and eight digits. The solver follows each question’s
artifact descriptor into nested ZIP files, reads the PE optional header, and
preserves that fixed-width representation. Mastery uses multiple executables
inside nested evidence archives.

The reusable Metadata Forensics toolkit is in
[`metadata-forensics-tools`](../../../../tools/later/metadata-forensics-tools/README.md).

### Zig Zag

ID: `binary-reverse-engineering-day-10-zig-cross-platform-services`

Prompt: “Zig promises one binary for every platform. Compare the ELF and PE
service descriptors side by side and prove they're the same program wearing
different uniforms.”

The Single Solve and Time Trial each return 100 questions; Mastery returns
three 100-question sets. The exact question text, formats, and answer IDs are
in the saved Game Master response files linked from `completion-index.json`.
The evidence ZIP uses the supplied password `infected`.

The solver reads hashes and ELF/PE/JAR metadata from the delivered bytes,
recovers HCFG configuration records by XOR decoding and CRC32 validation, and
reads PE COFF symbols and section tables where needed. ZIP compression
methods include directory entries as well as files; the two JAR method arrays
therefore include both method `0` and method `8`.

### Network Config Split

ID: `mobile-android-day-10-network-config-split`

Prompt: “Diff manifest and Network Security Config variants to locate the
true transport exception.”

The Single Solve asks for the exact backend answer code for its assigned case.
Its answer ID is `answer`; the format is `ANS-` followed by 16 uppercase
hexadecimal characters. The solver reads the split `parts` and `order` arrays
from the APK asset and restores the code. Mastery assigns three separate APKs;
the runner downloads every API-listed delivery by its index and keeps files
with duplicate names in separate folders.

## Reuse

Install the optional AES ZIP reader:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Set `GAME_MASTER_PROXY_URL` to the supported Game Master proxy and pass the
challenge ID returned by the current list response:

```sh
GAME_MASTER_PROXY_URL="$PROXY_URL" \
  .venv/bin/python solve_artifact.py "$CHALLENGE_ID" --output attempt-records
```

For a bundle with many answers, add `--reconcile` to submit one logical group
at a time and split only groups the service rejects. Use `--retry` after an
attempt ends. The runner gets artifact names, delivery indexes, hashes,
questions, and answer IDs from each live start response; it does not store
campaign IDs, URLs, artifact filenames, or expected answers.

## Accepted artifacts

Each link below is the exact root-relative download path from its successful
Game Master response. The SHA-256 is for the assigned bytes.

| Challenge | Mode | File and purpose | Download | SHA-256 |
| --- | --- | --- | --- | --- |
| Zig Zag | single_solve | `evidence.zip` — Password-protected evidence archive with ELF, PE, and JAR service samples. | evidence.zip (retired artifact link; see artifact inventory) | `9c31fb3a95b866cc9984b7db740db1a36e9f59fc7ecb924f8dc497cae2b11fc4` |
| Zig Zag | time_trial | `evidence.zip` — Password-protected evidence archive with ELF, PE, and JAR service samples. | evidence.zip (retired artifact link; see artifact inventory) | `36f88f34b8e3ebbc96ebf437d1fe6c7272af58bdc1e6c1cce7e125f7ae7814ea` |
| Zig Zag | mastery | `evidence.zip` — Password-protected evidence archive with ELF, PE, and JAR service samples. | evidence.zip (retired artifact link; see artifact inventory) | `ec0fe604f34848578df4b0452bd2cb441b1fa8fe8f7b2c994d7a6bb386d755f9` |
| Zig Zag | mastery | `evidence.zip` — Password-protected evidence archive with ELF, PE, and JAR service samples. | evidence.zip (retired artifact link; see artifact inventory) | `04e550bab09c1b45f2322734c3314940d5906fea0e3508b9507a2608d8abd790` |
| Zig Zag | mastery | `evidence.zip` — Password-protected evidence archive with ELF, PE, and JAR service samples. | evidence.zip (retired artifact link; see artifact inventory) | `63ebce0eea94e3d01dd998738979082e4d7d1b47f0fd70c90ca73e3f7265de87` |
| Where Do We Begin? | single_solve | `metadata-day-10-evidence.zip` — PE evidence archive containing the executable named by each question. | metadata-day-10-evidence.zip (retired artifact link; see artifact inventory) | `75db7f473673d7f55503920cbcd4a9945b44e3a9705c4cd62248975469ea3407` |
| Where Do We Begin? | time_trial | `metadata-day-10-evidence.zip` — PE evidence archive containing the executable named by each question. | metadata-day-10-evidence.zip (retired artifact link; see artifact inventory) | `584b3418ad398e76530600a9de9ed6ec7d2dd72eceb3aa2ce0ccebd842d4415c` |
| Where Do We Begin? | mastery | `metadata-forensics-day-10-where-do-we-begin-mastery.zip` — PE evidence archive containing the executable named by each question. | metadata-forensics-day-10-where-do-we-begin-mastery.zip (retired artifact link; see artifact inventory) | `6bfcf7e9338bc4f30f35f76afa68e1ca17c5aebfc2662509c4bcbe69b849a063` |
| Network Config Split | single_solve | `network_config_split.apk` — Assigned Android APK with manifest, Network Security Config, and split answer data. | network_config_split.apk (retired artifact link; see artifact inventory) | `c4a967db659bb471bbd939b41eb97baf96e7bc8c10f8deaed0e9927522ce3a59` |
| Network Config Split | time_trial | `network_config_split_time_trial.apk` — Assigned Android APK with manifest, Network Security Config, and split answer data. | network_config_split_time_trial.apk (retired artifact link; see artifact inventory) | `a0f02c6f96eb455d3aa04ff00e4b44f14f7e5b71c245eb904e2fd98901260ebc` |
| Network Config Split | mastery | `network_config_split_mastery_01.apk` — Assigned Android APK with manifest, Network Security Config, and split answer data. | network_config_split_mastery_01.apk (retired artifact link; see artifact inventory) | `bdf12ff525466f49b03afffea065956546007d3e42744d071561f39106aae0db` |
| Network Config Split | mastery | `network_config_split_mastery_02.apk` — Assigned Android APK with manifest, Network Security Config, and split answer data. | network_config_split_mastery_02.apk (retired artifact link; see artifact inventory) | `11f583de7d06e4205920a8c7bf55c91ecbb33936f0f28ffe7bd51afb6326bb8a` |
| Network Config Split | mastery | `network_config_split_mastery_03.apk` — Assigned Android APK with manifest, Network Security Config, and split answer data. | network_config_split_mastery_03.apk (retired artifact link; see artifact inventory) | `46e179a865d69bb482778d33d70a632c47c9bfe9be90744446b1887abd882b6b` |
| Thirty-Two Below | single_solve | `blob.txt` — Assigned encoded warmup text. | blob.txt (retired artifact link; see artifact inventory) | `8c4573345e8701b7750ce670d10c3330ea15710c859a9c0598f9f36d0344e0e5` |
| Thirty-Two Below | time_trial | `blob.txt` — Assigned encoded warmup text. | blob.txt (retired artifact link; see artifact inventory) | `41c138bbbbb8e3d246f397c9bdc8149f74ce9029c068a4dbbd03a8080d3afb09` |
| Thirty-Two Below | mastery | `warmups-day-10-mastery.zip` — Encoded warmup text; Mastery bundles independent blobs. | warmups-day-10-mastery.zip (retired artifact link; see artifact inventory) | `b8ca3bfe041f74e51e04bbc1168fe089cb63ccbb5ece658c1b74b073b45b3291` |
