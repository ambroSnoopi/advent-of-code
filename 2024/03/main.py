# %%
import re

# everything between "do()" and "don't()"
do_pattern = r"(?<=do\(\)).*?(?=don't\(\))"

# mul(X,Y), where X and Y are each 1-3 digit numbers
mul_pattern = r"mul\(\d{1,3},\d{1,3}\)"

with open("input.txt", "r") as file:
    content = file.read()

# let's save us the edge case handling and round up the edges instead...
does = re.findall(do_pattern, "do()"+content+"don't()")

matches = []
for do in does:
    matches.extend(re.findall(mul_pattern, do))

print(does)
print(matches)

# %%
results = []
for match in matches:
    x,y = map(int, match[4:-1].split(','))
    results.append(x * y)
total = sum(results)
print(results) 
print(total) #Part 1: 182'619'815  // Part 2: 61'054'530 (f) -> 63'518'894 (f) -> 65'949'847 (f)

# %%
