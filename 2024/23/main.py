import puzzle

test = puzzle.load_puzzle('input/test.txt')
test.do()
expected = 12
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

expected = 7
actual = test.checksum(starts_with="t")
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"
"""
test2 = puzzle.load_puzzle('input/test.txt')
test2.do()
expected = 0123
actual = test2.checksum()
assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"

#or

expected = 01234
actual = test.check_p2()
assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"
"""
quest = puzzle.load_puzzle('input/quest.txt')
quest.do()
actual = quest.checksum(starts_with="t")
print("Quest Checksum:", actual)
"""
expected = 0123
assert expected==actual, f"Part 1 failed!\n  Expected: {expected}\n  Actual: {actual}"

p2 = quest.check_p2()
print("Quest Checksum Part 2:", p2)
"""