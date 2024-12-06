import map as m
from map import Cell
from tqdm import tqdm

map = m.load_map('input.txt') # test / input

# Part 1
happy_path = map.simulate_guard_movement()[0]
visited_cells = {map.get_cell(x, y) for x, y, _ in happy_path}
print("\nGuard's path:", len(happy_path)) # 45 / 5378
print("Guard's visited cells:", len(visited_cells)) # 41 / 4890
map.reset()

# Part 2
looping_obstructions: list[Cell] = []
for cell in tqdm(visited_cells, desc="Obstructing cells in happy path", unit="cell"): # let's try blocking every cell the guard would have visited and see if it would cause a loop (any other cell would have no impact)
    if not cell.is_obstacle and not cell.guard_direction:
        cell.set_obstacle()
        exited = map.simulate_guard_movement()[1]
        if not exited: 
            looping_obstructions.append(cell)
        cell.clear()
        map.reset()

print("Possible positions for obstructions", len(looping_obstructions)) # 6 / <2300!