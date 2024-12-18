import puzzle

test = puzzle.load_puzzle('input/test1.txt', 12, 7)
test.do()
expected = 22
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

expected = (6, 1)
actual = test.find_critical_corruption()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = puzzle.load_puzzle('input/quest.txt', 1024, 71)
quest.do()
best_score = quest.checksum()
print("Quest Best Score:", best_score)
expected = 294
assert expected==best_score, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}" 

quest.viz("Before further corruption")
crit = quest.find_critical_corruption()
print("The first byte to break the critical path is:", crit)
expected = (31, 22)
assert expected==crit, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}" 
quest.viz("After critical corruption")