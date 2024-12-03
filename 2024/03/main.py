# %%
import re

# everything between "do()" and "don't()"
do_pattern = r"(?<=do\(\)).*?(?=don't\(\))"

# mul(X,Y), where X and Y are each 1-3 digit numbers
mul_pattern = r"mul\(\d{1,3},\d{1,3}\)"

with open("input.txt", "r") as file:
    content = file.read()

idx_first_dont = content.find("don't()")
idx_last_do = content.rfind("do()")
idx_last_dont = content.rfind("don't()")
does = re.findall(do_pattern, content[idx_first_dont:])
does.append(content[:idx_first_dont]) #there is none, so this doesn't actually matter
if idx_last_do > idx_last_dont: #let's prettend we didn't know that is the case and didn't need a second attempt to catch this edge case
    does.append(content[idx_last_do:])

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
print(total) #Part 1: 182'619'815  // Part 2: 61'054'530 (f) -> 63'518'894 (f)

# %%
