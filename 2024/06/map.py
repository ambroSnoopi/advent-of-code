from enum import Enum
from typing import List, Optional, Tuple, Iterator
from dataclasses import dataclass

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
    
    def turn_right(self) -> 'Direction':
        directions = list(Direction)
        current_index = directions.index(self)
        return directions[(current_index + 1) % 4]

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.is_obstacle = False
        self.guard_direction: Optional[Direction] = None
#        self.visited = False   #this was just for the looks... and we cant afford it!
    
    def set_obstacle(self):
        self.is_obstacle = True
    
    def set_guard(self, direction: Direction):
        self.is_obstacle = False
        self.guard_direction = direction
    
    def clear(self):
        self.is_obstacle = False
#        self.visited = False
#
#    def reset(self):
#        self.visited = False
#    
#    def mark_visited(self):
#        self.visited = True
    
    def __str__(self) -> str:
        if self.is_obstacle:
            return '#'
        elif self.guard_direction:
            return self.guard_direction.symbol
 #       elif self.visited:
 #           return 'X'
        return '.'

@dataclass(frozen=True)
class Position:
    cell: Cell
    direction: Direction
@dataclass
class Guard:
    x: int
    y: int
    direction: Direction
    
    def move(self) -> Tuple[int, int]:
        """Returns the new (x, y) position after moving in the current direction"""
        return (
            self.x + self.direction.dx,
            self.y + self.direction.dy
        )
    
    def turn_right(self):
        """Turn the guard 90 degrees to the right"""
        self.direction = self.direction.turn_right()

    def reset(self, pos: Position):
        """Reset guard on a specific (starting) position."""
        self.x = pos.cell.x
        self.y = pos.cell.y
        self.direction = pos.direction

class Map:
    def __init__(self, input_str: str):
        # Split the input string into lines and create the grid
        lines = input_str.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0
        
        # Initialize the map with empty cells
        self.cells = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        
        # Parse the input and populate the grid
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '#':
                    self.get_cell(x, y).set_obstacle()
                elif char in ('^', '>', 'v', '<'):
                    direction = next(d for d in Direction if d.symbol == char)
                    self.get_cell(x, y).set_guard(direction)
                    self.guard = Guard(x, y, direction)
                    self.starting_pos = Position(self.get_cell(x, y), Direction.UP)
    
    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None
    
    def get_cells(self) -> Iterator[Cell]:
        """Returns an iterator over all cells in the map, row by row."""
        for row in self.cells:
            yield from row

    def reset(self):
        """Resets the map to it's original state."""
        #for cell in self.get_cells():   # nothing to reset, as we don't alter the cells during simulation anymore
        #    cell.reset()
        self.guard.reset(self.starting_pos)

#    def is_on_map(self, cell: Cell) -> bool:   # primitives ftw...
#        """Check if the position is within the map bounds"""
#        return cell is not None and 0 <= cell.x < self.width and 0 <= cell.y < self.height
    
    def simulate_guard_movement(self) -> Tuple[set[Tuple[int, int, Direction]], bool]:
        """
        Simulate movement of the guard until they leave the map or loop.
        Returns the list of traversed Positions and whether the guard exited the map.
        """
        guard = self.guard
        path: set[Tuple[int, int, Direction]] = set() #apparently, creating objects is expensive, so let's try to work with primitives

        while True:
            pos = (guard.x, guard.y, guard.direction)

            #if self.cells[guard.y][guard.x].is_obstacle: raise ValueError("Cannot stand on an obstacle!")
                
            # Check for loops
            if pos in path:
                return path, False

            path.add(pos)
            
            # Handle obstacles and movement
            x, y = guard.move()       
            try:
                while self.cells[y][x].is_obstacle:
                    guard.turn_right()
                    x, y = guard.move()
            except IndexError:
                return path, True #we'd leave the map
            guard.x, guard.y = x, y
    
    def __str__(self) -> str:
        return '\n'.join(''.join(str(cell) for cell in row) for row in self.cells)

def load_map(filename: str) -> Map:
    with open(filename, 'r') as file:
        return Map(file.read())