import puzzle

test = puzzle.load_puzzle('input/test1.txt', 12, 7)
test.do()
expected = 22
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

#test.do(100, 7036)
#expected = 45
#actual = len(test.get_best_path_cells())
#assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"
#
#test2 = puzzle.load_puzzle('input/test2.txt')
#test2.do()
#expected = 11048
#actual = test2.checksum()
#assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"
#
#test2.do(50, 11048)
#expected = 64
#actual = len(test2.get_best_path_cells())
#assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = puzzle.load_puzzle('input/quest.txt', 1024, 71)
quest.do()
best_score = quest.checksum()
print("Quest Best Score:", best_score)