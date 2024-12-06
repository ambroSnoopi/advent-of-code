from typing import List, Optional, Tuple, Iterator
from enum import Enum
from dataclasses import dataclass
import numpy as np

class Direction(Enum):
    UP    = (0 ,-1)
    RIGHT = (1 , 0)
    DOWN  = (0 , 1)
    LEFT  = (-1, 0)
    UR    = (1 ,-1)
    UL    = (-1,-1)
    LR    = (1,  1)
    LL    = (-1, 1)

    @property
    def dx(self) -> int:
        return self.value[0]
    
    @property
    def dy(self) -> int:
        return self.value[1]

@dataclass(frozen=True)
class Cell:
    x: int
    y: int
    char: str

class Puzzle:

    def __init__(self, input_str: str):
        # Split the input string into lines and create the grid
        lines = input_str.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0
        self.cells = np.full((self.height, self.width), "", dtype=Cell)
        self.chars: dict[str, set[Cell]] = {}

        # Parse the input and populate the grid
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                c = Cell(x, y, char)
                self.cells[y][x] = c

                # let's also store a reference by character for easy lookup
                s = self.chars.get(char)
                if s is None:
                    self.chars.update({char: {c}})
                else:
                    s.add(c)

    def get_cells(self) -> Iterator[Cell]:
        """Returns an iterator over all cells in the map, row by row."""
        for row in self.cells:
            yield from row
    
    def count_word(self, word="XMAS") -> int:
        """Counts the occurance of a specified word in the Puzzle"""
        n = 0
        for cell in self.chars.get(word[0]):
            for dir in list(Direction):
                if word == self.gather_chars(cell, dir, len(word)):
                    n += 1
        return n
    
    def gather_chars(self, start: Cell, dir: Direction, lenght: int) -> str:
        """Gathers all characters reading from a starting cell in a specific direction for a specified length."""
        word = ""
        for n in range(lenght):
            next_x = start.x + dir.dx * n
            next_y = start.y + dir.dy * n
            if not (0 <= next_x < self.width and 0 <= next_y < self.height):
                return word
            next_c = self.cells[next_y][next_x]
            word += next_c.char
        return word

def load_puzzle(filename: str) -> Puzzle:
    with open(filename, 'r') as file:
        return Puzzle(file.read())