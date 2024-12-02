# %%

reports = {
    "toproc": [],
    "unsafe": [],
    "safe": []
}
with open("input.csv", "r") as file:
    for line in file:
        levels = list(map(int, line.split()))
        reports["toproc"].append(levels)

print(reports)
# %%

for report in reports["toproc"]:
    const_dir: bool = True
    valid_dif: bool = True

    last_level: int = None
    last_cmp: int = None
    for level in report:
        if last_level is None: 
            last_level = level
            continue

        cmp = (last_level > level) - (last_level < level)
        if last_cmp is not None:
            const_dir = const_dir and cmp != 0 and cmp == last_cmp

        dif = abs(last_level - level)
        valid_dif = valid_dif and (1 <= dif <=3)

        last_cmp = cmp
        last_level = level

    if const_dir and valid_dif:
        reports["safe"].append(report)
    else:
        reports["unsafe"].append(report)
    
print(len(reports["toproc"])) #1000
print(len(reports["unsafe"])) # 476
print(len(reports["safe"]))   # 524
# %%
