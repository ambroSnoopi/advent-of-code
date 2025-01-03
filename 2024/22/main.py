import puzzle

test0 = puzzle.load_puzzle('input/test0.txt')
test0.do()
expected = [
    15887950
   , 16495136
   , 527345
   , 704524
   , 1553684
   , 12683156
   , 11100544
   , 12249484
   , 7753432
   , 5908254
]
actual = [seq[0] for seq in test0.sequences[123][:10]]
assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"

test = puzzle.load_puzzle('input/test.txt')
test.do()
expected = 37327623
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

test2 = puzzle.load_puzzle('input/test2.txt')
test2.do()
expected = 23
actual = test2.check_p2()
assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = puzzle.load_puzzle('input/quest.txt')
quest.do()
actual = quest.checksum()
print("Quest Checksum:", actual)

expected = 14180628689
assert expected==actual, f"Part 1 failed!\n  Expected: {expected}\n  Actual: {actual}"

p2 = quest.check_p2()
print("Quest Checksum Part 2:", p2) #1690
