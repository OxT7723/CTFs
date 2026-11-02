> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Huntress CTF Day 4 progress and handoff

Saved on 2026-10-04 from the current Homebase session. The live Game Master proxy is:

```text
http://192.0.2.1/huntress-ctf-proxy
```

The player requested this order for each challenge: finish Single Solve, then Time Trial, then Mastery. If one challenge stalls, switch to another unsolved challenge and come back later. Never execute the supplied specimens; solve from the downloaded bytes and submit under the exact `answer_ids` returned by the Game Master.

## Accepted challenge modes

### Two of a Kind — `warmups-day-04`

- Single Solve accepted. Submitted `witty-starfish-turtle-96`; flag `1897a15ec6928f5bd072406766afe671`.
- Time Trial accepted. The accepted retry artifact decoded to `clever-quilt-maple-12`; flag `975acaa32623345deb3a894e48922dfd`.
- Mastery accepted (18 blobs). Flag `2cc26d2ca7d0f0b2f514e7e4ef3583ff`.

  The accepted mastery answers, in set order, were:

  1. `quick-daisy-trail-34`
  2. `eager-starfish-nugget-19`
  3. `handy-forest-badger-10`
  4. `spiffy-rainbow-copper-63`
  5. `peppy-summit-butter-41`
  6. `clever-chimney-pebble-32`
  7. `calm-banner-lagoon-82`
  8. `dashing-rainbow-ripple-55`
  9. `nimble-coral-juniper-13`
  10. `lucky-rocket-brook-80`
  11. `proud-valley-maple-71`
  12. `merry-comet-harbor-28`
  13. `brisk-quilt-wagon-27`
  14. `speedy-compass-ember-85`
  15. `sturdy-meadow-laurel-17`
  16. `bright-forest-bridge-63`
  17. `calm-island-pebble-88`
  18. `lucky-lantern-nugget-92`

### Picture This — `metadata-forensics-day-04-picture-this`

- Single Solve accepted. Submitted `257x146`; flag `5d2023e604b30c1bc092427997bb9de7`.
- Time Trial accepted. Assigned `camera-002.jpg` SOF dimensions were `274x157`; flag `45c7fc2beb82ecd69b15b427aa4733c5`.
- Mastery accepted. Set 1 (`camera-003.jpg`) was `291x168`; set 2 (`camera-004.jpg`) was `308x179`; flag `4dbb304712ec2fc4a674c8e43287d1b8`.

### Pending Intent Relay — `mobile-android-day-04-pending-intent-relay`

- Single Solve accepted. Decoded code `ANS-60A1CA8E89978462`; flag `41b96982d7bd475944cc0eb59913c95f`.
- Time Trial accepted. The accepted retry APK decoded to `ANS-0A397F20453561C8`; flag `1c0af898920e6325b6583fee5d07e88b`.
- Mastery accepted (3 APKs). In set order:
  - `ANS-B9B5B032D37CA13C`
  - `ANS-49982616535AB843`
  - `ANS-0B16898E1B56C917`

  Flag: `f6064998b195fa2a3c5a623a55d8e93b`.

  APKs were analyzed statically. The asset `assets/huntress_puzzle.json` contains Base64 `data` and a numeric `key`; decode the Base64 and XOR each byte with `key`.

## Unfinished Single Solve work

### Dim and Dimmer — `script-analysis-day-04-shell-contrast`

Single Solve is active and partially solved. The evidence ZIP was downloaded and AES extracted with password `infected`:

- ZIP: `/tmp/script-analysis-day-04-evidence.zip`
- Extracted specimens: `/tmp/script-day-04-evidence/`
- Answer generation helper: `/tmp/build_day04_script_answers.py`
- Generated candidate answers: `/tmp/script-day-04-known-answers.json`
- Original start response/questions: `/tmp/script-day-04-start.json`

About 222 of 231 fields were accepted according to the preceding session state. The remaining fields recorded in the handoff are:

- Batch control flow: `batch-benign-control`, `batch-dropper-control`, `batch-launcher-control`
- VBScript control flow: `vbscript-stager-control`, `vbscript-downloader-control`, `vbscript-uploader-control`, `vbscript-launcher-control`, `vbscript-impact-control`, `vbscript-chain-control`

Already accepted control classifications include `select_case` for the VBScript benign, dropper, and relay specimens. The helper maps role to filenames; the VBScript specimens are in `/tmp/script-day-04-evidence/`. Specimens are inert evidence and must remain unexecuted.

Recent unsuccessful candidates:

