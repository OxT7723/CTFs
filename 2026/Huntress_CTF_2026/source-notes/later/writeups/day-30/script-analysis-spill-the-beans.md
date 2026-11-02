> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Day 30 Script Analysis: Spill the Beans

All three available regular modes completed with Game Master status `CORRECT`.
The maintained `script-analysis-tools/run_modes.py` runner downloaded and
verified each assigned artifact, built answers from the extracted bytes, and
confirmed zero unresolved answer IDs.

| Mode | Attempt ID | Accepted | Artifact SHA-256 |
| --- | --- | ---: | --- |
| Single Solve | `fec836f2-7203-4559-bf18-6e2d35727d25` | 1,802/1,802 | `7b6e455789ef2017acb3c5a100eb16c78cf5840ba0fe5fb83fb1e3b5e4fceaab` |
| Time Trial (regular) | `50266abf-0c03-477c-a5fe-5f2ff57f1042` | 1,898/1,898 | `077cee17534ee083e30c7268e2a92d09aa035079bde36bbbac62af268369337d` |
| Mastery (regular) | `99052902-33d5-4a1a-a7c1-809fb52ec172` | 26,572/26,572 | `df493174a517cbe041f4f52bf448fc66b174edee8cea7bc6962402dfc206c875` |

The final filtered Game Master list marked all three modes solved. Its
responses did not include a CourseStack points total or scoring-status field,
and no response reported `pending`. The existing solver logic was correct;
timed-mode performance optimizations are recorded below.

## Ranked timed runs

Each run returned `CORRECT` and was Hall of Fame eligible. Saved artifact
hashes were checked after the run so hashing did not use the server deadline.

| Mode / run | Attempt ID | Accepted | Full client time | Artifact SHA-256 |
| --- | --- | ---: | ---: | --- |
| Time Trial 1/5 | `7a943095-e23e-411a-bc0e-5d907e6a62e3` | 1,898/1,898 | 3.72 s | `5a1c4c2691c00481769fe326f63363a988e6f89c100c139e1cdf807034dd2924` |
| Time Trial 2/5 | `e3491ce0-1d06-42fd-a6a7-e252da299799` | 1,898/1,898 | 2.91 s | `6c6bf0873438a4c89e3f6252221735f9a0ae8a6e5e5b506442257fcf09b5cb3f` |
| Time Trial 3/5 | `16e15241-459d-4761-a166-59b2c1bc424c` | 1,898/1,898 | 3.31 s | `8ae02e6dece5dcae3d836836dac3c5479aed9025da5d4590c45099810b530d4d` |
| Time Trial 4/5 | `94ada8b4-46f6-4964-aa6b-c411f933f0da` | 1,898/1,898 | 3.23 s | `46c6f541d0334e2eae545eabd77825b9a772fcd054cbef24f724fcbb7eeb662c` |
| Time Trial 5/5 | `2a0e4422-fe0a-493f-90b9-74b8bf996ad2` | 1,898/1,898 | 2.98 s | `5ead71198cab0348ad92cc6f32fff8e7ace191a3c8fc4ff0241c60c599d1f627` |
| Mastery 1/5 | `27bbd159-afe7-43c7-87e8-dc3c2f1020d5` | 26,572/26,572 | 22.75 s | `4295a04aabe6d436fa21b78ba9a473e7c55a482e4cab337b013d18e4949ea0d4` |
| Mastery 2/5 | `c68a3d4f-531f-479e-b696-ac463b3ba4b4` | 26,572/26,572 | 24.19 s | `d0aee81efe27b49df702fd3383d2e2e52841b2967779079dfa3f7c5edbc41e4e` |
| Mastery 3/5 | `80433656-c41a-4730-9d31-d71ce00bdb35` | 26,572/26,572 | 21.47 s | `41a27d23d39fb6895bf6c627846bd1a970a71888f47bd653954552c11589f233` |
| Mastery 4/5 | `552c3f30-a794-4008-8448-d1561e66c885` | 26,572/26,572 | 21.69 s | `b77df1a5fa8a771df382675dd8beeb372caaceb2b5350e1db77903cf1b4ea608` |
| Mastery 5/5 | `bc06ef19-538f-4549-80f1-11e5fcf96b06` | 26,572/26,572 | 21.95 s | `487f61b7d25b3a9d6fb84291192e2b3f4310beed46a2a98916e144e4629c39a0` |
| Mastery cache-only check | `ac9306e4-d5c1-4974-a264-d133fcec8d6d` | 26,572/26,572 | 25.37 s | `b933db747a0cbf4959c67b4f374bced48e6e6725909ce8911ac33f13e020a2b8` |
| Mastery in-memory check | `25056b4e-18c2-4aa6-9711-a16a7bbd1c9c` | 26,572/26,572 | 18.06 s | `637ffbaabb5ccc8399b2879d4bf3122aa949d5c42e1303ab29c1a1cf847a0ba5` |

The full client time includes request setup and a status poll after submission.
The optimized run's artifact download, processing, and submit stages totaled
10.70 seconds, versus the previous fastest 13.04 seconds across the first five
Mastery runs. The Hall of Fame UI is the source for its recorded time; the Game
Master status response confirms correctness and Hall of Fame eligibility but
does not return that time.

The answer builder's profiled time fell from 4.22 to 2.42 seconds after caching
specimen contents and classifiers. The in-memory ZIP path then decoded and
solved all 26,572 answers in 6.72 seconds offline; the live run's processing
stage took 6.94 seconds. All generated answers matched the accepted run.
