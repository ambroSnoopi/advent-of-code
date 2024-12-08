from typing import Iterator
from dataclasses import dataclass
import numpy as np
import itertools


@dataclass
class Cell:
    x: int
    y: int
    antenna: str
    antinode: bool

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.x, self.y) == (other.x, other.y)
        return False

class Grid:
    def __init__(self, input_str: str):
        # Split the input string into lines and create the grid
        lines = input_str.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0
        self.cells = np.full((self.height, self.width), "", dtype=Cell)
        self.antennas: dict[str, set[Cell]] = {}
        self.antinodes: set[Cell] = set()

        # Parse the input and populate the grid
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                antenna = char if char != '.' else None
                c = Cell(x, y, antenna, False)
                self.cells[y][x] = c

                # let's also store a reference by antenna for easy lookup
                if antenna:
                    s = self.antennas.get(antenna)
                    if s is None:
                        self.antennas.update({antenna:  {c}})
                    else:
                        s.add(c)

    def get_cells(self) -> Iterator[Cell]:
        """Returns an iterator over all cells in the map, row by row."""
        for row in self.cells:
            yield from row
    
    def create_antinodes(self):
        for cells in self.antennas.values():
            pairs = list(itertools.combinations(cells, 2))
            for pair in pairs:
                # calc distance
                a, b = pair
                ax, ay, bx, by = a.x, a.y, b.x, b.y
                dy = ay - by
                dx = ax - bx
                # mirror antinode
                n1y = ay + dy
                n1x = ax + dx
                n2y = by - dy
                n2x = bx - dx
                self.register_antinode(n1y, n1x)
                self.register_antinode(n2y, n2x)
    
    def register_antinode(self, y: int, x: int):
        """ Register an antinode at the specified coordinates if they're valid. """
        if 0 <= x < self.width and 0 <= y < self.height:
            n: Cell = self.cells[y][x]
            n.antinode = True
            self.antinodes.add(n)

def load_puzzle(filename: str) -> Grid:
    with open(filename, 'r') as file:
        return Grid(file.read())