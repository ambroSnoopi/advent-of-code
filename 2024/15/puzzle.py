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

    def build_move(self, piece: Cell, dir: Direction, moving: list[Cell] = []) -> list[Cell]:
        """Builds a move chain for the piece on the given cell in a given direction. Returns all cells in the chain that would be moved."""
        if piece.ptype in [Ptype.WALL, Ptype.EMPTY]:
            return [] #cannot move, thus return empty list
        
        target: Cell = self.cells[piece.y + dir.dy][piece.x + dir.dx]
        if target.ptype == Ptype.WALL:
            return [] #hitting a wall breaks the chain, thus return empty list
        
        if target == piece.other_half: # edge case (moving onto own other half)
            moving.append(piece) # incl. self
            return self.build_move(piece.other_half, dir, moving) # and return move chain of other half
        
        moving_target, moving_other = [], []
        if target.ptype == Ptype.BOX:
            moving_target.extend(self.build_move(target, dir, [])) #get chain of target...
            moving_other.extend(self.build_move(target.other_half, dir, [])) #...and it's other_half
            if not (moving_target and moving_other):
                return [] #both need to be able to move or the entire chain is broken
        
        #if target.ptype == Ptype.EMPTY or BOX moved succefully

        moving_twin = []
        moving.append(piece)
        antitarget: Cell = self.cells[piece.y - dir.dy][piece.x - dir.dx]
        if (piece.ptype == Ptype.BOX and 
            piece != antitarget.other_half and  # break out of circular ref if i'm moving away (i.e. being pushed) from my own other_half
            piece.other_half not in moving # break out of circular ref if my other half is already in the moving list
        ):
            moving_twin.extend(self.build_move(piece.other_half, dir, moving)) #get move chain for own other_half
            if not (moving_twin):
                return [] #break the chain if my other half cant move
            
        # build the chain in proper order of execution
        move_order = []
        for cell in moving_twin:
            if cell not in move_order: move_order.append(cell)
        for cell in moving:
            if cell not in move_order: move_order.append(cell)
        for cell in moving_target:
            if cell not in move_order: move_order.append(cell)
        for cell in moving_other:
            if cell not in move_order: move_order.append(cell)

        if dir in {Direction.UP, Direction.DOWN}:
            return sorted(move_order, key=lambda cell: cell.y, reverse=(dir==Direction.DOWN))
        else:
            return sorted(move_order, key=lambda cell: cell.x, reverse=(dir==Direction.RIGHT))
    
    def move_piece(self, piece: Cell, dir: Direction):
        """Moves piece on the given cell in a given direction and cascades to other movable objects on the path."""
        execution_order = self.build_move(piece, dir, [])
        for piece in execution_order:
            target: Cell = self.cells[piece.y + dir.dy][piece.x + dir.dx]
            if target.ptype != Ptype.EMPTY or target.other_half:
                raise ValueError('Tried to move onto a non empty cell!', piece, target)
            target.ptype = piece.ptype
            if target.ptype == Ptype.BOX:
                target.other_half = piece.other_half
                target.other_half.other_half = target # updating ref to self... that's what i get for using Cell instead of Piece objects...
                piece.other_half = None
            piece.ptype = Ptype.EMPTY
            if target.ptype == Ptype.ROBOT: 
                self.robot = target          
    
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