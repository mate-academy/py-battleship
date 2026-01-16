from typing import TypeAlias

# Represents a board cell as a (row, column) coordinate pair.
Cell: TypeAlias = tuple[int, int]

# Represents a set of board cells (row, column coordinate pairs).
CellSet: TypeAlias = set[Cell]

# Represents all cells occupied by a single ship (deck positions).
ShipCells: TypeAlias = list[Cell]

# Represents the placement of a single ship (start and end cells).
ShipPlacement: TypeAlias = tuple[Cell, Cell]

# Represents a list of all ship placements on the board.
ShipPlacements: TypeAlias = list[ShipPlacement]

# Represents all valid placement options for a ship.
ShipPlacementOptions: TypeAlias = list[ShipCells]

# Represents a fleet structure: ship size → ship count.
Ships: TypeAlias = dict[int, int]
