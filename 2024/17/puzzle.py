from multiprocessing import Pool, cpu_count
from enum import Enum
from tqdm import tqdm

class Instruction(Enum):
    adv = (0)
    bxl = (1)
    bst = (2)
    jnz = (3)
    bxc = (4)
    out = (5)
    bdv = (6)
    cdv = (7)

    @property
    def opcode(self) -> str:
        return self.value
    
    @classmethod
    def from_opcode(cls, opcode: int) -> 'Instruction':
        for instruction in cls:
            if instruction.opcode == opcode:
                return instruction
        raise ValueError(f"No Instruction matches opcode: {opcode}")

class ChronospatialPC:
    def __init__(self, program: list[int], regA: int, regB=0, regC=0):
        self.regA = regA
        self.regB = regB
        self.regC = regC
        self.program: list[int] = program
        self.output: list[int] = []
        #self.instructions[Instruction] = [Instruction.from_opcode(value) for value in program]

    def checksum(self):
        return ','.join(map(str, self.output))
    
    def do(self):
        self.n = 0
        while self.n < len(self.program):
            inst = Instruction.from_opcode(self.program[self.n])
            operand = self.program[self.n+1]
            self.execute(inst, operand)

    def do_copy_program(self):
        """ Same as do() but terminates early if the program is not producing a copy of itself. """
        self.n = 0
        while self.program[:len(self.output)] == self.output and self.n < len(self.program):
            inst = Instruction.from_opcode(self.program[self.n])
            operand = self.program[self.n+1]
            self.execute(inst, operand)
    
    def fixRegA(self, start=0) -> int:
        in_regA = start
        pbar = tqdm(desc=f"Searching Value for Registry A starting at {start}... Tested", unit="values", )
        while self.output != self.program:
            in_regA += 1
            self.output.clear()
            self.regA = in_regA
            self.do_copy_program()
            pbar.update(1)
        return in_regA

    def execute(self, instruction: Instruction, operand: int):
        if instruction == Instruction.adv: self.adv(self.combo(operand))
        elif instruction == Instruction.bxl: self.bxl(operand)
        elif instruction == Instruction.bst: self.bst(self.combo(operand))
        elif instruction == Instruction.jnz: self.jnz(operand)
        elif instruction == Instruction.bxc: self.bxc()
        elif instruction == Instruction.out: self.out(self.combo(operand))
        elif instruction == Instruction.bdv: self.bdv(self.combo(operand))
        elif instruction == Instruction.cdv: self.cdv(self.combo(operand))
        else: raise ValueError("Unhandled instruction!", instruction)

    def combo(self, operand: int) -> int:
        if 0 <= operand <= 3: return operand
        if 4 == operand: return self.regA
        if 5 == operand: return self.regB
        if 6 == operand: return self.regC
        if operand >= 7: raise ValueError("Combo operands need to be lower than 7!", operand)
    
    def adv(self, operand: int):
        self.regA //= 2 ** operand
        self.n += 2

    def bxl(self, operand: int):
        self.regB ^= operand
        self.n += 2

    def bst(self, operand: int):
        self.regB = operand % 8
        self.n += 2

    def jnz(self, operand: int):
        if self.regA==0: self.n += 2
        else: self.n = operand

    def bxc(self):
        self.regB ^= self.regC
        self.n += 2

    def out(self, operand: int):
        self.output.append(operand % 8)
        self.n += 2

    def bdv(self, operand: int):
        self.regB = self.regA // 2 ** operand
        self.n += 2

    def cdv(self, operand: int):
        self.regC = self.regA // 2 ** operand
        self.n += 2

def search_range_for_regA(args: tuple[int, int, list[int]]) -> int | None:
    """
    Search a specific range of regA values that produce a copy of the proogram.
    Args:
        args: Tuple of (start, end, program)
    Returns:
        The working regA value if found, None otherwise
    """
    start, end, program = args
    pc = ChronospatialPC(program, 0)
    
    for regA in range(start, end):
        pc.regA = regA
        pc.output.clear()
        pc.do_copy_program()
        if pc.output == pc.program:
            return regA
    return None

def parallel_search_for_regA(program: list[int], start: int = 0, chunk_size: int = 5_000_000) -> int | None:
    """
    Search for regA values that produce a copy of the proogram in parallel using multiple processes.
    Args:
        program: The program to reproduce
        start: Starting value for regA
        chunk_size: Size of chunks to distribute to processes
    Returns:
        The working regA value if found, None otherwise
    """
    num_processes = cpu_count()
    
    # Create ranges for each process
    current = start
    with Pool(num_processes) as pool:
        pbar = tqdm(desc=f"Searching with {num_processes} processes", unit="chunks")
        
        while True:
            # Create chunks for each process
            ranges = [
                (current + i * chunk_size, current + (i + 1) * chunk_size, program)
                for i in range(num_processes)
            ]
            
            # Process chunks in parallel
            for result in pool.imap_unordered(search_range_for_regA, ranges):
                if result is not None:
                    # Solution found
                    pool.terminate()  # Stop all other processes
                    return result
            
            # Update progress and move to next range
            current += chunk_size * num_processes
            pbar.update(num_processes)