import wordsearch as ws
from tqdm import tqdm

test = ws.load_puzzle('input/test.txt')
expected = 18
actual = test.count_word()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = ws.load_puzzle('input/quest.txt')
print(quest.count_word()) #2591

test_p2 = ws.load_puzzle('input/test-p2.txt')
expected = 9
actual = test_p2.count_x()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

expected = 9
actual = test.count_x()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

print(quest.count_x()) # <2505!