import puzzle

test = puzzle.load_puzzle('input/test1_map.txt', 'input/test1_moves.txt')
test.do()
expected = 2028
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

test2 = puzzle.load_puzzle('input/test2_map.txt', 'input/test2_moves.txt')
test2.do()
expected = 10092
actual = test2.checksum()
assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = puzzle.load_puzzle('input/quest_map.txt', 'input/quest_moves.txt')
quest.do()
actual = quest.checksum()
print("Quest Checksum:", actual)