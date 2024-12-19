from enum import Enum

class Color(Enum):
    WHITE = "w"
    BLUE = "u"
    BLACK = "b"
    RED = "r"
    GREEN = "g"

    def __str__(self):
        return self.value

    @property
    def char(self) -> str:
        return self.value
    
    @classmethod
    def from_char(cls, char: str) -> 'Color':
        for enum in cls:
            if enum.char == char:
                return enum
        raise ValueError(f"No Color matches char: {char}")

class Pattern:
    def __init__(self, *colors: Color):
        self.colors = list(colors)
    
    @classmethod
    def from_string(cls, pattern_str: str) -> 'Pattern':
        """Create a Pattern from a string of color characters"""
        # Remove any whitespace and split the string into individual color chars
        color_chars = [c for c in pattern_str.strip() if c != ' ']
        colors = [Color.from_char(char) for char in color_chars]
        return cls(*colors)
    
    def __str__(self) -> str:
        return ''.join(str(color) for color in self.colors)
    
    def __repr__(self) -> str:
        return f"Pattern({', '.join(repr(color) for color in self.colors)})"

class Puzzle:
    def __init__(self, towels: list[Pattern], designs: list[Pattern]):
        self.available_towels = towels
        self.desired_designs = designs

    def do():
        return
    
    def checksum():
        return

def load_puzzle(input_towels: str, input_designs: str) -> Puzzle:
    """Load patterns from a file containing comma-separated pattern strings"""
    with open(input_towels, 'r') as file:
        content = file.read().strip()
        pattern_strings = [p.strip() for p in content.split(',')]
        towels = [Pattern.from_string(p) for p in pattern_strings]
    with open(input_designs, 'r') as file:
        content = file.read()
        pattern_strings = lines = content.strip().split('\n')
        designs = [Pattern.from_string(p) for p in pattern_strings]
    return Puzzle(towels, designs)