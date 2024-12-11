import puzzle

test = puzzle.load_puzzle('input/test.txt')
test.blink(25)
expected = 55312
actual = len(test.stones)
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"
"""
test2 = puzzle.load_puzzle('input/test.txt')
test2.do()
expected = 0123
actual = test2.checksum()
assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"
"""
quest = puzzle.load_puzzle('input/quest.txt')
quest.blink(25)
actual = len(quest.stones)
print(f"Quest Checksum: {actual}")