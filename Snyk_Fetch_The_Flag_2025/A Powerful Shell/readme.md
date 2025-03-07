# A Powerful Shell

**Description:**

<small>Author: @Kkevsterrr</small><br><br>How can a SHELL have so much POWER?!   <br><br> <b>Download the file(s) below.</b>


**Category:** Reverse Engineering

**Difficulty:** easy

**File:** [challenge.ps1](challenge.ps1)

## Solution

One of the most notable elements in the script was a base64 encoded string, witch, when decoded, revealed additional PowerShell code:
```powershell
$decoded = [System.Convert]::FromBase64String('ZmxhZ3s0NWQyM2MxZjY3ODliYWRjMTIzNDU2Nzg5MDEyMzQ1Nn0=')
$flag = [System.Text.Encoding]::UTF8.GetString($decoded)

# Only show flag if specific environment variable is set
if ($env:MAGIC_KEY -eq 'Sup3rS3cr3t!') {
    Write-Output $flag
} else {
    Write-Output "Nice try! But you need the magic key!"
}
```

Within this decoded script, there was another base64 encoded string, which, once decoded, revealed the flag: `flag{45d23c1f6789badc1234567890123456}`