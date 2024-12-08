import puzzle

test = puzzle.load_puzzle('input/test.txt')
test.create_antinodes()
expected = 14
actual = len(test.antinodes)
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"


quest = puzzle.load_puzzle('input/quest.txt')
quest.create_antinodes()
actual = len(quest.antinodes)
print(actual)