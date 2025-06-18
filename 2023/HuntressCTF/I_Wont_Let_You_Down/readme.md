# I Wont Let You down - Miscellaneous - easy

Author: @proslasher

OK Go take a look at this IP:
Connect here: http://155.138.162.158 # USING ANY OTHER TOOL OTHER THAN NMAP WILL DISQUALIFY YOU. DON'T USE BURPSUITE, DON'T USE DIRBUSTER.


## Solution

Since only Nmap was allowed, I ran a scan on the provided IP: `nmap -p- 155.138.162.158`

The results showed the following open ports:
```
Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-05 13:46 EDT
Stats: 0:06:06 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 84.50% done; ETC: 13:53 (0:01:07 remaining)
Nmap scan report for 155.138.162.158.vultrusercontent.com (155.138.162.158)
Host is up (0.049s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
8888/tcp open  sun-answerbook

Nmap done: 1 IP address (1 host up) scanned in 708.65 seconds

```

Navigated to http://155.138.162.158:8888 to see what was hosted on port 8888.


The page contained the lyrics to Rick Astley's "Never Gonna Give You Up" a Rickroll! After scrolling through, I found the flag at the bottom of the lyrics:
```
We're no strangers to love
You know the rules and so do I (do I)
A full commitment's what I'm thinking of
You wouldn't get this from any other guy
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching, but you're too shy to say it (say it)
Inside, we both know what's been going on (going on)
We know the game and we're gonna play it
And if you ask me how I'm feeling
Don't tell me you're too blind to see
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching, but you're too shy to say it (to say it)
Inside, we both know what's been going on (going on)
We know the game and we're gonna play it
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
flag{93671c2c38ee872508770361ace37b02}
```