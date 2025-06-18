from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import requests

with open('public_key.pem', 'r') as f:
    key = RSA.importKey(f.read())

cipher = PKCS1_v1_5.new(key)

guesses = [b"This is the admin secret!", b"FLAG{test}", b"FLAG{admin_wins}"]

for guess in guesses:
    encrypted = cipher.encrypt(guess).hex()
    cookies = {'secret': encrypted}
    r = requests.get("http://challenge.nahamcon.com:32374/cookie", cookies=cookies)
    print(f"[+] Trying: {guess} -> {r.text}")
