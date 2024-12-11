
class PlutonianPebbles:

    def __init__(self, data: str):
        self.stones: list[int] = []
        for digit in data.split(' '):
            engraving = int(digit)
            self.stones.append(engraving)

    def blink(self, repeat=1):
        for _ in range(repeat):
            idx = 0
            for _ in self.stones:
                if idx == len(self.stones):
                    break
                engraving = self.stones[idx]
                if engraving == 0:
                    self.stones[idx] = 1
                elif len(str(engraving)) % 2 == 0:
                    engraving_str = str(engraving)
                    half_len = int(len(engraving_str)/2)
                    engr1 = int(engraving_str[:half_len])
                    engr2 = int(engraving_str[half_len:])
                    self.stones[idx] = engr1
                    idx += 1
                    self.stones.insert(idx, engr2)
                else:
                    self.stones[idx] = engraving*2024
                idx += 1


def load_puzzle(filename: str):
    with open(filename, 'r') as file:
        return PlutonianPebbles(file.read())