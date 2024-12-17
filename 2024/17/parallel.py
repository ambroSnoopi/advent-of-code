from puzzle import ChronospatialPC
import puzzle
from multiprocessing import cpu_count

def main():
    program = [2,4,1,5,7,5,1,6,0,3,4,1,5,5,3,0]
    #program = [0,3,5,4,3,0]
    print(f"Starting parallel search using {cpu_count()} CPU cores...")
    result = puzzle.parallel_search_for_regA(program, 580_000_000, 1_000_000)
    #result = puzzle.parallel_search_for_regA(program, 0, 25_000)
    if result is not None:
        print(f"\nFound solution: regA = {result}")
        
        # Verify the solution
        pc = ChronospatialPC(program, result)
        pc.do()
        print(f"Verification - Output: {pc.output}")
        print(f"Matches program: {pc.output == program}")
    else:
        print("\nNo solution found in the searched range")

if __name__ == '__main__':
    main()