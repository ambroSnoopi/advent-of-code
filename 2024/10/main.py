import puzzle

test = puzzle.load_puzzle('input/test.txt')
expected = 36
actual = test.find_trails()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"
"""
test2 = puzzle.load_puzzle('input/test.txt')
expected = 0123
actual = test2.find_trails()
assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"
"""
quest = puzzle.load_puzzle('input/quest.txt')
actual = quest.find_trails()
print(f"Quest Checksum: {actual}")