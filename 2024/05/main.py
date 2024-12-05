# %%
before_than: dict[int, set[int]] = {}
later_than: dict[int, set[int]] = {}
with open("input/ordering_rules.csv", "r") as file:
    for line in file:
        ordering_rule = list(map(int, line.split('|')))
        first = ordering_rule[0]
        after = ordering_rule[1]
        if after in before_than:
            before_than[after].add(first) 
        else:
            before_than[after] = {first}
        if first in later_than:
            later_than[first].add(after)
        else:
            later_than[first] = {after}

print(before_than)
print(later_than)

def validate_page_order(update: list[int]) -> bool:
    isInOrder = True
    for index, page in enumerate(update):
        prior = set(update[:index])
        after = set(update[index:])
        # since the update may contain pages that are not specified in the ordering_rules we have to check for violations rather then compliance
        isInOrder = isInOrder and after.isdisjoint(before_than.get(page)) and prior.isdisjoint(later_than.get(page))
        if not isInOrder: break
    return isInOrder
# %%
updates = {
    "toproc": [],
    "ordered": [],
    "disordered": []
}
with open("input/updates.csv", "r") as file:
    for line in file:
        update = list(map(int, line.split(',')))
        updates["toproc"].append(update)

middle_pages: list[int] = []
for update in updates["toproc"]:
    isInOrder = validate_page_order(update)
    if isInOrder:
        updates["ordered"].append(update)
        middle_pages.append(update[int((len(update)-1)/2)])
    #else: updates["disordered"].append(update) #if we need for part2...

print(sum(middle_pages))