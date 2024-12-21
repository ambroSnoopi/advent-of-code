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
    
    @classmethod
    def from_delta(cls, dx: int, dy: int) -> 'Direction':
        for dir in cls:
            if dir.dx == dx and dir.dy == dy:
                return dir
        raise ValueError(f"No Direction matches delta: ({dx}, {dy})")

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
    
    def delta(self, other: 'Button') -> tuple[int, int]:
        return (other.x - self.x, other.y - self.y)

class Keypad:
    def __init__(self, buttons: list[Button]):
        self.buttons = buttons

        self.graph = nx.Graph()
        self.graph.add_nodes_from(self.buttons)
        for b1 in self.buttons:
            for b2 in self.buttons:
                if b1 != b2 and b1.distance(b2) == 1:
                    self.graph.add_edge(b1, b2)
        #self.graph.remove_node(self.button_from_char(' ')) # remove the empty button

    def button_from_char(self, char: str) -> Button:
        #TODO: raise ValueError instead if char not in buttons
        return next(b for b in self.buttons if b.char == char)
    
    def shortest_path_for_pin(self, pin: str) -> list[list[Button]]:
        """ Gives the shortest path for a pin (series of Buttons as str), grouped by Button in separat lists. """
        path: list[tuple[Button]] = []
        for start, goal in zip(pin, pin[1:]):
            start = self.button_from_char(start)
            goal = self.button_from_char(goal)
            path_for_button = nx.shortest_path(self.graph, start, goal)
            #path_for_button.remove(start)
            path.append(path_for_button)
            #if self.button_from_char(' ') in path:
            #    raise ValueError("Path contains empty button! Panic ensues!")
        return path
    
    def directions_for_pin(self, pin: str) -> str:
        """ Gives the directions for a pin (series of Buttons as str), separated by "A" for Button-presses. """
        path = self.shortest_path_for_pin(pin)
        directions = ""
        for button_path in path:
            for start, goal in zip(button_path, button_path[1:]):
                dx, dy = start.delta(goal)
                directions += (Direction.from_delta(dx, dy).symbol)
            directions += "A"
        return directions

class Puzzle:
    def __init__(self, data):
        self.pincodes: list[str] = data
        self.numpad = Keypad([  Button(0, 0, '7'), Button(1, 0, '8'), Button(2, 0, '9'),
                                Button(0, 1, '4'), Button(1, 1, '5'), Button(2, 1, '6'),
                                Button(0, 2, '1'), Button(1, 2, '2'), Button(2, 2, '3'),
                                                   Button(1, 3, '0'), Button(2, 3, 'A')])
                               #Button(0, 3, ' '), Button(1, 3, '0'), Button(2, 3, 'A')])
        
        self.dirpad_t1=Keypad([#Button(0, 0, ' '), Button(1, 0, '^'), Button(2, 0, 'A'),
                                                   Button(1, 0, '^'), Button(2, 0, 'A'),
                                Button(0, 1, '<'), Button(1, 1, 'v'), Button(2, 1, '>')])
        
        self.dirpad_t2=Keypad([                    Button(1, 0, '^'), Button(2, 0, 'A'),
                                Button(0, 1, '<'), Button(1, 1, 'v'), Button(2, 1, '>')])
        
        self.instructions: list[str] = []

    @classmethod
    def extract_numpart(cls, pin: str) -> int:
        num_part = ""
        for char in pin:
            if char.isdigit():
                num_part += char
        return int(num_part)
    
    def do(self):
        for pin in self.pincodes:
            dir_t1 = self.numpad.directions_for_pin("A"+pin)
            dir_t2 = self.dirpad_t1.directions_for_pin("A"+dir_t1)
            dir_t3 = self.dirpad_t2.directions_for_pin("A"+dir_t2)
            self.instructions.append(dir_t3)

    def checksum(self):
        r = 0
        for pin, instr in zip(self.pincodes, self.instructions):
            r += Puzzle.extract_numpart(pin) * len(instr)
        return r
    
    def check_p2(self):
        pass

def load_puzzle(input_file: str) -> Puzzle:
    """Load Puzzle from input file (path)."""
    with open(input_file, 'r') as file:
        content = file.read()
        data = content.strip().split('\n')
    return Puzzle(data)