> **Preserved source note.** This is a historical, AI-assisted working document. It may contain provisional findings, old completion states, and references to files that did not survive the original workspace. Editorial summaries elsewhere in this collection distinguish those limits. Private lab addresses and retired artifact download links have been removed or replaced; see the source manifest.

# Huntress CTF 2026: AI Arena

Notes and writeups for this CTF.

<!-- huntress:index:start -->
## Challenges

| Day | Lane | Challenge | Single Solve | Time Trial | Mastery | Writeup |
| --- | --- | --- | --- | --- | --- | --- |
| Day 01 <!-- cs:aae074eb7ded4f86b779 --> | welcome | [Read the Rules](01-Read_the_Rules/readme.md) | ? | — | — |  |
| Day 01 <!-- cs:7bd3466b645e5a709d85 --> | welcome | [Welcome Robots](01-Welcome_Robots/readme.md) | ✅ | — | — |  |
| Day 01 <!-- cs:83b2aa1f68b67c2dd2fd --> | binary-reverse-engineering | [⚙️ ELF Aware](01-ELF_Aware/readme.md) | ✅ | ✅ | ✅ |  |
| Day 01 <!-- cs:62f1123ed3035b150680 --> | warmups | [👶 A Little Based](01-A_Little_Based/readme.md) | ✅ | ✅ | ✅ |  |
| Day 01 <!-- cs:e0fef4f37d93ca4f5876 --> | script-analysis | [📜 Power Play](01-Power_Play/readme.md) | ✅ | ✅ | ✅ |  |
| Day 01 <!-- cs:be880705e30cbaf2980c --> | mobile-android | [📱 Exported Trust](01-Exported_Trust/readme.md) | ✅ | ✅ | ✅ |  |
| Day 01 <!-- cs:9f4b487276077d990ba4 --> | metadata-forensics | [🔎 You Must Be This Hash to Ride](01-You_Must_Be_This_Hash_to_Ride/readme.md) | ✅ | ✅ | ✅ |  |
| Day 02 <!-- cs:5a6e0957f998abb46e2b --> | binary-reverse-engineering | [⚙️ Mangled](02-Mangled/readme.md) | ✅ | ✅ | ✅ |  |
| Day 02 <!-- cs:97df7baf6f95b8f9c445 --> | warmups | [👶 Half a Turn](02-Half_a_Turn/readme.md) | ✅ | ✅ | ✅ |  |
| Day 02 <!-- cs:cf24dcd4891088c2de0b --> | script-analysis | [📜 Host With the Most](02-Host_With_the_Most/readme.md) | ✅ | ✅ | ✅ |  |
| Day 02 <!-- cs:8ba49c8c652f71d169d2 --> | mobile-android | [📱 Deep Link Drift](02-Deep_Link_Drift/readme.md) | ✅ | ✅ | ✅ |  |
| Day 02 <!-- cs:8ce48c0f2579d52d1f60 --> | metadata-forensics | [🔎 Looks Can Be Deceiving](02-Looks_Can_Be_Deceiving/readme.md) | ✅ | ✅ | ✅ |  |
| Day 03 <!-- cs:1c5f13db653e4eba47af --> | binary-reverse-engineering | [⚙️ Table Manners](03-Table_Manners/readme.md) | ✅ | ✅ | ✅ |  |
| Day 03 <!-- cs:2909523d9301bf8f6f34 --> | warmups | [👶 Hex Appeal](03-Hex_Appeal/readme.md) | ✅ | ✅ | ✅ |  |
| Day 03 <!-- cs:9b66dec6d7336a87b134 --> | script-analysis | [📜 Expansion Pack](03-Expansion_Pack/readme.md) | ✅ | ✅ | ✅ |  |
| Day 03 <!-- cs:c9ddab8069f128195121 --> | mobile-android | [📱 Intent Injection](03-Intent_Injection/readme.md) | ✅ | ✅ | ✅ |  |
| Day 03 <!-- cs:47305f44c2583f8fd061 --> | metadata-forensics | [🔎 BOM Voyage](03-BOM_Voyage/readme.md) | ✅ | ✅ | ✅ |  |
| Day 04 | binary-reverse-engineering | [⚙️ Go Fish](04-Go_Fish/readme.md) | ✅ | ✅ | ✅ |  |
| Day 04 | warmups | [👶 Two of a Kind](04-Two_of_a_Kind/readme.md) | ✅ | ✅ | ✅ |  |
| Day 04 | script-analysis | [📜 Dim and Dimmer](04-Dim_and_Dimmer/readme.md) | ✅ | ✅ | ✅ |  |
| Day 04 | mobile-android | [📱 Pending Intent Relay](04-Pending_Intent_Relay/readme.md) | ✅ | ✅ | ✅ |  |
| Day 04 | metadata-forensics | [🔎 Picture This](04-Picture_This/readme.md) | ✅ | ✅ | ✅ |  |
| Day 05 | binary-reverse-engineering | [⚙️ Rust Belt](05-Rust_Belt/readme.md) | ✅ | ✅ | ✅ |  |
| Day 05 | warmups | [👶 By the Numbers](05-By_the_Numbers/readme.md) | ✅ | ✅ | ✅ |  |
| Day 05 | script-analysis | [📜 Hatch Careful](05-Hatch_Careful/readme.md) | ✅ | ✅ | ✅ |  |
| Day 05 | mobile-android | [📱 Backup Spill](05-Backup_Spill/readme.md) | ✅ | ✅ | ✅ |  |
| Day 05 | metadata-forensics | [🔎 Chunk Norris](05-Chunk_Norris/readme.md) | ✅ | ✅ | ✅ |  |
| Day 06 | binary-reverse-engineering | [⚙️ Pool Party](06-Pool_Party/readme.md) | ✅ | ✅ | ✅ |  |
| Day 06 | warmups | [👶 Eight Is Enough](06-Eight_Is_Enough/readme.md) | ✅ | ✅ | ✅ |  |
| Day 06 | script-analysis | [📜 Shell We Begin](06-Shell_We_Begin/readme.md) | ✅ | ✅ | ✅ |  |
| Day 06 | mobile-android | [📱 Provider Paths](06-Provider_Paths/readme.md) | ✅ | ✅ | ✅ |  |
| Day 06 | metadata-forensics | [🔎 Portable Deception](06-Portable_Deception/readme.md) | ✅ | ✅ | ✅ |  |
| Day 07 | binary-reverse-engineering | [⚙️ Routine Check](07-Routine_Check/readme.md) | ✅ | ✅ | ✅ |  |
| Day 07 | warmups | [👶 Percent Chance](07-Percent_Chance/readme.md) | ✅ | ✅ | ✅ |  |
| Day 07 | script-analysis | [📜 Node by Node](07-Node_by_Node/readme.md) | ✅ | ✅ | ✅ |  |
| Day 07 | mobile-android | [📱 WebView Bridge](07-WebView_Bridge/readme.md) | ✅ | ✅ | ✅ |  |
| Day 07 | metadata-forensics | [🔎 Seven-Zip, No Relation](07-Seven-Zip_No_Relation/readme.md) | ✅ | ✅ | ✅ |  |
| Day 08 | binary-reverse-engineering | [⚙️ Swift Justice](08-Swift_Justice/readme.md) | ✅ | ✅ | ✅ |  |
| Day 08 | warmups | [👶 Entity Relations](08-Entity_Relations/readme.md) | ✅ | ✅ | ✅ |  |
| Day 08 | script-analysis | [📜 Lost in Translation](08-Lost_in_Translation/readme.md) | ✅ | ✅ | ✅ |  |
| Day 08 | mobile-android | [📱 Cleartext Session](08-Cleartext_Session/readme.md) | ✅ | ✅ | ✅ |  |
| Day 08 | metadata-forensics | [🔎 What’s in the Box?](08-Whats_in_the_Box/readme.md) | ✅ | ✅ | ✅ |  |
| Day 09 | binary-reverse-engineering | [⚙️ Nimble](09-Nimble/readme.md) | ✅ | ✅ | ✅ |  |
| Day 09 | warmups | [👶 Escape Room](09-Escape_Room/readme.md) | ✅ | ✅ | ✅ |  |
| Day 09 | script-analysis | [📜 All the World's a Stager](09-All_the_Worlds_a_Stager/readme.md) | ✅ | ✅ | ✅ |  |
| Day 09 | mobile-android | [📱 Trust Everyone](09-Trust_Everyone/readme.md) | ✅ | ✅ | ✅ |  |
| Day 09 | metadata-forensics | [🔎 Built Different](09-Built_Different/readme.md) | ✅ | ✅ | ✅ |  |
| Day 10 | binary-reverse-engineering | [⚙️ Zig Zag](10-Zig_Zag/readme.md) | ✅ | ✅ | ✅ |  |
| Day 10 | warmups | [👶 Thirty-Two Below](10-Thirty-Two_Below/readme.md) | ✅ | ✅ | ✅ |  |
| Day 10 | script-analysis | [📜 Bind Over Matter](10-Bind_Over_Matter/readme.md) | ✅ | ✅ | ✅ |  |
| Day 10 | mobile-android | [📱 Network Config Split](10-Network_Config_Split/readme.md) | ✅ | ✅ | ✅ |  |
| Day 10 | metadata-forensics | [🔎 Where Do We Begin?](10-Where_Do_We_Begin/readme.md) | ✅ | ✅ | ✅ |  |
| Day 11 | binary-reverse-engineering | [⚙️ D-Day](11-D-Day/readme.md) | ✅ | ✅ | ✅ |  |
| Day 11 | warmups | [👶 Safe Travels](11-Safe_Travels/readme.md) | ✅ | ✅ | ✅ |  |
| Day 11 | script-analysis | [📜 By Any Other Name](11-By_Any_Other_Name/readme.md) | ✅ | ✅ | ✅ |  |
| Day 11 | mobile-android | [📱 Local Secrets](11-Local_Secrets/readme.md) | ✅ | ✅ | ✅ |  |
| Day 11 | metadata-forensics | [🔎 What’s My Name Again?](11-Whats_My_Name_Again/readme.md) | ✅ | ✅ | ✅ |  |
| Day 12 | binary-reverse-engineering | [⚙️ Pascal's Wager](12-Pascals_Wager/readme.md) | ✅ | ✅ | ✅ |  |
| Day 12 | warmups | [👶 Back at You](12-Back_at_You/readme.md) | ✅ | ✅ | ✅ |  |
| Day 12 | script-analysis | [📜 AutoIt Takes Two](12-AutoIt_Takes_Two/readme.md) | ✅ | ✅ | ✅ |  |
| Day 12 | mobile-android | [📱 SQLite Assumptions](12-SQLite_Assumptions/readme.md) | ✅ | ✅ | ✅ |  |
| Day 12 | metadata-forensics | [🔎 Managed Expectations](12-Managed_Expectations/readme.md) | ✅ | ✅ | ✅ |  |
| Day 01 <!-- cs:3952792d095906a89205 --> | Local history | [Sanity Check](01-Sanity_Check/readme.md) | Historical | Historical | Historical |  |
<!-- huntress:index:end -->
