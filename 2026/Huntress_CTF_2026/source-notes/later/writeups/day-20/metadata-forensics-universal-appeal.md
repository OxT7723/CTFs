> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 20 Metadata Forensics — Universal Appeal

## Results

All three modes returned `CORRECT`; the status endpoint reported every answer accepted. All were regular, untimed attempts (`run_for_time: false` for the timed modes), with no deadline or pending scoring status.

| Mode | Attempt | Accepted |
| --- | --- | --- |
| Single Solve | `00ac39bb-1963-44f9-8acf-8e5aef330a3d` | 1 / 1 |
| Time Trial | `53554fc3-646c-4f10-b279-27c9a0e79690` | 25 / 25 |
| Mastery | `2bb93f02-4e07-4a65-b112-490d56a7f08a` | 125 / 125 |

## Assigned artifacts

- Single Solve: Download metadata-day-20-evidence.zip (retired artifact link; see artifact inventory) — SHA-256 `ebabe0728645387e69ea7547e33f9fea1d2c867358429112398487e598167360`.
- Time Trial: Download evidence.zip (retired artifact link; see artifact inventory) — SHA-256 `fdd06df803d76e06c330815280b6615db05e953443efa4981728c9c273d45cec`.
- Mastery: Download metadata-forensics-day-20-universal-appeal-mastery.zip (retired artifact link; see artifact inventory) — SHA-256 `cc4842a049ff29b8bed57887aeb55cee122f86f024104a5fcd43f6eb5a67846f`.

## Solver update

Added `macho_metadata.py` and wired it into `run_challenge.py` for thin and fat Mach-O files and ar archives. CPU types are returned as distinct, sorted, zero-padded hexadecimal strings. The assigned thin ARM64 sample has `cputype` `0x0100000c`; the accepted answer was `["0x0100000c"]`.
