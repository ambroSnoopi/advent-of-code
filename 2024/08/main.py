import puzzle

test = puzzle.load_puzzle('input/test.txt')
test.create_antinodes(resonance=True)
expected = 34 # 14
actual = len(test.antinodes)
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"


quest = puzzle.load_puzzle('input/quest.txt')
quest.create_antinodes(resonance=True)
actual = len(quest.antinodes)
print(actual)