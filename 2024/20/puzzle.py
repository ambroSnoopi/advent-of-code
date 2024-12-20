from enum import Enum
from dataclasses import dataclass
from tqdm import tqdm
import numpy as np
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

class Ptype(Enum):
    WALL  = '#'
    EMPTY = '.'

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value

@dataclass
class Cell:
    x: int
    y: int
    ptype: Ptype #transient

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.x, self.y) == (other.x, other.y)
        return False
    
    def __str__(self):
        return str(self.ptype)
    
    def to_node(self):
        return (self.y, self.x)

class Map:
    def __init__(self, map_data: str):
        lines = map_data.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0
        self.cells = np.empty((self.height, self.width), dtype=Cell)
        self.start: Cell
        self.goal: Cell
        self.track: list[Cell] = []
        # Parse the input and populate the grid 
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "S":
                    c = Cell(x, y, Ptype.EMPTY)
                    self.start = c
                elif char == "E":
                    c = Cell(x, y, Ptype.EMPTY)
                    self.goal = c
                else:
                    ptype = Ptype(char)
                    c = Cell(x, y, ptype)
                self.cells[y][x] = c
        self._build_track()

    def get_cell(self, x: int, y: int) -> Cell | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None
    
    def _build_track(self):
        pos = self.start
        pbar = tqdm(desc="Building track...", unit="step")
        while pos != self.goal:
            pbar.update(1)
            self.track.append(pos)
            for dir in list(Direction):
                target: Cell = self.cells[pos.y + dir.dy][pos.x + dir.dx] # the map is walled of, so no need for bounds checking
                if target.ptype == Ptype.EMPTY and target not in self.track:
                    pos = target
                    break
        self.track.append(self.goal)

@dataclass
class Cheat:
    start: Cell
    end: Cell
    advantage: int # number of steps saved

class Puzzle:
    def __init__(self, m: Map):
        self.map = m
        self.cheats: list[Cheat] = []

    def find_cheats(self, min_advantage=2) -> list[Cheat]:
        self.cheats.clear()
        for pos in tqdm(self.map.track, desc="Finding cheats for every step on the track", unit="step"):
            for dir in list(Direction):
                # there no corners that could be cut so we just skip in the same dir twice
                target: Cell | None = self.map.get_cell(pos.x + dir.dx*2, pos.y + dir.dy*2)
                if target and target.ptype == Ptype.EMPTY:
                    advantage = self.map.track.index(target) - self.map.track.index(pos) - 2
                    if advantage >= min_advantage:
                        self.cheats.append(Cheat(pos, target, advantage))
        return self.cheats
    
    def do(self):
        pass

    def checksum(self):
        return len(self.cheats)
    
    def check_p2(self):
        pass

def load_puzzle(input_file: str) -> Puzzle:
    """Load Puzzle from input file (path)."""
    with open(input_file, 'r') as file:
        content = file.read()
        m = Map(content)
    return Puzzle(m)