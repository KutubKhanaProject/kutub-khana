import json

# Load the JSON file from the correct path
with open('minimal_urdu_texts.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Check the structure and count entries
if isinstance(data, list):
    num_texts = len(data)
elif isinstance(data, dict):
    num_texts = len(data.keys())
else:
    num_texts = 0

print(f"Number of texts in the JSON file: {num_texts}")
