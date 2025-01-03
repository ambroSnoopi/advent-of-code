import puzzle

test = puzzle.load_puzzle('input/test.txt')
test.do(max_size=3)
expected = 12
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

test.do(max_size=3, starts_with="t")
expected = 7
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

test.do(starts_with="t")
expected = 'co,de,ka,ta'
actual = test.check_p2()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = puzzle.load_puzzle('input/quest.txt')
quest.do(max_size=3, starts_with="t")
actual = quest.checksum()
print("Quest Checksum:", actual)

expected = 1119
assert expected==actual, f"Part 1 failed!\n  Expected: {expected}\n  Actual: {actual}"

quest.do(starts_with="t")
p2 = quest.check_p2()
print("Quest Checksum Part 2:", p2)
