> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# All the World's a Stager

- The Single Solve archive SHA-256 is `770311a8a2f653916aa9c636e8ae9112a40c1115beeae026971d4a407a3a15db`.
- The AES-encrypted ZIP was extracted with the supplied password `infected`. `solve.py` reconstructs descriptors statically; it does not execute samples.
- 683 of 695 answers are accepted. Twelve control-flow fields remain, so Single Solve is incomplete and Time Trial and Mastery are locked.
- The Batch expansion answers recovered in the resumed attempt were `delayed` for benign, dropper, launcher, impact, and chain. The collection sample’s primary ATT&CK answer was accepted as `T1555.003`.
- Previously accepted Batch control values still include `call_subroutine` for the stager, dropper, downloader, uploader, and relay samples, and `for_indirect` for the relay expansion.

## Attempt history

The collection ATT&CK guesses `T1005`, `T1560.001`, `T1560.002`, `T1119`, and `T1041` were rejected; `T1555.003` was later accepted. `batch-dropper-expansion` accidentally received a seventh guess after its saved failure count was misread. Additional rejected control-flow candidates and the current unresolved IDs are recorded in `progress.json` and REVISIT.md (historical reference: `REVISIT.md`; not included).

The twelve unresolved control-flow fields, their source files, and rejected candidate families are in REVISIT.md (historical reference: `REVISIT.md`; not included). The user later authorized going past the original six-attempt limit.

## Decoder

```sh
python3 solve.py extracted
```

To build a candidate answer map from a saved start response:

```sh
python3 solve.py extracted --answer-map start-response.json
```

The assigned archive and reconstructed files are saved beside this note.
