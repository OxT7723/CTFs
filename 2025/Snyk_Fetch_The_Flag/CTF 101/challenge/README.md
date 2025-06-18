![image](https://github.com/user-attachments/assets/c98ecd62-7ff7-4a36-bc8e-d22ddc3bbc83)

# CTF 101
Welcome to the Snyk Fetch the Flag 2025 CTF 101 intro challenge! This challenge serves as an introduction to the CTF so players will be familiar with the game on game day.

## Challenge Files
Many, if not all, of the web application challenges come packaged with their source code. This makes each web app challenge into an open-book code review and exploitation challenge that will help developers fine tune their sense for vulnerable code.

All challenge source files will be packaged in `challenge.zip` which is attached to each challenge on the game board. Every web app challenge will come with the Dockerfile required to run the application. Each set of source code files also come with a dummy flag file (`flag{not_really_tho}`) which will be copied into the container in the exact location where the real flag will be. This will help remove the guess work for where the flag will be during the game.

The password for all `challenge.zip` files is `snyk-ftf-2025` 

To run an application, unzip the challenge files into a directory, change directories into the folder you just unzipped the source files into, and then build the application container:
```
$ docker build -t [challenge_name] .
```
Then, run the container. Make sure to publish the correct port for the container:
```
$ docker run -it -p [host_port]:[application_port]
```
(i.e., for the CTF 101 challenge...)
```
$ docker build -t ctf101
$ docker run -it -p 5000:5000 ctf101
```
Now, you'll have a local instance of the challenge application to analyze! This should help players discover vulnerabilities and test their proofs of concept to capture the flag.

## Solve
The CTF 101 challenge is a simple web application exploitation challenge. The player is greeted with a form to fill in:

![image](https://github.com/user-attachments/assets/d8e1f1ce-3fb6-4911-90bd-feddcf8d038c)

The player can review the source code of the application by unpacking the challenge zip file. Inside, they will see the source code for the application. The application is written in Python and there is only one file of interest: `app.py`

`app.py` houses the back-end logic for the site's form submission. 

```python
...[snip]....

try:
  # I sure hope no one tries to run any commands by injecting here...
  output = subprocess.check_output(f"echo {name}", shell=True, text=True, stderr=subprocess.STDOUT)
  flash(f"Hello, {output.strip()}! Good luck!", "success")
  # ...alright, the challenges won't be this obvious on game day, but I hope it gives you a good idea of how the game is played!

...[snip]...
```
The use of the `subprocess.check_output()` method with the `shell=True` parameter is a dead giveaway that this form is probably vulnerable to OS command injection. We can check this by attempting to terminate the echo command and injecting an arbitrary command to execute:

![image](https://github.com/user-attachments/assets/efc9efc2-b2ed-4967-bcf9-126d8c56863f)

![image](https://github.com/user-attachments/assets/ee198b07-4355-4f33-8e3c-8b3f056a97d2)


We would also know the location of the flag from reading the Dockerfile:

```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY app/ /app

RUN pip install flask

EXPOSE 5000

COPY flag.txt /app/flag.txt

CMD ["python", "app.py"]
```

Therefore, all we need to do is inject a command into the form to read the contents of the flag.txt file!

![image](https://github.com/user-attachments/assets/2c33e6c9-813e-40b4-b0be-8bb37992abeb)

On game day, the challenges will be much more involved. But the general approach will be the same:
- Read the application's source code if it's available.
- Stand up a local instance for testing.
- Identify any vulnerable code.
- Build and test a proof of concept to exploit the vulnerable code.
- and finally... fetch the flag!

## Snyk CLI
While manual source code review is an excellent practice, you *may* be able to gain an advantage by using the [Snyk CLI](https://docs.snyk.io/snyk-cli) to identify vulnerabilities faster. Give it a shot! You never know what it might find...

![image](https://github.com/user-attachments/assets/a4a798df-8677-4a3a-85f2-8d7be6f38050)
