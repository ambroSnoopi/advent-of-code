import puzzle

test = puzzle.load_puzzle('input/test.txt', 11, 7)
test.tick()
expected = 12
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"
"""
test2 = puzzle.load_puzzle('input/test.txt')
test2.do()
expected = 0123
actual = test2.checksum()
assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"
"""
quest = puzzle.load_puzzle('input/quest.txt', 101, 103)
quest.tick()
actual = quest.checksum()
print("Quest Checksum:", actual)