# Dialtone - Warmups - easy

Author: @JohnHammond#6971

Well would you listen to those notes, that must be some long phone number or something!

<audio src="dialtone.wav" controls title="Title"></audio>

## Solution 

I installed the DTMF decoder from [GitHub](https://github.com/ribt/dtmf-decoder) to decode the audio file.

Next, I ran DTMF that coverted the file to this large number:
`13040004482820197714705083053746380382743933853520408575731743622366387462228661894777288573`

Next I converted the big int to hex:
`666C61677B36633733336566303962633466326134333133666636333038376532356436377D`

Finally I converted the hex string to text to find the flag of `flag{6c733ef09bc4f2a4313ff63087e25d67}`
