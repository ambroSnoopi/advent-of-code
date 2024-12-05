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

# %%
def validate_page_order(update: list[int]) -> bool:
    isInOrder = True
    for index, page in enumerate(update):
        prior = set(update[:index])
        after = set(update[index:])
        # since the update may contain pages that are not specified in the ordering_rules we have to check for violations rather then compliance
        isInOrder = isInOrder and after.isdisjoint(before_than.get(page)) and prior.isdisjoint(later_than.get(page))
        if not isInOrder: break
    return isInOrder

def order_pages(update: list[int], debug=False) -> list[int]:
    if debug: print(f"Original update: {update}")
    ordered_update: list[int] = []
    for page in update:
        if not ordered_update:
            ordered_update.append(page)
            continue #i.e. skip first iter

        inserted = False
        for i, p in enumerate(ordered_update):
            if page in before_than.get(p): 
                ordered_update.insert(i, page)
                inserted = True
                if debug: 
                    print(f"Page {page} was inserted before {p}.")
                    print(f"Ordered update: {ordered_update}")
                break
        if inserted: continue

        ordered_update.reverse()
        for i, p in enumerate(ordered_update):
            if page in later_than.get(p): 
                ordered_update.insert(i, page)
                inserted = True
                if debug: print(f"Page {page} was inserted after {p}.")
                break
        ordered_update.reverse()
        
        if not inserted:
            ordered_update.append(page) # if it wasn't in either rule set, we should be able to just append it, right?
            if debug: print(f"Page {page} was appended.")
        if debug: print(f"Ordered update: {ordered_update}")
    assert validate_page_order(ordered_update), f"Ordering failed!\n  Original update: {update}\n  Disordered update: {ordered_update}"

    return ordered_update

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

ordered_middle_pages: list[int] = []
disordered_middle_pages: list[int] = []
for update in updates["toproc"]:
    isInOrder = validate_page_order(update)
    if isInOrder:
        updates["ordered"].append(update)
        ordered_middle_pages.append(update[int((len(update)-1)/2)])
    else: # i knew it! :D
        ordered_update = order_pages(update)
        updates["disordered"].append(ordered_update)
        disordered_middle_pages.append(ordered_update[int((len(update)-1)/2)])

print(sum(disordered_middle_pages))
# %%
