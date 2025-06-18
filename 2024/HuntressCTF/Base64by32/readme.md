# Base64by32

**Description:**

<small>Author: @JohnHammond</small><br><br>This is a dumb challenge. I'm sorry. <br><br> <b>Download the file(s) below.</b>


**Category:** Scripting

**Difficulty:** easy

**File:** [base64by32.zip](base64by32.zip)

## Solution

The challenge description hints that the file has been Base64 encoded 32 times. Created a Python script to decode the file and reveal the flag

```python
import base64

def decode_base64(file_path, output_path, iterations=32):
    # Read the base64 encoded content from the file
    with open(file_path, 'r') as file:
        encoded_data = file.read()

    # Decode the data 32 times
    for _ in range(iterations):
        encoded_data = base64.b64decode(encoded_data)

    # Write the final decoded data to the output file
    with open(output_path, 'wb') as output_file:
        output_file.write(encoded_data)

input_file = 'base64by32'  
output_file = 'decoded.txt'

#decoding function
decode_base64(input_file, output_file)

print(f"Decoded data has been saved to {output_file}")

```

Flag of `flag{8b3980f3d33f2ad2f531f5365d0e3970}`