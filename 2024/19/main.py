import puzzle

test = puzzle.load_puzzle('input/test_towels.txt', 'input/test_designs.txt')
test.do()
expected = 6
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

expected = 16
actual = test.check_p2()
assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = puzzle.load_puzzle('input/quest_towels.txt', 'input/quest_designs.txt')
quest.do()
actual = quest.checksum()
print("Quest Checksum:", actual)

expected = 272
assert expected==actual, f"Part 1 failed!\n  Expected: {expected}\n  Actual: {actual}"

p2 = quest.check_p2()
print("Quest Checksum Part 2:", p2)