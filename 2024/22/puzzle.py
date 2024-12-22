from tqdm import tqdm

class Puzzle:
    def __init__(self, secrets: list[int]):
        self.secrets = secrets
        self.sequences: dict[int, list[int]] = {} # secret -> sequence

    @staticmethod
    def mix_n_prune(secret: int, interim: int) -> int:
        return (secret ^ interim) % 16777216
    
    def next_secret(self, secret: int) -> int:
        interim = secret * 64
        secret = self.mix_n_prune(secret, interim)

        interim = secret // 32
        secret = self.mix_n_prune(secret, interim)

        interim = secret * 2048
        secret = self.mix_n_prune(secret, interim)
        return secret

    def do(self):
        for secret in tqdm(self.secrets, desc="Computing sequences", unit="secret"):
            sequences = []
            seq = secret
            for _ in range(2000):
                seq = self.next_secret(seq)
                sequences.append(seq)
            self.sequences[secret] = sequences

    def checksum(self):
        total_sum = 0
        for sequence in self.sequences.values():
            total_sum += sequence[-1]
        return total_sum
    
    def check_p2(self):
        pass

def load_puzzle(input_file: str) -> Puzzle:
    """Load Puzzle from input file (path)."""
    with open(input_file, 'r') as file:
        content = file.read()
        lines = content.strip().split('\n')
        data = [int(line) for line in lines]
    return Puzzle(data)