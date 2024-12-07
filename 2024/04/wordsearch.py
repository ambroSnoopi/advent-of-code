from typing import Iterator
from collections import Counter
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
    
    def gather_cells(self, start: Cell, dir: Direction, lenght: int) -> str:
        """Gathers all cells reading from a starting cell in a specific direction for a specified length."""
        collection = []
        for n in range(lenght):
            next_x = start.x + dir.dx * n
            next_y = start.y + dir.dy * n
            if not (0 <= next_x < self.width and 0 <= next_y < self.height):
                return collection
            next_c = self.cells[next_y][next_x]
            collection.append(next_c)
        return collection
    
#    def find_word(self, word="MAS") -> list[list[Cell]]:
#        findings = []
#        for cell in self.chars.get(word[0]):
#            for dir in list(Direction):
#                if word == self.gather_chars(cell, dir, len(word)):
#                    findings.append(self.gather_cells(cell, dir, len(word)))
#        return findings
#    
#    def count_x(self, word="MAS") -> int:
#        findings = self.find_word(word)
#        half_len = int((len(word)-1)/2)
#        x_cells: list[Cell] = []
#        for f in findings:
#            x_cells.append(f[half_len])
#        cnt = Counter(x_cells)  # Count how often each Cell is listed
#        double_cnt = {key: value for key, value in cnt.items() if value > 1}  # Filter for entries with more than 1 occurrence
#        return len(double_cnt)

# they have actually to be in 90degree to eachother...    
    def count_x_mas(self) -> int:
        """Counts how many time MAS appears overlapping itself in an X-shape."""
        n = 0
        word = "MAS" # cant be bothered to make it dynamic...
        x_char = "A"
        for cell in self.chars.get(x_char):
            star: dict[Direction, str] = {} # let collect a char in each direction
            for dir in list(Direction):
                star[dir] = self.gather_chars(cell, dir, 2)[1:]
            #if (
            #    (star[Direction.LEFT]+x_char+star[Direction.RIGHT] == word or star[Direction.RIGHT]+x_char+star[Direction.LEFT] == word) and 
            #    (star[Direction.UP]+x_char+star[Direction.DOWN] == word or star[Direction.DOWN]+x_char+star[Direction.UP] == word)
            #): n += 1
            if (
                (star[Direction.UL]+x_char+star[Direction.LR] == word or star[Direction.LR]+x_char+star[Direction.UL] == word) and 
                (star[Direction.UR]+x_char+star[Direction.LL] == word or star[Direction.LL]+x_char+star[Direction.UR] == word)
            ): n += 1
        return n

def load_puzzle(filename: str) -> Puzzle:
    with open(filename, 'r') as file:
        return Puzzle(file.read())