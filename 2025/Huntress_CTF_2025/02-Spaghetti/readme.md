# Malware - Day 02
**Category:** Malware  
**Author:**  [John Hammond](https://www.youtube.com/@_JohnHammond) 

## Challenge Prompt 

You know, I've been thinking... at the end of the day, spaghetti is really just strings of pasta!

Anyway, we saw this weird file running on startup. Can you figure out what this is?

I'm sure you'll get more understanding of the questions below as you explore!


> **CAUTION:** This is the Malware category, and as such, includes malware. Please be sure to analyze these files within an isolated virtual machine.  
> **IMPORTANT** The ZIP archive password is `infected`.    
> **NOTE** You may find a public paste URL that is expired. This is an artifact of the original malware sample and is intentional. This URL is not necessary for the challenge.



### Questions MainFileSettings 4 points

Uncover the flag within the "main file."

> **NOTE** **Once you uncover the intended payload, you shouldn't need to do any further analysis.** Use context clues from the challenge description and you should find the flag.

### My Fourth Oasis 3 points
Uncover the flag within "my fourth oasis."

### MEMEMAN 3 points
Uncover the flag beside "MEMEMAN."



## Solution


After trying several manual techniques and sanitizing the PowerShell script, I used ChatGPT GPT-5 as an analysis aid. When supplied with the artifacts and context, it was able to identify and extract all of the flags. The output is below: 

Nice — I dug through both files you uploaded and recovered all three flags.

### Results (flags)

- MainFileSettings (in the main file) — `flag{39544d3b5374ebf7d39b8c260fc4afd8}`
(found inside the decoded main binary reconstructed from `/mnt/data/AYGIW.tmp`)

- My Fourth Oasis — `flag{b313794dcef335da6206d54af81b6203}`
(found inside the decoded `$MyOasis4` payload written to `/mnt/data/MyOasis4.decoded.bin` — the payload contained HTML numeric entities which decode to this flag)

- MEMEMAN — `flag{60814731f508781b9a5f8636c817af9d}`
(found in the decoded $TDefo payload written to /mnt/data/TDefo.decoded.bin; it appeared in a commented line next to the MEMEMAN path)

### Short explanation of how I found them

- `spaghetti` is an obfuscated PowerShell dropper with several embedded bit-strings. The script defines FonatozQZ() which converts long binary strings (encoded with `~` / `%` as 0/1) into ASCII. I located the four `FonatozQZ(...)` blobs in `/mnt/data/spaghetti`, applied the same replacements (`~ -> 0`, `% -> 1`) and converted the bitstreams into bytes — producing:

    - `/mnt/data/fonatozqz_decoded_2.bin` → MyOasis4 payload

    - `/mnt/data/fonatozqz_decoded_3.bin` → TDefo payload

    - two very small decodes that contained Invoke / Execute fragments

- The MyOasis4 decoded payload contained HTML numeric entities (e.g. `&#98;`, etc.). I decoded contiguous runs of those entities to ASCII and found `flag{b31379...}`.

- The TDefo decoded payload included Defender exclusion commands and a commented line with the MEMEMAN flag.

- The other uploaded file `/mnt/data/AYGIW.tmp` contained a long ASCII hex string with WT noise inserted; removing the WT junk and unhexlifying produced a PE binary (`/mnt/data/AYGIW.tmp.decoded1.bin`) whose printable strings contained the main-file flag `flag{39544d3b...}`.

### Files I created / wrote while extracting (you can inspect them)

- `/mnt/data/AYGIW.tmp.decoded1.bin` — decoded PE from `/mnt/data/AYGIW.tmp` (contains main-file flag)

- `/mnt/data/MyOasis4.decoded.bin` — decoded `$MyOasis4` payload (contains oasis flag)

- `/mnt/data/TDefo.decoded.bin` — decoded `$TDefo` payload (contains MEMEMAN flag)

- `/mnt/data/fonatozqz_decoded_0.bin` and `_1.bin` — small decoded fragments (Execute, Invoke)

- `/mnt/data/fonatozqz_decoded_2.bin` and `_3.bin` — copies of the two larger decodes (same as the MyOasis4/TDefo outputs)

