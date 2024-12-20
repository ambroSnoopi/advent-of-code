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
    
    def find_all_combinations(self, patterns: list['Pattern']) -> list[list['Pattern']]:
        """
        Finds all possible combinations of patterns that can create this pattern.
        
        Args:
            patterns: List of patterns that could be used as building blocks
        
        Returns:
            list[list[Pattern]]: List of all valid combinations of patterns that create this pattern
        """
        target = str(self)
        n = len(target)
        
        # dp[i] will store list of lists, where each inner list contains the patterns
        # that can be used to build the substring ending at position i
        dp = [[] for _ in range(n + 1)]
        dp[0] = [[]]  # Empty string can be made with empty combination
        
        # Convert patterns to dictionary for easier lookup when reconstructing
        pattern_map = {str(p): p for p in patterns}
        
        # For each position in the target string
        for i in range(1, n + 1):
            # Try to end a pattern at position i
            for pattern in patterns:
                pattern_str = str(pattern)
                pattern_len = len(pattern_str)
                
                # If pattern is too long for current position, skip it
                if pattern_len > i:
                    continue
                
                # Check if this pattern matches at current position
                if target[i - pattern_len:i] == pattern_str:
                    # For each combination that builds the prefix
                    for prefix_combo in dp[i - pattern_len]:
                        # Add current pattern to create new combination
                        dp[i].append(prefix_combo + [pattern])
        
        return dp[n]
    
    def get_all_ways_to_make(self, patterns: list['Pattern']) -> list[list['Pattern']]:
        """
        Finds all possible combinations of patterns that can create this pattern using backtracking.
        
        Args:
            patterns: List of patterns that could be used as building blocks
        
        Returns:
            list[list[Pattern]]: List of valid combinations, where each combination is a list of patterns
        """
        target = str(self)
        results = []
        current_combination = []
        
        def backtrack(remaining_target: str):
            # If nothing left to match, we found a valid combination
            if not remaining_target:
                results.append(current_combination.copy())
                return
                
            # Try each pattern at the current position
            for pattern in patterns:
                pattern_str = str(pattern)
                
                # If pattern matches at start of remaining target
                if remaining_target.startswith(pattern_str):
                    # Add this pattern to our current combination
                    current_combination.append(pattern)
                    # Recursively try to match the rest
                    backtrack(remaining_target[len(pattern_str):])
                    # Remove the pattern to try other possibilities
                    current_combination.pop()
        
        # Start the backtracking process
        backtrack(target)
        return results

class Puzzle:
    def __init__(self, towels: list[Pattern], designs: list[Pattern]):
        self.available_towels = towels
        self.desired_designs = designs
        self.possible_designs: list[Pattern] = []
        self.design_combos: dict[Pattern, list[list[Pattern]]] = {}
        
        self.building_towels: list[Pattern] = []
        self.redundant_towels: list[Pattern] = []
        self.redundant_to_building: dict[Pattern: list[list[Pattern]]] = {} #redundant_towel -> list[*building_towels]
        self.building_to_redundant: dict[tuple[Pattern]: Pattern] = {} #tuple[building_towels] -> redundant_towel

    def reduce_towels(self):
        """
        Reduces the set of towels by removing those that can be made from combinations of others.
        i.e. splits the "available_towels" into "building_towels" which can be used to form "redundant_towels"
        """
        for towel in tqdm(self.available_towels, desc="Reducing available towels", unit="towel"):
            candidates = towel.find_composites(self.available_towels)
            candidates.remove(towel) # ignore self
            if towel.can_be_made_of(candidates):
                self.redundant_towels.append(towel)
            else:
                self.building_towels.append(towel)

    def map_reduced_towels(self):
        """ Creates a mapping between building_towels and redundant_towels. """
        for towel in tqdm(self.redundant_towels, desc="Mapping reduced towels", unit="towel"):
            combos = towel.get_all_ways_to_make(self.building_towels)
            self.redundant_to_building[towel] = combos
            for possibility in combos:
                self.building_to_redundant[tuple(possibility)] = towel

    def expand_towels(self, seq: list[Pattern]) -> list[list[Pattern]]:
        """ Processes a combo of towels and replaces any subsequences of building_towels with the respective redundant_towel. Returns all additional combinations. """
        
        results: list[list[Pattern]] = []
        #subseq: tuple[Pattern], new_value: Pattern
        for subseq, new_value in self.building_to_redundant.items():
            subseq = list(subseq)
            subseq_len = len(subseq)
            
            # Recursive function to generate combinations
            def generate_combinations(current_seq, start_index):
                # Search for the subsequence starting from `start_index`
                for i in range(start_index, len(current_seq) - subseq_len + 1):
                    if current_seq[i:i + subseq_len] == subseq:
                        # Create a new sequence with the substitution
                        new_seq = current_seq[:i] + [new_value] + current_seq[i + subseq_len:]
                        # Add this new sequence to the results
                        if new_seq not in results: results.append(new_seq)
                        # Recurse to find further substitutions in the new sequence
                        generate_combinations(new_seq, i + 1)

            # Start generating combinations from the original sequence
            generate_combinations(seq, 0)
        return results
    
    def do(self):
        # Part 1
        for design in tqdm(self.desired_designs, desc=f"Recreating desings using {len(self.available_towels)} available towels", unit="design"):
            if design.can_be_made_of(self.available_towels):
                self.possible_designs.append(design)
        # Part 2
        candidates: list[Pattern] = []
        self.reduce_towels()
        self.map_reduced_towels()
        with tqdm(self.possible_designs, desc=f"Compiling all possible combinations to recreate designs using {len(candidates)} applicable towels", unit="design") as pbar:
            for design in pbar:
                candidates.extend(design.find_composites(self.building_towels))
                pbar.set_description(f"Compiling all possible combinations to recreate designs using {len(candidates)} applicable towels")
                combos = design.get_all_ways_to_make(candidates)
                for possibility in combos:
                    extras = self.expand_towels(possibility)
                    # combos.extend(extras) #combos.extend(x for x in extras if x not in combos)
                    for extra in extras:
                        if extra not in combos: combos.append(extra)
                self.design_combos[design] = combos
                candidates.clear()

    def checksum(self) -> int:
        return len(self.possible_designs)
    
    def check_p2(self) -> int:
        return sum(len(combos) for combos in self.design_combos.values())

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