from enum import Enum
import itertools
from tqdm import tqdm

class Operator(Enum):
    ADD = ('+')
    MULTIPLY = ('*')
    #i wonder if part 2 could include other operators...?
    
    @property
    def symbol(self) -> str:
        return self.value[0]
    
def load_equations(filename: str) -> dict[int, list[int]]:
    equations = {}
    with open(filename, 'r') as file:
        for line in file:
            total, operands = line.split(':')
            total = int(total)
            operands = list(map(int, operands.strip().split()))
            equations[total] = operands
    return equations

def guess_operators(total: int, operands: list[int], operators=[Operator.ADD, Operator.MULTIPLY]) -> bool:
    """Tries to combine the given operands using a combination of the provided operators to reach the total. Returns True if successfull."""

    configurations = list(itertools.product(operators, repeat=len(operands)-1)) #generates all possible combinations of the provided operators
    for config in configurations:
        
        subtotal = operands[0]
        for operator, operand in zip(config, operands[1:]): #iterates through operands & operators in parallel and increments the subtotal accordingly
            if subtotal > total: # break early if we have already exceed the total (since we only support increasing operators, and there are no 0 operands)
                break
            match operator:
                case Operator.ADD: subtotal += operand
                case Operator.MULTIPLY: subtotal *= operand

        if subtotal == total:
            return True
        
    return False

def validate_totals(equations: dict[int, list[int]]) -> list[int]:
    """ Validates each total of a dict of equations returning only valid totals (aka test values). """
    valid_testvalues = []
    for total, operands in tqdm(equations.items(), desc="Validationg test values of equations", unit="equation"):
        if guess_operators(total, operands):
            valid_testvalues.append(total)
    return valid_testvalues


test = load_equations('input/test.txt')
expected = 3749
actual = sum(validate_totals(test))
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

quest = load_equations('input/quest.txt')
total_calibration_result = sum(validate_totals(quest))
print(total_calibration_result)