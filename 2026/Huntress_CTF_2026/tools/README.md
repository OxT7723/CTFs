# Historical solver and analyzer source

The source is organized by workspace generation. Relative paths inside each generation are preserved where practical. The early generation contains challenge-specific solvers and sync helpers; the later generation contains shared category toolkits.

| Toolkit | Main reusable components |
| --- | --- |
| [Warmups](later/warmup-tools/README.md) | Layered and mixed-codec decoding, archive delivery handling, current-attempt answer preparation. |
| [Metadata forensics](later/metadata-forensics-tools/README.md) | PE, ELF, archive, APK, media, registry, disk, event log, certificate, and other format readers. |
| [Script analysis](later/script-analysis-tools/README.md) | Static decoding and extraction across challenge script families; earlier day-specific implementations retained in `archive/`. |
| [Binary reverse engineering](later/binary-reverse-engineering-tools/README.md) | Container metadata, symbol inspection, bounded configuration records, CRC validation, and multi-artifact answer mapping. |
| [Mobile Android](later/mobile-android-tools/README.md) | Manifest/DEX inspection and puzzle-asset codecs across APK/APKS assignments. |
| [Web exploitation](later/web-tools/README.md) | Challenge-specific inspection and solve routines for the event's assigned targets. |

## Execution boundary

These are historical event tools, not a tested standalone product. The Game Master runners can start attempts and submit answers. The web routines send requests and may change state on their assigned challenge targets. Use the code as a record of the event workflow; do not point it at unrelated systems.

The files include event-specific APIs, external tools, relative paths, and dependencies on artifacts and records not supplied in the archive. Python dependency lists are retained where present. External utilities referenced by the tools include `readelf`, `objdump`, `aapt`, `ffprobe`/MediaInfo, `msiinfo`, and archive utilities. Exact reproducible versions were not consistently recorded.

Private lab addresses have been replaced by the non-routable documentation example `192.0.2.1`. Scripts that accept `GAME_MASTER_PROXY_URL` or `HUNTRESS_GM_TOKEN` still read those values from the environment; no working credential is bundled. Original README commands generally assume the original workspace root. Here that is `tools/later/` or `tools/early/`, and missing specimen/state paths still need to be supplied independently.

Publication verification parsed all included Python files with Python's AST parser. It did not import them, execute them, exercise network operations, or verify their original dependencies and runtime behavior. The final package's validation summary records the count checked.

## SHA1-Hulud helpers

The files under `later/day-30/binary/fresh-sha1-hulud/analysis/` are the original Game AI investigation helpers. They are not the later successful custom C interpreter, `cipher_core.py`, or a complete executable-to-flag solver. The [later successful account](../source-notes/user-updates/sha1-hulud-web-pro-writeup.md) explains the missing harness and companion boundary. No executable, memory dump, or challenge ZIP is included here.
