# Huntress CTF 2026: AI Arena

**Seeking_Security_Job_And_Flags · 45th of 1,602 teams · 1,885 points**

This is my record of Huntress CTF 2026: the challenges, the AI-assisted workflow I developed during the month, the retained solver code, and the results. Work moved between Codex, the event's Homebase AI, and ChatGPT. The collection preserves both useful technical investigations and the limits of the evidence that survived the event.

> **AI authorship and verification**
>
> The writeups, tool documentation, summaries, and data presentations in this collection were generated using AI, drawing on retained challenge artifacts, logs, solver code, and saved results. The material was subsequently organized and reviewed for publication.
>
> AI can produce factual errors, unsupported assumptions, and incorrect interpretations, even when stated confidently. The checks documented here cover specific aspects of the collection; they do not establish that every technical claim is correct or every solve has been independently reproduced.
>
> Before relying on an explanation, command, code sample, or reported result, verify it against the underlying artifacts and source evidence, and reproduce the relevant steps where possible. Known gaps and verification limits are documented throughout the collection.

## Results

| Measure | Result | Evidence |
| --- | --- | --- |
| Final placement | **45th of 1,602 teams** | [Completion certificate](assets/huntress-ctf-2026-certificate.pdf) |
| Final score | **1,885 points** | Certificate and [saved scoring results](results/README.md) |
| Completion | **561 / 561**, as labeled on the certificate | 558 daily mode awards plus three scored extras |
| Daily challenges | **186 across six lanes**, with all three scoring modes recorded | [Complete challenge catalog](writeups/README.md) |
| Best reconstructed daily placement | **3rd on October 20** | [Daily scoring reconstruction](results/README.md) |

The certificate counts individual mode completions. It does **not** mean 561 distinct named challenge writeups. The saved catalog contains 186 daily challenges, three scored extras, and an unscored Sanity Check. An award in the mode called Time Trial or Mastery does not by itself establish a ranked Hall of Fame run.

![Daily placement during October, reconstructed from saved scoring events](assets/team-placement.png)

The chart uses the end of each **UTC** day and reconstructs placement from the retained scoreboard. It is not a series of official daily leaderboard screenshots or a measurement of the best rank reached within each day. The final result above uses the certificate's 1,602-team count; the saved scoreboard has 1,596 entries. [Calculation, source differences, and downloadable data](results/README.md).

## Hall of Fame

The shared Hall of Fame snapshot captured on **November 1, 2026** lists **90 ranked entries across 49 challenges** for this team: **48 Time Trial** and **42 Mastery** entries, including **15 top-ten results across 11 challenges**.

| Challenge | Mode | Rank / exported entries | Recorded elapsed time |
| --- | --- | ---: | ---: |
| [Seeing Double](writeups/day-30/metadata-forensics.md) | Time Trial | #3 / 41 | 0.610 s |
| [No Artifact Left Behind](writeups/day-31/metadata-forensics.md) | Time Trial | #4 / 36 | 0.850 s |
| [The Full Transform](writeups/day-31/script-analysis.md) | Time Trial | #6 / 39 | 1.299 s |
| [Full Stack Incident](writeups/day-31/web-exploitation.md) | Mastery | #8 / 22 | 20.084 s |
| [Go Fish](writeups/day-04/binary-reverse-engineering.md) | Mastery | #1 / 2 | 1.633 s |

Ranks are specific to each challenge and mode. Board sizes count exported entries; the file does not establish complete participation. Go Fish's first-place result is specifically among two listed Mastery entries. These are recorded ranked-attempt times, separate from the time spent investigating challenges and developing solvers.

[All 90 results, source qualifications, and reproducible data](results/hall-of-fame.md).

## Start here

| Section | What it contains |
| --- | --- |
| [Challenge catalog](writeups/README.md) | Every named task in the saved roster, with links to available accounts and clear gaps where only scoring evidence remains |
| [SHA1-Hulud](writeups/day-30/sha1-hulud.md) | A detailed reverse-engineering account, including the shift away from unsuccessful hash guesses and the limits of the retained successful-solve record |
| [AI workflow](AI_WORKFLOW.md) | How category-specific prompts, reusable solvers, replay checks, and credit management fit together |
| [Final prompt snapshots](prompts/README.md) | The six category prompts and the separate review/training prompt used near the end of the event |
| [Solver tools](tools/README.md) | Preserved early and later tooling, with historical platform dependencies explained |
| [Results and placement](results/README.md) | Certificate-backed results, scoring timestamps, daily placement, and reproducible calculations |
| [Hall of Fame](results/hall-of-fame.md) | Recorded ranked-attempt durations and challenge/mode placements from the shared snapshot |
| [Source notes](source-notes/README.md) | Earlier notes and later session accounts behind the edited articles |
| [Authorship and evidence](ABOUT.md) | AI attribution, editorial changes, and what was and was not verified |

## Reading the writeups

The depth of the retained material varies. Some articles contain detailed investigations; others are short session notes or evidence-limited summaries. A short account is labeled accordingly. The catalog also records completed challenges for which no dedicated walkthrough was recovered.

Historical notes can show an unsuccessful attempt before a later completion. The final scoring data is kept separate so an old progress note is not mistaken for the final outcome. Original command examples describe their event workspace; the current package does not recreate the retired event services or every downloaded challenge artifact.

## Certificate

[![Huntress CTF 2026 completion certificate](assets/huntress-ctf-2026-certificate.png)](assets/huntress-ctf-2026-certificate.pdf)

The certificate also reports 16,017 model turns, 1.55 billion tokens, and GPT-6 Luna as the favorite model at 99% of turns. These are platform-reported event statistics, not an estimate of personal API spending.

Challenge names and event materials belong to their respective creators. This repository is a participant's collection of notes and code, with AI assistance disclosed. See [attribution](ATTRIBUTION.md).
