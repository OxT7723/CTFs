import re
import math

# Define the weights for the skills
weights = {
    "health": 0.2,
    "agility": 0.3,
    "charisma": 0.1,
    "knowledge": 0.05,
    "energy": 0.05,
    "resourcefulness": 0.3
}

# Function to calculate skill score
def calculate_skill_score(skill, weight):
    return round(6 * (int(skill) * weight)) + 10

# Function to calculate overall value
def calculate_overall_value(skills):
    return round(5 * (
        (skills["health"] * 0.18) + 
        (skills["agility"] * 0.20) + 
        (skills["charisma"] * 0.21) + 
        (skills["knowledge"] * 0.08) + 
        (skills["energy"] * 0.17) + 
        (skills["resourcefulness"] * 0.16)
    ))

# Read the data from the file
with open('data.txt', 'r') as file:
    lines = file.readlines()

# Define the regex pattern to parse the data
pattern = re.compile(r'\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')

# Parse the data
candidates = []
for line in lines[3:]:  # Skip the first 3 lines (headers and separator)
    match = pattern.match(line)
    if match:
        first_name, last_name, *skills = match.groups()
        skill_scores = {k: calculate_skill_score(v, weights[k]) for k, v in zip(weights.keys(), skills)}
        overall_value = calculate_overall_value(skill_scores)
        candidates.append((f"{first_name} {last_name}", overall_value))

# Sort candidates by overall value in descending order
candidates.sort(key=lambda x: x[1], reverse=True)

# Output the first 14 candidates
top_14 = candidates[:14]
output = ', '.join([f"{name} - {score}" for name, score in top_14])
print(output)
