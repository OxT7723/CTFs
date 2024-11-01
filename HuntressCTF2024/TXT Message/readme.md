# TXT Message

**Description:**

<small>Author: @JohnHammond</small><br><br>Hmmm, have you seen some of the strange DNS records for the <code>ctf.games</code> domain?  One of them sure is <a href="https://en.wikipedia.org/wiki/Od_(Unix)">od</a>d...


**Category:** Warmups

**Difficulty:** easy

## Solution
I executed the following command `dig ctf.games TXT`

This returned the following response:
```
; <<>> DiG 9.19.21-1-Debian <<>> ctf.games TXT
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12781
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; MBZ: 0x0005, udp: 1232
;; QUESTION SECTION:
;ctf.games.                     IN      TXT

;; ANSWER SECTION:
ctf.games.              5       IN      TXT     "146 154 141 147 173 061 064 145 060 067 062 146 067 060 065 144 064 065 070 070 062 064 060 061 144 061 064 061 143 065 066 062 146 144 143 060 142 175"

;; Query time: 75 msec
;; SERVER: 192.168.150.2#53(192.168.150.2) (UDP)
;; WHEN: Sun Oct 06 15:03:53 EDT 2024
;; MSG SIZE  rcvd: 202
```

Using the clue from the description about the od command, I ran the following Python script to decode the flag

```python
# Given octal numbers as a string
octal_numbers = "146 154 141 147 173 061 064 145 060 067 062 146 067 060 065 144 064 065 070 070 062 064 060 061 144 061 064 061 143 065 066 062 146 144 143 060 142 175"

# Split the string into individual octal numbers
octal_list = octal_numbers.split()

# Convert octal to ASCII
readable_text = ''.join(chr(int(octal, 8)) for octal in octal_list)

print(readable_text)
```

This script revealed the flag: `flag{14e072f705d45882401d141c562fdc0b}`.

