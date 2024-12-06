import map as m
from map import Cell

map = m.load_map('test.txt') # test / input

# Part 1
path = map.simulate_guard_movement()[0]
print("\nGuard's path:", len(path)) # 45 / 5378
print("Guard's distinct path:", len(set(pos.cell for pos in path))) # 41 / 4890
map.reset()

# Part 2
looping_obstructions: list[Cell] = []
for cell in map.get_cells():
    if not cell.is_obstacle and not cell.guard_direction:
        cell.set_obstacle()
        exited = map.simulate_guard_movement()[1]
        if not exited: 
            looping_obstructions.append(cell)
        cell.clear()
        map.reset()

print("Possible positions for obstructions", len(looping_obstructions)) # 85! / 