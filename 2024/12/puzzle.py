from typing import Iterator, Tuple
from dataclasses import dataclass
import numpy as np
from tqdm import tqdm

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
    def __init__(self, cell: Cell):
        self.plant = cell.plant
        self.plots: dict[Tuple[int,int], Cell] = {(cell.x, cell.y): cell}
        self.max_x = cell.x
        self.max_y = cell.y
        self.area = 1
        self.perimeter = 4 #TODO: What's the best way of deriving this / storing data for this?

    def add_plot(self, cell: Cell):
        """Adds the Cell to the Plots of this Region.""" #, if it contains the same Plant
        #if cell.plant == self.plant:
        self.plots[(cell.x, cell.y)] = cell
        self.max_x = max(cell.x, self.max_x)
        self.max_y = max(cell.y, self.max_y)
        self.area += 1
        n = self.count_prev_neighbors(cell)
        if n < 2:
            self.perimeter += 2
        return

    def count_prev_neighbors(self, cell: Cell) -> int:
        """Counts the number of *previous* neighbors in the Region."""
        return sum(1 for x, y in [(cell.x - 1, cell.y), (cell.x, cell.y - 1)] if self.plots.get((x, y)))
    
    def price(self) -> int:
        return self.area * self.perimeter

class Map:
    def __init__(self, input_str: str):
        lines = input_str.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0
        self.cells = np.full((self.height, self.width), "", dtype=Cell)
        self.regions: dict[Tuple[int,int,str], Region] = {} #(max_x,max_y,plant):Region

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                plant = char
                c = Cell(x, y, plant)
                self.cells[y][x] = c

                #check left and top neighbor if they can form a region, or create a new one otherwise
                r = self.regions.pop((x-1, y, plant), None)
                if r:
                    r.add_plot(c)
                    self.regions[(x, y, plant)] = r
                else:
                    r = self.regions.pop((x, y-1, plant), None)
                    if r:
                        r.add_plot(c)
                        self.regions[(x, y, plant)] = r
                    else:
                        self.regions[(x, y, plant)] = Region(c)


    def get_cells(self) -> Iterator[Cell]:
        """Returns an iterator over all cells in the map, row by row."""
        for row in self.cells:
            yield from row

    def total_price(self) -> int:
        return sum(r.price() for r in self.regions.values())

def load_puzzle(filename: str):
    with open(filename, 'r') as file:
        return Map(file.read())