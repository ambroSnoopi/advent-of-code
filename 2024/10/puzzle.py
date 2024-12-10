from typing import Iterator
from dataclasses import dataclass
import numpy as np

@dataclass
class Cell:
    x: int
    y: int
    h: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.x, self.y) == (other.x, other.y)
        return False

@dataclass
class Trail:
    start: Cell
    routes: list[set[Cell]]
    score: int

    def __hash__(self):
        return hash(self.head)

    def __eq__(self, other):
        if isinstance(other, Trail):
            return self.head == other.head
        return False

class Map:
    def __init__(self, input_str: str):
        # Split the input string into lines and create the grid
        lines = input_str.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0
        self.cells = np.full((self.height, self.width), "", dtype=Cell)
        self.trails: list[Trail] = []
        self.score = 0

        # Parse the input and populate the grid
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                h = int(char)
                c = Cell(x, y, h)
                self.cells[y][x] = c

    def get_cells(self) -> Iterator[Cell]:
        """Returns an iterator over all cells in the map, row by row."""
        for row in self.cells:
            yield from row

    def find_trails(self) -> int:
        """Finds all Trails on the Map and update the Map's score accordingly. Returns the total score."""
        for cell in self.get_cells():
            if cell.h == 0:
                routes = self.find_routes(cell)
                score = self.score_routes(routes)
                trail = Trail(cell, routes, score)
                if score > 0:
                    self.trails.append(trail)
                    self.score += score
        return self.score

    def find_routes(self, start: Cell) -> list[set[Cell]]:
        """Finds all Routes for a trailhead Cell."""
        routes: list[set[Cell]] = [{start}]
        neighbors: set[Cell] = self.find_elevated_neighbor(start)
        while neighbors:
            routes.append(neighbors)
            neighbors = {neighbor for n in neighbors for neighbor in self.find_elevated_neighbor(n)}
        return routes
    
    def find_elevated_neighbor(self, cell: Cell) -> set[Cell]:
        """Find all neigbors that are elevated by 1."""
        x = cell.x
        y = cell.y
        seek_h = cell.h+1

        neighbors: set[Cell] = set()

        if 0 <= y-1 < self.height:
            n = self.cells[y-1][x]
            if n.h == seek_h:
                neighbors.add(n)
       
        if 0 <= y+1 < self.height:
            n = self.cells[y+1][x]
            if n.h == seek_h:
                neighbors.add(n)
        
        if 0 <= x-1 < self.width:
            n = self.cells[y][x-1]
            if n.h == seek_h:
                neighbors.add(n)

        if 0 <= x+1 < self.width:
            n = self.cells[y][x+1]
            if n.h == seek_h:
                neighbors.add(n)
        
        return neighbors
    
    def score_routes(self, routes: list[set[Cell]]) -> int:
        "Score Trail based on how many heads can be reached."
        score = len(routes[9]) if len(routes) > 9 else 0
        return score
            




def load_puzzle(filename: str):
    with open(filename, 'r') as file:
        return Map(file.read())