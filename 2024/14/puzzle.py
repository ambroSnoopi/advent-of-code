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
        self.tick(0)

    def __str__(self) -> str:
        # Convert entire array to string array, replace zeros with dots
        str_grid = np.where(self.cells == 0, ' ', self.cells.astype(str))
        # Join each row into a single string, then join rows with newlines
        return '\n'.join(''.join(row) for row in str_grid)
    
    def may_look_like_a_christmas_tree(self) -> bool:
        """ 
        Returns true if the string representation of the Map looks anything like a Christmas Tree
        based on symmetry, density, width distribution and width to height ration.
        """
        # Treshold Parameters
        min_width_increase_ratio = 0.6
        max_asymmetry = 1
        min_density = 0.047

        # Find the bounds of robot cluster
        robot_rows, robot_cols = np.where(self.cells == 1)
            
        min_row, max_row = np.min(robot_rows), np.max(robot_rows)
        min_col, max_col = np.min(robot_cols), np.max(robot_cols)
        
        # Check if cluster is taller than wide
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        if height < width:
            return False
        
        # Get the cluster's width at different heights (let's assume it wont just be an outline but a filled out tree)
        widths = []
        for row in range(min_row, max_row + 1):
            width = np.sum(self.cells[row, min_col:max_col+1])
            widths.append(width)
        # Width should generally increase as we go down
        width_increases = sum(w1 <= w2 for w1, w2 in zip(widths[:-1], widths[1:]))
        if width_increases < len(widths) * min_width_increase_ratio: # At least x% should increase
            return False

        # Check for rough symmetry around vertical center
        center_col = (min_col + max_col) // 2
        for row in range(min_row, max_row + 1):
            left_sum = np.sum(self.cells[row, :center_col])
            right_sum = np.sum(self.cells[row, center_col+1:])
            if abs(left_sum - right_sum) > max(left_sum, right_sum) * max_asymmetry:  # Allow x% asymmetry
                return False

        # Check density (again, let's assume it wont just be an outline...)
        tree_area = height * (max_col - min_col + 1)
        robot_count = len(robot_rows)
        density = robot_count / tree_area
        if density < min_density:  # At least x% filled
            return False

        return True
    
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