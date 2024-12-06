from enum import Enum
from typing import List, Optional, Tuple
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
        self.visited = False
    
    def set_obstacle(self):
        self.is_obstacle = True
        self.guard_direction = None
    
    def set_guard(self, direction: Direction):
        self.is_obstacle = False
        self.guard_direction = direction
    
    def clear(self):
        self.is_obstacle = False
        self.guard_direction = None
    
    def mark_visited(self):
        self.visited = True
    
    def __str__(self) -> str:
        if self.is_obstacle:
            return '#'
        elif self.guard_direction:
            return self.guard_direction.symbol
        elif self.visited:
            return 'X'
        return '.'

@dataclass
class Guard:
    x: int
    y: int
    direction: Direction
    
    def move(self) -> Tuple[int, int]:
        """Returns the new position after moving in the current direction"""
        return (
            self.x + self.direction.dx,
            self.y + self.direction.dy
        )
    
    def turn_right(self):
        """Turn the guard 90 degrees to the right"""
        self.direction = self.direction.turn_right()

class Map:
    def __init__(self, input_str: str):
        # Split the input string into lines and create the grid
        lines = input_str.strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0
        
        # Initialize the map with empty cells
        self.cells = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        
        # Keep track of guards (the way a "single guard" was highlighted suggests ther might be more in part 2?)
        self.guards: List[Guard] = []
        
        # Parse the input and populate the grid
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '#':
                    self.cells[y][x].set_obstacle()
                elif char in ('^', '>', 'v', '<'):
                    direction = next(d for d in Direction if d.symbol == char)
                    self.cells[y][x].set_guard(direction)
                    self.guards.append(Guard(x, y, direction))
    
    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if the position is within the map bounds"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def simulate_guard_movement(self, guard_index: int = 0) -> List[Tuple[int, int]]:
        """
        Simulate movement of a specific guard until they leave the map.
        Returns the list of positions visited.
        """
        if not (0 <= guard_index < len(self.guards)):
            return []
        
        guard = self.guards[guard_index]
        path = [(guard.x, guard.y)]
        
        # Mark initial position as visited
        self.cells[guard.y][guard.x].mark_visited()
        
        while True:
            new_x, new_y = guard.move()
            
            # Check if guard has left the map
            if not self.is_valid_position(new_x, new_y):
                break
                
            # Check if we hit an obstacle
            cell = self.cells[new_y][new_x]
            if cell.is_obstacle:
                guard.turn_right()
                continue
                
            # Move to new position
            guard.x, guard.y = new_x, new_y
            cell.mark_visited()
            path.append((new_x, new_y))
        
        return path
    
    def __str__(self) -> str:
        return '\n'.join(''.join(str(cell) for cell in row) for row in self.cells)

def load_map(filename: str) -> Map:
    with open(filename, 'r') as file:
        return Map(file.read())