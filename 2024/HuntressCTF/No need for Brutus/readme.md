# No need for Brutus

**Description:**

<small>Author: @aenygma</small><br><br>A simple message for you to decipher: <br><br> <code>squiqhyiiycfbudeduutvehrhkjki</code> <br><br> Submit the original plaintext hashed with MD5, wrapped between the usual flag format: <code>flag{<hash_goes_here>}</code> <br><br> <small><i>Ex: If the deciphered text is "hello world", the MD5 hash would be <code>5eb63bbbe01eeed093cb22bb8f5acdc3</code>, and the flag would be <code>flag{5eb63bbbe01eeed093cb22bb8f5acdc3}</code>.</i></small>


**Category:** Cryptography

**Difficulty:** easy

## Solution

This challenge involves a Caesar cipher. I created a Python script to try all possible shifts (1 through 25)

```python
import string

def caesar_cipher_decrypt(ciphertext, shift):
    decrypted = []
    for char in ciphertext:
        if char in string.ascii_lowercase:
            new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            decrypted.append(new_char)
        else:
            decrypted.append(char) 
    return ''.join(decrypted)

ciphertext = "squiqhyiiycfbudeduutvehrhkjki"

# Test all shifts from 1 to 25
for shift in range(1, 26):
    print(f"Shift {shift}: {caesar_cipher_decrypt(ciphertext, shift)}")

```
After examining the output, shift 16 revealed the message `caesarissimplenoneedforbrutus`

I hashed the plaintext using MD5, which resulted in `c945bb2173e7da5a292527bbbc825d3f`. Finally, I wrapped it in the flag format to get a flag of `flag{c945bb2173e7da5a292527bbbc825d3f}`