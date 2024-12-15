from typing import Iterator, Optional
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
    other_half: Optional["Cell"]

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
        self.width = len(lines[0])*2 if self.height > 0 else 0
        self.cells = np.empty((self.height, self.width), dtype=Cell)
        # Parse the input and populate the grid 
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                x = x*2
                ptype = Ptype(char)
                if ptype==Ptype.ROBOT:
                    c_half = Cell(x, y, ptype, None)
                    c_other = Cell(x+1, y, Ptype.EMPTY, None)
                    self.robot = c_half
                else:
                    c_half = Cell(x, y, ptype, None)
                    c_other = Cell(x+1, y, ptype, None)
                if ptype == Ptype.BOX:
                    c_half.other_half = c_other
                    c_other.other_half = c_half
                self.cells[y][x] = c_half
                self.cells[y][x+1] = c_other

    def __str__(self) -> str:
        str_grid = self.cells.astype(str)
        # Join each row into a single string, then join rows with newlines
        return '\n'.join(''.join(row) for row in str_grid)

    def get_cells(self) -> Iterator[Cell]:
        """Returns an iterator over all cells in the map, row by row, left to right."""
        for row in self.cells:
            yield from row

    def checksum(self) -> int:
        score = 0
        ignore: list[Cell] = []
        for cell in self.get_cells():
            if cell.ptype==Ptype.BOX and cell not in ignore:
                gps = 100 * cell.y + cell.x
                score += gps
                ignore.append(cell.other_half)
        return score
    
    def do(self):
        for dir in self.moves:
            self.move_piece(self.robot, dir)

    def can_move(self, piece: Cell, dir: Direction) -> bool:
        """Checks if the piece on the given cell could move in a given direction and handles obstacles recursively. Returns True if successfull."""
        if piece.ptype in [Ptype.WALL, Ptype.EMPTY]:
            return False
        target: Cell = self.cells[piece.y + dir.dy][piece.x + dir.dx]
        if target == piece.other_half:
            return self.can_move(target, dir)
        if target.ptype == Ptype.WALL:
            return False
        if target.ptype == Ptype.BOX:
            return self.can_move(target, dir) and self.can_move(target.other_half, dir)
        #if target.ptype == Ptype.EMPTY or BOX moved succefully
        #if piece.ptype == Ptype.BOX:
         #   twin_success = self.can_move(piece.other_half, dir)
        return True
    
    def move_piece(self, piece: Cell, dir: Direction):
        """Moves piece on the given cell in a given direction and cascades to other movable objects on the path."""
        if (
            piece.ptype==Ptype.ROBOT and self.can_move(piece, dir) or 
            piece.ptype==Ptype.BOX and self.can_move(piece, dir) and self.can_move(piece.other_half, dir)
        ):
            if piece.ptype in [Ptype.ROBOT, Ptype.BOX]:
                target: Cell = self.cells[piece.y + dir.dy][piece.x + dir.dx]
                if target.ptype == Ptype.BOX:
                    if target.other_half != piece: self.move_piece(target.other_half, dir)
                    self.move_piece(target, dir)
                target.ptype = piece.ptype
                if target.ptype == Ptype.BOX:
                    target.other_half = piece.other_half
                    target.other_half.other_half = target # updating ref to self... that's what i get for using Cell instead of Piece objects...
                    piece.other_half = None
                piece.ptype = Ptype.EMPTY
                if target.ptype == Ptype.ROBOT: self.robot = target
                
    
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