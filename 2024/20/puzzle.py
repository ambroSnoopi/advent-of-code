from enum import Enum
from tqdm import tqdm
import networkx as nx

class Puzzle:
    def __init__(self, data):
        pass

    def do(self):
        pass

    def checksum(self):
        pass
    
    def check_p2(self):
        pass

def load_puzzle(input_file: str) -> Puzzle:
    """Load Puzzle from input file (path)."""
    with open(input_file, 'r') as file:
        content = file.read()
        lines = content.strip().split('\n')
        data = [x for x in lines]
    return Puzzle(data)