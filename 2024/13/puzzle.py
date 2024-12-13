from dataclasses import dataclass
import re
from tqdm import tqdm
from math import gcd

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
    
    def derive_optimal_play(self, m: Machine) -> tuple[int, int, int] | None:
        """
        Find optimal integer Na, Nb that minimize C = Ca*Na + Cb*Nb
        subject to coordinate constraints, without upper bound.
        """
        Xp = m.prize_x 
        Yp = m.prize_y
        Xa = m.button_a.x_offset
        Ya = m.button_a.y_offset
        Xb = m.button_b.x_offset
        Yb = m.button_b.y_offset
        Ca = m.button_a.cost
        Cb = m.button_b.cost
        
        # First check if the system has any integer solutions
        # For the first equation: Xa*Na + Xb*Nb = Xp
        if gcd(Xa, Xb) != 0 and Xp % gcd(Xa, Xb) != 0:
            return None
        
        # For the second equation: Ya*Na + Yb*Nb = Yp
        if gcd(Ya, Yb) != 0 and Yp % gcd(Ya, Yb) != 0:
            return None
        
        # Find determinant of coefficient matrix
        det = Xa * Yb - Xb * Ya
        
        # If determinant is zero, equations are dependent or inconsistent
        if det == 0:
            return None
        
        # Find one particular solution using Cramer's rule with fractions
        Na = (Xp * Yb - Xb * Yp) // det
        Nb = (Xa * Yp - Xp * Ya) // det
        
        # If the particular solution isn't integer, no integer solution exists
        if (Xp * Yb - Xb * Yp) % det != 0 or (Xa * Yp - Xp * Ya) % det != 0:
            return None
        
        # Verify the solution
        if (Xa * Na + Xb * Nb != Xp) or (Ya * Na + Yb * Nb != Yp):
            return None
        
        # Check if solution is non-negative
        if Na < 0 or Nb < 0:
            return None
        
        # Calculate cost
        C = Ca * Na + Cb * Nb
        
        return Na, Nb, C

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
                    current_config['prize_x'] = int(x)+10000000000000
                    current_config['prize_y'] = int(y)+10000000000000
                    
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
    
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Returns (gcd, x, y) where gcd is the greatest common divisor of a and b
    and x, y are coefficients where ax + by = gcd
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def solve_diophantine(a: int, b: int, c: int) -> tuple[int, int] | None:
    """
    Solves the Diophantine equation: ax + by = c
    Returns one solution (x0, y0) if exists, None otherwise
    """
    # Find GCD and coefficients
    g, x0, y0 = extended_gcd(abs(a), abs(b))
    
    # Check if solution exists
    if c % g != 0:
        return None
    
    # Adjust for sign and scale to match c
    x0 *= (c // g) * (1 if a > 0 else -1)
    y0 *= (c // g) * (1 if b > 0 else -1)
    
    return x0, y0