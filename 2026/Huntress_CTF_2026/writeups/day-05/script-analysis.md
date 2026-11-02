# Hatch Careful

Day 5 · Script analysis · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `script-analysis-day-05-python-carrier-lab`

## Earlier local account

---

All three modes are complete. The Game Master returned `CORRECT` for Single Solve (357 answer IDs), Time Trial (357), and Mastery (714). The final timed attempts are documented below; every exact indicator came from that attempt's assigned bytes. Earlier timed attempts and their outcomes remain in `challenge_state.json` for history.

| Mode | Successful attempt | Assigned archive SHA-256 |
| --- | --- | --- |
| Single Solve | `a77c2af6-ecd5-45e3-854c-c1376df87086` | `0ad1ebe9953e7dde6d4ecdc54d7e4309d7547c9c7cb2bc842f51f4156169a599` |
| Time Trial | `ac0d73f6-ff32-4fe3-b1b3-73d4d0c78d5d` | `456d035b0876474398952fefea10ce2fdaa80b2f13469517a17859bd1a71dcce` |
| Mastery, set 1 | `275c007c-9153-4055-8701-3eaaa9eee629` | `8b5eaa5d19cb1079bcf92e1f447b8524d5a0c6500cba38c069b7ddca4e0b64b4` |
| Mastery, set 2 | same attempt | `f199c7b83bbd2b8bc1d3bb064f07ebe41eb1d246354a7cdd0d2809cb43bf296f` |

The successful ZIPs are in `artifacts/{single_solve,time_trial,mastery}`. `answers.json` beside each timed attempt is the answer map derived from its assigned archive. The archives use the password `infected`. The Time Trial and Mastery clocks were seven seconds; their final status is `CORRECT`, so those clocks are no longer running.

1. Download the current attempt's archive through the authenticated Game Master response and verify its SHA-256. Extract ZIP entries with `7z x -pinfected`. Mastery has two independent evidence sets; the start response can provide an outer ZIP while a retry can provide two direct downloads. Map `set1.*` answers only to `evidence-01.zip`, and `set2.*` only to `evidence-02.zip`.
2. Build the answer map from the extracted files without importing or executing any specimen. `tools/static_recover.py` reads literal Python `MATERIAL_*` and `CODEC_*` assignments with `ast`, then reverses the declared encoding and byte transform. It statically decodes JScript payloads from string or integer-array material, VBScript `Material_*`/`Codec_*` constants, and Batch `:HUNTRESS_INSPECT` fragments. The PowerShell samples carry base64-encoded JSON descriptors.
3. Split each recovered descriptor on `|` and its fields on the first `=`. Copy exact values such as `campaign_id`, URL, path, adapter, next stage, and carrier profile from that decoded data. Determine role and ATT&CK answers from the inert operation plan in each specimen. Read syntax/control labels from the source structure. `tools/solve_hatch.py` combines those values under the exact current `answer_ids`.
4. Batch expansion and control labels require particular care. Similar looking command files can validate different labels. The timed runners submit all other answers as one group, then submit Batch labels individually. On Mastery, `tools/run_mastery.py` first tries the likely labels and sends alternatives only for fields the Game Master rejects. It uses HTTP/2 to fit those requests within the server deadline. The final Mastery run accepted all 678 other fields and all 36 Batch labels.

For a concrete example, Mastery set 1's `wheel-recovered.py` declares `base64_literal|reverse_then_xor|ed`: base64-decode the literal, reverse the bytes, XOR each byte with `0xed`, then parse the resulting descriptor. Its visible operation plan references an HTTP client and memory handoff, supporting the `stager` role. The carrier and syntax answers are separate fields, so a package's format does not by itself determine its behavior.

```text
7z x -pinfected artifacts/single_solve/evidence.zip -oartifacts/single_solve/extracted
python 05-Hatch_Careful/tools/solve_hatch.py --unconfirmed-only
python 05-Hatch_Careful/tools/run_time_trial.py
python 05-Hatch_Careful/tools/run_mastery.py
```

The timed runners check live status first and return `already_solved` for completed modes, so rerunning them now does not start another timer. They read `HUNTRESS_GM_TOKEN` from the environment and never write its value to the repository. Successful attempt ZIPs, answer maps, submission verdicts, and Game Master responses are retained; extracted timed trees were removed because the ZIPs reproduce them.

- Derive per-attempt indicators from the downloaded bytes. Retries can receive new material even when the question IDs stay the same.
- Keep role and ATT&CK classification separate from the superficial Python carrier or package name.
- Preserve each submission verdict by answer ID. A single bulk `incorrect` result cannot identify the bad field; targeted Batch probes found the remaining labels.
- HTTP 429 and expiration were observed on earlier rapid timed attempts. The final attempts were confirmed by a live `CORRECT` status, without assuming CourseStack points from the Game Master response alone.

## Retained sources

- [early/05-Hatch_Careful/readme.md](../../source-notes/early/05-Hatch_Careful/readme.md)
