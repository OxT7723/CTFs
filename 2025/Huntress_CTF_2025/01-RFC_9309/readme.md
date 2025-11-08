# RFC 9309 - Day 01
**Category:** Warmups
**Author:**  [John Hammond](https://www.youtube.com/@_JohnHammond) 



## Challenge Prompt 

Sorry. You know every CTF has to have it. 🤷

## Solution

Quick google of RFC 9209 leads to robots.txt

When hitting the /robots.txt page it just shows 
![alt text](image.png)

It was only after I used curl to access the page that I saw it included a lot of empty white space. Hidden way down in the white space was the flag of `flag{aec1142c199aa5d8ad0f3ae3fa82e13c}`
![alt text](image-1.png)

