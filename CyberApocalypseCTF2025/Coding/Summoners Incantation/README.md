# Summoners Incantation

**Creator:** ch4p

**Description:** To awaken the ancient power of the Dragon's Heart, the summoners must combine magical incantation tokens. However, the tokens are delicate; no two adjacent tokens can be combined without losing their energy. The optimal incantation is the maximum sum obtainable by choosing non-adjacent tokens.

**Category:** Coding

**Difficulty:** very easy

## Solution 


```python 
# Input the text as a single string
input_text = input()  # Example: "shock;979;23"

# Write your solution below and make sure to encode the word correctly

tokens = eval(input_text)

if not tokens:
    print(0)
elif len(tokens) == 1:
    print(tokens[0])
else:
    prev1 = max(tokens[0], tokens[1])
    prev2 = tokens[0]

    for i in range(2, len(tokens)):
        current = max(prev1, prev2 + tokens[i])
        prev2 = prev1
        prev1 = current
    
    print(prev1)
```

Flag of `HTB{SUMM0N3RS_INC4NT4T10N_R3S0LV3D_7305466de02e687b23c162bcffefcd64}`
