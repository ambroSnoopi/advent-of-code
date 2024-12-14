from typing import Iterator
from collections import Counter
from functools import reduce
from operator import mul
import numpy as np

class Robot:
    def __init__(self, x: int, y: int, vx: int, vy:int):
        self.px = x
        self.py = y
        self.vx = vx
        self.vy = vy
    
class Map:
    def __init__(self, width: int, height: int, robots: list[Robot]):
        self.robots = robots
        self.height = height
        self.width = width
        self.cells = np.full((self.height, self.width), 0, dtype=int)

        self.mid_x = (self.width-1) // 2
        self.mid_y = (self.height-1) // 2  
        self.quadrants = Counter({'NW': 0, 'NO': 0, 'SW': 0, 'SO': 0})

    def __str__(self) -> str:
        # Convert entire array to string array, replace zeros with dots
        str_grid = np.where(self.cells == 0, ' ', self.cells.astype(str))
        # Join each row into a single string, then join rows with newlines
        return '\n'.join(''.join(row) for row in str_grid)
    
    def checksum(self):
        return reduce(mul, self.quadrants.values(), 1)

    def __update_quadrant(self, robot: Robot):
        """ Determines quadrant based on robots position and increments counter. """
        if robot.px == self.mid_x or robot.py == self.mid_y:
            return
        elif robot.px < self.mid_x:
            quadrant = 'N' if robot.py > self.mid_y else 'S'
            quadrant += 'W'
        else:  # robot.x > mid_x
            quadrant = 'N' if robot.py > self.mid_y else 'S'
            quadrant += 'O'
        self.quadrants[quadrant] += 1
        return
    
    def tick(self, n=100):
        """ Simulate n seconds."""
        self.quadrants.clear()
        self.cells.fill(0)
        for robot in self.robots:
            robot.px, robot.py = self.move(robot, n)
            self.__update_quadrant(robot)
            self.cells[robot.py][robot.px] += 1

    def move(self, robot: Robot, n=1) -> tuple[int, int]:
        """
        Move the robot n times according to its velocity, wrapping around boundaries.
        
        Args:
            robot: Robot instance to move
            n: Number of time steps to simulate
            
        Returns:
            Tuple[int, int]: Final (x, y) position after movement
        """
        # Calculate total displacement
        dx = robot.vx * n
        dy = robot.vy * n
        
        # Calculate new position with wrapping
        new_x = (robot.px + dx) % self.width
        new_y = (robot.py + dy) % self.height
        
        # Ensure positive values
        new_x = (new_x + self.width) % self.width
        new_y = (new_y + self.height) % self.height
        
        return (int(new_x), int(new_y))

def parse_robot_config(config_data: str) -> list[Robot]:
    robots = []   
    for line in config_data.strip().split('\n'):

        pos_part, vel_part = line.split(' ')
        px, py = map(int, pos_part.replace('p=', '').split(','))
        vx, vy = map(int, vel_part.replace('v=', '').split(','))

        robot = Robot(px, py, vx, vy)
        robots.append(robot)   
    return robots

def load_puzzle(filename: str, width: int, height: int) -> Map:
    with open(filename, 'r') as file:
        config_data = file.read()
    robots = parse_robot_config(config_data)
    return Map(width, height, robots)