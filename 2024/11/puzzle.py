from tqdm import tqdm

class PlutonianPebbles:

    def __init__(self, data: str):
        self.stones = [int(digit) for digit in data.split()]

    def blink(self, repeat=1):
        for _ in tqdm(range(repeat), desc="Blinking...", unit="blinks"):
            new_stones = [] # eliminating idx mgmnt by using a new list
            for engraving in self.stones:
                engraving_str = str(engraving)
                str_len = len(engraving_str)
                if engraving == 0:
                    new_stones.append(1)
                elif str_len % 2 == 0:
                    half_len = str_len // 2  # integer division is faster
                    new_stones.extend([ # appending both parts at once
                        int(engraving_str[:half_len]),
                        int(engraving_str[half_len:])
                    ])
                else:
                    new_stones.append(engraving * 2024)
            self.stones = new_stones


def load_puzzle(filename: str):
    with open(filename, 'r') as file:
        return PlutonianPebbles(file.read())