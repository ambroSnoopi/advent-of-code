import puzzle

test = puzzle.load_puzzle('input/test.txt')
test.compact()
expected = 1928
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

test2 = puzzle.load_puzzle('input/test.txt')
test2.compact_files()
expected = 2858
actual = test2.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = puzzle.load_puzzle('input/quest.txt')
quest.compact_files()
actual = quest.checksum()
print(actual)