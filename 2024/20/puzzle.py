from enum import Enum
from dataclasses import dataclass
from multiprocessing import Pool, cpu_count
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
    
    def distance(self, other: 'Cell') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

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
    
    def get_radius(self, c: Cell, r: int) -> list[Cell]:
        """ Returns a list of cells that are r steps away. """
        return self._get_radius(c.x, c.y, r)

    def _get_radius(self, x: int, y: int, r: int) -> list[Cell]:
        """ Returns a list of cells that are r steps away. """
        radius = []
        for i in range(-r, r+1):
            for j in range(-r, r+1):
                if abs(i)+abs(j) <= r:
                    cell = self.get_cell(x+i, y+j)
                    if cell:
                        radius.append(cell)
        return radius
    
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

    def __hash__(self):
        return hash((self.start, self.end))

class Puzzle:
    def __init__(self, m: Map):
        self.map = m
        self.cheats: set[Cheat] = set()

    def _find_cheats(self, chunk_data: tuple[list[Cell], int, int]) -> set[Cheat]:
        """Process a chunk of track cells to find cheats."""
        chunk, min_advantage, radius = chunk_data
        local_cheats = set()
        for pos in chunk:
            for target in self.map.get_radius(pos, radius):
                if target in self.map.track and target.ptype == Ptype.EMPTY:
                    advantage = self.map.track.index(target) - self.map.track.index(pos) - pos.distance(target)
                    if advantage >= min_advantage:
                        local_cheats.add(Cheat(pos, target, advantage))
        return local_cheats

    def find_cheats(self, min_advantage=2, radius=2) -> list[Cheat]:
        """Finds all possible wallhacks with a specified maximum radius which provide a specified minimum advantage."""
        self.cheats.clear()
        num_processes = cpu_count()
        track_slice = self.map.track[:-min_advantage+1]  # we can skip the last few since they won't be able to achieve the desired advantage even if it cuts right into a straight path to the goal
        
        # Create chunks of roughly equal size
        chunk_size = len(track_slice) // (num_processes * 24) + 1
        chunks = [track_slice[i:i + chunk_size] for i in range(0, len(track_slice), chunk_size)]
        
        # Prepare data for parallel processing
        chunk_data = [(chunk, min_advantage, radius) for chunk in chunks]
        
        # Process chunks in parallel
        with Pool(processes=num_processes) as pool:
            results = list(tqdm(
                pool.imap(self._find_cheats, chunk_data),
                total=len(chunks),
                desc="Finding cheats for a good chunk of the track",
                unit="chunk"
            ))
        
        # Combine results
        for result in results:
            self.cheats.update(result)
            
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