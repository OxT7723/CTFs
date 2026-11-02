> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Bridge Troll

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
