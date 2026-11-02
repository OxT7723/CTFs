> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Metadata Forensics helpers

This folder contains reusable metadata readers and a Game Master runner. The
runner takes the challenge ID from the command line, uses the live start
response for its questions and artifact descriptors, extracts nested archives
in memory, builds answers from downloaded bytes, and saves the start,
candidate, submission, and status records under the attempt ID.

Day 1 challenge notes and measured replay results:
[You Must Be This Hash to Ride](../../../source-notes/later/writeups/day-01/metadata-forensics-you-must-be-this-hash-to-ride.md).

Install the optional readers in this folder's virtual environment:

```sh
python3 -m venv metadata-forensics-tools/.venv
metadata-forensics-tools/.venv/bin/python -m pip install -r metadata-forensics-tools/requirements.txt
```

## PE parser

Read PE headers without relying on filenames or a fixed campaign:

```sh
python3 metadata-forensics-tools/pe_metadata.py path/to/input.exe
```

The output includes the entry point RVA, optional-header type, machine value,
section count, and image base. Add `--version-info` to include PE
`VERSIONINFO` string values such as `OriginalFilename`. The module helper also
reads a managed PE assembly's Module Version ID (MVID) from its CLR metadata.

## Game Master runner

Set `GAME_MASTER_PROXY_URL` to the supported proxy URL, then pass the challenge
ID from the current Game Master response:

```sh
GAME_MASTER_PROXY_URL="$PROXY_URL" \
  metadata-forensics-tools/.venv/bin/python metadata-forensics-tools/run_challenge.py "$CHALLENGE_ID"
```

Use `--retry` only after the current attempt has ended. Records are written
under `attempt-records/<challenge-id>/<attempt-id>/`.

The answer builder currently handles Android APK package names through
Android build-tools `aapt`; Windows Installer ProductCode and UpgradeCode
values, ProductVersion, ProductName, Manufacturer, package code, and template
fields through the system `msiinfo` command; managed assembly
MVIDs, PE entry point and machine fields; ZIP EOCD fields and central-directory
names; OOXML external relationship targets from DOCX packages; file size,
hashes, magic prefixes, and UTF-8 BOM checks; JPEG and PNG dimensions; PDF
header versions; primary video stream dimensions through `ffprobe` or MediaInfo;
and Windows Shell Link target paths through `pylnk3`. Targets
come from each question's artifact chain, including nested ZIP files. Primary
audio codec names use `ffprobe` when installed; otherwise the runner uses
MediaInfo and maps common codec names. The fallback requires the `mediainfo`
command. Mach-O CPU type sets are read from thin and universal binaries and
ar archives; values use sorted, zero-padded hexadecimal strings. Encrypted
ZIP members, including WinZip AES archives, are read with the event-provided
`infected` password.

Compressed Windows Prefetch (`.pf`) files are unwrapped from their MAM
XPRESS-Huffman container and the executable name is read from the Prefetch
header using `dissect.util`.

Classic PCAP captures are parsed from their global and per-packet headers.
Snap-length-truncated packets count as records; structurally truncated or
invalid records are rejected.

Raw MBR and GPT disk images are parsed by `disk_metadata.py` for ordered
partition-start LBA sequences. GPT entry order is preserved, MBR extended
containers are excluded, and their logical partitions are included.

Java archive `Main-Class` values are read from the main section of
`META-INF/MANIFEST.MF`. Android APK package names use `aapt dump badging`;
APK question support requires the Android Asset Packaging Tool to be installed.

MSI question support requires `msiinfo` from msitools to be installed on the
system.

EVTX record counts are read with `python-evtx`; install it from the requirements
file before running challenges that ask about Windows event logs.

Registry hive root key names are read from the REGF base block and root NK cell.

Check the live route before starting a timed attempt. On opt-in routes, use
`--run-for-time`; on legacy timed-by-default routes, `--retry` starts the
ranked attempt without that option. `--retry` advances to a new assignment
after the current attempt ends, so do not use it as an availability probe.
For an opt-in route, a deliberate ranked retry looks like:

```sh
GAME_MASTER_PROXY_URL="$PROXY_URL" \
  metadata-forensics-tools/.venv/bin/python metadata-forensics-tools/run_challenge.py "$CHALLENGE_ID" --retry --run-for-time
```

The runner treats a server deadline as a timed attempt even on legacy routes,
reuses one HTTP connection for the start, artifact, and submission requests,
and skips optional outer-artifact hashing on that speed-critical path. On an
ended legacy attempt, `--warm-connection` checks status before retry, confirms
there is no active deadline or pending score, and uses that request to warm
the connection. Add `--profile` to report request and local processing times
after completion.

The runner verifies that candidate answer IDs exactly match the live response.
After submission, inspect the saved status and its `accepted_ids`; an aggregate
incorrect result does not establish that every answer was rejected.
