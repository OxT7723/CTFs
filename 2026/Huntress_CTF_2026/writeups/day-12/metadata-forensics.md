# Managed Expectations

Day 12 · Metadata forensics · **Evidence summary**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

Challenge ID: `metadata-forensics-day-12-managed-expectations`.

## Challenge

The .NET assemblies share names, versions, and source ancestry—but their module identities remain distinct. Separate rebuilds from renames.

The saved assignment asks, for example:

- Determine dotnet.mvid_guid for managed-001.dll.

## Recorded AI approach

The shared day notes retain the following challenge-specific account:

read the MVID from the CLR metadata Module row and
  its GUID heap for each assigned DLL. The MVID helper is now in
  `metadata-forensics-tools/pe_metadata.py`, and the metadata runner dispatches
  MVID questions to it. The accepted MVIDs were
  `21e410f3-c977-465c-80eb-6890ddd3085c` (Single Solve),
  `9e0e197f-d610-4ec9-bd1c-d28da985893a` (Time Trial),
  `2658bcc7-f07c-48b1-8cb9-2bb645f8680e` and
  `ecc37f87-9668-43c5-b9f4-011ee0d07c7c` (Mastery). All three modes returned
  `CORRECT`.

## Recorded result

The historical challenge-state snapshot records:

| Mode | Listed solved | Status result |
| --- | --- | --- |
| single_solve | True | CORRECT |
| time_trial | True | CORRECT |
| mastery | True | CORRECT |

These are retained service-state values, not a fresh check. They do not by themselves establish a ranked timed completion or a CourseStack points total.

## Evidence retained

- [Original challenge notes](../../source-notes/early/12-Managed_Expectations/readme.md)
- [Saved challenge state](../../source-notes/early/12-Managed_Expectations/challenge_state.json)
- [Reusable tooling guide](../../tools/later/metadata-forensics-tools/README.md)
- [Shared day notes](../../source-notes/later/writeups/day-12/progress-notes.md)

This short record preserves what the available material supports. The original AI transcript and a complete per-attempt command/output trail are not included here; no challenge was rerun to fill those gaps.

## Retained sources

- [early/12-Managed_Expectations/readme.md](../../source-notes/early/12-Managed_Expectations/readme.md)
- [later/writeups/day-12/progress-notes.md](../../source-notes/later/writeups/day-12/progress-notes.md)