- `vbscript-impact-control`: `while_wend`, `while_loop`
- A combined candidate submission tried `if_else`, `do_loop`, `if_do_loop`, `for_next`, `while_wend`, `if_do_loop` for the six unresolved VBScript fields; the service returned `incorrect`. Since that was a combined request, it did not identify which individual guesses were wrong.

Earlier session notes said these Batch controls were accepted: stager=`call_subroutine`, downloader=`call_subroutine`, uploader=`goto_dispatch`, impact=`call_subroutine`, chain=`call_subroutine`, relay=`goto_dispatch`. Remaining Batch controls still need classification from the source.

### Go Fish — `binary-reverse-engineering-day-04-go-runtime-fingerprints`

Single Solve is active and currently has two unresolved fields (the third was just accepted):

- Accepted `d01_analysis_symbols` with the ordered symbol-table names from `.symtab` (empty entries omitted).
- Still unresolved: `d01_analysis_disassembly`, `d03_analysis_format`.

Files:

- Start response and question formats: `/tmp/binary-day-04-start.json`
- Downloaded ZIP: `/tmp/go-fish-day-04.zip`
- Extracted artifacts: `/tmp/go-fish-day-04/`
- Current candidate answer map: `/tmp/go-fish-day-04-answers.json`

`d01--variant-000.elf` is ELF64 x86-64. `recover_code` at `0x401126` contains:

```text
mov eax, 0x1fa4
ret
```

Its `main` also loads `0x1fa4`, compares a local value to `0xff`, and conditionally clears `eax`. Several candidate JSON arrays for `d01_analysis_disassembly` were tried earlier without acceptance; inspect the question and disassembly output for the exact expected array shape before trying another.

`d03--variant-000.dll` is reported by `file` as `PE32 executable (console) Intel 80386 Mono/.Net assembly`; strings show metadata version `v4.0.30319`. The associated runtime config targets `net8.0`. The exact expected `d03_analysis_format` value remains unknown. Previously tried candidates include `PE32`, `pe32`, `PE`, `PE32 executable`, the full `file` description, `.NET`, `pei-i386`, and `dotnet`.

Other Day 4 fields for this Binary Single Solve were accepted, including D01 ELF class/machine/type/endianness/section names, D02 ELF/configuration, D03 hashes/machine/metadata/config, and D04 ELF/configuration.

## Timer and artifact workflow notes

The Game Master timers observed for timed modes are extremely short (about six seconds). Do not stop between start, artifact download, decoding, and submission. Keep the decode logic in one script and use the attempt’s live artifact.

Use the exact challenge mode ID, for example:

```text
warmups-day-04/time_trial
warmups-day-04/mastery
```

For each timed run:

1. Start or renew through POST to the proxy. If the server says `expired`, POST `{"op":"retry","challenge":"<mode-id>"}`.
2. Fetch assigned bytes through `GET ?op=artifact&challenge=<mode-id>`.
3. For a bundle, the live OpenAPI schema exposes `delivery`; zero-based delivery requests worked for 18 warmup blobs and 3 Android APKs. Parallel GETs are useful:

   ```text
   ?op=artifact&challenge=<mode-id>&delivery=0
   ```

4. Submit immediately with POST `{"challenge":"<mode-id>","answers":{"<exact-answer-id>":"<answer>"}}`.

Mastery artifact behavior varies by challenge. Warmup mastery was available as an 18-file ZIP, and its `delivery=0..17` responses were decoded concurrently. Mobile mastery artifacts were APKs at `delivery=0..2`. Metadata mastery’s default artifact response was an outer ZIP containing the two evidence ZIPs; each inner ZIP held its assigned JPEG.

The proxy’s OpenAPI document was saved at `/tmp/gm-openapi.json`. It shows query operations `openapi`, `list`, `status`, `artifact`, and `download`.

## Day 4 challenge IDs and order

1. Warmups: `warmups-day-04` — all three modes accepted.
2. Metadata Forensics: `metadata-forensics-day-04-picture-this` — all three modes accepted.
3. Script Analysis: `script-analysis-day-04-shell-contrast` — Single Solve incomplete; no timed modes started.
4. Binary: `binary-reverse-engineering-day-04-go-runtime-fingerprints` — Single Solve has two unresolved fields; no timed modes started.
5. Mobile Android: `mobile-android-day-04-pending-intent-relay` — all three modes accepted.

Continue using the per-challenge order. Finish Go Fish Single Solve, then its Time Trial and Mastery; return to Dim and Dimmer’s unresolved Single Solve and then its timed modes. Move on if either Single Solve stalls.
