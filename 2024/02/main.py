# %%

def check_safety(report: list[int], skip=-1) -> int:
    """
    Checks safety of a report.

    Args:
        report (list[int]): The levels in a report.
        skip: Index of a level in the report to be skipped.

    Returns:
        int: The index of the first level that was unsafe. Or -1 if safe.
    """
    const_dir = True
    valid_dif = True

    last_level: int = None
    last_cmp: int = None
    for index, level in enumerate(report):
        if index == skip: continue
        if last_level is None: 
            last_level = level
            continue

        cmp = (last_level > level) - (last_level < level)
        if last_cmp is not None:
            const_dir = const_dir and cmp != 0 and cmp == last_cmp

        dif = abs(last_level - level)
        valid_dif = valid_dif and (1 <= dif <=3)

        if not (const_dir and valid_dif):
            return index
        
        last_cmp = cmp
        last_level = level

    return -1

def problem_dampener(report: list[int]) -> bool:
    """
    The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

    Args:
        report (list[int]): The levels in a report.

    Return:
        bool: True if Safe
    """
    failed_level = check_safety(report)
    if failed_level < 0: return True

    #the only way to fix a failed level should be by either removing that level itself or any adjacents
    for x in range(failed_level-1, failed_level+1):
        failed_level = check_safety(report, x)
        if failed_level < 0: return True
    return False
    
reports = {
    "toproc": [],
    "unsafe": [],
    "safe": []
}
with open("input.csv", "r") as file:
    for line in file:
        levels = list(map(int, line.split()))
        reports["toproc"].append(levels)
# %%
for report in reports["toproc"]:
    
    is_safe = problem_dampener(report)

    if is_safe:
        reports["safe"].append(report)
    else:
        reports["unsafe"].append(report)
    
print(len(reports["toproc"])) #1000
print(len(reports["unsafe"])) # 476 -> 432
print(len(reports["safe"]))   # 524 -> 568
# %%
