import map as m

map = m.load_map('input.txt')

print("Initial state:")
print(map)

path = map.simulate_guard_movement(0)  # Simulate (first) guard movement until it leaves the map

print("\nAfter guard movement:")
print(map)

print("\nGuard's path:", len(path))
print("Guard's distinct path:", len(set(path)))