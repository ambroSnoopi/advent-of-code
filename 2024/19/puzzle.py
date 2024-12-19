from enum import Enum
from tqdm import tqdm

class Color(Enum):
    WHITE = "w"
    BLUE = "u"
    BLACK = "b"
    RED = "r"
    GREEN = "g"

    def __str__(self):
        return self.value

    def __repr__(self):
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
    
    def is_composite_of(self, other: 'Pattern') -> bool:
        return str(self) in str(other)
    
    def find_composites(self, collection: list['Pattern']) -> list['Pattern']:
        """ Looks for composite candidates in a collection of Patterns. """
        composites = []
        for pattern in collection:
            if pattern.is_composite_of(self):
                composites.append(pattern)
        return composites
    
    def can_be_made_of(self, patterns: list['Pattern']) -> bool:
        """
        Checks whether this pattern can be fully constructed from a combination of other patterns.
        Uses dynamic programming to solve the problem efficiently.
        
        Args:
            patterns: List of patterns that could be used as building blocks
        
        Returns:
            bool: True if this pattern can be constructed from the given patterns
        """
        target = str(self)
        n = len(target)
        
        # dp[i] represents whether we can make the substring target[0:i]
        dp = [False] * (n + 1)
        dp[0] = True  # Empty string can always be made
        
        # Convert patterns to strings for easier matching
        pattern_strings = [str(p) for p in patterns]
        
        # For each position in the target string
        for i in range(1, n + 1):
            # Try to end a pattern at position i
            for pattern in pattern_strings:
                pattern_len = len(pattern)
                # If the pattern is too long, skip it
                if pattern_len > i:
                    continue
                    
                # Check if we can use this pattern to build the substring
                # We need:
                # 1. The previous state (i - pattern_len) to be achievable
                # 2. The current pattern to match the substring ending at i
                if (dp[i - pattern_len] and 
                    target[i - pattern_len:i] == pattern):
                    dp[i] = True
                    break
        
        return dp[n]

class Puzzle:
    def __init__(self, towels: list[Pattern], designs: list[Pattern]):
        self.available_towels = towels
        self.desired_designs = designs
        self.possible_designs: list[Pattern] = []

    def do(self):
        for design in tqdm(self.desired_designs, desc=f"Recreating desings using {len(self.available_towels)} available towels.", unit="design"):
            if design.can_be_made_of(self.available_towels):
                self.possible_designs.append(design)
    
    def checksum(self) -> int:
        return len(self.possible_designs)
    
    def reduce_towels():
        """ Drops redundant towels, which pattern can be made entirely out of other towels. """
        pass

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