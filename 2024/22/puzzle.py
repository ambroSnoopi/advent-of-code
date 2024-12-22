from tqdm import tqdm

class Puzzle:
    def __init__(self, secrets: list[int]):
        self.secrets = secrets
        self.sequences: dict[int, list[tuple[int,int,int]]] = {} # secret -> sequences(secret, price, change)

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

    @staticmethod
    def bananas_from_secret(secret: int):
        return secret % 10
    
    def proc_sequences(self, n=2000):
        for secret in tqdm(self.secrets, desc="Computing sequences", unit="secret"):
            sequences: list[tuple[int,int,int]] = [] # (secret, price, change)
            seq = secret
            for _ in range(n):
                old_bananas = self.bananas_from_secret(seq)
                seq = self.next_secret(seq)
                new_bananas = self.bananas_from_secret(seq)
                change = new_bananas - old_bananas
                sequences.append((seq, new_bananas, change))

            self.sequences[secret] = sequences
    
    def do(self):
        self.proc_sequences(2000)

    def checksum(self):
        total_sum = 0
        for sequence in self.sequences.values():
            total_sum += sequence[-1][0]
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