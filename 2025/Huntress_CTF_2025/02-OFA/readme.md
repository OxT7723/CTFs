# OFA - Day 02
**Category:** Warmups
**Author:**  Matt Kiely (HuskyHacks)  



## Challenge Prompt 

Two factors? In this economy??!!

## Solution

Visiting the challenge page displays a simple login form that asks for a username and password:
![alt text](image.png)

Entering any credentials (e.g., user:test) proceeds to a second prompt for a one-time password (OTP):
![alt text](image-1.png)


I inspected the page's source code. Inside the HTML, there was a small JavaScript snippet that contained a numeric code `103248`:
![alt text](image-2.png)


Entering that `103248` code into the OTP form successfully completed the login and revealed the flag: `flag{013cb9b123afec26b572af5087364081}`
![alt text](image-3.png)

