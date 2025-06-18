# Given octal numbers as a string
octal_numbers = "146 154 141 147 173 061 064 145 060 067 062 146 067 060 065 144 064 065 070 070 062 064 060 061 144 061 064 061 143 065 066 062 146 144 143 060 142 175"

# Split the string into individual octal numbers
octal_list = octal_numbers.split()

# Convert octal to ASCII
readable_text = ''.join(chr(int(octal, 8)) for octal in octal_list)

print(readable_text)
