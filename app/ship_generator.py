import random
from itertools import product

from app.constants import EXPECTED_SHIPS, GRID_SIZE
from app.field_utils import get_surrounding_cells
from app.types_aliases import (
    Cell,
    ShipCells,
    ShipPlacement,
    ShipPlacements,
    Ships,
)


def generate_random_ship_placements() -> ShipPlacements:
    ship_sizes = _expand_ship_counts(EXPECTED_SHIPS)

    ship_placements: ShipPlacements = []
    occupied_cells: set[Cell] = set()

    for ship_size in ship_sizes:
        ship_cells = _get_random_ship_cells(
            ship_size,
            occupied_cells,
        )
        ship_placement: ShipPlacement = (ship_cells[0], ship_cells[-1])
        ship_placements.append(ship_placement)
        occupied_cells.update(ship_cells)

    return ship_placements


def _expand_ship_counts(ships: Ships) -> list[int]:
    return [
        size
        for size, count in ships.items()
        for _ in range(count)
    ]


def _get_random_ship_cells(
    ship_size: int,
    occupied_cells: set[Cell],
) -> ShipCells:
    valid_ship_cells: list[ShipCells] = _get_all_valid_ship_cells(
        ship_size,
        occupied_cells,
    )

    if not valid_ship_cells:
        raise RuntimeError(
            f"Ship placement failed (size {ship_size}): "
            "no available space on the board."
        )

    return random.choice(valid_ship_cells)


def _get_all_valid_ship_cells(
    ship_size: int,
    occupied_cells: set[Cell],
) -> list[ShipCells]:
    valid_ship_cells: list[ShipCells] = []

    for row, col in product(range(GRID_SIZE), repeat=2):
        horizontal_cells = [(row, col + i) for i in range(ship_size)]
        if (
            col + ship_size <= GRID_SIZE
            and _is_valid_ship_cells(horizontal_cells, occupied_cells)
        ):
            valid_ship_cells.append(horizontal_cells)

        vertical_cells = [(row + i, col) for i in range(ship_size)]
        if (
            row + ship_size <= GRID_SIZE
            and _is_valid_ship_cells(vertical_cells, occupied_cells)
        ):
            valid_ship_cells.append(vertical_cells)

    return valid_ship_cells


def _is_valid_ship_cells(
    ship_cells: ShipCells,
    occupied_cells: set[Cell],
) -> bool:
    surrounding_cells = get_surrounding_cells(ship_cells)
    return all(cell not in occupied_cells for cell in surrounding_cells)
