from typing import List


def are_ships_separated(ships: List[tuple]) -> None:
    def are_cells_neighbors(cell1: tuple, cell2: tuple) -> bool:
        x1, y1 = cell1
        x2, y2 = cell2
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1

    for i in range(len(ships)):
        for coord in range(i + 1, len(ships)):
            for cell1 in ships[i]:
                for cell2 in ships[coord]:
                    if are_cells_neighbors(cell1, cell2):
                        raise ValueError(
                            "ships shouldn't be located in the"
                            " neighboring cells"
                            " (even if cells are neighbors by diagonal)")
