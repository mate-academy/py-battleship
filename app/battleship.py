from app.constants import (
    DEBUG_COORDS,
    EXPECTED_SHIPS,
    GRID_SIZE,
    SHOT_HIT,
    SHOT_MISS,
    SHOT_REPEAT,
    SHOT_SUNK,
    SYMBOL_ALIVE,
    SYMBOL_AROUND,
    SYMBOL_EMPTY,
    SYMBOL_MISS,
    SYMBOL_SUNK,
)
from app.field_utils import get_surrounding_cells
from app.ship import Ship
from app.types_aliases import Cell, CellSet, ShipPlacements


class Battleship:
    def __init__(self, ships: ShipPlacements) -> None:
        self.ships: list[Ship] = []
        self.field: dict[Cell, Ship] = {}
        self.shots: CellSet = set()
        self.marked_cells_around_sunk_ships: CellSet = set()

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[deck.position] = ship

        self._validate_field()

    @property
    def remaining_ships(self) -> int:
        return sum(1 for ship in self.ships if not ship.is_drowned)

    @property
    def is_game_over(self) -> bool:
        return all(ship.is_drowned for ship in self.ships)

    def fire(self, target: Cell) -> str:
        if target in self.shots:
            return SHOT_REPEAT

        self.shots.add(target)

        if target in self.field:
            ship = self.field[target]
            ship.hit(target)

            if ship.is_drowned:
                self._surround_sunk_ship(ship)
                return SHOT_SUNK

            return SHOT_HIT

        return SHOT_MISS

    def __str__(self) -> str:
        header_range = (
            range(GRID_SIZE)
            if DEBUG_COORDS
            else range(1, GRID_SIZE + 1)
        )
        header = "   " + " ".join(str(i) for i in header_range)
        lines = [header]

        for row in range(GRID_SIZE):
            line = f"{row: <2} " if DEBUG_COORDS else f"{row + 1: <2} "

            for col in range(GRID_SIZE):
                position = (row, col)

                if position in self.field:
                    ship = self.field[position]
                    deck = ship.get_deck(position)

                    if ship.is_drowned or not deck.is_alive:
                        line += f"{SYMBOL_SUNK} "
                    else:
                        line += f"{SYMBOL_ALIVE} "
                elif position in self.marked_cells_around_sunk_ships:
                    line += f"{SYMBOL_AROUND} "
                elif position in self.shots:
                    line += f"{SYMBOL_MISS} "
                else:
                    line += f"{SYMBOL_EMPTY} "

            lines.append(line.rstrip())

        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"Battleship(ships={len(self.ships)}, "
            f"remaining={self.remaining_ships})"
        )

    def _validate_field(self) -> None:
        expected_total_ships = sum(EXPECTED_SHIPS.values())
        actual_total_ships = len(self.ships)

        if actual_total_ships != expected_total_ships:
            raise ValueError(
                f"Expected {expected_total_ships} ships, "
                f"but found {actual_total_ships}."
            )

        actual_ships = {size: 0 for size in EXPECTED_SHIPS}

        for ship in self.ships:
            size = ship.size
            if size not in actual_ships:
                raise ValueError(f"Invalid ship size: {size}")
            actual_ships[size] += 1

            for deck in ship.decks:
                for neighbor in get_surrounding_cells([deck.position]):
                    if (
                        neighbor in self.field
                        and self.field[neighbor] is not ship
                    ):
                        raise ValueError(
                            "Invalid placement: ships must not touch "
                            "each other"
                        )

        for size, expected_ship_count in EXPECTED_SHIPS.items():
            actual_ship_count = actual_ships[size]

            if actual_ship_count != expected_ship_count:
                unit_label = "ship" if expected_ship_count == 1 else "ships"
                raise ValueError(
                    f"Expected {expected_ship_count} {unit_label} of size "
                    f"{size}, but found {actual_ship_count}."
                )

    def _surround_sunk_ship(self, ship: Ship) -> None:
        deck_positions = [deck.position for deck in ship.decks]
        surrounding_cells = get_surrounding_cells(deck_positions)

        for cell in surrounding_cells:
            if cell not in self.field:
                self.marked_cells_around_sunk_ships.add(cell)
