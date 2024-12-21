from enum import Enum
from dataclasses import dataclass
from tqdm import tqdm
import networkx as nx

class Direction(Enum):
    UP = ('^', 0, -1)
    RIGHT = ('>', 1, 0)
    DOWN = ('v', 0, 1)
    LEFT = ('<', -1, 0)

    def __str__(self):
        return self.value[0]
    
    @property
    def symbol(self) -> str:
        return self.value[0]
    
    @property
    def dx(self) -> int:
        return self.value[1]
    
    @property
    def dy(self) -> int:
        return self.value[2]

@dataclass
class Button:
    x: int
    y: int
    char: str #transient

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Button):
            return (self.x, self.y) == (other.x, other.y)
        return False
    
    def __str__(self):
        return str(self.char)
    
    def to_node(self):
        return (self.y, self.x)
    
    def distance(self, other: 'Button') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

class Keybad:
    def __init__(self, buttons: list[Button]):
        self.buttons = buttons
        self.graph = nx.Graph()
        
        # Add all buttons as nodes
        for button in self.buttons:
            self.graph.add_node(button.to_node())
        
        # Connect adjacent buttons
        for b1 in self.buttons:
            for b2 in self.buttons:
                if b1 != b2 and b1.distance(b2) == 1:  # Adjacent buttons are 1 unit apart
                    self.graph.add_edge(b1.to_node(), b2.to_node())

class Puzzle:
    def __init__(self, data):
        self.pincodes: list[str] = data
        self.numbad = Keybad([  Button(0, 0, '7'), Button(1, 0, '8'), Button(2, 0, '9'),
                                Button(0, 1, '4'), Button(1, 1, '5'), Button(2, 1, '6'),
                                Button(0, 2, '1'), Button(1, 2, '2'), Button(2, 2, '3'),
                                Button(0, 3, ' '), Button(1, 3, '0'), Button(2, 3, 'A')])
        
        self.dirpad_t1=Keybad([ Button(0, 0, ' '), Button(1, 0, '^'), Button(2, 0, 'A'),
                                Button(0, 1, '<'), Button(1, 1, 'v'), Button(2, 1, '>')])
        
        self.dirpad_t2=Keybad([ Button(0, 0, ' '), Button(1, 0, '^'), Button(2, 0, 'A'),
                                Button(0, 1, '<'), Button(1, 1, 'v'), Button(2, 1, '>')])
        
        self.dirpad_t3=Keybad([ Button(0, 0, ' '), Button(1, 0, '^'), Button(2, 0, 'A'),
                                Button(0, 1, '<'), Button(1, 1, 'v'), Button(2, 1, '>')])
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
        data = content.strip().split('\n')
    return Puzzle(data)