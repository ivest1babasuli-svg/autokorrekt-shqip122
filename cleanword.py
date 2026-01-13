import re

input_file = "raw_words.txt"
output_file = "clean_words.txt"

with open(input_file, encoding="utf-8") as f:
    lines = f.readlines()

cleaned = []

for line in lines:
    line = line.strip()
    word = re.sub(r"/.*", "", line)
    if word:
        cleaned.append(word)

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(cleaned))

print(f"Done! Saved {len(cleaned)} words to {output_file}")
