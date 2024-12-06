import wordsearch as ws
from tqdm import tqdm

test = ws.load_puzzle('input/test.txt')
expected = 18
actual = test.count_word()
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = ws.load_puzzle('input/quest.txt')
print(quest.count_word()) #2591