from tqdm import tqdm
from collections import Counter

class PlutonianPebbles:

    def __init__(self, data: str):
        self.stones = Counter(int(x) for x in data.split()) # let's process every unique engraving only once!

    def blink(self, repeat=1):
        for _ in tqdm(range(repeat), desc="Blinking...", unit="blink"):
            new_stones = Counter()
            for engraving, count in self.stones.items():
                engraving_str = str(engraving)
                str_len = len(engraving_str)
                if engraving == 0:
                    new_stones[1] += count
                elif str_len % 2 == 0:
                    half_len = str_len // 2  # integer division is faster
                    new_stones[int(engraving_str[:half_len])] += count
                    new_stones[int(engraving_str[half_len:])] += count
                else:
                    new_stones[engraving * 2024] += count
            self.stones = new_stones

    def total_stones(self):
        return sum(self.stones.values())

def load_puzzle(filename: str):
    with open(filename, 'r') as file:
        return PlutonianPebbles(file.read())