from app.main import Battleship

# Test the fire method behavior
battle = Battleship([
    ((0, 0), (0, 2)),  # 3-deck ship (horizontal)
    ((2, 0), (2, 0)),  # 1-deck ship
])

print("Testing fire method behavior:")
print("=" * 40)

# Test hitting a 3-deck ship
print("1. Hit first deck of 3-deck ship:", battle.fire((0, 0)))
print("2. Hit second deck of 3-deck ship:", battle.fire((0, 1)))
print("3. Hit third deck of 3-deck ship (should sink):", battle.fire((0, 2)))

# Test hitting already hit deck
print("4. Hit already hit deck:", battle.fire((0, 0)))

# Test hitting 1-deck ship (should sink immediately)
print("5. Hit 1-deck ship (should sink immediately):", battle.fire((2, 0)))

# Test miss
print("6. Miss:", battle.fire((5, 5)))

print("\nField visualization:")
battle.print_field()
