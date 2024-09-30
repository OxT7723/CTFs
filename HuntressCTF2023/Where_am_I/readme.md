# Where am I - OSINT - medium

Author: @proslasher

Your friend thought using a JPG was a great way to remember how to login to their private server. Can you find the flag?

Download the file(s) below [PXL_20230922_231845140_2.jpg](PXL_20230922_231845140_2.jpg)

## Solution

Using a metadata extraction tool, I checked the image’s metadata and found both the title and subject fields contained base64-encoded strings:

- Title:
ZmxhZ3tiMTFhM2YwZWY0YmMxNzBiYTk0MDljMDc3MzU1YmJhMik=

- Subject:
ZmxhZ3tiMTFhM2YwZWY0YmMxNzBiYTk0MDljMDc3MzU1YmJhMik=

I decoded the base64 string using an online base64 decoder, which revealed the flag:
`flag{b11a3f0ef4bc170ba9409c077355bba2)`