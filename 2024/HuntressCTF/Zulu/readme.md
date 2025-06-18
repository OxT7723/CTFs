# Zulu

**Description:**

<small>Author: @JohnHammond</small><br><br>Did you know that zulu is part of the phonetic alphabet? <br><br> <b>Download the file(s) below.</b>


**Category:** Warmups

**Difficulty:** easy

**File:** [zulu](zulu)

## Solution

Ran `file` to check the file - it was a compressed file: `file zulu`

The output indicated that it was a compressed file.

To extract its contents, I used 7z to decompress it and redirect the output into a new file: `7z x zulu -so > unzipfile`. 

After extracting the file, I viewed its contents and found the flag: `flag{74235a9216ee609538022e6689b4de5c}`
