# Prompt snapshots and reusable template

The seven files in [snapshots](snapshots/) are byte-for-byte copies of the final prompt files supplied in `ai prompt.zip`, with filenames normalized for navigation. Their contents have not been silently modernized. The [source manifest](../source-manifest.json) records matching input/output SHA-256 hashes.

| Snapshot | Assignment retained in original | Publication note |
| --- | --- | --- |
| [Warmups](snapshots/01-warmups.txt) | Day 30 | Retains the original rapid release polling text. |
| [Metadata forensics](snapshots/02-metadata-forensics.txt) | Day 31 | Uses `[Assigned Day]` in the surrounding instructions. |
| [Script analysis](snapshots/03-script-analysis.txt) | Day 31 | Preserves category-specific retry limits. |
| [Binary reverse engineering](snapshots/04-binary-reverse-engineering.txt) | Day 31 | Allows the lane-name variants recorded during the event. |
| [Mobile Android](snapshots/05-mobile-android.txt) | Day 31 | Keeps the original category wording. |
| [Web exploitation](snapshots/06-web-exploitation.txt) | Day 31, but release sentence says October 26 | This stale date is part of the saved prompt; it should not be reused unchanged. |
| [Review, training, and optimization](snapshots/09-review-training-optimization.md) | A previously completed challenge | Separates preparation from a limited, explicitly authorized ranked phase. |

The uploaded archives show earlier workflow instructions and later prompts, but do not contain a complete prompt-version timeline. This collection does not invent intermediate versions or dates.

The [cleaned daily template](daily-lane-template.md) is a new editorial adaptation. It removes fixed day values, makes the date explicit, and preserves the useful distinctions between current artifacts, prior answers, regular practice, ranked attempts, and measured performance. It is not presented as a prompt used during the original CTF.

The snapshots describe authorization given during the event. They are historical text, not authorization to access an active target, submit an answer, or consume an attempt today.
