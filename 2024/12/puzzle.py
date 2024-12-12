from typing import Iterator
from dataclasses import dataclass
import numpy as np
from tqdm import tqdm
from itertools import product


@dataclass
class Cell:
    x: int
    y: int
    plant: str

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.x, self.y) == (other.x, other.y)
        return False

class Region:
    def __init__(self, plant: str):
        self.plant = plant
        self.plots: set[Cell] = set()
        self.area = 0
        self.perimeter = 0 #TODO: What's the best way of deriving this / storing data for this?

    def add_plot(self, cell: Cell):
        """Adds the Cell to the Plots of this Region, if it contains the same Plant."""
        if cell.plant == self.plant:
            self.plots.add(cell)

class Map:
    def __init__(self, input_str: str):
        # Split the input string into lines and create the grid
        lines = input_str.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0
        self.cells = np.full((self.height, self.width), "", dtype=Cell)
        self.regions: list[Region] = []

        # Parse the input and populate the grid
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                plant = char
                c = Cell(x, y, plant)
                self.cells[y][x] = c

    def get_cells(self) -> Iterator[Cell]:
        """Returns an iterator over all cells in the map, row by row."""
        for row in self.cells:
            yield from row

def load_puzzle(filename: str):
    with open(filename, 'r') as file:
        return Map(file.read())