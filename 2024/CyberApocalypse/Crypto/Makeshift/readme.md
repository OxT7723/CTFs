# Makeshift 

**Description:** Weak and starved, you struggle to plod on. Food is a commodity at this stage, but you can’t lose your alertness - to do so would spell death. You realise that to survive you will need a weapon, both to kill and to hunt, but the field is bare of stones. As you drop your body to the floor, something sharp sticks out of the undergrowth and into your thigh. As you grab a hold and pull it out, you realise it’s a long stick; not the finest of weapons, but once sharpened could be the difference between dying of hunger and dying with honour in combat.

**Category:** Crypto

**Difficulty:** very easy

**File:** [crypto_makeshift.zip](crypto_makeshift.zip)

## Solution 

Using the code provided, I worked with the string from the output.txt file:

```python
FLAG = "!?}De!e3d_5n_nipaOw_3eTR3bt4{_THB"

flag = FLAG[::-1]
new_flag = ''

for i in range(0, len(flag), 3):
    new_flag += flag[i+1]
    new_flag += flag[i+2]
    new_flag += flag[i]

print(new_flag)
```

Running the script retrieves the flag: `HTB{4_b3tTeR_w3apOn_i5_n3edeD!?!}`