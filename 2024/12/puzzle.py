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
        self.area = 1
        self.perimeter = 4 #TODO: What's the best way of deriving this / storing data for this?

    @classmethod
    def from_regions(cls, regions: list["Region"]) -> "Region":
        first_cell = next(iter(regions[0].plots.values()))
        new_region = cls(first_cell)

        merged_cells = set()
        for region in regions:
            merged_cells.update(region.plots.values())
        for c in merged_cells:
            if c != first_cell:
                new_region.add_plot(c)
        return new_region
    
    def add_plot(self, cell: Cell):
        """Adds the Cell to the Plots of this Region.""" #, if it contains the same Plant
        #if cell.plant == self.plant:
        self.plots[(cell.x, cell.y)] = cell
        self.area += 1
        n = self.count_n(cell)
        self.perimeter += 4-(2*n)
        return

    def count_prev_neighbors(self, cell: Cell) -> int:
        """Counts the number of *previous* neighbors in the Region."""
        return sum(1 for x, y in [(cell.x - 1, cell.y), (cell.x, cell.y - 1)] if self.plots.get((x, y)))
    
    def count_n(self, cell: Cell) -> int:
        """Counts the number of neighbors in the Region."""
        return sum(1 for x, y in [(cell.x - 1, cell.y), (cell.x, cell.y - 1), (cell.x + 1, cell.y), (cell.x, cell.y + 1)] if self.plots.get((x, y)))
    
    def price(self) -> int:
        return self.area * self.perimeter

class Map:
    def __init__(self, input_str: str):
        lines = input_str.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0
        self.cells = np.full((self.height, self.width), "", dtype=Cell)
        self.regions: dict[str, list[Region]] = {} #by plant

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                plant = char
                c = Cell(x, y, plant)
                self.cells[y][x] = c

                regions = self.regions.pop(plant, [Region(c)])
                n_regions = [r for r in regions if r.count_prev_neighbors(c) > 0]
                if len(n_regions)>1:
                    merged_region = Region.from_regions(n_regions)
                    merged_region.add_plot(c)
                    regions.append(merged_region)
                    for r in n_regions:
                        regions.remove(r)
                elif len(n_regions)==1:
                    n_regions[0].add_plot(c)
                else:
                    regions.append(Region(c))
                self.regions[plant] = regions

    def get_cells(self) -> Iterator[Cell]:
        """Returns an iterator over all cells in the map, row by row."""
        for row in self.cells:
            yield from row

    def total_price(self) -> int:
        return sum(r.price() for region_list in self.regions.values() for r in region_list)


def load_puzzle(filename: str):
    with open(filename, 'r') as file:
        return Map(file.read())