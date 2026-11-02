# Root of Trust

Day 22 · Mobile / Android · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 22 Mobile: Root of Trust

The assigned APKs contain `assets/huntress_puzzle.json` using the existing
`huntress.mobile.puzzle.v1` asset schema. The current variants declare their
codec, so the shared decoder handles the payload without challenge-specific
answer values. `run_modes.py` checks each decoded value against the live
question's answer format and submits with the answer IDs returned by the
current start response. Mastery uses six APK deliveries and is handled by the
same runner.

Run the regular modes in progression order:

```sh
python3 mobile-android-tools/run_modes.py mobile-android-day-22-root-of-trust
python3 mobile-android-tools/run_modes.py mobile-android-day-22-root-of-trust/time_trial
python3 mobile-android-tools/run_modes.py mobile-android-day-22-root-of-trust/mastery
```

The runner saves each attempt's downloaded APKs, start response, candidate
answers, submission response, and final status under
`work/day-22/mobile-android/<attempt-id>/`.

## Retained sources

- [later/writeups/day-22/mobile-root-of-trust.md](../../source-notes/later/writeups/day-22/mobile-root-of-trust.md)
