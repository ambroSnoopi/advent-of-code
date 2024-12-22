from tqdm import tqdm
import pandas as pd

class Puzzle:
    def __init__(self, secrets: list[int]):
        self.secrets = secrets
        self.sequences: dict[int, list[tuple[int,int,int,list[int]]]] = {} # secret -> sequences(secret, price, change, change_seq)
        self.df_top_seq: pd.DataFrame

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
    
    def gen_sequences(self, n=2000):
        for secret in tqdm(self.secrets, desc="Computing sequences", unit="secret"):
            sequences: list[tuple[int,int,int,list[int]]] = [] # (secret, price, change, change_seq)
            seq = secret
            change_seq = [None, None, None, None]
            for _ in range(n):
                old_bananas = self.bananas_from_secret(seq)
                seq = self.next_secret(seq)
                new_bananas = self.bananas_from_secret(seq)
                change = new_bananas - old_bananas
                change_seq.pop(0)
                change_seq.append(change)
                changes = change_seq.copy()
                sequences.append((seq, new_bananas, change, changes))

            self.sequences[secret] = sequences
    
    def calc_top_change_seq(self):
        df_master = pd.DataFrame(columns=["secret", "price", "change", "change_seq", "base"])
        for base, seq in self.sequences.items():
            df = pd.DataFrame(seq, columns=["secret", "price", "change", "change_seq"])
            df["base"] = base
            df_master = pd.concat([df_master, df])
        df_master['change_str'] = df_master['change_seq'].astype(str)
        self.df_top_seq = df_master[['change_str', 'price']].groupby(['change_str']).sum().sort_values(by='price', ascending=False)
    
    def do(self):
        self.gen_sequences(2000)
        self.calc_top_change_seq()

    def checksum(self):
        total_sum = 0
        for sequence in self.sequences.values():
            total_sum += sequence[-1][0]
        return total_sum
    
    def check_p2(self):
        return self.df_top_seq.values.item(0)

def load_puzzle(input_file: str) -> Puzzle:
    """Load Puzzle from input file (path)."""
    with open(input_file, 'r') as file:
        content = file.read()
        lines = content.strip().split('\n')
        data = [int(line) for line in lines]
    return Puzzle(data)