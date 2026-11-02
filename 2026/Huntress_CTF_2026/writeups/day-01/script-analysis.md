# Power Play

Day 1 · Script analysis · **Investigation record**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `script-analysis-day-01-native-signals`.

## The task

Three PowerShell specimens represented resource hijacking, synthetic browser-data collection, and synthetic file impact. The task asked for each script’s scenario, primary ATT&CK technique, and exact embedded indicators. Single Solve and Time Trial each asked for 15 fields; the recorded Mastery bundle used two sets and 30 prefixed fields.

The useful first observation was that the data was embedded as Base64-encoded JSON. These fixtures could be inspected and decoded as data without running the PowerShell.

## Inspecting the specimens

The early notes first checked file types and searched for recognizable API calls, URLs, wallet strings, mutex names, and filenames. The saved extraction loop was:

```bash
for f in *.ps1; do
    grep -oP "FromBase64String\('\K[^']+" "$f" \
      | base64 -d \
      | jq
done
```

This command assumes the recorded single-quoted `FromBase64String('...')` shape and one matching payload per specimen. It is an example from these samples, not a general PowerShell deobfuscator. The reusable [script-analysis tooling](../../tools/later/script-analysis-tools/README.md) handles the broader challenge family.

The decoded resource record contained an exact URL, wallet, and mutex. The collection record contained a URL, a filename list, and a user-agent. The impact record supplied a file extension, recovery-note name, and URL.

## Mapping decoded data to the questions

The submitted mapping from the early Single Solve account included:

| Specimen | Scenario | ATT&CK value used | Key artifact-derived indicators |
| --- | --- | --- | --- |
| `resource-sample.ps1` | `resource_hijacking` | `T1496` | Wallet, download URL, mutex |
| `collection-sample.ps1` | `synthetic_collection` | `T1555.003` | First requested filename, URL, user-agent |
| `impact-sample.ps1` | `synthetic_impact` | `T1486` | Target extension, recovery-note filename, URL |

For the recorded resource sample, the values were:

```json
{
  "resource-scenario": "resource_hijacking",
  "resource-attack": "T1496",
  "resource-url": "https://cdn-03ce326948.example.invalid/3e59094b24e2.bin",
  "resource-wallet": "wallet_d327bc1114a907589af81bba71226b77",
  "resource-mutex": "Global\\HuntressLab_6460b4f6aa72"
}
```

Those values belong to that artifact instance. A new assignment could use different indicators even when the same parser and classification rules applied.

The later question contract gave an extra clarification for the collection specimen: browser credential-store access was the central behavior for the ATT&CK field, and the broader Data from Local System technique was also accepted. This is a useful example of why the exact current question text mattered as much as the filename or a generic behavior label.

## Submission and recorded result

The answer object used the **exact Game Master question IDs**. The decoded values were submitted as JSON, with the mutex backslash escaped for JSON transport. The early account retains a `CORRECT` response and the returned completion flag.

The later account separately records assigned artifact hashes, solver changes, training runs, and ranked attempts. Those timing and mode details remain in the linked source notes. They are historical observations; the challenge was not rerun during preparation of this collection.

## What this example shows

The main skill was translating evidence into a strict answer contract: identify the embedded representation, decode it without executing the specimen, connect the observed behavior to the requested classification, and submit literal artifact-derived values under the right IDs. A parser could accelerate the repetitive extraction, while the question wording still determined which value counted as the answer.

## Retained sources

- [early/01-Power_Play/readme.md](../../source-notes/early/01-Power_Play/readme.md)
- [later/writeups/day-01/script-analysis-power-play.md](../../source-notes/later/writeups/day-01/script-analysis-power-play.md)
