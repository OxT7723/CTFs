# Obfuscation Station

**Description:**

<small>Author: @resume</small><br><br>You've reached the Obfuscation Station! <br>  Can you decode this PowerShell to find the flag? <br> <b>Archive password: <code>infected</code></b> <br><br> <b>Download the file(s) below.</b> 


**Category:** Forensics

**Difficulty:** easy

**File:** [Challenge.zip](Challenge.zip)

## Solution


After extracting Challenge.zip (using the password infected), I found a PowerShell script file named chal.ps1.

The script contained obfuscated code using Base64 and zlib compression
```powershell 
(nEW-objECt  SYstem.iO.COMPreSsIon.deFlaTEStREAm( [IO.mEmORYstreAM][coNVERt]::FROMBAse64sTRING( 'UzF19/UJV7BVUErLSUyvNk5NMTM3TU0zMDYxNjSxNDcyNjexTDY2SUu0NDRITDWpVQIA') ,[io.COmPREssioN.coMpreSSioNmODE]::DeCoMpReSS)| %{ nEW-objECt  sYStEm.Io.StREAMrEADeR($_,[TeXT.encodiNG]::AsCii)} |%{ $_.READTOENd()})| & ( $eNV:cOmSPEc[4,15,25]-JOin'')

```
The main components included
- A Base64-encoded string: 'UzF19/UJV7BVUErLSUyvNk5NMTM3TU0zMDYxNjSxNDcyNjexTDY2SUu0NDRITDWpVQIA'
- Compression using the DeflateStream method.


I wrote a Python script to decode the Base64 string and decompress it using the zlib library.

```python
import base64
import zlib

# Base64 string from the script
base64_string = 'UzF19/UJV7BVUErLSUyvNk5NMTM3TU0zMDYxNjSxNDcyNjexTDY2SUu0NDRITDWpVQIA'

# Decode the Base64 string
decoded_data = base64.b64decode(base64_string)
print(decoded_data)

# Decompress the data using the deflate algorithm
decompressed_data = zlib.decompress(decoded_data, -zlib.MAX_WBITS)

# Output the decompressed data
decompressed_data.decode('ascii')
print(decompressed_data)

```

Executing the Python script to get the flag of`flag{3ed675ef0343149723749c34fa910ae4}`