import puzzle
from tqdm import tqdm

test = puzzle.load_puzzle('input/test.txt', 11, 7)
test.tick()
expected = 12
actual = test.checksum()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"
"""
test2 = puzzle.load_puzzle('input/test.txt')
test2.do()
expected = 0123
actual = test2.checksum()
assert expected==actual, f"Test2 failed!\n  Expected: {expected}\n  Actual: {actual}"
"""
quest = puzzle.load_puzzle('input/quest.txt', 101, 103)
quest.tick()
actual = quest.checksum()
print("Quest Checksum:", actual)

part2 = puzzle.load_puzzle('input/quest.txt', 101, 103)
n_max = 101 * 103
for n in tqdm(range(n_max), desc="Looking for a christmas tree...", unit="tick"):
    part2.tick(1)

    if part2.may_look_like_a_christmas_tree():
        print("\n\n")
        print(f"Grid after {n} seconds:")
        print(part2)