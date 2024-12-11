import puzzle

test = puzzle.load_puzzle('input/test.txt')
test.blink(25)
expected = 55312
actual = test.total_stones()
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
post25 = quest.total_stones()
print(f"No of Stones after 25 blinks: {post25}")
quest.blink(50)
post75 = quest.total_stones()
print(f"No of Stones after 75 blinks: {post75}")