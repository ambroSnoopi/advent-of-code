from dataclasses import dataclass
from typing import List
import re
from tqdm import tqdm

@dataclass
class Button:
    symbol: str
    x_offset: int
    y_offset: int
    cost: int

@dataclass
class Machine:
    button_a: Button
    button_b: Button
    prize_x: int
    prize_y: int

class Arcade:
    def __init__(self, machine_configs: str):
        self.machines: list[Machine] = self.parse_machine_configs(machine_configs)
        self.optimals: list[tuple[int, int, int]] = [] #Na, Nb, C

        for m in tqdm(self.machines, desc="Simulating optimal plays", unit="machine"):
            optimum = self.derive_optimal_play(m)
            self.optimals.append(optimum)
        
    def checksum(self) -> int:
        """ Sum the cost for winning the prize of each machine with an optimal play. """
        return sum(item[2] for item in self.optimals if item is not None)
    
    def derive_optimal_play(self, m: Machine, bound=100)-> tuple[int, int, int] | None:
        """
        Find optimal integer Na, Nb that minimize C = Ca*Na + Cb*Nb
        subject to coordinate constraints and upper bound.
        """

        Xp = m.prize_x 
        Yp = m.prize_y
        Xa = m.button_a.x_offset
        Ya = m.button_a.y_offset
        Xb = m.button_b.x_offset
        Yb = m.button_b.y_offset
        Ca = m.button_a.cost
        Cb = m.button_b.cost

        max_cost = Ca * bound + Cb * bound + 1
        min_cost = max_cost
        best_solution = None

        # Try all integer combinations within bounds
        for Na in range(bound + 1):
            for Nb in range(bound + 1):
                # Check if this combination satisfies both equations
                if (Xa * Na + Xb * Nb == Xp) and (Ya * Na + Yb * Nb == Yp):
                    cost = Ca * Na + Cb * Nb
                    # Update best solution if this cost is lower
                    if cost < min_cost:
                        min_cost = cost
                        best_solution = (Na, Nb, cost)
        return best_solution



    def parse_machine_configs(self, machine_configs: str) -> list[Machine]:
        """
        Parse machine configuration text file and return a list of Machine instances.
        
        Args:
            file_content (str): Content of the configuration file
        
        Returns:
            List[Machine]: List of parsed Machine instances
        """
        machines = []
        current_config = {}
        
        # Split the content into lines and process each line
        for line in machine_configs.strip().split('\n'):
            if not line:
                continue
                
            # Parse button coordinates
            if line.startswith('Button'):
                match = re.match(r'Button ([AB]): X\+(\d+), Y\+(\d+)', line)
                if match:
                    button, x, y = match.groups()
                    current_config[f'button_{button.lower()}'] = Button(
                        symbol = button,
                        x_offset=int(x),
                        y_offset=int(y),
                        cost = 3 if button=="A" else 1
                    )
            
            # Parse prize coordinates
            elif line.startswith('Prize'):
                match = re.match(r'Prize: X=(\d+), Y=(\d+)', line)
                if match:
                    x, y = match.groups()
                    current_config['prize_x'] = int(x)
                    current_config['prize_y'] = int(y)
                    
                    # Create a new Machine instance when we have all the data
                    if len(current_config) == 4:
                        machines.append(Machine(
                            button_a=current_config['button_a'],
                            button_b=current_config['button_b'],
                            prize_x=current_config['prize_x'],
                            prize_y=current_config['prize_y']
                        ))
                        current_config = {}
        
        return machines

def load_puzzle(filename: str):
    with open(filename, 'r') as file:
        return Arcade(file.read())