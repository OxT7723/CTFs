# Product Placement

Day 13 · Metadata forensics · **Session note**

[All records](../README.md) · [Authorship and evidence](../../ABOUT.md)

This record draws on saved CTF notes. Results and operations described below belong to those sessions; they were not replayed during publication preparation.

## Later Homebase account

### Day 13 Metadata Forensics — Product Placement

**Challenge:** 🔎 Product Placement
**ID:** `metadata-forensics-day-13-product-placement`
**Description:** Installers were copied, renamed, and repackaged. Recover stable product identities, distinguish revisions from different products, and find the collision.

### Solved modes

| Mode | Answer IDs | Result |
| --- | --- | --- |
| Single Solve | `d13-msi-001-msi-product-code-guid` | `CORRECT` |
| Time Trial | `d13-msi-002-msi-product-code-guid` | `CORRECT`, before the 13:03:08 UTC deadline |
| Mastery | `set1.d13-msi-003-msi-product-code-guid`, `set2.d13-msi-004-msi-product-code-guid` | Both accepted; `CORRECT` before the 13:04:04 UTC deadline |

Every question requested `msi.product_code_guid` and accepted the MSI
`Property` table's `ProductCode` value:

```text
{DD1A80D5-0250-4F4D-B289-13096D633C61}
```

Keep the braces. The unbraced form was rejected; the braced canonical GUID
was accepted. The same ProductCode appeared in all four assigned installers.

### Assigned bundles

- Single Solve: metadata-day-13-evidence.zip (private download link removed) — SHA-256 `6e401e69ecf6c3d048c285a950a3cc10611da4a070b7e10d2d69aa5b26bac954`. Contains `installer-001.msi`.
- Time Trial: metadata-day-13-evidence.zip (private download link removed) — SHA-256 `0ed0afb7bc79dc394fa8c5814c76d6059c33292a8dda27a7a43954807f3b0cc3`. Contains `installer-002.msi`.
- Mastery: metadata-forensics-day-13-product-placement-mastery.zip (private download link removed) — SHA-256 `1c2e207fa73af60650a364892cc7e605c2f3f39df4e86d41cc1164eabcce94c5`. Contains the two assigned installer bundles for `installer-003.msi` and `installer-004.msi`.

### Method and tooling

The assigned ZIPs were downloaded through the Game Master, then read from
their MSI bytes with `msiinfo export <file> Property`. The reusable runner now
extracts MSI ProductCode, Upgrade table codes, ProductVersion, ProductName,
Manufacturer, summary Revision Number, and Template fields from live
assignments. It submitted under the exact live answer IDs.

The Game Master returned `CORRECT` for all three modes, with no `pending`
scoring status. Attempt records are under
`attempt-records/metadata-forensics-day-13-product-placement/`.

## Retained sources

- [later/writeups/day-13/metadata-forensics-product-placement.md](../../source-notes/later/writeups/day-13/metadata-forensics-product-placement.md)
