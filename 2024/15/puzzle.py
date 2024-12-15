from typing import Iterator
from enum import Enum
from dataclasses import dataclass
import numpy as np

class Direction(Enum):
    UP = ('^', 0, -1)
    RIGHT = ('>', 1, 0)
    DOWN = ('v', 0, 1)
    LEFT = ('<', -1, 0)
    
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
    def from_symbol(cls, symbol: str) -> 'Direction':
        for member in cls:
            if member.symbol == symbol:
                return member
        raise ValueError(f"No Direction matches symbol: {symbol}")

class Ptype(Enum):
    WALL  = '#'
    BOX   = 'O'
    ROBOT = '@'
    EMPTY = '.'

    def __str__(self):
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

class Map:
    def __init__(self, map_data: str, moves_data: str):
        self.moves = self.parse_moves_config(moves_data)
        lines = map_data.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0
        self.cells = np.empty((self.height, self.width), dtype=Cell)
        # Parse the input and populate the grid 
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                c = Cell(x, y, Ptype(char))
                self.cells[y][x] = c
                if c.ptype==Ptype.ROBOT:
                    self.robot = c
                    self.robot_x_addon = 0.0

    def __str__(self) -> str:
        str_grid = self.cells.astype(str)
        # Join each row into a single string, then join rows with newlines
        return '\n'.join(''.join(row) for row in str_grid)

    def get_cells(self) -> Iterator[Cell]:
        """Returns an iterator over all cells in the map, row by row."""
        for row in self.cells:
            yield from row

    def checksum(self) -> int:
        score = 0
        for cell in self.get_cells():
            if cell.ptype==Ptype.BOX:
                gps = 100 * cell.y + 2 * cell.x
                score += gps
        return score
    
    def do(self):
        for dir in self.moves:
            self.move_piece(self.robot, dir)

    def move_piece(self, piece: Cell, dir: Direction) -> bool:
        """Attempts to move the piece on the given cell in a given direction and handles obstacles recursively. Returns True if successfull."""
        if piece.ptype == Ptype.ROBOT and dir.dx!=0:
            #handle half-steps:
            self.robot_x_addon += dir.dx/2
            if self.robot_x_addon % 1 == 0.5:
                return True
        if piece.ptype in [Ptype.WALL, Ptype.EMPTY]:
            return False
        target: Cell = self.cells[piece.y + dir.dy][piece.x + dir.dx]
        if target.ptype == Ptype.WALL:
            return False
        if target.ptype == Ptype.BOX:
            if not self.move_piece(target, dir):
                return False
        #if target.ptype == Ptype.EMPTY or BOX moved succefully
        target.ptype = piece.ptype
        piece.ptype = Ptype.EMPTY
        if target.ptype == Ptype.ROBOT:
            self.robot = target
        return True
    
    def parse_moves_config(self, moves_data: str) -> list[Direction]:
        moves: list[Direction] = []   
        for line in moves_data.strip().split('\n'):
            for char in line:
                moves.append(Direction.from_symbol(char))
        return moves

def load_puzzle(map_file: str, moves_file: str) -> Map:
    with open(moves_file, 'r') as file:
        moves_data = file.read()
    with open(map_file, 'r') as file:
        map_data = file.read()
    return Map(map_data, moves_data)