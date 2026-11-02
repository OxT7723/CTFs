# Bridge Troll

Day 22 · Binary reverse engineering · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Bridge Troll

Challenge: `binary-reverse-engineering-day-22-managed-native-bridge`

Completed Single Solve, Time Trial, and Mastery. Mastery used six evidence
sets. Each assignment bundled the prior binary specimens with the current
managed assembly and its runtime support files.

The existing evidence analyzer needed two reusable updates:

- Index `dNN--sample*` archive members as well as `dNN--variant-*`.
- Select the Day 21 loader and plugin by filename role, and include `.cmxs`
  when choosing binaries. The loader has no scored HCFG; its paired plugin
  does.
- For normalized PE architecture questions, use the machine label reported by
  `objdump -f`. The Day 22 managed assembly's `i386` label was accepted; its
  numeric PE code was rejected for that answer field.

The HCFG parser and existing PE CLI metadata reader handled the Day 22
configuration and metadata fields. All answer IDs were accepted in each mode.

## Retained sources

- [later/writeups/day-22/binary-bridge-troll.md](../../source-notes/later/writeups/day-22/binary-bridge-troll.md)
