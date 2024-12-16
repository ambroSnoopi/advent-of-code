from typing import Iterator, Optional
from collections import Counter
from enum import Enum
from dataclasses import dataclass, field
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

    def turn_around(self) -> 'Direction':
        directions = list(Direction)
        current_index = directions.index(self)
        return directions[(current_index + 2) % 4]

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
    visits: Counter = field(default_factory=Counter)

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
        self.pos.visits[dir] += 1
    
    def add_move(self, target: Cell, dir: Direction, highscore = float('inf')) -> int:
        """ Scores and registers a move. Handles revison. Returns the score. """
        # edge case: if we are revisiting the same cell, let's cut back in time and assume we have walked the other way instead
        if target in self.moves:
            new_moves = {} #incl. target
            for key in self.moves:
                new_moves[key] = self.moves[key]
                if key == target:
                    break
            self.moves = new_moves
            self.pos = target
            self.pos.visits[dir] += 1
            self.dir = dir
            last_move = next(reversed(self.moves.values()))
            return last_move['score']
        # happy case: derive new score and register move
        last_move = next(reversed(self.moves.values()))
        cost = 1 if dir==last_move['dir'] else 1001
        score = last_move['score'] + cost
        if score <= highscore: #move
            self.moves[target] = {'dir': dir, 'score': score}
            self.pos = target
            self.pos.visits[dir] += 1
            self.dir = dir
        else: # make it so much more expensive for the next ranking
            target.visits[dir] += 1 # 1000?
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
        self.runs: list[dict[Cell, dict]] = [] # list[player.moves]
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

    def do(self, n=1, best_score=0):
        for _ in tqdm(range(n), desc="Simulating runs...", unit="run"):
            self.player = Player(self.start, Direction.RIGHT)
            while self.player.pos.ptype != Ptype.GOAL:
                final_score = self.move()
            if final_score == best_score or best_score==0:
                self.runs.append(self.player.moves)

    def checksum(self) -> int:
        return next(reversed(self.player.moves.values())).get('score', 0)
    
    def get_best_path_cells(self) -> set[Cell]:
        best_path_cells = set()
        for moves in self.runs:
            best_path_cells.update(moves.keys())
        return best_path_cells

    def get_ranked_dirs(self, pos: Cell) -> list[Direction]:
        """ Returns a list of walkable directions sorted by number of visits of the target cell. """
        walkable_targets = []
        for dir in list(Direction):
            target: Cell = self.cells[pos.y + dir.dy][pos.x + dir.dx]
            if target.ptype != Ptype.WALL:
                walkable_targets.append((target.visits[dir], dir)) 
        ranked_targets = sorted(walkable_targets, key=lambda item: (item[0], item[1].symbol)) # i.e. sorted by visits
        return [dir for visits, dir in ranked_targets]
    
    def move(self):
        """ Orders the cheapest possible move, i.e. move to the least visited neighbor but prefer moving straight. """
        pos = self.player.pos

        ranked_dir = self.get_ranked_dirs(pos)
        straight_target: Cell = self.cells[pos.y + self.player.dir.dy][pos.x + self.player.dir.dx]
        nextbest_target: Cell = self.cells[pos.y + ranked_dir[0].dy][pos.x + ranked_dir[0].dx]
        if (self.player.dir in ranked_dir # i.e. is walkable
            and straight_target.visits[self.player.dir] <= nextbest_target.visits[ranked_dir[0]] #+1000 or smth like that? bc it's 1000 more expensive to turn
            ):
            target = straight_target
            dir = self.player.dir
        else:
            target = nextbest_target
            dir = ranked_dir[0]

        highscore = self.highscores.get((target, dir), float('inf'))
        score = self.player.add_move(target, dir, highscore)
        if score < highscore:
            self.highscores[(target, dir)] = score
        return score

    def __str__(self) -> str:
        str_grid = self.cells.astype(str)
        # overwrite with player path
        for cell, move in self.player.moves.items():
            str_grid[cell.y][cell.x] = str(move['dir'])
        last_score = str(next(reversed(self.player.moves.values())).get('score','unknown'))
        # Join each row into a single string, then join rows with newlines
        return '\n'.join(''.join(row) for row in str_grid)+'\nScore: '+last_score

    def get_cells(self) -> Iterator[Cell]:
        """Returns an iterator over all cells in the map, row by row, left to right."""
        for row in self.cells:
            yield from row

def load_puzzle(map_file: str) -> Map:
    with open(map_file, 'r') as file:
        map_data = file.read()
        return Map(map_data)