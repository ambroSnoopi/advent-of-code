from typing import Iterator, Optional
from enum import Enum
from dataclasses import dataclass
import numpy as np
from tqdm import tqdm

class Direction(Enum):
    UP = ('^', 0, -1)
    RIGHT = ('>', 1, 0)
    DOWN = ('v', 0, 1)
    LEFT = ('<', -1, 0)

    def __str__(self):
        return self.value[0]
    
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
    
    def turn_right(self) -> 'Direction':
        directions = list(Direction)
        current_index = directions.index(self)
        return directions[(current_index + 1) % 4]
    
    def turn_left(self) -> 'Direction':
        directions = list(Direction)
        current_index = directions.index(self)
        return directions[(current_index - 1) % 4]

class Ptype(Enum):
    WALL  = '#'
    EMPTY = '.'
    GOAL = 'E'

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

class Player:
    def __init__(self, pos: Cell, dir: Direction):
        self.pos = pos
        self.dir = dir
        self.moves: dict[Cell, dict] = {pos: {'dir': dir, 'score': 0}} #value = dict of dir and score
    
    def add_move(self, target: Cell, dir: Direction, highscore = float('inf')) -> int:
        """ Scores and registers a move. Handles revison. Returns the score. """
        # edge case: if we are revisiting the same cell, let's cut back in time and assume we have turned the other way instead
        if target in self.moves:
            new_moves = {} #excluding target
            for key in self.moves:
                if key == target:
                    break
                new_moves[key] = self.moves[key]
            if new_moves:
                self.moves = new_moves
            else: #catching going through start again
                self.moves = {target: {'dir': Direction.RIGHT, 'score': 0}}
                self.pos = target
                self.dir = dir
                return 0
        # happy case: derive new score and register move
        last_move = next(reversed(self.moves.values()))
        cost = 1 if dir==last_move['dir'] else 1000
        score = last_move['score'] + cost
        if score <= highscore: #move
            self.moves[target] = {'dir': dir, 'score': score}
            self.pos = target
            self.dir = dir
        else: # just turn if moving would result in a worse score
            self.dir = dir.turn_left() 
        return score

class Map:
    def __init__(self, map_data: str):
        lines = map_data.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0
        self.cells = np.empty((self.height, self.width), dtype=Cell)
        self.start: Cell
        self.player: Player
        self.highscores: dict[tuple[Cell, Direction], int] = {}
        self.runs: list[int] = [] # final scores
        # Parse the input and populate the grid 
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "S":
                    c = Cell(x, y, Ptype.EMPTY)
                    self.start = c
                else:
                    ptype = Ptype(char)
                    c = Cell(x, y, ptype)
                self.cells[y][x] = c

    def do(self):
        self.player = Player(self.start, Direction.RIGHT)
        while self.player.pos.ptype != Ptype.GOAL:
            final_score = self.move()
        self.runs.append(final_score)

    def checksum(self):
        return next(reversed(self.player.moves.values())).get('score')

    def move(self):
        # simple move pattern: always try to move right
        dir = self.player.dir.turn_right()
        pos = self.player.pos
        target: Cell = self.cells[pos.y + dir.dy][pos.x + dir.dx] 

        if target.ptype == Ptype.WALL:
            self.player.dir = self.player.dir.turn_left() # therefore, the next try will be moving forward, then left, then back
        if target.ptype in [Ptype.EMPTY, Ptype.GOAL] :
            highscore = self.highscores.get((target, dir), float('inf'))
            score = self.player.add_move(target, dir, highscore)
            if score < highscore:
                self.highscores[(target, dir)] = score
        

    def __str__(self) -> str:
        str_grid = self.cells.astype(str)
        for cell, move in self.player.moves.items():
            str_grid[cell.y][cell.x] = str(move['dir'])
        # Join each row into a single string, then join rows with newlines
        return '\n'.join(''.join(row) for row in str_grid)

    def get_cells(self) -> Iterator[Cell]:
        """Returns an iterator over all cells in the map, row by row, left to right."""
        for row in self.cells:
            yield from row

def load_puzzle(map_file: str) -> Map:
    with open(map_file, 'r') as file:
        map_data = file.read()
        return Map(map_data)