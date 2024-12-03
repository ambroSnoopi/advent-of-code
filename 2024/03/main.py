# %%
import re

# mul(X,Y), where X and Y are each 1-3 digit numbers
pattern = r"mul\(\d{1,3},\d{1,3}\)"

with open("input.txt", "r") as file:
    content = file.read()
matches = re.findall(pattern, content)

print(matches)

# %%
results = []
for match in matches:
    x,y = map(int, match[4:-1].split(','))
    results.append(x * y)
total = sum(results)
print(results)
print(total)

# %%
