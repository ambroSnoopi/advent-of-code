import map as m
from map import Cell
from tqdm import tqdm

map = m.load_map('input.txt') # test / input

# Part 1
happy_path = map.simulate_guard_movement()[0]
happy_cells = set(pos.cell for pos in happy_path)
print("\nGuard's path:", len(happy_path)) # 45 / 5378
print("Guard's distinct cells:", len(happy_cells)) # 41 / 4890
map.reset()

# Part 2
looping_obstructions: list[Cell] = []
for cell in tqdm(happy_cells, desc="Obstructing cells in happy path", unit="cell"): # let's try blocking every cell the guard would have visited and see if it would cause a loop (any other cell would have no impact)
    if not cell.is_obstacle and not cell.guard_direction:
        cell.set_obstacle()
        exited = map.simulate_guard_movement()[1]
        if not exited: 
            looping_obstructions.append(cell)
        cell.clear()
        map.reset()

print("Possible positions for obstructions", len(looping_obstructions)) # 6 / 