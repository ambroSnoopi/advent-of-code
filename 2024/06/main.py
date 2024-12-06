import map as m
# Load the map
map = m.load_map('input.txt')

# Print initial state
print("Initial state:")
print(map)

# Simulate guard movement until they leave the map
path = map.simulate_guard_movement(0)  # Simulate first guard

print("\nAfter guard movement:")
print(map)

print("Guard's path:", len(path))
print("Guard's distinct path:", len(set(path)))