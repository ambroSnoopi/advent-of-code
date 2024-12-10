import puzzle

test = puzzle.load_puzzle('input/test.txt')
test.discover_trails()
expected = 36
actual = test.score
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

test = puzzle.load_puzzle('input/test.txt')
test.discover_trails()
expected = 81
actual = test.rating
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = puzzle.load_puzzle('input/quest.txt')
quest.discover_trails()
print(f"Map Score: {quest.score}")
print(f"Map Rating: {quest.rating}")