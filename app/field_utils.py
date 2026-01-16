from app.constants import GRID_SIZE
from app.types_aliases import Cell, CellSet


def get_surrounding_cells(positions: list[Cell]) -> CellSet:
    surrounding_cells: CellSet = set()

    for row, col in positions:
        for delta_row in (-1, 0, 1):
            for delta_col in (-1, 0, 1):
                neighbor_row = row + delta_row
                neighbor_col = col + delta_col

                if (
                    0 <= neighbor_row < GRID_SIZE
                    and 0 <= neighbor_col < GRID_SIZE
                ):
                    surrounding_cells.add((neighbor_row, neighbor_col))

    return surrounding_cells
