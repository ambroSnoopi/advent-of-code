import puzzle

test = puzzle.load_puzzle('input/test1.txt')
test.do()
expected = 7036
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

test2 = puzzle.load_puzzle('input/test2.txt')
test2.do()
expected = 11048
actual = test2.checksum()
assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = puzzle.load_puzzle('input/quest.txt')
quest.do()
actual = quest.checksum()
print("Quest Checksum:", actual)