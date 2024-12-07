from enum import Enum
import itertools
from tqdm import tqdm
#import math

class Operator(Enum):
    ADD = ('+')
    MULTIPLY = ('*')
    CONCAT = ('||')
    #i knew it! :D
    
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

def guess_operators(total: int, operands: list[int], operators: list[Operator] = list(Operator)) -> bool:
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
                #case Operator.CONCAT: subtotal = int(str(subtotal)+str(operand)) # down from subsecond to 1min 30s... we can do better, right? let's do away with type casting
                #case Operator.CONCAT: subtotal = subtotal*10**(math.floor(math.log10(operand)) + 1) + operand #multiplying subtotal by 10 to the power of number of digits of operand to make space for it... still takes 1min 20s
                case Operator.CONCAT: subtotal = subtotal*10**(len(str(operand))) + operand #maybe math is slow? still 1min 20s

        if subtotal == total:
            return True
        
    return False

def validate_totals(equations: dict[int, list[int]], operators: list[Operator] = list(Operator)) -> list[int]:
    """ Validates each total of a dict of equations returning only valid totals (aka test values). """
    valid_testvalues = []
    for total, operands in tqdm(equations.items(), desc="Validationg test values of equations", unit="equation"):
        if guess_operators(total, operands, operators):
            valid_testvalues.append(total)
    return valid_testvalues

# Part 1
test = load_equations('input/test.txt')
expected = 3749
actual = sum(validate_totals(test, [Operator.ADD, Operator.MULTIPLY]))
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"

# Part 2
expected = 11387
actual = sum(validate_totals(test, [Operator.ADD, Operator.MULTIPLY, Operator.CONCAT]))
assert expected==actual, f"Test failed!\n  Expected: {expected}\n  Actual: {actual}"


quest = load_equations('input/quest.txt')
total_calibration_result = sum(validate_totals(quest))
print(total_calibration_result)